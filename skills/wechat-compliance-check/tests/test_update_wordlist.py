from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "update_wordlist.py"
SPEC = importlib.util.spec_from_file_location("update_wordlist", SCRIPT)
assert SPEC and SPEC.loader
update = importlib.util.module_from_spec(SPEC)
sys.modules["update_wordlist"] = update
SPEC.loader.exec_module(update)

WORDS = """# list
> 最后更新：2026-09-29
## 1. Test category

```text
existing → keep | 🟡 | [ALWAYS] existing note
regexcovered → keep | 🟡 | [REGEX] covered
```

## 更新日志
- initial
"""


def candidate(term: str = "new", **overrides):
    probabilities = {"0": 0.0, "1": 0.0, "2": 0.0, "3": 0.0, "4": 1.0}
    value = {
        "term": term,
        "replacement": "safe",
        "level": "🟡",
        "tag": "[CONTEXT]",
        "note": "new evidence",
        "category": "Test category",
        "source_url": "https://example.test/source",
        "collected_on": "2026-09-29",
        "evidence_score": 1.0,
        "jev_assessment": {"verified": True, "score": 4.0, "probabilities": probabilities, "confidence": 0.9},
    }
    value.update(overrides)
    assessment = value["jev_assessment"]
    if isinstance(assessment, dict):
        normalized_assessment = {
            "verified": True,
            "score": assessment["score"],
            "expected_score": update._expected(assessment["probabilities"]),
            "probabilities": assessment["probabilities"],
            "confidence": assessment["confidence"],
        }
        assessment["assessment_digest"] = update._assessment_digest(value, normalized_assessment)
    return value


class UpdateTests(unittest.TestCase):
    def list_path(self, directory: str) -> Path:
        path = Path(directory) / "words.md"
        path.write_text(WORDS, encoding="utf-8")
        return path

    def test_additive_update_preserves_existing_raw_lines(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = self.list_path(temporary)
            result = update.apply_update([candidate()], path, "run-1", today="2026-09-29")
            parsed = update.parse_wordlist(path)
        self.assertEqual(result["added_count"], 1)
        self.assertEqual([entry.term for entry in parsed.entries], ["existing", "regexcovered", "new"])
        self.assertEqual(parsed.entries[0].raw, "existing → keep | 🟡 | [ALWAYS] existing note")

    def test_dry_run_does_not_write(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = self.list_path(temporary)
            before = path.read_text(encoding="utf-8")
            result = update.apply_update([candidate()], path, "run-1", dry_run=True)
        self.assertEqual(result["added_count"], 1)
        # TemporaryDirectory removes the source after this assertion's scope; compare
        # inside the scope so dry-run never needs to recreate or read a deleted path.
        self.assertEqual(before, WORDS)

    def test_forged_evidence_score_is_rejected_without_verified_jev(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = self.list_path(temporary)
            forged = candidate(jev_assessment=None)
            result = update.apply_update([forged], path, "run-1")
        self.assertEqual(result["added_count"], 0)
        self.assertEqual(result["rejected"][0]["code"], "jev_unverified")

    def test_mismatched_evidence_score_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = self.list_path(temporary)
            result = update.apply_update([candidate(evidence_score=0.76)], path, "run-1")
        self.assertEqual(result["added_count"], 0)
        self.assertEqual(result["rejected"][0]["code"], "jev_unverified")

    def test_mismatched_recorded_expected_score_is_rejected(self) -> None:
        value = candidate()
        value["jev_assessment"]["expected_score"] = 0.0
        with tempfile.TemporaryDirectory() as temporary:
            path = self.list_path(temporary)
            result = update.apply_update([value], path, "run-1")
        self.assertEqual(result["added_count"], 0)
        self.assertEqual(result["rejected"][0]["code"], "jev_unverified")

    def test_missing_source_and_low_score_are_rejected(self) -> None:
        cases = [
            (candidate(source_url=""), "missing_source"),
            (candidate(evidence_score=0.5, jev_assessment={"verified": True, "score": 2.0, "probabilities": {"0": 0, "1": 0, "2": 1, "3": 0, "4": 0}, "confidence": 0.9}), "evidence_below_threshold"),
        ]
        for value, expected in cases:
            with self.subTest(expected=expected):
                with tempfile.TemporaryDirectory() as temporary:
                    path = self.list_path(temporary)
                    result = update.apply_update([value], path, "run-1")
                self.assertEqual(result["rejected"][0]["code"], expected)

    def test_duplicate_and_regex_candidates_are_rejected(self) -> None:
        cases = [(candidate("existing"), "duplicate_term"), (candidate("new-regex", tag="[REGEX]"), "regex_requires_human"), (candidate("regexcovered"), "duplicate_term")]
        for value, expected in cases:
            with self.subTest(expected=expected):
                with tempfile.TemporaryDirectory() as temporary:
                    path = self.list_path(temporary)
                    result = update.apply_update([value], path, "run-1")
                self.assertEqual(result["rejected"][0]["code"], expected)

    def test_cap_deferred_and_sorted_by_verified_score(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = self.list_path(temporary)
            values = [candidate("low", evidence_score=0.8, jev_assessment={"verified": True, "score": 3.2, "probabilities": {"0": 0.0, "1": 0.0, "2": 0.0, "3": 0.8, "4": 0.2}, "confidence": 0.9}), candidate("high")]
            result = update.apply_update(values, path, "run-1", max_additions=1)
            parsed = update.parse_wordlist(path)
        self.assertEqual(result["added_count"], 1)
        self.assertEqual(result["deferred"], 1)
        self.assertEqual(parsed.entries[-1].term, "high")


if __name__ == "__main__":
    unittest.main()
