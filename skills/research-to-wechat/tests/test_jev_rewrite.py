#!/usr/bin/env python3
"""Offline tests for the conditional original-rewrite evaluator.

Every fixture is clearly synthetic and no test performs a network request. These
tests verify request construction, strict response validation, gate arithmetic,
status bookkeeping and failure handling. They cannot establish model accuracy,
copyright clearance, research quality or real readership.
"""

from __future__ import annotations

import io
import json
import sys
import unittest
import urllib.error
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import jev_rewrite as jev  # noqa: E402

FAKE_KEY = "SYNTHETIC-TEST-KEY-not-a-real-credential"
ENV = {jev.API_KEY_ENV: FAKE_KEY}

LOW_RISK = {"0": 0.9, "1": 0.07, "2": 0.02, "3": 0.01, "4": 0.0}
HIGH_RISK = {"0": 0.05, "1": 0.05, "2": 0.1, "3": 0.4, "4": 0.4}
TAIL_RISK = {"0": 0.85, "1": 0.0, "2": 0.0, "3": 0.0, "4": 0.15}
GOOD_EDITORIAL = {"0": 0.02, "1": 0.08, "2": 0.4, "3": 0.4, "4": 0.1}
WEAK_EDITORIAL = {"0": 0.4, "1": 0.4, "2": 0.15, "3": 0.05, "4": 0.0}


def sample_input(**overrides: object) -> dict:
    payload = {
        "intake": {
            "request_text": "SYNTHETIC TEST 请保留方法论重写这篇素材。",
            "source_inventory": ["SYNTHETIC TEST source: fixture.md (full body)"],
            "source_body_obtained": True,
            "rewrite_intent": True,
            "no_rewrite_restriction": False,
        },
        "original": "SYNTHETIC TEST ORIGINAL placeholder body.",
        "draft": "SYNTHETIC TEST DRAFT placeholder body.",
        "title": "SYNTHETIC TEST TITLE",
        "cover_brief": "SYNTHETIC TEST cover direction placeholder.",
        "audience": "SYNTHETIC TEST audience placeholder.",
        "persona_assumptions": "SYNTHETIC TEST persona assumption placeholder.",
        "proposed_issues": [],
        "round": 1,
    }
    payload.update(overrides)
    return payload


def answer(probabilities: dict, confidence: float = 0.8, score: float | None = None) -> dict:
    if score is None:
        # A real Score answer reports the probability-weighted expected level index,
        # rounded by the provider, not the most likely level.
        score = round(sum(index * probabilities[str(index)] for index in range(jev.SCALE_LEVELS)), 2)
    return {
        "type": "score",
        "score": score,
        "probabilities": dict(probabilities),
        "confidence": confidence,
        "legend": ["SYNTHETIC level 0", "1", "2", "3", "4"],
    }


def sample_response(**overrides: object) -> dict:
    answers = {name: answer(LOW_RISK) for name in jev.RISK_DIMENSIONS}
    answers.update({name: answer(GOOD_EDITORIAL) for name in jev.EDITORIAL_DIMENSIONS})
    answers.update(overrides)  # type: ignore[arg-type]
    return {
        "model": "SYNTHETIC-TEST-MODEL",
        "answers": answers,
        "usage": {"input_tokens": 1, "output_tokens": 1},
    }


class Poster:
    """Synthetic transport: records calls, never touches the network."""

    def __init__(self, responses: list) -> None:
        self.responses = list(responses)
        self.calls: list[dict] = []
        self.keys: list[str] = []

    def __call__(self, payload: dict, api_key: str, timeout: float) -> bytes:
        self.calls.append(payload)
        self.keys.append(api_key)
        item = self.responses.pop(0) if self.responses else self.responses
        if isinstance(item, Exception):
            raise item
        if isinstance(item, (bytes, bytearray)):
            return bytes(item)
        return json.dumps(item).encode("utf-8")


def forbidden_post(payload: dict, api_key: str, timeout: float) -> bytes:
    raise AssertionError("no provider request may be made in this case")


def run(payload: dict, env: dict | None = None, poster: object | None = None) -> dict:
    post = poster if poster is not None else Poster([sample_response()])
    return jev.evaluate(payload, ENV if env is None else env, post=post, sleep=lambda _seconds: None)


class PolicyAndExampleTests(unittest.TestCase):
    def test_policy_version_and_thresholds(self) -> None:
        data = jev.policy()
        self.assertEqual(data["policy_version"], "screening-policy-1")
        self.assertEqual(data["risk_gate"]["max_expected_score"], 1.0)
        self.assertEqual(data["risk_gate"]["max_severe_tail_probability"], 0.05)
        self.assertEqual(data["risk_gate"]["min_confidence"], 0.50)
        self.assertEqual(data["risk_gate"]["severe_levels"], [3, 4])
        self.assertEqual(data["editorial_gate"]["min_expected_score"], 2.0)
        self.assertIsNone(data["editorial_gate"]["min_confidence"])
        self.assertEqual(data["revision_budget"], 3)

    def test_policy_digest_changes_with_policy(self) -> None:
        before = jev.policy_digest()
        original = jev.RISK_MAX_EXPECTED_SCORE
        try:
            jev.RISK_MAX_EXPECTED_SCORE = 2.0
            self.assertNotEqual(jev.policy_digest(), before)
        finally:
            jev.RISK_MAX_EXPECTED_SCORE = original
        self.assertEqual(jev.policy_digest(), before)

    def test_examples_are_synthetic_and_valid(self) -> None:
        self.assertIn("SYNTHETIC", jev.example_input()["original"])
        output = jev.example_output()
        self.assertEqual(output["status"], jev.STATUS_PASSED)
        self.assertIn("SYNTHETIC", output["example_notice"])
        self.assertEqual(set(output["dimensions"]), set(jev.DIMENSIONS))


