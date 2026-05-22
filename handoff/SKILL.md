---
name: handoff
description: Compact the current conversation into a tracked handoff document for another agent to pick up.
argument-hint: "What will the next session be used for?"
license: MIT
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
metadata:
  version: 1.3.0
  category: session-memory
---

# Handoff

Use this skill when the user explicitly wants a compact or lightweight handoff.

Write a short handoff file, but keep it inside the same tracked lifecycle as `session-handoff`.

## Step 1: Determine output path and index files

1. If `.trellis/` exists, use `.trellis/handoffs/`.
2. Else if `docs/` exists, use `docs/handoffs/`.
3. Otherwise use the project root.
4. The active pointer file is `<handoff-dir>/CURRENT`.
5. The metadata index file is `<handoff-dir>/INDEX.md`.

```bash
if [ -d ".trellis" ]; then
  mkdir -p .trellis/handoffs
  HANDOFF_DIR=".trellis/handoffs"
elif [ -d "docs" ]; then
  mkdir -p docs/handoffs
  HANDOFF_DIR="docs/handoffs"
else
  HANDOFF_DIR="."
fi
HANDOFF_PATH="$HANDOFF_DIR/$(date +%Y-%m-%d-%H-%M)-compact.md"
CURRENT_PATH="$HANDOFF_DIR/CURRENT"
INDEX_PATH="$HANDOFF_DIR/INDEX.md"
printf '%s\n%s\n%s\n' "$HANDOFF_PATH" "$CURRENT_PATH" "$INDEX_PATH"
```

## Step 2: Preserve any previous active handoff

If `CURRENT` points to an existing handoff, update that file before writing the new one:

- `status: paused`
- `updated_at: <now>`

Do not rewrite handoffs already marked `done` or `superseded`.
Use `superseded` only when you are explicitly replacing the same work stream.

## Step 3: Write a compact handoff

Use this template:

```markdown
---
status: open
created_at: YYYY-MM-DD HH:MM
updated_at: YYYY-MM-DD HH:MM
taken_over_at:
taken_over_by:
superseded_by:
source_handoff:
stream_note:
---

# Handoff

## Goal
<one short paragraph>

## Current State
<one short paragraph>

## Next Steps
1. <next action>
2. <next action>

## Suggested Skills
- `<skill-name>`
```

Keep it concise. Reference existing artifacts instead of duplicating them.

## Step 4: Update pointer and index

Write the new handoff path into `CURRENT`.
Then update `INDEX.md` with exactly one row per known handoff:

| Path | Status | Updated | Goal |
|------|--------|---------|------|
| `.trellis/handoffs/2026-05-22-13-05-ui-bugs-compact.md` | `open` | `2026-05-22 13:05` | `Fix onboarding UI bugs` |

Rules:

- keep `CURRENT` out of the table
- preserve existing rows for `paused`, `done`, and `superseded` handoffs
- add or update only minimal metadata
- never copy full `Next Steps` into the index

## Step 5: Confirm to user

After writing the file, output exactly:

```text
Handoff written to: <relative path>

## Goal
<one sentence summary>

## Next Steps
<numbered list from the file>
```

## Example

If `.trellis/handoffs/CURRENT` points to `2026-05-22-12-40-open-core.md` and
you create `2026-05-22-13-05-ui-bugs-compact.md`, then:

- `2026-05-22-12-40-open-core.md` becomes `status: paused`
- `CURRENT` is updated to `2026-05-22-13-05-ui-bugs-compact.md`
- `INDEX.md` records both streams so `handoff-receiver` does not scan the directory
