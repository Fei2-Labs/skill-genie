---
name: session-handoff
description: Summarize the current session into a precise, file-saved handoff document covering goals, files changed, commands run, errors, decisions, and next steps. Use mid-session or at end of session when handing off to another person or AI instance.
argument-hint: "What will the next session focus on?"
license: MIT
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
metadata:
  version: 1.5.0
  category: session-memory
  triggers:
    - "handoff"
    - "session summary"
    - "summarize session"
    - "hand this off"
    - "create handoff"
    - "write handoff"
    - "/handoff"
---

# Session Handoff

Use this skill when the user says "handoff", "summarize this session", "create a handoff", "hand this off", or invokes `/handoff`.

Produce a precise handoff document and write it to a file. Do not ask the user questions — derive everything from conversation history and git state.

If the user provides arguments, treat them as the intended focus of the next session and prioritize that focus in **Goal**, **Current State**, and **Next Steps**.
If the user says "update handoff" or similar, update the most recent handoff file in place instead of creating a new one.

This skill writes the artifact. Use `handoff-receiver` when the task is to continue execution from an existing handoff.

---

## Step 1: Determine output path and index files

1. If `.trellis/` exists in the working directory → write to `.trellis/handoffs/YYYY-MM-DD-HH-MM.md`
2. Else if `docs/` exists in the working directory → write to `docs/handoffs/YYYY-MM-DD-HH-MM.md`
3. Otherwise → write to `handoff.md` in the project root
4. If the handoff directory is not the project root, maintain `<handoff-dir>/CURRENT` as the active pointer
5. Maintain `<handoff-dir>/INDEX.md` as the compact handoff index

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
if [ "$HANDOFF_DIR" = "." ]; then
  HANDOFF_PATH="handoff.md"
  CURRENT_PATH="CURRENT"
  INDEX_PATH="INDEX.md"
else
  HANDOFF_PATH="$HANDOFF_DIR/$(date +%Y-%m-%d-%H-%M).md"
  CURRENT_PATH="$HANDOFF_DIR/CURRENT"
  INDEX_PATH="$HANDOFF_DIR/INDEX.md"
fi
printf '%s\n%s\n%s\n' "$HANDOFF_PATH" "$CURRENT_PATH" "$INDEX_PATH"
```

Before creating a new handoff, if `CURRENT` points to an existing active handoff, update that file:

- `status: paused`
- `updated_at: <now>`

Do not rewrite handoffs already marked `done` or `superseded`.
Use `superseded` only when you are explicitly replacing the same work stream.

---

## Step 2: Gather facts from git

Run these commands to get objective facts. Do not skip any.

```bash
# What changed
git status --short
git diff --stat HEAD
git log --oneline -10

# What branch
git rev-parse --abbrev-ref HEAD

# Any stash
git stash list
```

Use results to populate the **Files Changed** and **Commands Run** sections.

---

## Step 3: Extract from conversation

Review the full conversation to extract:

| Field | How to find it |
|---|---|
| **Goal** | What the user asked for at the start or most recently |
| **Files Changed** | Tool calls to Edit/Write + git diff output |
| **Commands Run** | Bash tool calls — extract the command and its outcome |
| **Errors** | Any tool errors, failed commands, stack traces mentioned |
| **Decisions** | Choices made between options, trade-offs accepted, scope cuts |
| **Next Steps** | Unfinished work, items explicitly deferred, follow-ups named |
| **History** | Commit hashes and branch/state changes that matter to the next session |

Be precise. Prefer concrete facts over summaries. Include file paths and line numbers where known.

Avoid duplicating content already captured in other artifacts (PRDs, plans, ADRs, issues, commits, diffs). Reference those artifacts by path or URL in the relevant sections instead of repeating long content.

---

## Step 4: Write the handoff file

Use this exact template. Fill every section — write "none" if a section is genuinely empty.

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

# Session Handoff

**Date**: YYYY-MM-DD HH:MM  
**Branch**: <branch name>  
**Working directory**: <absolute path>

---

## Goal

<One paragraph. What was the user trying to accomplish and why? Be specific — not "improve the app" but "add X to Y so that Z".>

---

## Files Changed

| File | Change |
|------|--------|
| `path/to/file.ts` | Added `functionName()`, removed deprecated `oldFn()` |
| `path/to/config.yml` | Updated `timeout` from 30 to 60 |

*(list only files with actual changes; omit read-only)*

---

## Commands Run

| Command | Outcome |
|---------|---------|
| `npm run build` | ✓ passed |
| `git push origin main` | ✗ rejected — no upstream set |

---

## History

Summarize the commit and branch history that matters for the next session.

Include:
- recent commit hashes
- branch rewrites or force-pushes
- merges, rebases, or resets that changed the working line of development

---

## Errors Encountered

- **Error**: `Cannot find module './utils'` in `src/index.ts:12`  
  **Resolution**: Added missing import; resolved.

- **Error**: `git push` rejected  
  **Resolution**: Unresolved — see Next Steps.

*(list errors that occurred, whether resolved or not)*

---

## Decisions Made

- **Chose X over Y** because: <reason>
- **Deferred Z** because: <reason>
- **Accepted trade-off**: <what was given up and why>

---

## Current State

<One paragraph. Where does the work stand right now? Is it working? Partially done? Blocked? What is the state of the codebase at this moment?>

---

## Next Steps

1. [ ] <Concrete action — specific file, command, or decision needed>
2. [ ] <Next action>
3. [ ] <Stretch / nice-to-have if time allows>

---

## Context for the Next Session

<Any non-obvious context a new AI or developer would need to pick this up: gotchas, environment quirks, why something was done a certain way, what was explicitly ruled out.>
```

---

## Step 5: Update pointer and index

Write the final handoff path into `CURRENT`.
Then update `INDEX.md` with one row per tracked handoff:

| Path | Status | Updated | Goal |
|------|--------|---------|------|
| `.trellis/handoffs/2026-05-22-13-10-search.md` | `open` | `2026-05-22 13:10` | `Document the search feature handoff flow` |

Rules:

- keep rows stable and append-only when possible
- update only minimal metadata: `path`, `status`, `updated_at`, short goal summary
- never duplicate full handoff bodies inside the index
- preserve `paused`, `done`, and `superseded` rows for historical routing

`handoff-receiver` should read `CURRENT` and `INDEX.md` first. It should not scan the directory in the common case.

---

## Step 6: Confirm to user

After writing the file, output exactly:

```
Handoff written to: <relative path to file>

## Goal
<one sentence summary>

## Next Steps
<numbered list from the file>
```

Do not output the full file contents in chat — the file is the artifact. The inline summary is just a quick confirmation.

---

## Anti-patterns

- Do not ask the user "what did we work on?" — derive from conversation.
- Do not write vague entries like "various files updated" — be specific.
- Do not skip the git commands — they provide objective ground truth.
- Do not create a new handoff if the user says "update handoff" — overwrite the most recent one.
- Do not leave multiple active handoffs without updating `CURRENT`.

## Example

If the handoff directory contains:

- `CURRENT` → `.trellis/handoffs/2026-05-22-12-40-open-core.md`
- `.trellis/handoffs/2026-05-22-12-21-onboarding.md` with no `status`

and you create `.trellis/handoffs/2026-05-22-13-10-search.md`, then:

- `2026-05-22-12-40-open-core.md` becomes `status: paused`
- `2026-05-22-12-21-onboarding.md` remains untouched until indexed
- `CURRENT` moves to `2026-05-22-13-10-search.md`
- `INDEX.md` contains one row for each known stream
