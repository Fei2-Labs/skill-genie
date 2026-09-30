from __future__ import annotations

import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "compliance_scan.py"
SPEC = importlib.util.spec_from_file_location("compliance_scan", SCRIPT)
assert SPEC and SPEC.loader
scan = importlib.util.module_from_spec(SPEC)
sys.modules["compliance_scan"] = scan
SPEC.loader.exec_module(scan)


WORDLIST = """# fixture
## 1. Test category

```text
VPN → network | 🔴 | [ALWAYS] always
注入 → 插入 | 🟡 | [CONTEXT] SQL context may be safe
中国.*被禁 → regional | 🔴 | [REGEX] political wording
```
"""


def write_fixture(directory: Path, text: str = WORDLIST) -> Path:
    path = directory / "words.md"
    path.write_text(text, encoding="utf-8")
    return path


def response_for(
    contexts: list[float] | None = None,
    *,
    variant: dict | None = None,
    noul_confidence: bool = True,
) -> dict:
    contexts = contexts or []
    answers = {}
    for index, value in enumerate(contexts, 1):
        answer = {"type": "noul", "noul": value}
        if noul_confidence:
            answer["confidence"] = 0.9
        answers[f"context_{index}"] = answer
    probabilities = {"0": 0.80, "1": 0.10, "2": 0.05, "3": 0.03, "4": 0.02}
    answers["variant_score"] = variant or {
        "type": "score",
        "score": 0.37,
        "probabilities": probabilities,
        "confidence": 0.9,
    }
    answers["variant_choice"] = {
        "type": "choice",
        "choice": "none",
        "confidence": 0.9,
        # Context fixtures use SQL + CJK, which produces fragment_1; plain
        # fixtures offer only none. Keep the distribution complete either way.
        "probabilities": {"none": 1.0, **({"fragment_1": 0.0} if contexts else {})},
    }
    return {"answers": answers, "model": "jev-test"}