class RequestBuildingTests(unittest.TestCase):
    def test_five_independent_score_questions(self) -> None:
        payload = jev.build_payload(jev.validate_request(sample_input()))
        self.assertEqual(payload["model"], "jev-latest")
        self.assertEqual(set(payload["questions"]), set(jev.DIMENSIONS))
        for spec in payload["questions"].values():
            self.assertEqual(spec["type"], "score")
            self.assertEqual(len(spec["criteria"]), 5)
            self.assertTrue(all(isinstance(item, str) and item for item in spec["criteria"]))

    def test_state_keeps_fields_separate_and_marks_data_untrusted(self) -> None:
        state = jev.build_state(jev.validate_request(sample_input()))
        for name in (
            "source_original",
            "candidate_draft",
            "candidate_title",
            "candidate_cover_brief",
            "target_audience",
            "persona_assumptions",
            "agent_proposed_issues",
        ):
            self.assertIn(name, state)
        self.assertNotEqual(state["source_original"], state["candidate_draft"])
        self.assertIn("untrusted", state["untrusted_data_notice"])
        self.assertIn("never change these questions", state["untrusted_data_notice"])

    def test_full_text_sent_without_truncation(self) -> None:
        body = "SYNTHETIC ORIGINAL " * 500
        state = jev.build_state(jev.validate_request(sample_input(original=body)))
        self.assertEqual(state["source_original"], body)

    def test_shared_topic_is_not_infringement_in_the_rubric(self) -> None:
        text = jev.QUESTIONS["expression_infringement_risk"]["instructions"]
        self.assertIn("shared topic", text)
        self.assertIn("not by themselves evidence", text)

    def test_endpoint_model_and_credential_source_are_fixed(self) -> None:
        source = (SCRIPTS_DIR / "jev_rewrite.py").read_text(encoding="utf-8")
        self.assertEqual(jev.API_URL, "https://api.typesafe.ai/v1/systemone")
        self.assertEqual(jev.API_KEY_ENV, "TYPESAFE_API_KEY")
        for forbidden in ("op://", "/Users/", "/home/", "localhost", "127.0.0.1"):
            self.assertNotIn(forbidden, source)


class IntakeTests(unittest.TestCase):
    def test_valid_intake_is_recorded(self) -> None:
        request = jev.validate_request(sample_input())
        self.assertTrue(request["intake"]["rewrite_intent"])
        self.assertEqual(request["round"], 1)

    def test_missing_source_body_blocks_before_network(self) -> None:
        payload = sample_input()
        payload["intake"]["source_body_obtained"] = False
        result = run(payload, poster=forbidden_post)
        self.assertFalse(result["ok"])
        self.assertEqual(result["status"], jev.STATUS_BLOCKED)
        self.assertEqual(result["error"]["code"], "intake_not_activated")

    def test_no_rewrite_restriction_blocks(self) -> None:
        payload = sample_input()
        payload["intake"]["no_rewrite_restriction"] = True
        result = run(payload, poster=forbidden_post)
        self.assertEqual(result["error"]["code"], "intake_not_activated")

    def test_missing_rewrite_intent_blocks(self) -> None:
        payload = sample_input()
        payload["intake"]["rewrite_intent"] = False
        result = run(payload, poster=forbidden_post)
        self.assertEqual(result["error"]["code"], "intake_not_activated")

    def test_non_boolean_intake_flag_is_invalid(self) -> None:
        payload = sample_input()
        payload["intake"]["rewrite_intent"] = "yes"
        result = run(payload, poster=forbidden_post)
        self.assertEqual(result["error"]["code"], "invalid_input")

    def test_empty_source_inventory_is_invalid(self) -> None:
        payload = sample_input()
        payload["intake"]["source_inventory"] = []
        self.assertEqual(run(payload, poster=forbidden_post)["error"]["code"], "invalid_input")

    def test_proposed_issues_require_evidence(self) -> None:
        payload = sample_input(proposed_issues=[{"issue": "SYNTHETIC issue"}])
        self.assertEqual(run(payload, poster=forbidden_post)["error"]["code"], "invalid_input")

    def test_proposed_issues_are_attributed_to_the_agent(self) -> None:
        payload = sample_input(
            proposed_issues=[{"issue": "SYNTHETIC issue", "evidence": "SYNTHETIC evidence"}]
        )
        result = run(payload)
        self.assertEqual(result["agent_proposed_issues"][0]["author"], "writing_agent")


