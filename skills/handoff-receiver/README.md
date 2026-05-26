# handoff-receiver

Receive and continue from a prior session handoff.

## What it does

`handoff-receiver` picks up where `session-handoff` left off. It validates repo state, loads the active handoff document, and resumes execution from the next steps — with minimal drift and no scope expansion.

## When to use

- Starting a new session that should continue previous work
- User says "take over this handoff", "continue from handoff", "resume"

## How it works

1. Locate the active handoff via `CURRENT` pointer and `INDEX.md`
2. Validate git state matches the handoff's recorded branch and commit
3. Load goal, current state, and next steps
4. Begin executing next steps in order

## Key features

- State validation before resuming
- Reads CURRENT pointer — no directory scanning needed
- Updates handoff status (`taken_over_at`, `taken_over_by`)
- Pairs with `session-handoff` for full session continuity

---

**Source**: [github.com/Fei2-Labs/skill-genie](https://github.com/Fei2-Labs/skill-genie)
**Author**: [@clarezoe](https://x.com/clarezoe)
