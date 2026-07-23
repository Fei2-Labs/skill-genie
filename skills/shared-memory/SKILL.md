---
name: "shared-memory"
description: "Read and write shared state for ANY AI agent with a dual-layer model: durable cross-agent knowledge (`.agents/memory` + optional private local layer) and real-time cross-worktree runtime memory (`.trellis/shared` symlinked to `<git-common-dir>/trellis-shared`). Use for project memory, handoffs, and multi-worktree coordination."
license: "MIT"
allowed-tools: "Bash, Read, Write, Edit, Glob, Grep"
metadata: {"version":"1.1.2","category":"cross-agent-coordination","triggers":["save to shared memory","remember this for all agents","shared memory","global memory","cross-agent memory","worktree shared memory","cross-worktree handoff","agent shared state"],"license":"MIT","tags":["shared-memory","cross-agent-coordination","project-memory","worktree","handoff"],"hermes":{"tags":["shared-memory","cross-agent-coordination","project-memory","worktree","handoff"]}}
---

# Shared Memory — durable knowledge + real-time worktree state

Use one skill for two different concerns:

1. **Durable knowledge memory** for cross-agent reuse over time
2. **Real-time runtime memory** for cross-worktree coordination now

Keep these concerns separate in storage and mutation rules.

## Layer model

### Layer K0: global private memory (machine-wide)

- Path: `~/.shared-memory/global/`
- Purpose: reusable operating preferences and lessons that apply across projects
- Format: markdown files + `MEMORY.md` index
- Read its index at the start of every session; load entries on demand

### Layer K1: shared durable knowledge (git-tracked)

- Path: `<repo>/.agents/memory/`
- Purpose: project facts, decisions, conventions, glossary
- Format: markdown files + `MEMORY.md` index

### Layer K2: private durable knowledge (machine-local)

- Path: `~/.shared-memory/<project-slug>/`
- Purpose: personal notes or sensitive details not suitable for git
- Format: same structure as K1

### Layer R: real-time worktree runtime memory

- In worktree: `<repo>/.trellis/shared` (symlink)
- Target: `<git-common-dir>/trellis-shared/`
- Required subdirs:
  - `handoffs/` (cross-worktree handoff files)
  - `knowledge/` (append-only runtime discoveries)
  - `agents/` (one append-only log per agent)
  - `events/` (timestamped event stream)

## Operation 1 — Locate memory at session start

```bash
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
SLUG="$(basename "$REPO_ROOT" | tr '[:upper:]' '[:lower:]')"

# Durable layers
K0="$HOME/.shared-memory/global"
K1="$REPO_ROOT/.agents/memory"
K2="$HOME/.shared-memory/$SLUG"

[ -f "$K0/MEMORY.md" ] && cat "$K0/MEMORY.md"
[ -f "$K1/MEMORY.md" ] && cat "$K1/MEMORY.md"
[ -f "$K2/MEMORY.md" ] && cat "$K2/MEMORY.md"

# Runtime layer pointer
[ -L "$REPO_ROOT/.trellis/shared" ] && ls -1 "$REPO_ROOT/.trellis/shared/handoffs" 2>/dev/null || true
```

Read indexes first, then load specific files on demand.

## Operation 2 — Write durable memory (K1/K2)

Classify each write as:
- `global` -> K0 (`~/.shared-memory/global`) for machine-wide private lessons
- `shared` -> K1 (`.agents/memory`) and enters git
- `private` -> K2 (`~/.shared-memory/<slug>`) and stays local

Required frontmatter:

```markdown
---
name: some-memory
description: one-line retrieval hook
metadata:
  type: user | feedback | project | reference | engineering
  scope: shared | private
  created: 2026-07-23
  updated: 2026-07-23
---
```

Update `MEMORY.md` after every new memory file.

## Operation 3 — Enable runtime layer (R) for worktrees

Run:

```bash
bash skills/shared-memory/templates/link_shared_memory.sh
```

Script contract:
- Resolves absolute git common dir
- Creates `trellis-shared/{handoffs,knowledge,agents,events}`
- Creates `.trellis/shared` symlink if missing
- Fails loudly on conflicting existing path
- Never `rm -rf` user content implicitly

Also ensure `.gitignore` has:

```gitignore
.trellis/shared
```

Install the Skill Genie session-start rules so every new agent session runs the
idempotent linker before it reads handoffs. Merely installing this skill does
not make a client invoke it automatically.

## Operation 4 — Write runtime state (R)

### Handoffs

- Location: `.trellis/shared/handoffs/`
- Suggested name: `YYYY-MM-DD-<stream>-<agent>.md`
- Mutable only by owning stream; others append notes in their own files

### Agent logs

- Location: `.trellis/shared/agents/<agent>.jsonl`
- One JSON object per line
- Append-only

### Events

- Location: `.trellis/shared/events/YYYY/MM/DD.jsonl`
- Append-only timestamped entries

### Runtime knowledge

- Location: `.trellis/shared/knowledge/`
- Prefer append-only files or timestamped entry blocks

## Operation 5 — Boundary enforcement

Use this checklist before every write:

1. Is this long-lived, reusable project knowledge? -> K1/K2
2. Is this active coordination/handoff/runtime state? -> R
3. Is this secret or credential? -> refuse shared write; route to private notes

Never mix layers in one file.

## Anti-patterns

- Writing handoffs only under branch-local `.trellis/handoffs/` when runtime layer exists
- Storing project knowledge exclusively in tool-specific private stores
- Putting secrets in K1 or R
- Overwriting another agent's runtime file instead of append-only or per-agent ownership

## Cross-references

- `session-handoff`: structured handoff generation
- `handoff-receiver`: strict handoff continuation
- Framework spec: `skills/shared-memory/references/worktree-shared-framework.md`