class InputValidationTests(unittest.TestCase):
    def test_each_required_text_field_must_be_non_empty(self) -> None:
        for field in ("original", "draft", "title", "cover_brief", "audience", "persona_assumptions"):
            with self.subTest(field=field):
                result = run(sample_input(**{field: "   "}), poster=forbidden_post)
                self.assertEqual(result["error"]["code"], "invalid_input")
                self.assertIn(field, result["error"]["message"])

    def test_round_must_be_a_positive_integer(self) -> None:
        for bad in (0, -1, True, "1", 1.5):
            with self.subTest(value=bad):
                result = run(sample_input(round=bad), poster=forbidden_post)
                self.assertEqual(result["error"]["code"], "invalid_input")

    def test_oversized_field_is_blocked_before_any_network_call(self) -> None:
        payload = sample_input(original="x" * (jev.MAX_FIELD_CHARS + 1))
        result = run(payload, poster=forbidden_post)
        self.assertEqual(result["status"], jev.STATUS_BLOCKED)
        self.assertEqual(result["error"]["code"], "input_too_large")
        self.assertIn("unresolved coverage", result["error"]["message"])
        self.assertIn("original", result["error"]["message"])

    def test_oversized_combined_state_is_blocked(self) -> None:
        size = jev.MAX_FIELD_CHARS
        payload = sample_input(original="x" * size, draft="y" * size, audience="z" * size)
        result = run(payload, poster=forbidden_post)
        self.assertEqual(result["error"]["code"], "input_too_large")
        self.assertIn("combined_state", result["error"]["message"])

    def test_non_object_input_is_invalid(self) -> None:
        self.assertEqual(run(["not", "an", "object"], poster=forbidden_post)["error"]["code"], "invalid_input")


class ResponseValidationTests(unittest.TestCase):
    def assert_response_rejected(self, response: object) -> dict:
        result = run(sample_input(), poster=Poster([response]))
        self.assertFalse(result["ok"])
        self.assertEqual(result["status"], jev.STATUS_BLOCKED)
        self.assertEqual(result["error"]["code"], "provider_response_invalid")
        self.assertNotIn("dimensions", result)
        return result

    def test_missing_answer_blocks(self) -> None:
        response = sample_response()
        del response["answers"]["title_potential"]
        self.assert_response_rejected(response)

    def test_missing_answers_object_blocks(self) -> None:
        self.assert_response_rejected({"model": "SYNTHETIC"})

    def test_wrong_question_type_blocks(self) -> None:
        bad = answer(GOOD_EDITORIAL)
        bad["type"] = "choice"
        self.assert_response_rejected(sample_response(title_potential=bad))

    def test_missing_probability_level_blocks(self) -> None:
        bad = answer(GOOD_EDITORIAL)
        del bad["probabilities"]["4"]
        self.assert_response_rejected(sample_response(article_potential=bad))

    def test_unknown_probability_level_blocks(self) -> None:
        bad = answer(GOOD_EDITORIAL)
        bad["probabilities"]["5"] = 0.0
        self.assert_response_rejected(sample_response(article_potential=bad))

    def test_distribution_not_summing_to_one_blocks(self) -> None:
        bad = answer({"0": 0.5, "1": 0.1, "2": 0.1, "3": 0.1, "4": 0.1})
        self.assert_response_rejected(sample_response(homogeneity=bad))

    def test_nan_infinity_and_boolean_probabilities_block(self) -> None:
        for value in (float("nan"), float("inf"), float("-inf"), True, "0.5", None):
            with self.subTest(value=repr(value)):
                bad = answer(GOOD_EDITORIAL)
                bad["probabilities"]["2"] = value
                self.assert_response_rejected(sample_response(article_potential=bad))

    def test_negative_probability_blocks(self) -> None:
        bad = answer({"0": 1.2, "1": -0.2, "2": 0.0, "3": 0.0, "4": 0.0}, score=0)
        self.assert_response_rejected(sample_response(expression_infringement_risk=bad))

    def test_score_inconsistent_with_distribution_blocks(self) -> None:
        bad = answer(LOW_RISK, score=4)
        self.assert_response_rejected(sample_response(expression_infringement_risk=bad))

    def test_score_out_of_scale_or_of_the_wrong_type_blocks(self) -> None:
        # 5 and -1 are off the 0-4 scale; 1.0 is on the scale but contradicts the
        # distribution; True, "2" and None are not real numbers at all.
        for value in (5, -1, 1.0, True, "2", None):
            with self.subTest(value=repr(value)):
                bad = answer(GOOD_EDITORIAL)
                bad["score"] = value
                self.assert_response_rejected(sample_response(article_potential=bad))

    def test_invalid_confidence_blocks(self) -> None:
        for value in (1.5, -0.1, float("nan"), True, "0.8", None):
            with self.subTest(value=repr(value)):
                bad = answer(GOOD_EDITORIAL, confidence=0.8)
                bad["confidence"] = value
                self.assert_response_rejected(sample_response(article_potential=bad))

    def test_malformed_json_body_blocks(self) -> None:
        self.assert_response_rejected(b"{not json")

    def test_non_object_body_blocks(self) -> None:
        self.assert_response_rejected(b"[1, 2, 3]")

    def test_oversized_body_blocks(self) -> None:
        result = run(sample_input(), poster=Poster([b"x" * (jev.MAX_RESPONSE_BYTES + 1)]))
        self.assertEqual(result["error"]["code"], "provider_response_too_large")

    def test_fractional_expected_score_is_accepted(self) -> None:
        """The provider reports Σ(level × probability), which is normally fractional."""
        spread = {"0": 0.0, "1": 0.0, "2": 0.4, "3": 0.4, "4": 0.2}
        validated = jev.validate_answer(answer(spread, score=2.8), "article_potential")
        self.assertAlmostEqual(validated["score"], 2.8)
        self.assertAlmostEqual(validated["expected_score"], 2.8)

    def test_argmax_level_inconsistent_with_the_expectation_is_rejected(self) -> None:
        """An argmax level is not a valid score when it disagrees with the distribution."""
        spread = {"0": 0.0, "1": 0.0, "2": 0.4, "3": 0.4, "4": 0.2}
        for score in (2, 3):
            with self.subTest(score=score):
                with self.assertRaises(jev.JevError):
                    jev.validate_answer(answer(spread, score=score), "article_potential")

    def test_provider_rounding_of_the_score_is_tolerated(self) -> None:
        """Observed on a real response: the provider rounds score and probabilities apart."""
        spread = {"0": 0.71, "1": 0.28, "2": 0.01, "3": 0.0, "4": 0.0}
        validated = jev.validate_answer(answer(spread, score=0.32), "expression_infringement_risk")
        self.assertAlmostEqual(validated["score"], 0.32)
        self.assertAlmostEqual(validated["expected_score"], 0.30)

    def test_score_beyond_the_rounding_bound_is_rejected(self) -> None:
        spread = {"0": 0.71, "1": 0.28, "2": 0.01, "3": 0.0, "4": 0.0}
        with self.assertRaises(jev.JevError):
            jev.validate_answer(answer(spread, score=0.40), "expression_infringement_risk")

    def test_full_distribution_and_confidence_are_preserved(self) -> None:
        result = run(sample_input())
        dimension = result["dimensions"]["article_potential"]
        self.assertEqual(dimension["probabilities"], GOOD_EDITORIAL)
        self.assertEqual(dimension["confidence"], 0.8)
        self.assertEqual(len(dimension["criteria"]), 5)
        self.assertIn("legend", dimension)


