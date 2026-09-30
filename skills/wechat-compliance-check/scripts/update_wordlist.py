#!/usr/bin/env python3
"""Apply a verified, additive-only word-list update.

This command is intentionally conservative.  A caller-provided ``evidence_score``
is not evidence of a Jev assessment: every accepted candidate must carry a
validated ``jev_assessment`` distribution whose expected score agrees with it.
The old file is parsed before and after the write, and every old entry line must
remain byte-for-byte unchanged.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path
from typing import Any, Iterable

# Import the scanner's strict parser without importing anything from another skill.
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from compliance_scan import (  # noqa: E402
    ComplianceError,
    PROBABILITY_SUM_TOLERANCE,
    SCALE_LEVELS,
    SCORE_CONSISTENCY_TOLERANCE,
    Wordlist,
    fold_fullwidth,
    parse_wordlist,
    strict_real,
)

DEFAULT_MAX_ADDITIONS = 25
MIN_EVIDENCE_SCORE = 0.75
LEVELS = {"🔴", "🟡", "⚠️"}
TAGS = {"[ALWAYS]", "[CONTEXT]"}
_METADATA_SAFE = re.compile(r"^[^{}\r\n]+$")


def _canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _assessment_digest(candidate: dict[str, Any], assessment: dict[str, Any]) -> str:
    """Bind normalized provider values to exact candidate evidence fields."""
    bound = {
        key: candidate.get(key)
        for key in ("term", "replacement", "level", "tag", "note", "category", "source_url", "collected_on")
    }
    normalized = {
        "verified": assessment.get("verified"),
        "score": float(assessment.get("score")),
        "expected_score": float(assessment.get("expected_score")),
        "probabilities": {
            str(index): float(assessment["probabilities"][str(index)])
            for index in range(SCALE_LEVELS)
        },
        "confidence": float(assessment.get("confidence")),
    }
    return hashlib.sha256(_canonical_json({"candidate": bound, "assessment": normalized}).encode("utf-8")).hexdigest()


class UpdateError(RuntimeError):
    """A locally authored update rejection."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


def _object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise UpdateError("invalid_candidate", f"{label} must be an object")
    return value


def _probabilities(value: Any, label: str) -> dict[str, float]:
    if not isinstance(value, dict) or set(value) != {str(i) for i in range(SCALE_LEVELS)}:
        raise UpdateError("jev_unverified", f"{label} probabilities must contain levels 0-4")
    parsed: dict[str, float] = {}
    for key in (str(i) for i in range(SCALE_LEVELS)):
        try:
            number = strict_real(value[key], f"{label}.probabilities[{key}]")
        except ComplianceError as exc:
            raise UpdateError("jev_unverified", exc.message) from None
        if not 0 <= number <= 1:
            raise UpdateError("jev_unverified", f"{label} probability was outside 0-1")
        parsed[key] = number
    if abs(sum(parsed.values()) - 1.0) > PROBABILITY_SUM_TOLERANCE:
        raise UpdateError("jev_unverified", f"{label} probabilities did not sum to one")
    return parsed


def _expected(probabilities: dict[str, float]) -> float:
    return sum(index * probabilities[str(index)] for index in range(SCALE_LEVELS))


