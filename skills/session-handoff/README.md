# session-handoff

Summarize the current session into a precise, file-saved handoff document.

## What it does

`session-handoff` produces a structured handoff file covering goals, files changed, commands run, errors, decisions, and next steps — so a future agent or person can pick up exactly where you left off.

## When to use

- Mid-session or end of session when handing off to another person or AI instance
- User says "handoff", "summarize session", "hand this off"

## How it works

1. Determine output path (`.trellis/shared/handoffs/` when the runtime layer is configured, else `.trellis/handoffs/`, `docs/handoffs/`, or project root)
2. Gather facts from git (`status`, `diff`, `log`)
3. Extract from conversation (goal, files, commands, errors, decisions, next steps)
4. Write the handoff file using a strict template
5. Update `CURRENT` pointer and `INDEX.md`

## Handoff path precedence

1. `.trellis/shared/handoffs/` (if `.trellis/shared` exists)
2. `.trellis/handoffs/`
3. `docs/handoffs/`
4. project root

This keeps multi-worktree agents synchronized in real time when shared memory runtime layer is enabled.

## Key features

- Derives everything from conversation + git state — never asks the user
- Maintains a handoff index for multi-stream tracking
- Status management: open / paused / done / superseded
- Pairs with `handoff-receiver` for seamless session continuity

---

**Source**: [github.com/Fei2-Labs/skill-genie](https://github.com/Fei2-Labs/skill-genie)
**Author**: [@clarezoe](https://x.com/clarezoe)