class ArithmeticTests(unittest.TestCase):
    def test_expected_score_uses_level_indices_not_percentages(self) -> None:
        self.assertEqual(jev.expected_score({"0": 1.0, "1": 0.0, "2": 0.0, "3": 0.0, "4": 0.0}), 0.0)
        self.assertEqual(jev.expected_score({"0": 0.0, "1": 0.0, "2": 0.0, "3": 0.0, "4": 1.0}), 4.0)
        self.assertEqual(jev.expected_score(GOOD_EDITORIAL), 2.48)

    def test_severe_tail_is_levels_three_and_four(self) -> None:
        self.assertEqual(jev.severe_tail(TAIL_RISK), 0.15)
        self.assertEqual(jev.severe_tail(LOW_RISK), 0.01)

    def test_only_risk_dimensions_report_a_severe_tail(self) -> None:
        """Levels 3 and 4 are severe on a risk scale and desirable on an editorial one."""
        result = run(sample_input())
        for name in jev.RISK_DIMENSIONS:
            dimension = result["dimensions"][name]
            self.assertIn("severe_tail_probability", dimension)
            self.assertNotIn("top_tail_probability", dimension)
        for name in jev.EDITORIAL_DIMENSIONS:
            dimension = result["dimensions"][name]
            self.assertIn("top_tail_probability", dimension)
            self.assertNotIn("severe_tail_probability", dimension)


class GateTests(unittest.TestCase):
    def test_all_gates_met_passes(self) -> None:
        result = run(sample_input())
        self.assertTrue(result["ok"])
        self.assertEqual(result["status"], jev.STATUS_PASSED)
        self.assertEqual(result["gaps"], [])
        self.assertEqual(result["policy_version"], "screening-policy-1")
        self.assertTrue(all(d["gate"]["passed"] for d in result["dimensions"].values()))

    def test_high_expression_risk_alone_fails(self) -> None:
        result = run(sample_input(), poster=Poster([sample_response(expression_infringement_risk=answer(HIGH_RISK))]))
        self.assertEqual(result["status"], jev.STATUS_NEEDS_REVISION)
        reasons = result["dimensions"]["expression_infringement_risk"]["gate"]["reasons"]
        self.assertIn("expected_score_above_maximum", reasons)
        self.assertIn("severe_tail_above_maximum", reasons)

    def test_high_homogeneity_alone_fails(self) -> None:
        result = run(sample_input(), poster=Poster([sample_response(homogeneity=answer(HIGH_RISK))]))
        self.assertEqual(result["status"], jev.STATUS_NEEDS_REVISION)
        self.assertFalse(result["dimensions"]["homogeneity"]["gate"]["passed"])
        self.assertTrue(result["dimensions"]["expression_infringement_risk"]["gate"]["passed"])

    def test_each_editorial_dimension_alone_can_fail(self) -> None:
        for name in jev.EDITORIAL_DIMENSIONS:
            with self.subTest(dimension=name):
                result = run(sample_input(), poster=Poster([sample_response(**{name: answer(WEAK_EDITORIAL)})]))
                self.assertEqual(result["status"], jev.STATUS_NEEDS_REVISION)
                self.assertEqual(
                    result["dimensions"][name]["gate"]["reasons"], ["expected_score_below_minimum"]
                )
                self.assertEqual(len(result["gaps"]), 1)

    def test_severe_tail_fails_even_with_a_passing_mean(self) -> None:
        response = sample_response(expression_infringement_risk=answer(TAIL_RISK))
        result = run(sample_input(), poster=Poster([response]))
        dimension = result["dimensions"]["expression_infringement_risk"]
        self.assertLessEqual(dimension["expected_score"], jev.RISK_MAX_EXPECTED_SCORE)
        self.assertEqual(dimension["gate"]["reasons"], ["severe_tail_above_maximum"])
        self.assertEqual(result["status"], jev.STATUS_NEEDS_REVISION)

    def test_low_confidence_blocks_risk_only(self) -> None:
        low = 0.49
        for name in jev.RISK_DIMENSIONS:
            with self.subTest(dimension=name):
                result = run(sample_input(), poster=Poster([sample_response(**{name: answer(LOW_RISK, low)})]))
                self.assertEqual(result["status"], jev.STATUS_NEEDS_REVISION)
                self.assertIn("confidence_below_floor", result["dimensions"][name]["gate"]["reasons"])
        for name in jev.EDITORIAL_DIMENSIONS:
            with self.subTest(dimension=name):
                result = run(
                    sample_input(), poster=Poster([sample_response(**{name: answer(GOOD_EDITORIAL, low)})])
                )
                self.assertEqual(result["status"], jev.STATUS_PASSED)
                self.assertIsNone(result["dimensions"][name]["gate"]["checks"]["min_confidence"])

    def test_confidence_exactly_at_the_floor_passes(self) -> None:
        response = sample_response(homogeneity=answer(LOW_RISK, jev.RISK_MIN_CONFIDENCE))
        self.assertEqual(run(sample_input(), poster=Poster([response]))["status"], jev.STATUS_PASSED)

    def test_editorial_scores_never_offset_a_risk_failure(self) -> None:
        top = {"0": 0.0, "1": 0.0, "2": 0.0, "3": 0.0, "4": 1.0}
        response = sample_response(expression_infringement_risk=answer(HIGH_RISK))
        for name in jev.EDITORIAL_DIMENSIONS:
            response["answers"][name] = answer(top, 0.99)
        result = run(sample_input(), poster=Poster([response]))
        self.assertEqual(result["status"], jev.STATUS_NEEDS_REVISION)
        self.assertTrue(any("expression_infringement_risk" in gap for gap in result["gaps"]))

    def test_boundary_values_are_inclusive(self) -> None:
        at_limit = {"0": 0.0, "1": 1.0, "2": 0.0, "3": 0.0, "4": 0.0}
        exact_tail = {"0": 0.95, "1": 0.0, "2": 0.0, "3": 0.05, "4": 0.0}
        exact_editorial = {"0": 0.0, "1": 0.0, "2": 1.0, "3": 0.0, "4": 0.0}
        response = sample_response(
            expression_infringement_risk=answer(at_limit),
            homogeneity=answer(exact_tail),
            article_potential=answer(exact_editorial),
        )
        self.assertEqual(run(sample_input(), poster=Poster([response]))["status"], jev.STATUS_PASSED)


