#!/usr/bin/env python3
"""Offline tests for the ChatGPT web delegation routing helper."""

from __future__ import annotations

import json
import os
import pathlib
import socket
import subprocess
import sys
import unittest
import urllib.error
from unittest import mock

SCRIPTS = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))
import route  # noqa: E402


DUMMY_KEY = "dummy-typesafe-key-for-offline-tests"
SECRET = "credential-must-not-appear-in-errors"


class FakeResponse:
    def __init__(self, body: bytes):
        self.body = body
        self.closed = False

    def read(self, limit: int = -1) -> bytes:
        return self.body if limit < 0 else self.body[:limit]

    def close(self) -> None:
        self.closed = True


def decision(choice: str, probabilities: dict[str, float], confidence: float = 0.9) -> dict:
    return {
        "choice": choice,
        "probabilities": probabilities,
        "confidence": confidence,
    }


def base_input(mode: str = "chat") -> dict:
    return {
        "task_summary": "Summarize public documentation for a non-sensitive decision.",
        "mode": mode,
        "disclosure_reviewed": True,
        "ui": {
            "snapshot_fresh": True,
            "origin": "https://chatgpt.com",
            "authenticated": True,
            "selected_mode": mode,
            "mode_compatibility": {
                "chat": ["fictional-alpha", "fictional-default"],
                "search": ["fictional-alpha", "fictional-default"],
                "research": ["fictional-alpha"],
            },
            "models": [
                {
                    "id": "fictional-alpha",
                    "label": "Fictional Alpha (observed)",
                    "description": "A fictitious model label observed in an offline fixture.",
                    "effort_control": "available",
                    "efforts": [
                        {
                            "id": "fictional-balanced",
                            "label": "Fictional balanced",
                            "description": "A fictitious effort label observed in an offline fixture.",
                        },
                        {
                            "id": "fictional-deep",
                            "label": "Fictional deep",
                            "description": "A second fictitious effort label for branch tests.",
                        },
                    ],
                },
                {
                    "id": "fictional-default",
                    "label": "Fictional default-only model",
                    "description": "A fictitious model with no separate effort selector.",
                    "effort_control": "none",
                    "efforts": [],
                },
            ],
        },
    }


def delegated_answers(model: str = "fictional-alpha", effort_key: str = "effort_0") -> dict:
    return {
        "route": decision("delegate", {"delegate": 0.80, "keep_local": 0.12, "clarify": 0.08}),
        "model": decision(
            model,
            {"fictional-alpha": 0.80, "fictional-default": 0.10, "no_suitable_model": 0.10},
        ),
        effort_key: decision(
            "fictional-balanced",
            {"fictional-balanced": 0.80, "fictional-deep": 0.10, "no_suitable_effort": 0.10},
        ),
    }


