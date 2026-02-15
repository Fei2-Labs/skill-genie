#!/usr/bin/env python3
"""Collect browser debugging artifacts into a single bundle with manifest metadata."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from dataclasses import asdict, dataclass
from pathlib import Path

DEFAULT_PATTERNS = [
    "**/*.png",
    "**/*.jpg",
    "**/*.jpeg",
    "**/*.webm",
    "**/*.mp4",
    "**/*.har",
    "**/*.trace",
    "**/*trace*.zip",
    "**/*playwright*.log",
]

DEFAULT_SEARCH_DIRS = ["test-results", "playwright-report", ".debug", "cypress"]


@dataclass
class Artifact:
    source: str
    target: str
    size: int
    sha256: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Capture browser debug artifacts")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--max-files", type=int, default=500)
    parser.add_argument("--allow-empty", action="store_true")
    parser.add_argument("--pattern", action="append", dest="patterns")
    return parser.parse_args()


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        while True:
            chunk = fh.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    args = parse_args()
    root = Path(args.project_root).resolve()
    out_dir = Path(args.output_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    patterns = args.patterns if args.patterns else DEFAULT_PATTERNS

    candidates: list[Path] = []
    for rel in DEFAULT_SEARCH_DIRS:
        base = root / rel
        if not base.exists():
            continue
        for pattern in patterns:
            candidates.extend(base.glob(pattern))

    unique_files = []
    seen = set()
    for path in candidates:
        if not path.is_file():
            continue
        full = path.resolve()
        if str(full) in seen:
            continue
        seen.add(str(full))
        unique_files.append(full)
        if len(unique_files) >= args.max_files:
            break

    artifacts: list[Artifact] = []
    for src in unique_files:
        rel = src.relative_to(root) if src.is_relative_to(root) else Path(src.name)
        target = out_dir / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, target)
        artifacts.append(
            Artifact(
                source=str(src),
                target=str(target),
                size=target.stat().st_size,
                sha256=file_hash(target),
            )
        )

    manifest = {
        "project_root": str(root),
        "output_dir": str(out_dir),
        "artifact_count": len(artifacts),
        "artifacts": [asdict(item) for item in artifacts],
    }
    manifest_path = out_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))
    print(f"manifest: {manifest_path}")

    if artifacts or args.allow_empty:
        return 0
    return 10


if __name__ == "__main__":
    raise SystemExit(main())