class BudgetTests(unittest.TestCase):
    def test_failing_final_budgeted_round_reports_exhaustion(self) -> None:
        response = sample_response(homogeneity=answer(HIGH_RISK))
        result = run(sample_input(round=3), poster=Poster([response]))
        self.assertEqual(result["status"], jev.STATUS_NEEDS_REVISION)
        self.assertTrue(result["budget_exhausted"])
        self.assertTrue(any("budget exhausted" in gap for gap in result["gaps"]))

    def test_passing_final_budgeted_round_still_passes(self) -> None:
        result = run(sample_input(round=3))
        self.assertEqual(result["status"], jev.STATUS_PASSED)
        self.assertFalse(result["budget_exhausted"])

    def test_round_beyond_budget_makes_no_request_and_never_passes(self) -> None:
        result = run(sample_input(round=4), poster=forbidden_post)
        self.assertEqual(result["status"], jev.STATUS_NEEDS_REVISION)
        self.assertTrue(result["budget_exhausted"])
        self.assertEqual(result["dimensions"], {})
        self.assertTrue(any("budget exhausted" in gap for gap in result["gaps"]))

    def test_transient_retries_do_not_consume_the_revision_budget(self) -> None:
        poster = Poster(
            [
                jev.JevError("provider_rate_limited", transient=True),
                jev.JevError("provider_overloaded", transient=True),
                sample_response(),
            ]
        )
        result = run(sample_input(round=1), poster=poster)
        self.assertEqual(result["status"], jev.STATUS_PASSED)
        self.assertEqual(result["round"], 1)
        self.assertEqual(result["provider"]["transient_retries"], 2)