def verify_candidate_jev(candidate: dict[str, Any]) -> tuple[float, dict[str, Any]]:
    """Validate a candidate's Jev evidence and return normalized score + record.

    ``evidence_score`` is accepted only when it is bound to the recorded Jev
    distribution.  The assessment may be named ``jev_assessment`` (the public
    contract) or ``jev`` (a convenient producer alias), but it must contain a
    score, complete probabilities, and confidence.  A separate ``verified``
    boolean is required so a forged shape cannot accidentally be treated as a
    live verification.
    """

    assessment_value = candidate.get("jev_assessment", candidate.get("jev"))
    if not isinstance(assessment_value, dict):
        raise UpdateError("jev_unverified", "candidate lacks an explicit verified Jev assessment")
    assessment = _object(assessment_value, "jev_assessment")
    if assessment.get("verified") is not True:
        raise UpdateError("jev_unverified", "candidate lacks an explicit verified Jev assessment")
    # A producer must bind the provider record to this exact candidate.  The
    # digest prevents copying a valid assessment from one term onto another;
    # `verified: true` alone remains explicitly insufficient.
    supplied_digest = assessment.get("assessment_digest")
    if not isinstance(supplied_digest, str) or not re.fullmatch(r"[0-9a-f]{64}", supplied_digest):
        raise UpdateError("jev_unverified", "Jev assessment lacks a candidate-bound digest")
    try:
        score = strict_real(assessment.get("score"), "jev_assessment.score")
        confidence = strict_real(assessment.get("confidence"), "jev_assessment.confidence")
    except ComplianceError as exc:
        raise UpdateError("jev_unverified", exc.message) from None
    if not 0 <= score <= SCALE_LEVELS - 1:
        raise UpdateError("jev_unverified", "Jev score was outside 0-4")
    if not 0 <= confidence <= 1 or confidence < 0.50:
        raise UpdateError("jev_unverified", "Jev confidence was below the verification floor")
    probabilities = _probabilities(assessment.get("probabilities"), "jev_assessment")
    expected = _expected(probabilities)
    if abs(score - expected) > SCORE_CONSISTENCY_TOLERANCE:
        raise UpdateError("jev_unverified", "Jev score disagreed with its distribution")
    if "expected_score" in assessment:
        try:
            recorded_expected = strict_real(assessment.get("expected_score"), "jev_assessment.expected_score")
        except ComplianceError as exc:
            raise UpdateError("jev_unverified", exc.message) from None
        if abs(recorded_expected - expected) > SCORE_CONSISTENCY_TOLERANCE:
            raise UpdateError("jev_unverified", "Jev expected score disagreed with its distribution")
    # Evidence score is a derived normalized field, never an independent trust input.
    supplied = candidate.get("evidence_score")
    if isinstance(supplied, bool) or not isinstance(supplied, (int, float)):
        raise UpdateError("missing_evidence", "evidence_score is required")
    supplied_float = float(supplied)
    if not math.isfinite(supplied_float) or not 0 <= supplied_float <= 1:
        raise UpdateError("invalid_evidence", "evidence_score must be between 0 and 1")
    normalized = expected / float(SCALE_LEVELS - 1)
    if abs(supplied_float - normalized) > 0.06:
        raise UpdateError("jev_unverified", "evidence_score was not derived from the Jev score")
    normalized_record = {
        "verified": True,
        "score": score,
        "expected_score": expected,
        "probabilities": probabilities,
        "confidence": confidence,
    }
    if supplied_digest != _assessment_digest(candidate, normalized_record):
        raise UpdateError("jev_unverified", "Jev assessment was not bound to this candidate")
    return normalized, normalized_record


def _validate_date(value: Any) -> str:
    if not isinstance(value, str):
        raise UpdateError("missing_source", "collected_on is required")
    try:
        parsed = date.fromisoformat(value)
    except ValueError:
        raise UpdateError("invalid_source", "collected_on must be YYYY-MM-DD") from None
    if parsed.isoformat() != value:
        raise UpdateError("invalid_source", "collected_on must be YYYY-MM-DD")
    return value


