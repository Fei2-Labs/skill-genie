# shared-memory

Portable project memory that any AI agent can find, plus optional real-time state shared across git worktrees.

## What it does

`shared-memory` defines an on-disk convention for storing project knowledge that works across all AI coding agents (Claude Code, Cursor, Codex, OpenClaw, Aider, etc.). It includes a shared layer in the project repo and a private layer for personal notes.

It also covers a second, separate concern:

1. **Knowledge memory** (portable, searchable, long-lived)
2. **Worktree runtime memory** (real-time handoffs/logs across git worktrees)

This lets Claude Code, Codex, Kiro, Devin, and other agents share both:
- what the project knows (durable)
- what agents are doing right now (real-time)

## When to use

- Saving project knowledge that should survive across tools
- User says "save to shared memory", "remember this for all agents"
- When you suspect another agent's memory might be relevant
- Sharing handoffs/state between multiple worktrees immediately
- User says "handoff", "cross-worktree", "agent state"

## How it works

1. Reads existing shared memory from the project's `.agents/memory/` directory
2. Writes new knowledge using a structured format with metadata
3. Private notes go to a machine-local layer outside the repo
4. Any agent can discover and read the shared layer
5. Optionally links each worktree's `.trellis/shared` to one per-repository runtime store

## Key features

- Cross-agent compatible: works with any tool that can read files
- Structured format with timestamps and categories
- Private layer for personal/sensitive notes (never committed)
- Search and retrieval across all stored knowledge
- Sensitive-content gate before anything is written to the shared layer
- Real-time cross-worktree handoffs without commits or merges

## Storage model

### A) Durable knowledge layer

- Shared in repo (git-tracked): `.agents/memory/`
- Private local layer (not in git): `~/.shared-memory/<project-slug>/`
- Global private layer (not in git): `~/.shared-memory/global/`

Use this for decisions, conventions, glossary, user preferences (private), etc.
The global index is read at session start; project-specific files remain
on-demand to keep context bounded.

### B) Real-time worktree layer

- In every worktree: `.trellis/shared` (symlink)
- Target: `<git-common-dir>/trellis-shared/`
- Subdirs:
  - `handoffs/`
  - `knowledge/`
  - `agents/`
  - `events/`

Use this for cross-worktree handoffs, active stream state, append-only agent logs, and timestamped events that should be visible immediately to sibling worktrees.

## Layer boundaries

- Put **versioned project knowledge** in `.agents/memory/` (or private local memory).
- Put **real-time coordination state** in `.trellis/shared/`.
- Do not treat `.trellis/shared/` as a replacement for committed specs/tasks.
- Do not put secrets in any shared layer.

## Setup

Run the included linker template from repo root:

```bash
bash skills/shared-memory/templates/link_shared_memory.sh
```

Then ensure `.gitignore` contains:

```gitignore
.trellis/shared
```

## Related skills

- `session-handoff`: writes handoff artifacts
- `handoff-receiver`: resumes from active handoff safely

When `.trellis/shared` exists, handoff skills should prefer `.trellis/shared/handoffs/` for real-time cross-worktree continuity.

---

**Source**: [github.com/Fei2-Labs/skill-genie](https://github.com/Fei2-Labs/skill-genie)
**Author**: [@clarezoe](https://x.com/clarezoe)