class RouteTaskTests(unittest.TestCase):
    def setUp(self) -> None:
        self.key_patch = mock.patch.dict(os.environ, {"TYPESAFE_API_KEY": DUMMY_KEY})
        self.key_patch.start()

    def tearDown(self) -> None:
        self.key_patch.stop()

    def test_delegation_receipt_uses_selected_model_effort_only(self) -> None:
        captured: dict = {}

        def fake_post(payload: dict) -> dict:
            captured.update(payload)
            return delegated_answers()

        with mock.patch.object(route, "_post_jev", side_effect=fake_post) as call:
            result = route.route_task(base_input())

        self.assertTrue(result["ok"])
        self.assertEqual(result["route"], "delegate")
        self.assertEqual(result["selection"], {"model": "fictional-alpha", "effort": "fictional-balanced"})
        receipt = result["receipt"]
        self.assertEqual(receipt["used_decisions"], ["route", "model", "effort"])
        self.assertEqual(receipt["effort"]["probabilities"], {
            "fictional-balanced": 0.8,
            "fictional-deep": 0.1,
            "no_suitable_effort": 0.1,
        })
        # Questions are speculative for every offered model, but only the
        # selected branch is consumed and placed in the receipt.
        self.assertIn("effort_0", captured["questions"])
        self.assertIn("effort_1", captured["questions"])
        self.assertNotIn("effort_no_suitable_model", captured["questions"])
        call.assert_called_once()

    def test_default_effort_is_explicit_and_only_for_verified_no_control(self) -> None:
        answers = {
            "route": decision("delegate", {"delegate": 0.85, "keep_local": 0.10, "clarify": 0.05}),
            "model": decision(
                "fictional-default",
                {"fictional-alpha": 0.05, "fictional-default": 0.85, "no_suitable_model": 0.10},
            ),
            "effort_1": decision("default_no_effort_control", {"default_no_effort_control": 1.0}),
        }
        with mock.patch.object(route, "_post_jev", return_value=answers):
            result = route.route_task(base_input())

        self.assertTrue(result["ok"])
        self.assertEqual(result["route"], "delegate")
        self.assertEqual(result["selection"]["effort"], route.DEFAULT_EFFORT)
        self.assertEqual(result["receipt"]["effort"]["probabilities"], {route.DEFAULT_EFFORT: 1.0})

    def test_search_and_research_modes_use_their_observed_capability_sets(self) -> None:
        for mode in ("search", "research"):
            captured: dict = {}

            def fake_post(payload: dict) -> dict:
                captured.update(payload)
                model_options = tuple(payload["questions"]["model"]["criteria"])
                effort_key = next(key for key in payload["questions"] if key == "effort_0")
                effort_options = tuple(payload["questions"][effort_key]["criteria"])
                model_probabilities = {option: 0.10 for option in model_options}
                model_probabilities["fictional-alpha"] = 1.0 - 0.10 * (len(model_options) - 1)
                effort_probabilities = {option: 0.10 for option in effort_options}
                effort_probabilities["fictional-balanced"] = 1.0 - 0.10 * (len(effort_options) - 1)
                return {
                    "route": decision("delegate", {"delegate": 0.80, "keep_local": 0.12, "clarify": 0.08}),
                    "model": decision("fictional-alpha", model_probabilities),
                    effort_key: decision("fictional-balanced", effort_probabilities),
                }

            with mock.patch.object(route, "_post_jev", side_effect=fake_post):
                result = route.route_task(base_input(mode))

            self.assertTrue(result["ok"])
            self.assertEqual(result["route"], "delegate")
            self.assertEqual(result["receipt"]["requested_mode"], mode)
            self.assertEqual(result["selection"], {"model": "fictional-alpha", "effort": "fictional-balanced"})
            self.assertEqual(captured["state"]["requested_mode"], mode)

    def test_no_suitable_effort_is_non_delegation_without_substitution(self) -> None:
        answers = delegated_answers()
        answers["effort_0"] = decision(
            route.NO_SUITABLE_EFFORT,
            {"fictional-balanced": 0.10, "fictional-deep": 0.10, route.NO_SUITABLE_EFFORT: 0.80},
        )
        with mock.patch.object(route, "_post_jev", return_value=answers):
            result = route.route_task(base_input())

        self.assertTrue(result["ok"])
        self.assertEqual(result["route"], "keep_local")
        self.assertEqual(result["action"], "no_web_action")
        self.assertNotIn("selection", result)

    def test_uncertain_effort_sentinel_preserves_distribution_and_clarifies(self) -> None:
        for probabilities, confidence in (
            ({"fictional-balanced": 0.45, "fictional-deep": 0.10, route.NO_SUITABLE_EFFORT: 0.45}, 0.9),
            ({"fictional-balanced": 0.10, "fictional-deep": 0.10, route.NO_SUITABLE_EFFORT: 0.80}, 0.1),
        ):
            answers = delegated_answers()
            answers["effort_0"] = decision(route.NO_SUITABLE_EFFORT, probabilities, confidence)
            with mock.patch.object(route, "_post_jev", return_value=answers):
                result = route.route_task(base_input())
            self.assertTrue(result["ok"])
            self.assertEqual(result["route"], "clarify")
            self.assertEqual(result["action"], "no_web_action")
            self.assertEqual(result["receipt"]["effort"]["probabilities"], probabilities)
            self.assertNotIn("selection", result)

    def test_no_suitable_model_is_non_delegation_without_local_fallback(self) -> None:
        answers = {
            "route": decision("delegate", {"delegate": 0.90, "keep_local": 0.05, "clarify": 0.05}),
            "model": decision(
                route.NO_SUITABLE_MODEL,
                {"fictional-alpha": 0.05, "fictional-default": 0.05, "no_suitable_model": 0.90},
            ),
            "effort_no_suitable_model": decision(route.NO_SUITABLE_EFFORT, {route.NO_SUITABLE_EFFORT: 1.0}),
        }
        with mock.patch.object(route, "_post_jev", return_value=answers):
            result = route.route_task(base_input())

        self.assertTrue(result["ok"])
        self.assertEqual(result["route"], "keep_local")
        self.assertEqual(result["action"], "no_web_action")
        self.assertNotIn("selection", result)

    def test_keep_local_is_a_successful_non_delegation_decision(self) -> None:
        answers = delegated_answers()
        answers["route"] = decision("keep_local", {"delegate": 0.10, "keep_local": 0.85, "clarify": 0.05})
        with mock.patch.object(route, "_post_jev", return_value=answers):
            result = route.route_task(base_input())
        self.assertTrue(result["ok"])
        self.assertEqual(result["route"], "keep_local")
        self.assertEqual(result["action"], "no_web_action")

    def test_tie_or_low_confidence_fails_closed_without_web_selection(self) -> None:
        answers = delegated_answers()
        answers["route"] = decision("delegate", {"delegate": 0.50, "keep_local": 0.40, "clarify": 0.10}, 0.9)
        with mock.patch.object(route, "_post_jev", return_value=answers):
            result = route.route_task(base_input())
        self.assertTrue(result["ok"])
        self.assertEqual(result["route"], "clarify")
        self.assertNotIn("selection", result)

    def test_missing_or_unavailable_capabilities_send_no_request(self) -> None:
        cases = []
        not_reviewed = base_input()
        not_reviewed["disclosure_reviewed"] = False
        cases.append((not_reviewed, "disclosure_not_reviewed"))
        wrong_origin = base_input()
        wrong_origin["ui"]["origin"] = "https://example.invalid"
        cases.append((wrong_origin, "wrong_origin"))
        unauthenticated = base_input()
        unauthenticated["ui"]["authenticated"] = False
        cases.append((unauthenticated, "not_authenticated"))
        stale = base_input()
        stale["ui"]["snapshot_fresh"] = False
        cases.append((stale, "ui_stale"))
        changed_mode = base_input("search")
        changed_mode["ui"]["selected_mode"] = "chat"
        cases.append((changed_mode, "ui_stale"))
        unavailable = base_input("research")
        unavailable["ui"]["mode_compatibility"]["research"] = []
        cases.append((unavailable, "ui_unavailable"))

        with mock.patch.object(route, "_post_jev", side_effect=AssertionError("network called")) as call:
            for payload, code in cases:
                with self.subTest(code=code):
                    result = route.route_task(payload)
                    self.assertFalse(result["ok"])
                    self.assertEqual(result["error"]["code"], code)
        call.assert_not_called()

    def test_direct_route_task_rejects_oversized_ignored_fields_without_request(self) -> None:
        payload = base_input()
        payload["ignored"] = "x" * route.MAX_INPUT_BYTES
        with mock.patch.object(route, "_post_jev", side_effect=AssertionError("network called")) as call:
            result = route.route_task(payload)
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"]["code"], "input_too_large")
        call.assert_not_called()

    def test_invalid_input_shapes_and_duplicate_candidates_send_no_request(self) -> None:
        cases = [None, {}, "not an object"]
        duplicate = base_input()
        duplicate["ui"]["models"][1]["id"] = "fictional-alpha"
        cases.append(duplicate)
        duplicate_mode = base_input()
        duplicate_mode["ui"]["mode_compatibility"]["chat"] = ["fictional-alpha", "fictional-alpha"]
        cases.append(duplicate_mode)
        unknown_mode_model = base_input()
        unknown_mode_model["ui"]["mode_compatibility"]["chat"] = ["not-observed"]
        cases.append(unknown_mode_model)

        with mock.patch.object(route, "_post_jev", side_effect=AssertionError("network called")) as call:
            for payload in cases:
                result = route.route_task(payload)
                self.assertFalse(result["ok"])
                self.assertEqual(result["error"]["code"], "invalid_input")
        call.assert_not_called()

    def test_unknown_effort_and_malformed_decisions_are_rejected(self) -> None:
        malformed = delegated_answers()
        malformed["effort_0"]["choice"] = "not-observed"
        with mock.patch.object(route, "_post_jev", return_value=malformed):
            result = route.route_task(base_input())
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"]["code"], "invalid_response")

        tied = delegated_answers()
        tied["route"] = decision("delegate", {"delegate": 0.45, "keep_local": 0.45, "clarify": 0.10})
        with mock.patch.object(route, "_post_jev", return_value=tied):
            result = route.route_task(base_input())
        self.assertTrue(result["ok"])
        self.assertEqual(result["route"], "clarify")
        self.assertEqual(result["receipt"]["route"]["lead_over_next"], 0.0)

        for bad_probability in (True, float("nan"), float("inf"), -0.1):
            answers = delegated_answers()
            answers["route"]["probabilities"]["delegate"] = bad_probability
            with mock.patch.object(route, "_post_jev", return_value=answers):
                result = route.route_task(base_input())
            self.assertFalse(result["ok"])
            self.assertEqual(result["error"]["code"], "invalid_response")

    def test_unused_branches_do_not_invalidate_non_delegation(self) -> None:
        for choice in ("keep_local", "clarify"):
            probabilities = {name: 0.05 for name in route.ROUTE_OPTIONS}
            probabilities[choice] = 0.90
            with mock.patch.object(route, "_post_jev", return_value={
                "route": decision(choice, probabilities),
                "model": "malformed unused answer",
            }):
                result = route.route_task(base_input())
            self.assertTrue(result["ok"])
            self.assertEqual(result["route"], choice)
            self.assertEqual(result["receipt"]["used_decisions"], ["route"])

    def test_uncertain_keep_local_reports_clarify_with_distribution(self) -> None:
        with mock.patch.object(route, "_post_jev", return_value={
            "route": decision("keep_local", {"delegate": 0.33, "keep_local": 0.34, "clarify": 0.33}, 0.02),
        }):
            result = route.route_task(base_input())
        self.assertTrue(result["ok"])
        self.assertEqual(result["route"], "clarify")
        self.assertEqual(result["receipt"]["route"]["confidence"], 0.02)

    def test_no_model_and_uncertain_model_do_not_require_effort(self) -> None:
        for choice, probabilities, expected in (
            (route.NO_SUITABLE_MODEL, {"fictional-alpha": 0.05, "fictional-default": 0.05, route.NO_SUITABLE_MODEL: 0.90}, "keep_local"),
            ("fictional-alpha", {"fictional-alpha": 0.45, "fictional-default": 0.45, route.NO_SUITABLE_MODEL: 0.10}, "clarify"),
        ):
            answers = {"route": delegated_answers()["route"], "model": decision(choice, probabilities)}
            with mock.patch.object(route, "_post_jev", return_value=answers):
                result = route.route_task(base_input())
            self.assertTrue(result["ok"])
            self.assertEqual(result["route"], expected)
            self.assertEqual(result["receipt"]["used_decisions"], ["route", "model"])

    def test_network_failure_never_echoes_input_or_key(self) -> None:
        payload = base_input()
        payload["task_summary"] = SECRET
        with mock.patch.object(route, "_post_jev", side_effect=RuntimeError(SECRET)):
            result = route.route_task(payload)
        rendered = json.dumps(result)
        self.assertFalse(result["ok"])
        self.assertNotIn(SECRET, rendered)
        self.assertNotIn(DUMMY_KEY, rendered)


