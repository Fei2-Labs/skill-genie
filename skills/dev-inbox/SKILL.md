---
name: "dev-inbox"
description: "Triage and route anything that comes up during a session — bugs, ideas, improvements, small fixes — to the right place. Use when the user or you notice something that may not belong to the current task."
license: "MIT"
argument-hint: "Describe the problem, idea, or improvement"
allowed-tools: "Bash, Read, Write, Grep, Glob"
metadata: {"version":"1.0.2","category":"workflow","triggers":["记一下","记下来","以后再说","这个先不管","open an issue","log this","track this","dev inbox","inbox","/dev-inbox"],"license":"MIT","tags":["workflow","task-triage","issue-tracking","session-management"],"hermes":{"tags":["workflow","task-triage","issue-tracking","session-management"]}}
---

# Dev Inbox

Triage anything that comes up during a session — bugs, features, improvements, fleeting ideas — and route it to the right place so it is never lost and always discoverable by future sessions.

This skill works in any context: software development, writing, design, or any task.

---

## When to Activate

- **Proactive**: You notice the user said something unrelated to the current task (a bug, idea, improvement, or tangent). Intervene immediately with a suggestion.
- **Reactive**: The user explicitly says "记一下", "log this", "open an issue", "以后再说", "track this", or invokes `dev-inbox`.

---

## Decision Tree

```
User says something
│
├─ Is it part of the current task?
│   (Current task = current conversation + open files + git diff)
│   ├─ YES → Do it directly. Stop here.
│   └─ NO ↓
│
├─ Does it block the current task?
│   ├─ YES → Handle it first, then return to current task.
│   └─ NO ↓
│
├─ Priority?
│   ├─ HIGH — would cause data loss, money loss, security issue, or blocks others
│   ├─ NORMAL — clearly needs doing, but not urgent
│   └─ LOW — nice-to-have, fleeting thought, cosmetic
│
└─ Record it + ensure future discoverability
```

---

## Classification

Assign one type and one priority:

| Type | Meaning | Example |
|------|---------|---------|
| `fix` | Something existing is broken or wrong | Bug, incorrect content, wrong behavior |
| `add` | Something new is needed | Feature, new section, new capability |
| `improve` | Works but could be better | Better wording, cleaner UI, performance |
| `idea` | Fleeting thought, maybe later | "What if we also..." |

Priority: `high` / `normal` / `low`

---

## Interaction Pattern

When you identify something that doesn't belong to the current task, respond with a **concrete suggestion** — not an open question:

> This doesn't seem related to the current task. I suggest recording it as:
>
> **Type**: fix | **Priority**: normal
> **Title**: Receipt is not generated after order submission
>
> Confirm?

The user responds with one word (yes/no/adjust). Then execute.

---

## Where to Record

Detect the environment and pick the best destination. The goal is **future discoverability** — the record must surface in a future session without the user remembering it exists.

### Priority order:

1. **GitHub remote + `gh` CLI available**
   - Check: `git remote get-url origin 2>/dev/null && command -v gh`
   - Action: `gh issue create` with title, label, and body
   - Why discoverable: Agent can `gh issue list --state open --label <type>`
   - Merge logic: Search open issues with same label + similar title keywords. If found → append checklist item. If unsure → ask user.

2. **Agent memory system available** (Windsurf memories, Claude memory, etc.)
   - Action: Write to memory with `[TODO]` prefix and type/priority metadata
   - Why discoverable: Automatically loaded on next session start

3. **Project directory exists**
   - Action: Append to `TODO.md` in project root (create if absent)
   - Format: Grouped by type, each item has priority tag
   - Why discoverable: Agent should read `TODO.md` at session start

4. **None of the above**
   - Action: Output formatted content for the user to place manually
   - Format: Ready to paste anywhere

### After recording, confirm:

```
Recorded: [type] [title]
Location: [where it was saved]
Discovery: [how a future session will find it]
```

---

## Record Templates

Adapt detail level to priority — lower priority = lighter format.

### fix (high/normal)

```markdown
## Problem
[What is broken / wrong]

## Expected
[What should happen]

## Context
[Where/when discovered, related task if any]
```

### fix (low)

```markdown
- [One-line description of what's wrong]
```

### add

```markdown
## What
[What to add]

## Why
[Why it matters]
```

### improve

```markdown
- [What it is now] → [What it should be]
```

### idea

```markdown
- [One sentence]
```

---

## Merge Logic

Before creating a new record, check if a related one already exists:

- **GitHub Issues**: `gh issue list --state open --label <type>` — scan titles for keyword overlap
- **TODO.md**: Scan same type section for similar items
- **Memory**: Check for `[TODO]` entries with similar content

If a match is found → append as a sub-item or checklist entry.
If uncertain → ask: "This looks related to [existing item]. Add to it, or create separate?"

---

## GitHub Issue Labels

When using GitHub Issues, apply these labels (create if they don't exist):

```bash
gh label create "fix" --color "d73a4a" --description "Something is broken" 2>/dev/null
gh label create "add" --color "0075ca" --description "New feature or content" 2>/dev/null
gh label create "improve" --color "a2eeef" --description "Enhancement to existing" 2>/dev/null
gh label create "idea" --color "e4e669" --description "Exploration, maybe later" 2>/dev/null
gh label create "high" --color "b60205" --description "High priority" 2>/dev/null
gh label create "low" --color "c5def5" --description "Low priority" 2>/dev/null
```

---

## No-`gh` Fallback

If `gh` is not installed but a GitHub remote exists, output:

```
I can't create the issue automatically (gh CLI not found).
Here's the issue ready to paste:

Title: [title]
Labels: [type], [priority]
Body:
---
[formatted body]
---

Create it at: [repo URL]/issues/new
```

---

## Anti-patterns

- Do not interrupt the user's flow with long explanations. Keep triage to 2–3 lines.
- Do not ask open-ended questions like "What do you want to do with this?" — propose a concrete action.
- Do not create records that can't be found later. Always state the discovery path.
- Do not duplicate: always check for existing related records first.
- Do not use this skill for things that ARE part of the current task — just do them.
- Do not generate a file and leave it disconnected. The record must be in a system the agent will check.

---

## Relationship to Other Skills

- **`session-handoff`** / **`close-loop`**: At session end, mention count of items recorded this session (e.g., "Recorded 3 items to dev-inbox this session"). No need to re-save — items are already persisted.
- **`handoff-receiver`**: When resuming, check for pending inbox items as part of context loading.