def _validate_candidate(candidate: Any, existing: Wordlist, run_id: str) -> tuple[dict[str, Any], float, dict[str, Any]]:
    item = _object(candidate, "candidate")
    required = ("term", "replacement", "level", "tag", "note", "category", "source_url", "collected_on", "evidence_score")
    missing = [key for key in required if key not in item]
    if missing:
        raise UpdateError("invalid_candidate", "candidate missing: " + ", ".join(missing))
    term = item["term"] if isinstance(item["term"], str) else ""
    replacement = item["replacement"] if isinstance(item["replacement"], str) else ""
    note = item["note"] if isinstance(item["note"], str) else ""
    category = item["category"] if isinstance(item["category"], str) else ""
    tag = item["tag"] if isinstance(item["tag"], str) else ""
    if not term.strip() or not category.strip() or not _METADATA_SAFE.fullmatch(term) or "→" in term or "|" in term:
        raise UpdateError("invalid_candidate", "term is empty or contains word-list delimiters")
    if "\n" in replacement or "\n" in note or "→" in replacement or "|" in replacement:
        raise UpdateError("invalid_candidate", "replacement or note contains a line delimiter")
    if category not in existing.categories:
        raise UpdateError("invalid_category", f"category does not exist: {category}")
    if item["level"] not in LEVELS:
        raise UpdateError("invalid_candidate", "level is not a supported risk level")
    if tag not in TAGS:
        raise UpdateError("regex_requires_human", "new [REGEX] entries are refused; use [ALWAYS] or [CONTEXT]")
    source_url = item["source_url"]
    if not isinstance(source_url, str) or not source_url.startswith(("http://", "https://")):
        raise UpdateError("missing_source", "source_url must be an HTTP(S) URL")
    collected_on = _validate_date(item["collected_on"])
    if term in {entry.term for entry in existing.entries}:
        raise UpdateError("duplicate_term", f"term already exists: {term}")
    folded_term = fold_fullwidth(term)
    for entry in existing.entries:
        if entry.tag != "[REGEX]" or entry.pattern is None:
            continue
        if entry.pattern.search(folded_term):
            raise UpdateError("covered_by_regex", f"term is covered by existing regex: {entry.term}")
    normalized, assessment = verify_candidate_jev(item)
    if normalized < MIN_EVIDENCE_SCORE:
        raise UpdateError("evidence_below_threshold", "verified evidence_score is below 0.75")
    metadata = f"{{src={source_url}; date={collected_on}; jev={normalized:.3f}; run={run_id}}}"
    return {
        "term": term,
        "replacement": replacement,
        "level": item["level"],
        "tag": tag,
        "note": note,
        "category": category,
        "metadata": metadata,
    }, normalized, assessment


def _entry_line(candidate: dict[str, Any]) -> str:
    note = candidate["note"]
    suffix = f" {note}" if note else ""
    return (
        f"{candidate['term']} → {candidate['replacement']} | {candidate['level']} | "
        f"{candidate['tag']}{suffix} {candidate['metadata']}"
    ).rstrip()


def _append_to_category(lines: list[str], category: str, additions: list[str]) -> list[str]:
    heading = re.compile(r"^##\s+\d+\.\s+" + re.escape(category) + r"\s*$")
    in_category = False
    in_fence = False
    for index, line in enumerate(lines):
        if heading.fullmatch(line):
            in_category = True
            continue
        if in_category and line.strip().startswith("## "):
            break
        if not in_category:
            continue
        if line.strip().startswith("```"):
            if in_fence:
                # Add directly before the closing fence.
                lines[index:index] = additions
                return lines
            in_fence = True
    raise UpdateError("invalid_category", f"could not find an entry block for category: {category}")


def _update_header_and_log(lines: list[str], count: int, run_id: str, today: str) -> None:
    for index, line in enumerate(lines):
        if line.startswith("> 最后更新："):
            lines[index] = f"> 最后更新：{today}"
            break
    else:
        raise UpdateError("wordlist_invalid", "word list has no last-updated line")
    marker = "## 更新日志"
    try:
        index = lines.index(marker)
    except ValueError:
        raise UpdateError("wordlist_invalid", "word list has no update log") from None
    lines.insert(index + 1, f"- {today}：新增 {count} 条（run {run_id}），来源与 Jev 评估见各条目元数据")


def assert_additive(old: Wordlist, new: Wordlist) -> None:
    new_by_line = {entry.term: entry for entry in new.entries}
    for old_entry in old.entries:
        current = new_by_line.get(old_entry.term)
        if current is None or current.raw != old_entry.raw or current.category != old_entry.category:
            raise UpdateError("non_additive_update", f"existing entry changed or was removed: {old_entry.term}")


def _atomic_write(path: Path, text: str) -> None:
    """Replace a file atomically using a same-directory temporary file."""
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary = Path(handle.name)
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        temporary = None
    finally:
        if temporary is not None:
            try:
                temporary.unlink()
            except FileNotFoundError:
                pass


def _run_local_tests() -> bool:
    """Run the bundled offline suite without allowing recursive updater calls."""

    tests_dir = SCRIPT_DIR.parent / "tests"
    if not tests_dir.is_dir() or os.environ.get("WECHAT_WORDLIST_UPDATE_TESTING") == "1":
        return True
    environment = dict(os.environ)
    environment["WECHAT_WORDLIST_UPDATE_TESTING"] = "1"
    completed = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", str(tests_dir), "-p", "test_*.py"],
        cwd=str(SCRIPT_DIR.parent.parent.parent),
        env=environment,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return completed.returncode == 0


