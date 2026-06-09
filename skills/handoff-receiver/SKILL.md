---
name: "handoff-receiver"
description: "Receive a prior session handoff and continue execution safely by validating repo state, resuming from next steps, and refreshing the handoff artifact."
license: "MIT"
allowed-tools: "Bash, Read, Write, Glob, Grep"
metadata: {"version":"1.3.2","category":"session-memory","triggers":["take over this handoff","continue from handoff","resume from handoff","pick this up from previous session","handoff receiver"],"license":"MIT","tags":["session-memory","handoff","continuation","workflow"],"hermes":{"tags":["session-memory","handoff","continuation","workflow"]}}
---

# Handoff Receiver

Use this skill when you are the new skill/agent receiving work from a previous session handoff file.

Goal: continue delivery with minimal drift, no scope expansion, and clear state recovery.

## Step 1: Locate the active handoff and index

1. Prefer `.trellis/handoffs/CURRENT` when present.
2. Otherwise use `docs/handoffs/CURRENT` when present.
3. Otherwise use `CURRENT` in project root.
4. Read the matching `INDEX.md` in the same handoff directory.
5. Only if no pointer exists, fall back to the latest legacy handoff file.

```bash
if [ -f ".trellis/handoffs/CURRENT" ]; then
  cat .trellis/handoffs/CURRENT
  echo ".trellis/handoffs/INDEX.md"
elif [ -f "docs/handoffs/CURRENT" ]; then
  cat docs/handoffs/CURRENT
  echo "docs/handoffs/INDEX.md"
elif [ -f "CURRENT" ]; then
  cat CURRENT
  echo "INDEX.md"
else
  [ -f handoff.md ] && echo "handoff.md"
fi
```

If no handoff is found, stop and ask one minimal question requesting the handoff path.

### Step 1.5: Read the compact index before opening any other handoff

Read `INDEX.md` and classify streams from the table only.

- `status: in_progress` or `status: open` and matches `CURRENT` → active. Proceed.
- `status: in_progress` and does not match `CURRENT` → conflict. Ask the user
  which stream is authoritative.
- `status: paused` → parallel stream. Surface it in takeover output, but do
  not execute it.
- `status: done` or `status: superseded` → archive. Skip.
- any handoff row with `status: orphan` → open only that file's `Goal` and
  `Next Steps`, then ask the user whether to mark it `paused`, merge it,
  supersede it, or leave it as-is.
- if `CURRENT` points to a handoff missing from `INDEX.md`, treat that as an
  index drift bug and ask one focused question before continuing.

Do not scan the handoff directory in the normal path. Directory scans are
reserved for index repair only.

After locating the active handoff, mark it before execution:

- `status: in_progress`
- `taken_over_at: <now>`
- `taken_over_by: handoff-receiver`
- `updated_at: <now>`

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
5. If work is complete, set `status: done` and clear the matching `CURRENT` pointer.
6. If work is complete, update the matching `INDEX.md` row to `status: done`.
7. If work is paused and a fresh handoff is needed, create the new handoff, set the old file to `status: paused`, move `CURRENT` to the new file, and update both rows in `INDEX.md`.
8. If work is truly replaced by a new handoff in the same stream, set the old file to `status: superseded`, write `superseded_by: <new path>`, move `CURRENT` to the new file, and update both rows in `INDEX.md`.

Do not create extra summary files unless explicitly requested.

## Output contract to user

When reporting takeover status, respond with:

```text
Using handoff: <path>

## Goal
<one sentence>

## Current Step
<the exact Next Steps item being executed>

## Parallel Streams
<none OR one line per paused/orphan handoff>

## Blockers
<none OR one-line blocker>
```

## Anti-patterns

- Starting implementation before checking current git state.
- Ignoring `Decisions Made` and re-opening settled trade-offs.
- Mixing new feature requests into handoff continuation.
- Updating many files before finishing `Next Steps` item #1.
- Writing a new handoff file when an existing one should be updated.
- Scanning the entire handoff directory when `CURRENT` and `INDEX.md` already
  provide the active stream and compact metadata.
- Reading the full body of every historical handoff when the index already
  provides status and goal summaries.

## Example

Index state:

- `CURRENT` → `.trellis/handoffs/2026-05-22-12-40-open-core.md`
- `INDEX.md` row for onboarding says `status: orphan`
- `INDEX.md` row for billing says `status: paused`

Expected takeover flow:

1. Read `CURRENT` and detect the active path.
2. Read `INDEX.md` and surface the paused billing stream.
3. Open only the orphan onboarding handoff to read `Goal` and `Next Steps`.
4. Ask the user how to classify the orphan before continuing the active stream.
