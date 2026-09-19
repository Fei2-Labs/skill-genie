"""Guard the quality guardrail: Round 1 cannot be uniform agreement."""

import pathlib
import sys

SCRIPTS = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

import run_debate as r  # noqa: E402
from common import PROFILES, load_company  # noqa: E402

COMPANY = load_company(SCRIPTS.parent / "config" / "company.yaml")
CATEGORIES = ["pricing", "hiring", "architecture", "security", "growth", "general"]

failures = []

for stage, profile in PROFILES.items():
    debaters = [a for a in profile["agents"] if a not in {"CEO", "CoS"}]
    for category in CATEGORIES:
        positions = {a: r.stance(a, category) for a in debaters}
        unique = set(positions.values())
        if len(unique) < 2:
            failures.append(f"{stage}/{category}: only {len(unique)} distinct position(s)")
        duplicated = len(positions) - len(unique)
        if duplicated:
            failures.append(f"{stage}/{category}: {duplicated} role(s) share a position")

        finals = {a: r.round3(a, positions[a])[:2] for a in debaters}
        if len(set(finals.values())) < 2:
            failures.append(f"{stage}/{category}: round 3 concessions are uniform")

# A named dissenter must appear whenever positions diverge.
for category in CATEGORIES:
    body = r.build_output(
        "Test topic", COMPANY, PROFILES["seed"]["agents"], 3, category, use_jev=False
    )
    if "No substantive disagreement surfaced" in body:
        failures.append(f"seed/{category}: brief reported unanimity despite distinct stances")
    if "**Key Tensions:**" not in body:
        failures.append(f"seed/{category}: brief lost its Key Tensions line")

# Every role in the table needs a stance for every category, or it silently
# falls back to the shared RECS string and re-introduces the duplication.
for category, table in r.STANCES.items():
    missing = sorted(set(r.PERSONA) - set(table))
    if missing:
        failures.append(f"{category}: no stance for {', '.join(missing)}")

if failures:
    print(f"FAIL ({len(failures)})")
    for item in failures:
        print(f"  - {item}")
    raise SystemExit(1)

print("PASS - round 1 positions diverge across every stage and category")