class TransportTests(unittest.TestCase):
    def setUp(self) -> None:
        self.key_patch = mock.patch.dict(os.environ, {"TYPESAFE_API_KEY": DUMMY_KEY})
        self.key_patch.start()

    def tearDown(self) -> None:
        self.key_patch.stop()

    def test_successful_http_response_is_bounded_and_decoded(self) -> None:
        payload = {"answers": {"route": {"choice": "delegate"}}}
        response = FakeResponse(json.dumps(payload).encode())
        calls = []

        def opener(request, timeout):
            calls.append((request, timeout))
            return response

        answers = route._post_jev({"state": {}, "questions": {}}, opener=opener, sleeper=lambda _: None)
        self.assertEqual(answers, payload["answers"])
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0][0].full_url, route.ENDPOINT)
        self.assertEqual(calls[0][0].get_header("Authorization"), f"Bearer {DUMMY_KEY}")
        self.assertTrue(response.closed)

    def test_http_statuses_are_distinguished_and_retry_is_bounded(self) -> None:
        for status, expected in ((401, "http_401"), (422, "http_422"), (429, "http_429"), (529, "http_529"), (500, "http_error")):
            calls = []

            def opener(request, timeout, status=status):
                calls.append(1)
                raise urllib.error.HTTPError(route.ENDPOINT, status, "server detail", {}, None)

            with self.subTest(status=status):
                with self.assertRaises(route.RouteFailure) as raised:
                    route._post_jev({}, opener=opener, sleeper=lambda _: None)
                self.assertEqual(raised.exception.code, expected)
                self.assertEqual(len(calls), 3 if status in (429, 529) else 1)

    def test_transport_and_malformed_body_fail_without_details(self) -> None:
        failures = [
            lambda request, timeout: (_ for _ in ()).throw(socket.timeout(SECRET)),
            lambda request, timeout: (_ for _ in ()).throw(urllib.error.URLError(socket.timeout(SECRET))),
            lambda request, timeout: FakeResponse(b"not json"),
            lambda request, timeout: FakeResponse(json.dumps([]).encode()),
            lambda request, timeout: FakeResponse(b"x" * (route.MAX_RESPONSE_BYTES + 1)),
        ]
        expected = ["timeout", "timeout", "invalid_response", "invalid_response", "response_too_large"]
        for opener, code in zip(failures, expected):
            with self.subTest(code=code):
                with self.assertRaises(route.RouteFailure) as raised:
                    route._post_jev({}, opener=opener, sleeper=lambda _: None)
                self.assertEqual(raised.exception.code, code)

    def test_non_byte_response_is_invalid_and_close_failure_is_ignored(self) -> None:
        class NonByteResponse:
            def read(self, limit: int = -1):
                return "not bytes"

            def close(self):
                raise RuntimeError(SECRET)

        with self.assertRaises(route.RouteFailure) as raised:
            route._post_jev({}, opener=lambda request, timeout: NonByteResponse())
        self.assertEqual(raised.exception.code, "invalid_response")

    def test_real_redirect_handler_rejects_and_closes_response(self) -> None:
        import io
        from email.message import Message

        for code in (301, 302, 303, 307, 308):
            headers = Message()
            headers["Location"] = "https://untrusted.example.invalid/"
            response = io.BytesIO(b"redacted")
            request = route.urllib.request.Request(route.ENDPOINT, headers={"Authorization": "Bearer " + DUMMY_KEY})
            with self.assertRaises(route.RedirectRejected):
                route.NoRedirectHandler().http_error_302(request, response, code, "redirect", headers)
            self.assertTrue(response.closed)

    def test_duplicate_and_deep_response_json_is_rejected(self) -> None:
        for body in (
            b'{"answers":{},"answers":{}}',
            b'{"answers":{"route":{"choice":"delegate","choice":"keep_local"}}}',
            b"[" * 10000 + b"0" + b"]" * 10000,
        ):
            with self.assertRaises(route.RouteFailure) as raised:
                route._post_jev({}, opener=lambda request, timeout: FakeResponse(body))
            self.assertEqual(raised.exception.code, "invalid_response")

    def test_redirect_is_rejected_before_forwarding(self) -> None:
        forwarded = []

        def opener(request, timeout):
            forwarded.append(request.full_url)
            raise route.RedirectRejected()

        with self.assertRaises(route.RouteFailure) as raised:
            route._post_jev({}, opener=opener, sleeper=lambda _: None)
        self.assertEqual(raised.exception.code, "redirect_rejected")
        self.assertEqual(forwarded, [route.ENDPOINT])

    def test_route_reads_the_current_callers_environment_key(self) -> None:
        author_or_previous_key = "offline-key-one"
        current_caller_key = "offline-key-two"
        seen_authorizations: list[str] = []
        response_body = json.dumps({"answers": {}}).encode()

        def opener(request, timeout):
            seen_authorizations.append(request.get_header("Authorization"))
            return FakeResponse(response_body)

        for key in (author_or_previous_key, current_caller_key):
            with self.subTest(key=key), mock.patch.dict(
                os.environ, {"TYPESAFE_API_KEY": key}, clear=True
            ):
                route._post_jev({}, opener=opener)

        self.assertEqual(
            seen_authorizations,
            [f"Bearer {author_or_previous_key}", f"Bearer {current_caller_key}"],
        )

    def test_missing_key_is_rejected_before_network(self) -> None:
        opener = mock.Mock()
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(route.RouteFailure) as raised:
                route._post_jev({}, opener=opener)
        self.assertEqual(raised.exception.code, "missing_key")
        opener.assert_not_called()