class ComplianceScanTests(unittest.TestCase):
    def test_parser_accepts_metadata_and_counts_entries(self) -> None:
        text = WORDLIST.replace(
            "[ALWAYS] always", "[ALWAYS] always {src=https://example.test/a; date=2026-09-29; jev=0.900; run=x}"
        )
        with tempfile.TemporaryDirectory() as temporary:
            wordlist = write_fixture(Path(temporary), text)
            parsed = scan.parse_wordlist(wordlist)
        self.assertEqual(len(parsed.entries), 3)
        self.assertEqual(parsed.entries[0].metadata["src"], "https://example.test/a")

    def test_bad_entry_is_not_silently_skipped(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            wordlist = write_fixture(Path(temporary), WORDLIST.replace("注入 → 插入", "this is not an entry"))
            with self.assertRaises(scan.WordlistError) as raised:
                scan.parse_wordlist(wordlist)
        self.assertIn("line 6", raised.exception.message)

    def test_invalid_regex_and_unknown_level_are_errors(self) -> None:
        bad_regex = WORDLIST.replace("中国.*被禁", "[")
        bad_level = WORDLIST.replace("| 🔴 | [REGEX]", "| green | [REGEX]")
        for text in (bad_regex, bad_level):
            with tempfile.TemporaryDirectory() as temporary:
                with self.assertRaises(scan.WordlistError):
                    scan.parse_wordlist(write_fixture(Path(temporary), text))

    def test_deterministic_scan_reports_all_hits_and_full_width(self) -> None:
        article = "VPN and ＶＰＮ\n中国已经被禁\n"
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            wordlist = write_fixture(directory)
            parsed = scan.parse_wordlist(wordlist)
            deterministic, contextual = scan.deterministic_scan(article, parsed)
        self.assertEqual(len(deterministic), 3)
        self.assertEqual(len(contextual), 0)
        self.assertEqual([hit.line_number for hit in deterministic], [1, 1, 2])
        self.assertEqual(deterministic[1].fragment, "ＶＰＮ")

    def test_context_hit_keeps_paragraph_and_no_jev_blocks(self) -> None:
        article = "SQL 注入\n\nnext paragraph\n"
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            wordlist = write_fixture(directory)
            result, code = scan.scan_article(article, directory / "article.md", wordlist, no_jev=True)
        self.assertEqual(code, 2)
        self.assertEqual(result["status"], "blocked")
        self.assertEqual(result["error"]["code"], "jev_required")
        self.assertEqual(result["context_hits"][0]["paragraph"], "SQL 注入")

    def test_no_jev_never_claims_clean_even_without_context(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            wordlist = write_fixture(directory)
            result, code = scan.scan_article("ordinary prose", directory / "article.md", wordlist, no_jev=True)
        self.assertEqual(code, 2)
        self.assertEqual(result["status"], "blocked")
        self.assertEqual(result["error"]["code"], "jev_required")

    def test_missing_key_does_not_make_deterministic_hit_disappear(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            wordlist = write_fixture(directory)
            with patch.dict(os.environ, {}, clear=True):
                result, code = scan.scan_article("VPN", directory / "article.md", wordlist)
        self.assertEqual(code, 2)
        self.assertEqual(result["status"], "blocked")
        self.assertEqual(len(result["deterministic_hits"]), 1)
        self.assertEqual(result["error"]["code"], "missing_credential")

    def test_context_and_variant_response_can_pass(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            wordlist = write_fixture(directory)
            with patch.object(scan, "http_post_json", return_value=(response_for([0.1]), {"attempts": 1, "status": 200})):
                result, code = scan.scan_article("SQL 注入", directory / "article.md", wordlist)
        self.assertEqual(code, 0)
        self.assertEqual(result["status"], "clean")
        self.assertEqual(result["context_hits"][0]["jev"]["verdict"], "safe")
        self.assertIn("top_tail_probability", result["variant_scan"])

    def test_sensitive_context_and_variant_threshold_violate(self) -> None:
        high = {"type": "score", "score": 3.6, "probabilities": {"0": 0.0, "1": 0.0, "2": 0.2, "3": 0.2, "4": 0.6}, "confidence": 0.9}
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            wordlist = write_fixture(directory)
            with patch.object(scan, "http_post_json", return_value=(response_for([0.6], variant=high), {"attempts": 1, "status": 200})):
                result, code = scan.scan_article("SQL 注入", directory / "article.md", wordlist)
        self.assertEqual(code, 2)
        self.assertEqual(result["status"], "blocked")
        self.assertEqual(result["error"]["code"], "provider_response_invalid")
        self.assertIsNone(result["variant_scan"])

    def test_low_confidence_variant_locator_blocks_safe_score(self) -> None:
        response = response_for()
        response["answers"]["variant_choice"]["confidence"] = 0.2
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            wordlist = write_fixture(directory)
            with patch.object(scan, "http_post_json", return_value=(response, {"attempts": 1, "status": 200})):
                result, code = scan.scan_article("plain", directory / "article.md", wordlist)
        self.assertEqual(code, 2)
        self.assertEqual(result["status"], "blocked")
        self.assertEqual(result["error"]["code"], "low_confidence")
        self.assertIn("locator", result["gaps"][0])

    def test_invalid_provider_score_distribution_and_confidence_block(self) -> None:
        cases = [
            {"type": "score", "score": 3, "probabilities": {"0": 1, "1": 0, "2": 0, "3": 0, "4": 0}, "confidence": 0.9},
            {"type": "score", "score": 0, "probabilities": {"0": 0.5, "1": 0.5}, "confidence": 0.9},
            {"type": "score", "score": 0, "probabilities": {"0": 1, "1": 0, "2": 0, "3": 0, "4": 0}, "confidence": 0.2},
        ]
        for bad in cases:
            with self.subTest(bad=bad):
                with tempfile.TemporaryDirectory() as temporary:
                    directory = Path(temporary)
                    wordlist = write_fixture(directory)
                    with patch.object(scan, "http_post_json", return_value=(response_for(variant=bad), {"attempts": 1, "status": 200})):
                        result, code = scan.scan_article("plain", directory / "article.md", wordlist)
                self.assertEqual(code, 2)
                self.assertEqual(result["status"], "blocked")

    def test_provider_exchange_is_logged_without_authorization_header(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            wordlist = write_fixture(directory)
            captured: dict[str, object] = {}

            class Response:
                status = 200

                def read(self) -> bytes:
                    return json.dumps(response_for()).encode("utf-8")

                def __enter__(self):
                    return self

                def __exit__(self, *_args):
                    return None

            def fake_urlopen(request, timeout):
                captured["request"] = request
                return Response()

            with patch.dict(os.environ, {"TYPESAFE_API_KEY": "secret-not-to-output"}, clear=True), patch.object(scan.urllib.request, "urlopen", side_effect=fake_urlopen):
                result, code = scan.scan_article("plain", directory / "article.md", wordlist, log_dir=str(directory / "logs"))
            self.assertEqual(code, 0)
            self.assertNotIn("secret-not-to-output", json.dumps(result))
            request = captured["request"]
            self.assertEqual(request.get_header("Authorization"), "Bearer secret-not-to-output")
            logs = list((directory / "logs").glob("*.json"))
            self.assertEqual(len(logs), 2)
            self.assertNotIn("secret-not-to-output", "".join(path.read_text(encoding="utf-8") for path in logs))

    def test_oversized_article_is_blocked_without_truncation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            wordlist = write_fixture(directory)
            result, code = scan.scan_article("x" * (scan.MAX_ARTICLE_CHARS + 1), directory / "article.md", wordlist)
        self.assertEqual(code, 2)
        self.assertEqual(result["error"]["code"], "input_too_large")
        self.assertTrue(result["gaps"])


if __name__ == "__main__":
    unittest.main()
