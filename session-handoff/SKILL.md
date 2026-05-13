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
  version: 1.2.1
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

## Step 1: Determine output path

1. If `.trellis/` exists in the working directory → write to `.trellis/handoffs/YYYY-MM-DD-HH-MM.md`
2. Else if `docs/` exists in the working directory → write to `docs/handoffs/YYYY-MM-DD-HH-MM.md`
3. Otherwise → write to `handoff.md` in the project root

```bash
# Check for trellis
if [ -d ".trellis" ]; then
  mkdir -p .trellis/handoffs
  echo ".trellis/handoffs/$(date +%Y-%m-%d-%H-%M).md"
elif [ -d "docs" ]; then
  mkdir -p docs/handoffs
  echo "docs/handoffs/$(date +%Y-%m-%d-%H-%M).md"
else
  echo "handoff.md"
fi
```

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

## Step 5: Confirm to user

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
