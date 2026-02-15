#!/usr/bin/env python3
"""Run a browser reproduction command multiple times and validate deterministic failure."""

from __future__ import annotations

import argparse
import json
import subprocess
import time
from dataclasses import asdict, dataclass
from pathlib import Path

SIGNATURE_HINTS = (
    "TypeError",
    "ReferenceError",
    "TimeoutError",
    "AssertionError",
    "expect(",
    "Error:",
)


@dataclass
class RunResult:
    index: int
    exit_code: int
    duration_ms: int
    signature: str
    stdout_file: str
    stderr_file: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Deterministic browser issue reproducer")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--repro-cmd", required=True)
    parser.add_argument("--runs", type=int, default=2)
    parser.add_argument("--expect", choices=["fail", "pass"], default="fail")
    parser.add_argument("--output-dir", default=".debug/browser-repro")
    return parser.parse_args()


def extract_signature(output: str) -> str:
    for line in output.splitlines():
        text = line.strip()
        if not text:
            continue
        if any(hint in text for hint in SIGNATURE_HINTS):
            return text[:240]
    for line in output.splitlines():
        text = line.strip()
        if text:
            return text[:240]
    return ""


def run_once(cmd: str, cwd: Path, output_dir: Path, index: int) -> RunResult:
    start = time.time()
    proc = subprocess.run(cmd, cwd=str(cwd), shell=True, text=True, capture_output=True)
    duration_ms = int((time.time() - start) * 1000)
    stdout_path = output_dir / f"run_{index}.stdout.log"
    stderr_path = output_dir / f"run_{index}.stderr.log"
    stdout_path.write_text(proc.stdout or "", encoding="utf-8")
    stderr_path.write_text(proc.stderr or "", encoding="utf-8")
    signature = extract_signature((proc.stderr or "") + "\n" + (proc.stdout or ""))
    return RunResult(
        index=index,
        exit_code=proc.returncode,
        duration_ms=duration_ms,
        signature=signature,
        stdout_file=str(stdout_path),
        stderr_file=str(stderr_path),
    )


def main() -> int:
    args = parse_args()
    root = Path(args.project_root).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    runs: list[RunResult] = []
    for i in range(1, args.runs + 1):
        runs.append(run_once(args.repro_cmd, root, output_dir, i))

    failed = sum(1 for run in runs if run.exit_code != 0)
    passed = len(runs) - failed
    signatures = [run.signature for run in runs if run.signature]
    signature_consistent = bool(signatures) and len(set(signatures)) == 1

    if args.expect == "fail":
        reproducible = failed == len(runs) and signature_consistent
    else:
        reproducible = passed == len(runs)

    report = {
        "command": args.repro_cmd,
        "expected": args.expect,
        "reproducible": reproducible,
        "runs": len(runs),
        "failed_runs": failed,
        "passed_runs": passed,
        "signature_consistent": signature_consistent,
        "common_signature": signatures[0] if signature_consistent else "",
        "details": [asdict(run) for run in runs],
    }

    report_path = output_dir / "repro_report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    print(f"report: {report_path}")
    return 0 if reproducible else 10


if __name__ == "__main__":
    raise SystemExit(main())