class CliTests(unittest.TestCase):
    def test_cli_invalid_json_is_nonzero_json_without_traceback(self) -> None:
        env = os.environ.copy()
        env["TYPESAFE_API_KEY"] = DUMMY_KEY
        completed = subprocess.run(
            [sys.executable, str(SCRIPTS / "route.py")],
            input=b"not-json",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            check=False,
        )
        self.assertNotEqual(completed.returncode, 0)
        self.assertNotIn(b"Traceback", completed.stderr)
        result = json.loads(completed.stdout)
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"]["code"], "invalid_input")
        self.assertNotIn(DUMMY_KEY.encode(), completed.stdout)

    def test_cli_rejects_deep_and_duplicate_json_without_traceback(self) -> None:
        for payload in (
            b"[" * 10000 + b"0" + b"]" * 10000,
            b'{"disclosure_reviewed":false,"disclosure_reviewed":true}',
            b'{"ui":{"authenticated":false,"authenticated":true}}',
        ):
            completed = subprocess.run(
                [sys.executable, str(SCRIPTS / "route.py")],
                input=payload, capture_output=True, check=False,
            )
            self.assertEqual(completed.returncode, 2)
            self.assertEqual(completed.stderr, b"")
            self.assertEqual(json.loads(completed.stdout)["error"]["code"], "invalid_input")

    def test_cli_examples_are_offline_and_fictitious(self) -> None:
        for flag in ("--example-input", "--example-output"):
            completed = subprocess.run(
                [sys.executable, str(SCRIPTS / "route.py"), flag],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            with self.subTest(flag=flag):
                self.assertEqual(completed.returncode, 0)
                self.assertEqual(completed.stderr, b"")
                payload = json.loads(completed.stdout)
                if flag == "--example-input":
                    # Keep the documented fixture executable against the same
                    # preflight schema used by real callers.
                    self.assertEqual(route._validate_input(payload).mode, "search")
                self.assertNotIn(b"gpt-", completed.stdout.lower())

    def test_cli_with_mocked_jev_accepts_non_delegation_without_network(self) -> None:
        fixture = base_input()
        answers = delegated_answers()
        answers["route"] = decision("keep_local", {"delegate": 0.1, "keep_local": 0.85, "clarify": 0.05})
        source = """
import io, json, os, sys
sys.path.insert(0, %r)
import route
route._post_jev = lambda payload: %r
sys.stdin = io.StringIO(%r)
raise SystemExit(route.main([]))
""" % (str(SCRIPTS), answers, json.dumps(fixture))
        env = os.environ.copy()
        env["TYPESAFE_API_KEY"] = DUMMY_KEY
        completed = subprocess.run(
            [sys.executable, "-c", source],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            check=False,
        )
        self.assertEqual(completed.returncode, 0)
        self.assertEqual(json.loads(completed.stdout)["route"], "keep_local")
        self.assertNotIn(DUMMY_KEY.encode(), completed.stdout)


if __name__ == "__main__":
    unittest.main()
