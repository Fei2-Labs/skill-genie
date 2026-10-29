# Gate Schema — ecommerce-golive-check

`scripts/gate.py` consumes a single JSON object: the filled intake plus one
verdict per block. It assembles the summary, the blocking gate, and the
remediation list. It is deterministic and does NOT interpret law or judge CRO —
the owning skills already did that; this only rolls their verdicts up.

## Input JSON

```json
{
  "store": {
    "name": "Example Store",
    "url": "https://example.com",
    "model": "dropshipping",
    "markets": ["SE", "EU"],
    "release_commit": "abc1234"
  },
  "blocks": [
    {
      "id": "payment",
      "title": "Payment & checkout",
      "owner": "cross-layer-payment-provider-migration",
      "items": [
        {
          "check": "End-to-end checkout completes",
          "severity": "blocking",
          "status": "pass",
          "evidence": "test order #1042 completed, screenshot scratch/order-1042.png",
          "fix": null
        }
      ]
    }
  ],
  "waivers": [
    {
      "check": "Refund path exists",
      "reason": "manual refund via provider dashboard, documented in runbook",
      "approved_by": "owner"
    }
  ]
}
```

## Field rules

- `severity` ∈ `blocking | high | medium | low`.
- `status` ∈ `pass | fail | warning | needs-skill`.
  - `needs-skill` = the owning skill is not installed; the block could not run.
    Treated as a **fail** for a Blocking item unless waived.
- `evidence` is REQUIRED when `status == "pass"` on a Blocking item. A Blocking
  pass with no evidence is downgraded to `warning` and the gate says so — a pass
  you cannot prove is not a pass.
- `waivers[]` let the user launch over a Blocking fail, but only EXPLICITLY: each
  waiver names the check, a reason, and who approved it. The gate output lists
  every waiver, so it still tells the truth.

## Gate rule

```
launch_ready = (no Blocking item has status fail/needs-skill that is NOT waived)
             AND (every Blocking pass has evidence)
```

- Any unwaived Blocking fail / needs-skill ⇒ **NOT launch-ready**.
- High fails do not block but are listed as "fix before launch".
- Medium / Low are listed as post-launch / backlog.

## Output sections

1. **Summary table** — one row per block: block · #pass · #fail · #warning ·
   worst unresolved severity.
2. **Blocking gate** — every Blocking item with status + evidence; a bold
   verdict line: `LAUNCH-READY` or `NOT LAUNCH-READY (N blocking failures)`.
3. **Waivers** — each waived Blocking item with its reason and approver.
4. **Remediation** — all fails/warnings ordered blocking → high → medium → low.
5. **Needs-verification / Legal-review** — surfaced from `web-compliance-builder`.
6. **Disclaimer** — not legal advice.

## Why evidence is enforced

The repo's own hard-won lessons: a feature "done on a branch" is not live; a
"clean of credential VALUES" artifact can still leak real infra identifiers; a
screenshot render looking fine is not proof the user sees it right. So a Blocking
pass must carry evidence a cold reader can check, or the gate will not count it.
