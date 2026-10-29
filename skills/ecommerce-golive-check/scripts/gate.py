#!/usr/bin/env python3
"""ecommerce-golive-check — blocking go-live gate.

Takes the filled intake + per-block verdicts (JSON, see references/gate-schema.md)
and emits the summary table, the blocking gate, the waiver list, and the
remediation list. Deterministic: it assembles verdicts the owning skills
produced; it does not interpret law or judge CRO itself.

Usage:
    python3 gate.py verdicts.json
    cat verdicts.json | python3 gate.py -
"""
from __future__ import annotations

import json
import sys

SEV_ORDER = {"blocking": 0, "high": 1, "medium": 2, "low": 3}
SEV_LABEL = {"blocking": "\U0001F534 Blocking", "high": "\U0001F7E0 High",
             "medium": "\U0001F7E1 Medium", "low": "\U0001F7E2 Low"}

DISCLAIMER = (
    "This output is not legal advice. Compliance and launch-readiness vary by "
    "jurisdiction, business model, and actual operational practice. High-risk, "
    "regulated, sensitive-data, or cross-border stores should have final "
    "materials reviewed by qualified counsel. This skill orchestrates "
    "issue-spotting, checklisting, and gating only."
)


def load(path: str) -> dict:
    raw = sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()
    return json.loads(raw)


def waived(check: str, waivers: list) -> dict | None:
    for w in waivers:
        if w.get("check") == check:
            return w
    return None


def normalize(items: list) -> list:
    """Enforce the evidence rule: a Blocking pass with no evidence is a warning."""
    out = []
    for it in items:
        it = dict(it)
        if (it.get("severity") == "blocking"
                and it.get("status") == "pass"
                and not (it.get("evidence") or "").strip()):
            it["status"] = "warning"
            it["_downgraded"] = "blocking pass had no evidence"
        out.append(it)
    return out


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: gate.py <verdicts.json|->", file=sys.stderr)
        return 2
    data = load(sys.argv[1])
    store = data.get("store", {})
    blocks = data.get("blocks", [])
    waivers = data.get("waivers", [])

    all_items = []
    for b in blocks:
        for it in normalize(b.get("items", [])):
            it = dict(it)
            it["_block"] = b.get("title", b.get("id", "?"))
            it["_owner"] = b.get("owner", "")
            all_items.append(it)

    # Gate rule
    blocking_fails = []
    for it in all_items:
        if it.get("severity") != "blocking":
            continue
        status = it.get("status")
        if status in ("fail", "needs-skill", "warning"):
            w = waived(it.get("check", ""), waivers)
            if not w:
                blocking_fails.append(it)

    launch_ready = not blocking_fails

    out = []
    out.append(f"# Go-live gate — {store.get('name', '?')} ({store.get('url', '')})")
    out.append(f"Model: {store.get('model', '?')} · Markets: "
               f"{', '.join(store.get('markets', [])) or '?'} · "
               f"Commit: {store.get('release_commit', '?')}\n")

    # 1. Summary table
    out.append("## Summary\n")
    out.append("| Block | Owner | pass | fail | warn | needs-skill | worst unresolved |")
    out.append("|-------|-------|-----:|-----:|-----:|-----:|------------------|")
    for b in blocks:
        items = normalize(b.get("items", []))
        counts = {k: sum(1 for i in items if i.get("status") == k)
                  for k in ("pass", "fail", "warning", "needs-skill")}
        unresolved = [i for i in items if i.get("status") != "pass"]
        worst = min((SEV_ORDER.get(i.get("severity", "low"), 3) for i in unresolved),
                    default=None)
        worst_lbl = SEV_LABEL[[k for k, v in SEV_ORDER.items() if v == worst][0]] if worst is not None else "—"
        out.append(f"| {b.get('title', b.get('id'))} | {b.get('owner','')} | "
                   f"{counts['pass']} | {counts['fail']} | {counts['warning']} | "
                   f"{counts['needs-skill']} | {worst_lbl} |")
    out.append("")

    # 2. Blocking gate verdict
    out.append("## Blocking gate\n")
    if launch_ready:
        out.append("**\u2705 LAUNCH-READY** — all blocking items pass with evidence "
                   "(or are explicitly waived).\n")
    else:
        out.append(f"**\u274C NOT LAUNCH-READY — {len(blocking_fails)} blocking "
                   f"failure(s) unresolved.**\n")
        for it in sorted(blocking_fails, key=lambda i: i.get("_block", "")):
            note = f" ({it['_downgraded']})" if it.get("_downgraded") else ""
            out.append(f"- [{it['_block']}] {it.get('check')} — "
                       f"**{it.get('status')}**{note}"
                       + (f" · fix: {it['fix']}" if it.get("fix") else ""))
        out.append("")

    # 3. Waivers
    if waivers:
        out.append("## Waivers (explicit launch-over-blocking)\n")
        for w in waivers:
            out.append(f"- {w.get('check')} — reason: {w.get('reason','?')} "
                       f"· approved by: {w.get('approved_by','?')}")
        out.append("")

    # 4. Remediation
    unresolved = [i for i in all_items if i.get("status") != "pass"]
    if unresolved:
        out.append("## Remediation (ordered by severity)\n")
        for it in sorted(unresolved, key=lambda i: SEV_ORDER.get(i.get("severity", "low"), 3)):
            out.append(f"- {SEV_LABEL.get(it.get('severity','low'),'?')} "
                       f"[{it['_block']}] {it.get('check')} — {it.get('status')}"
                       + (f" · fix: {it['fix']}" if it.get("fix") else ""))
        out.append("")

    out.append("---")
    out.append(f"> {DISCLAIMER}")

    print("\n".join(out))
    return 0 if launch_ready else 1


if __name__ == "__main__":
    sys.exit(main())
