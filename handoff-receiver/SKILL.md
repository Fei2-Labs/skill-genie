---
name: handoff-receiver
description: Receive a prior session handoff and continue execution safely by validating repo state, resuming from next steps, and refreshing the handoff artifact.
license: MIT
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
metadata:
  version: 1.0.0
  category: session-memory
  triggers:
    - "take over this handoff"
    - "continue from handoff"
    - "resume from handoff"
    - "pick this up from previous session"
    - "handoff receiver"
---

# Handoff Receiver

Use this skill when you are the new skill/agent receiving work from a previous session handoff file.

Goal: continue delivery with minimal drift, no scope expansion, and clear state recovery.

## Step 1: Locate the latest handoff

1. Prefer `.trellis/handoffs/` when present.
2. Otherwise use `handoff.md` in project root.
3. If both exist, choose the most recent file by timestamp.

```bash
if [ -d ".trellis/handoffs" ]; then
  ls -1t .trellis/handoffs/*.md 2>/dev/null | head -n 1
else
  [ -f handoff.md ] && echo "handoff.md"
fi
```

If no handoff is found, stop and ask one minimal question requesting the handoff path.

## Step 2: Read only decision-critical sections first

Read these sections in this order:

1. `Goal`
2. `Current State`
3. `Next Steps`
4. `Decisions Made`
5. `Context for the Next Session`

Capture:
- in-scope objective
- current completion status
- first actionable next step
- explicit constraints and trade-offs

## Step 3: Reconcile handoff vs repository reality

Run objective checks before touching code:

```bash
git rev-parse --abbrev-ref HEAD
git status --short
git diff --stat HEAD
git log --oneline -10
```

Then compare with `Files Changed` and `Commands Run` in the handoff.

If mismatch is small and explainable, continue.
If mismatch is major (different branch, unrelated deltas, missing files), ask one minimal clarification question before edits.

## Step 4: Execute in strict order

1. Start with `Next Steps` item #1.
2. Keep scope fixed to handoff goal.
3. Do not re-architect unless blocked by correctness.
4. Re-run relevant validation commands listed in handoff.
5. If blocked by an unresolved decision, ask exactly one focused question.

## Step 5: Update handoff artifact before yielding

At pause/completion:

1. Update the latest handoff file in place.
2. Refresh `Current State`, `Next Steps`, and `Errors Encountered`.
3. Remove completed items; keep remaining items actionable.
4. Keep content factual and concise.

Do not create extra summary files unless explicitly requested.

## Output contract to user

When reporting takeover status, respond with:

```text
Using handoff: <path>

## Goal
<one sentence>

## Current Step
<the exact Next Steps item being executed>

## Blockers
<none OR one-line blocker>
```

## Anti-patterns

- Starting implementation before checking current git state.
- Ignoring `Decisions Made` and re-opening settled trade-offs.
- Mixing new feature requests into handoff continuation.
- Updating many files before finishing `Next Steps` item #1.
- Writing a new handoff file when an existing one should be updated.
