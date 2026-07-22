# handoff-receiver

Receive and continue from a prior session handoff.

## What it does

`handoff-receiver` picks up where `session-handoff` left off. It validates repo state, loads the active handoff document, and resumes execution from next steps with minimal drift.

## When to use

- Starting a new session that should continue previous work
- User says "take over this handoff", "continue from handoff", "resume"

## How it works

1. Locate active handoff via `CURRENT` pointer and `INDEX.md`
2. Validate git state against handoff context
3. Load goal, current state, and next steps
4. Execute next step in order

## Handoff read path precedence

1. `.trellis/shared/handoffs/` (if runtime shared layer is configured)
2. `.trellis/handoffs/`
3. `docs/handoffs/`
4. project root fallback

When path #1 exists, this receiver should treat it as canonical to keep all worktrees in sync in real time.

## Key features

- State validation before resuming
- Reads CURRENT pointer first, avoids broad scans
- Updates takeover metadata (`taken_over_at`, `taken_over_by`)
- Pairs with `session-handoff` for continuity

---

**Source**: [github.com/Fei2-Labs/skill-genie](https://github.com/Fei2-Labs/skill-genie)
**Author**: [@clarezoe](https://x.com/clarezoe)