class StalenessTests(unittest.TestCase):
    def passed_record(self, payload: dict) -> dict:
        result = run(payload)
        self.assertEqual(result["status"], jev.STATUS_PASSED)
        return result

    def test_identical_version_verifies_without_a_request(self) -> None:
        payload = sample_input()
        previous = self.passed_record(payload)
        check = dict(payload, verify_only=True, previous_result=previous, round=2)
        result = jev.evaluate(check, ENV, post=forbidden_post)
        self.assertEqual(result["status"], jev.STATUS_PASSED)
        self.assertTrue(result["verified_without_new_request"])

    def test_changed_draft_is_stale(self) -> None:
        payload = sample_input()
        previous = self.passed_record(payload)
        changed = dict(
            payload,
            draft="SYNTHETIC TEST DRAFT after renderer link normalization.",
            verify_only=True,
            previous_result=previous,
        )
        result = jev.evaluate(changed, ENV, post=forbidden_post)
        self.assertEqual(result["status"], jev.STATUS_STALE)
        self.assertEqual(result["changed_since_assessment"], ["draft"])

    def test_changed_title_or_cover_brief_is_stale(self) -> None:
        payload = sample_input()
        previous = self.passed_record(payload)
        for field in ("title", "cover_brief", "original"):
            with self.subTest(field=field):
                changed = dict(
                    payload,
                    verify_only=True,
                    previous_result=previous,
                    **{field: "SYNTHETIC TEST changed value"},
                )
                result = jev.evaluate(changed, ENV, post=forbidden_post)
                self.assertEqual(result["status"], jev.STATUS_STALE)
                self.assertEqual(result["changed_since_assessment"], [field])

    def test_changed_policy_is_stale(self) -> None:
        payload = sample_input()
        previous = self.passed_record(payload)
        previous["input_identity"]["policy"] = "sha256:" + "0" * 64
        check = dict(payload, verify_only=True, previous_result=previous)
        result = jev.evaluate(check, ENV, post=forbidden_post)
        self.assertEqual(result["status"], jev.STATUS_STALE)
        self.assertEqual(result["changed_since_assessment"], ["policy"])

    def test_a_hand_written_pass_claim_without_dimensions_is_blocked(self) -> None:
        """A `status: passed` string is not evidence; the gates are recomputed."""
        payload = sample_input()
        previous = self.passed_record(payload)
        forged = {"status": jev.STATUS_PASSED, "input_identity": previous["input_identity"]}
        check = dict(payload, verify_only=True, previous_result=forged)
        result = jev.evaluate(check, ENV, post=forbidden_post)
        self.assertFalse(result["ok"])
        self.assertEqual(result["status"], jev.STATUS_BLOCKED)
        self.assertEqual(result["error"]["code"], "invalid_input")

    def test_a_pass_claim_over_failing_recorded_scores_is_not_promoted(self) -> None:
        """Recorded distributions that fail a gate outrank the recorded status."""
        payload = sample_input()
        failing = run(payload, poster=Poster([sample_response(homogeneity=answer(HIGH_RISK))]))
        forged = dict(failing, status=jev.STATUS_PASSED, gaps=[])
        check = dict(payload, verify_only=True, previous_result=forged)
        result = jev.evaluate(check, ENV, post=forbidden_post)
        self.assertEqual(result["status"], jev.STATUS_NEEDS_REVISION)
        self.assertTrue(any("homogeneity" in gap for gap in result["gaps"]))

    def test_tampered_recorded_distribution_is_blocked(self) -> None:
        payload = sample_input()
        previous = self.passed_record(payload)
        previous["dimensions"]["homogeneity"]["probabilities"]["4"] = 0.5
        check = dict(payload, verify_only=True, previous_result=previous)
        result = jev.evaluate(check, ENV, post=forbidden_post)
        self.assertEqual(result["status"], jev.STATUS_BLOCKED)
        self.assertEqual(result["error"]["code"], "invalid_input")

    def test_unpassed_previous_result_is_not_promoted(self) -> None:
        payload = sample_input()
        failing = run(payload, poster=Poster([sample_response(homogeneity=answer(HIGH_RISK))]))
        check = dict(payload, verify_only=True, previous_result=failing)
        result = jev.evaluate(check, ENV, post=forbidden_post)
        self.assertEqual(result["status"], jev.STATUS_NEEDS_REVISION)

    def test_input_identity_covers_the_policy_and_the_four_texts(self) -> None:
        identity = jev.input_identity(jev.validate_request(sample_input()))
        self.assertEqual(
            set(identity), {"original", "draft", "title", "cover_brief", "policy", "policy_version"}
        )
        self.assertTrue(all(str(value).startswith("sha256:") for key, value in identity.items() if key != "policy_version"))


class TransportTests(unittest.TestCase):
    def fake_opener(self, behavior):
        outer = self

        class FakeResponse:
            def __init__(self, body: bytes, status: int = 200) -> None:
                self.body = body
                self.status = status

            def read(self, size: int = -1) -> bytes:
                return self.body[:size] if size and size > 0 else self.body

            def __enter__(self):
                return self

            def __exit__(self, *_args) -> bool:
                return False

        class FakeOpener:
            def open(self, request, timeout=None):
                outer.captured.append((request, timeout))
                outcome = behavior()
                if isinstance(outcome, Exception):
                    raise outcome
                return FakeResponse(*outcome)

        return lambda *_handlers: FakeOpener()

    def setUp(self) -> None:
        self.captured: list = []
        self._original = jev.urllib.request.build_opener

    def tearDown(self) -> None:
        jev.urllib.request.build_opener = self._original

    def install(self, behavior) -> None:
        jev.urllib.request.build_opener = self.fake_opener(behavior)

    def http_error(self, status: int) -> urllib.error.HTTPError:
        return urllib.error.HTTPError(jev.API_URL, status, "synthetic", {}, None)

    def test_successful_post_uses_the_documented_endpoint_and_bearer_header(self) -> None:
        self.install(lambda: (json.dumps(sample_response()).encode("utf-8"), 200))
        body = jev.http_post_json({"model": jev.API_MODEL}, FAKE_KEY, 5.0)
        request, timeout = self.captured[0]
        self.assertEqual(request.full_url, "https://api.typesafe.ai/v1/systemone")
        self.assertEqual(request.get_method(), "POST")
        self.assertEqual(request.get_header("Authorization"), f"Bearer {FAKE_KEY}")
        self.assertEqual(request.get_header("Content-type"), "application/json")
        self.assertEqual(timeout, 5.0)
        self.assertNotIn(FAKE_KEY, request.data.decode("utf-8"))
        self.assertIn(b"answers", body)

    def test_timeout_is_a_sanitized_unreachable_error(self) -> None:
        self.install(lambda: TimeoutError("synthetic socket timeout at 10.0.0.1"))
        with self.assertRaises(jev.JevError) as caught:
            jev.http_post_json({}, FAKE_KEY, 1.0)
        self.assertEqual(caught.exception.code, "provider_unreachable")
        self.assertNotIn("10.0.0.1", caught.exception.message)

    def test_url_error_is_sanitized(self) -> None:
        self.install(lambda: urllib.error.URLError("synthetic dns failure detail"))
        with self.assertRaises(jev.JevError) as caught:
            jev.http_post_json({}, FAKE_KEY, 1.0)
        self.assertEqual(caught.exception.code, "provider_unreachable")
        self.assertNotIn("dns failure", caught.exception.message)

    def test_http_statuses_map_to_stable_codes(self) -> None:
        expected = {
            401: ("provider_unauthorized", False),
            422: ("provider_invalid_request", False),
            429: ("provider_rate_limited", True),
            529: ("provider_overloaded", True),
            500: ("provider_http_error", False),
        }
        for status, (code, transient) in expected.items():
            with self.subTest(status=status):
                self.install(lambda status=status: self.http_error(status))
                with self.assertRaises(jev.JevError) as caught:
                    jev.http_post_json({}, FAKE_KEY, 1.0)
                self.assertEqual(caught.exception.code, code)
                self.assertEqual(caught.exception.transient, transient)

    def test_non_200_success_status_is_rejected(self) -> None:
        self.install(lambda: (b"{}", 204))
        with self.assertRaises(jev.JevError) as caught:
            jev.http_post_json({}, FAKE_KEY, 1.0)
        self.assertEqual(caught.exception.code, "provider_http_error")

    def test_redirects_are_rejected(self) -> None:
        handler = jev._NoRedirectHandler()
        with self.assertRaises(jev.JevError) as caught:
            handler.redirect_request(None, None, 302, "Found", {}, "https://example.invalid/moved")
        self.assertEqual(caught.exception.code, "provider_redirect")
        self.install(lambda: jev.JevError("provider_redirect"))
        with self.assertRaises(jev.JevError) as escaped:
            jev.http_post_json({}, FAKE_KEY, 1.0)
        self.assertEqual(escaped.exception.code, "provider_redirect")

    def test_response_larger_than_the_budget_is_rejected(self) -> None:
        self.install(lambda: (b"x" * (jev.MAX_RESPONSE_BYTES + 1), 200))
        with self.assertRaises(jev.JevError) as caught:
            jev.http_post_json({}, FAKE_KEY, 1.0)
        self.assertEqual(caught.exception.code, "provider_response_too_large")