def apply_update(
    candidates: list[Any],
    wordlist_path: Path,
    run_id: str,
    *,
    max_additions: int = DEFAULT_MAX_ADDITIONS,
    dry_run: bool = False,
    today: str | None = None,
) -> dict[str, Any]:
    if not isinstance(candidates, list):
        raise UpdateError("invalid_input", "candidate input must be an array")
    if not isinstance(run_id, str) or not run_id or not re.fullmatch(r"[A-Za-z0-9._-]+", run_id):
        raise UpdateError("invalid_run_id", "run-id contains unsupported characters")
    if max_additions < 1:
        raise UpdateError("invalid_input", "max additions must be positive")
    old_text = wordlist_path.read_text(encoding="utf-8")
    old = parse_wordlist(wordlist_path)
    accepted: list[tuple[dict[str, Any], float, dict[str, Any]]] = []
    rejected: list[dict[str, str]] = []
    seen_terms: set[str] = set()
    for candidate in candidates:
        try:
            item = _object(candidate, "candidate")
            term = item.get("term") if isinstance(item.get("term"), str) else ""
            if term in seen_terms:
                raise UpdateError("duplicate_term", f"duplicate candidate: {term}")
            seen_terms.add(term)
            accepted.append(_validate_candidate(candidate, old, run_id))
        except UpdateError as exc:
            rejected.append({"term": str(candidate.get("term", "")) if isinstance(candidate, dict) else "", "code": exc.code, "reason": exc.message})
    accepted.sort(key=lambda row: row[1], reverse=True)
    deferred = accepted[max_additions:]
    selected = accepted[:max_additions]
    if not selected:
        return {"added": [], "added_count": 0, "rejected": rejected, "deferred": len(deferred), "dry_run": dry_run}
    lines = list(old.lines)
    by_category: dict[str, list[str]] = {}
    for item, _, _ in selected:
        by_category.setdefault(item["category"], []).append(_entry_line(item))
    for category, additions in by_category.items():
        _append_to_category(lines, category, additions)
    _update_header_and_log(lines, len(selected), run_id, today or date.today().isoformat())
    new_text = "\n".join(lines) + ("\n" if old_text.endswith("\n") else "")
    if not dry_run:
        try:
            _atomic_write(wordlist_path, new_text)
            new = parse_wordlist(wordlist_path)
            assert_additive(old, new)
        except Exception:
            _atomic_write(wordlist_path, old_text)
            raise
        # Always leave a parser-valid file; this is the updater's local safety check.
        if not _run_local_tests():
            _atomic_write(wordlist_path, old_text)
            raise UpdateError("validation_failed", "offline compliance tests failed")
    added = [{"term": item["term"], "category": item["category"], "evidence_score": score} for item, score, _ in selected]
    # A dry run validates a unique temporary file and leaves the source untouched.
    if dry_run:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=wordlist_path.parent,
            prefix=f".{wordlist_path.name}.", suffix=".dry-run", delete=True
        ) as handle:
            handle.write(new_text)
            handle.flush()
            new = parse_wordlist(Path(handle.name))
            assert_additive(old, new)
    return {"added": added, "added_count": len(added), "rejected": rejected, "deferred": len(deferred), "dry_run": dry_run}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="update_wordlist.py")
    parser.add_argument("--candidates", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--wordlist", default=str(SCRIPT_DIR.parent / "references" / "sensitive-words.md"))
    parser.add_argument("--max-additions", type=int, default=DEFAULT_MAX_ADDITIONS)
    parser.add_argument("--dry-run", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        candidates = json.loads(Path(args.candidates).read_text(encoding="utf-8"))
        result = apply_update(candidates, Path(args.wordlist), args.run_id, max_additions=args.max_additions, dry_run=args.dry_run)
    except (OSError, UnicodeError, json.JSONDecodeError):
        result = {"error": {"code": "invalid_input", "message": "candidate file could not be read as UTF-8 JSON"}}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2
    except (UpdateError, ComplianceError) as exc:
        code = getattr(exc, "code", "update_failed")
        message = getattr(exc, "message", str(exc))
        result = {"error": {"code": code, "message": message}}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
