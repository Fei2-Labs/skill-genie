#!/usr/bin/env python3
"""Verify browser fix by rerunning deterministic command and checking old signature is gone."""

from __future__ import annotations

import argparse
import json
import subprocess
import time
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class RunResult:
    index: int
    exit_code: int
    duration_ms: int
    stdout_file: str
    stderr_file: str
    forbidden_hit: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Deterministic browser fix verifier")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--verify-cmd", required=True)
    parser.add_argument("--runs", type=int, default=2)
    parser.add_argument("--output-dir", default=".debug/browser-verify")
    parser.add_argument("--signature-file")
    parser.add_argument("--must-not-contain", action="append", dest="forbidden")
    return parser.parse_args()


def load_forbidden_patterns(signature_file: str | None, manual: list[str] | None) -> list[str]:
    patterns: list[str] = manual[:] if manual else []
    if not signature_file:
        return [item for item in patterns if item]
    path = Path(signature_file)
    if not path.exists():
        return [item for item in patterns if item]
    data = json.loads(path.read_text(encoding="utf-8"))
    common = data.get("common_signature", "")
    if common:
        patterns.append(common)
    return [item for item in patterns if item]


def run_once(cmd: str, cwd: Path, output_dir: Path, index: int, forbidden: list[str]) -> RunResult:
    start = time.time()
    proc = subprocess.run(cmd, cwd=str(cwd), shell=True, text=True, capture_output=True)
    duration_ms = int((time.time() - start) * 1000)
    stdout_path = output_dir / f"run_{index}.stdout.log"
    stderr_path = output_dir / f"run_{index}.stderr.log"
    stdout = proc.stdout or ""
    stderr = proc.stderr or ""
    stdout_path.write_text(stdout, encoding="utf-8")
    stderr_path.write_text(stderr, encoding="utf-8")
    merged = stderr + "\n" + stdout
    forbidden_hit = ""
    for pattern in forbidden:
        if pattern and pattern in merged:
            forbidden_hit = pattern[:240]
            break
    return RunResult(
        index=index,
        exit_code=proc.returncode,
        duration_ms=duration_ms,
        stdout_file=str(stdout_path),
        stderr_file=str(stderr_path),
        forbidden_hit=forbidden_hit,
    )


def main() -> int:
    args = parse_args()
    root = Path(args.project_root).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    forbidden = load_forbidden_patterns(args.signature_file, args.forbidden)

    runs: list[RunResult] = []
    for i in range(1, args.runs + 1):
        runs.append(run_once(args.verify_cmd, root, output_dir, i, forbidden))

    all_passed = all(run.exit_code == 0 for run in runs)
    no_forbidden = all(not run.forbidden_hit for run in runs)
    verified = all_passed and no_forbidden

    report = {
        "command": args.verify_cmd,
        "runs": len(runs),
        "all_passed": all_passed,
        "no_forbidden_signature": no_forbidden,
        "verified": verified,
        "forbidden_patterns": forbidden,
        "details": [asdict(run) for run in runs],
    }
    report_path = output_dir / "verify_report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    print(f"report: {report_path}")
    return 0 if verified else 11


if __name__ == "__main__":
    raise SystemExit(main())