class RetryTests(unittest.TestCase):
    def test_transient_failures_are_retried_up_to_the_bound(self) -> None:
        poster = Poster([jev.JevError("provider_rate_limited", transient=True)] * 3)
        with self.assertRaises(jev.JevError) as caught:
            jev.call_provider({}, FAKE_KEY, post=poster, sleep=lambda _s: None)
        self.assertEqual(caught.exception.code, "provider_rate_limited")
        self.assertEqual(len(poster.calls), jev.MAX_ATTEMPTS)

    def test_permanent_failures_are_not_retried(self) -> None:
        for code in ("provider_unauthorized", "provider_invalid_request", "provider_unreachable"):
            with self.subTest(code=code):
                poster = Poster([jev.JevError(code)] * 3)
                with self.assertRaises(jev.JevError):
                    jev.call_provider({}, FAKE_KEY, post=poster, sleep=lambda _s: None)
                self.assertEqual(len(poster.calls), 1)

    def test_a_single_transient_failure_recovers(self) -> None:
        poster = Poster([jev.JevError("provider_overloaded", transient=True), sample_response()])
        _response, attempts = jev.call_provider({}, FAKE_KEY, post=poster, sleep=lambda _s: None)
        self.assertEqual(attempts, 2)

    def test_retry_waits_between_attempts(self) -> None:
        waits: list[float] = []
        poster = Poster([jev.JevError("provider_rate_limited", transient=True), sample_response()])
        jev.call_provider({}, FAKE_KEY, post=poster, sleep=waits.append)
        self.assertEqual(len(waits), 1)
        self.assertGreater(waits[0], 0)


class CredentialTests(unittest.TestCase):
    def test_missing_key_blocks_without_a_request(self) -> None:
        result = jev.evaluate(sample_input(), {}, post=forbidden_post)
        self.assertFalse(result["ok"])
        self.assertEqual(result["status"], jev.STATUS_BLOCKED)
        self.assertEqual(result["error"]["code"], "missing_credential")
        self.assertIn("TYPESAFE_API_KEY", result["error"]["message"])

    def test_blank_key_blocks_without_a_request(self) -> None:
        result = jev.evaluate(sample_input(), {jev.API_KEY_ENV: "   "}, post=forbidden_post)
        self.assertEqual(result["error"]["code"], "missing_credential")

    def test_key_is_read_at_request_time_from_the_given_environment(self) -> None:
        poster = Poster([sample_response()])
        jev.evaluate(sample_input(), {jev.API_KEY_ENV: "SYNTHETIC-OTHER-KEY"}, post=poster)
        self.assertEqual(poster.keys, ["SYNTHETIC-OTHER-KEY"])

    def test_no_output_contains_the_credential(self) -> None:
        cases = [
            run(sample_input()),
            run(sample_input(), poster=Poster([jev.JevError("provider_unauthorized")])),
            run(sample_input(), poster=Poster([b"{broken"])),
            run(sample_input(round=99), poster=forbidden_post),
            jev.evaluate(sample_input(), {}, post=forbidden_post),
            jev.policy(),
            jev.example_output(),
        ]
        for index, case in enumerate(cases):
            with self.subTest(case=index):
                text = json.dumps(case, ensure_ascii=False)
                self.assertNotIn(FAKE_KEY, text)
                self.assertNotIn("Authorization", text)
                self.assertNotIn("Bearer", text)

    def test_failures_never_leak_provider_bodies_or_exception_text(self) -> None:
        secret_body = b'{"provider_secret_detail": "SHOULD-NOT-APPEAR"}'
        result = run(sample_input(), poster=Poster([secret_body]))
        text = json.dumps(result)
        self.assertNotIn("SHOULD-NOT-APPEAR", text)
        self.assertNotIn("provider_secret_detail", text)

    def test_blocked_results_do_not_claim_clearance(self) -> None:
        result = run(sample_input(), poster=Poster([jev.JevError("provider_unauthorized")]))
        self.assertEqual(result["status"], jev.STATUS_BLOCKED)
        self.assertTrue(any("not cleared" in gap for gap in result["gaps"]))
        self.assertNotIn("dimensions", result)


class ReportingTests(unittest.TestCase):
    def test_result_records_identity_policy_and_provider_model(self) -> None:
        result = run(sample_input())
        self.assertEqual(result["provider"]["model"], "SYNTHETIC-TEST-MODEL")
        self.assertEqual(result["provider"]["usage"], {"input_tokens": 1, "output_tokens": 1})
        self.assertEqual(result["input_identity"]["policy"], jev.policy_digest())
        self.assertEqual(result["input_identity"]["policy_version"], "screening-policy-1")

    def test_result_disclaims_legal_and_readership_conclusions(self) -> None:
        text = " ".join(run(sample_input())["disclaimers"])
        self.assertIn("not legal clearance", text)
        self.assertIn("not a prediction of real readership", text)

    def test_distinct_revisions_have_distinct_input_identities(self) -> None:
        first = run(sample_input(round=1))
        second = run(sample_input(round=2, draft="SYNTHETIC TEST DRAFT second revision."))
        self.assertNotEqual(first["input_identity"]["draft"], second["input_identity"]["draft"])
        self.assertEqual(first["input_identity"]["original"], second["input_identity"]["original"])

    def test_gap_text_names_the_failing_dimension_and_reason(self) -> None:
        result = run(sample_input(), poster=Poster([sample_response(title_potential=answer(WEAK_EDITORIAL))]))
        self.assertEqual(result["gaps"], ["title_potential: expected score below the policy minimum"])

    def test_status_values_are_exactly_the_documented_set(self) -> None:
        self.assertEqual(
            {jev.STATUS_PASSED, jev.STATUS_NEEDS_REVISION, jev.STATUS_BLOCKED, jev.STATUS_STALE},
            {"passed", "needs_revision", "blocked", "stale"},
        )


class CliTests(unittest.TestCase):
    def test_help_exits_zero(self) -> None:
        out = io.StringIO()
        original = sys.stdout
        sys.stdout = out
        try:
            with self.assertRaises(SystemExit) as caught:
                jev.main(["--help"])
        finally:
            sys.stdout = original
        self.assertEqual(caught.exception.code, 0)
        self.assertIn("usage", out.getvalue().lower())

    def test_offline_flags_print_json_and_exit_zero(self) -> None:
        for flag in ("--policy", "--example-input", "--example-output"):
            with self.subTest(flag=flag):
                out = io.StringIO()
                code = jev.main([flag], stdin=None, stdout=out, env={})
                self.assertEqual(code, 0)
                parsed = json.loads(out.getvalue())
                self.assertIsInstance(parsed, dict)

    def test_stdin_assessment_round_trip(self) -> None:
        out = io.StringIO()
        original_post = jev.http_post_json
        jev.http_post_json = Poster([sample_response()])  # type: ignore[assignment]
        try:
            code = jev.main([], stdin=io.StringIO(json.dumps(sample_input())), stdout=out, env=ENV)
        finally:
            jev.http_post_json = original_post  # type: ignore[assignment]
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out.getvalue())["status"], "passed")

    def test_blocked_result_exits_one(self) -> None:
        out = io.StringIO()
        code = jev.main([], stdin=io.StringIO(json.dumps(sample_input())), stdout=out, env={})
        self.assertEqual(code, 1)
        self.assertEqual(json.loads(out.getvalue())["error"]["code"], "missing_credential")

    def test_invalid_stdin_json_exits_one_with_a_safe_message(self) -> None:
        out = io.StringIO()
        code = jev.main([], stdin=io.StringIO("{not json"), stdout=out, env=ENV)
        self.assertEqual(code, 1)
        result = json.loads(out.getvalue())
        self.assertEqual(result["error"]["code"], "invalid_input_json")
        self.assertNotIn("not json", result["error"]["message"])

    def test_invalid_utf8_stdin_exits_one(self) -> None:
        class BinaryStdin:
            buffer = io.BytesIO(b"\xff\xfe\x00invalid")

        out = io.StringIO()
        code = jev.main([], stdin=BinaryStdin(), stdout=out, env=ENV)
        self.assertEqual(code, 1)
        self.assertEqual(json.loads(out.getvalue())["error"]["code"], "invalid_input_encoding")

    def test_oversized_stdin_is_blocked(self) -> None:
        class BigStdin:
            buffer = io.BytesIO(b"x" * (jev.MAX_STDIN_BYTES + 1))

        out = io.StringIO()
        code = jev.main([], stdin=BigStdin(), stdout=out, env=ENV)
        self.assertEqual(code, 1)
        result = json.loads(out.getvalue())
        self.assertEqual(result["error"]["code"], "input_too_large")
        self.assertIn("standard input", result["error"]["message"])

    def test_offline_flags_need_no_credential(self) -> None:
        out = io.StringIO()
        self.assertEqual(jev.main(["--policy"], stdout=out, env={}), 0)
        self.assertNotIn("TYPESAFE_API_KEY", json.loads(out.getvalue()).get("notes", [""])[0])


if __name__ == "__main__":
    unittest.main()
