# shared-memory

Unified shared state model for all AI agents: durable knowledge + real-time worktree state.

## What it does

`shared-memory` defines one cross-agent convention with two concerns:

1. **Knowledge memory** (portable, searchable, long-lived)
2. **Worktree runtime memory** (real-time handoffs/logs across git worktrees)

This lets Claude Code, Codex, Kiro, Devin, and other agents share both:
- what the project knows (durable)
- what agents are doing right now (real-time)

## When to use

- Saving project knowledge that should survive across tools
- Sharing handoffs/state between multiple worktrees immediately
- User says "shared memory", "handoff", "cross-worktree", "agent state"

## Storage model

### A) Durable knowledge layer

- Shared in repo (git-tracked): `.agents/memory/`
- Private local layer (not in git): `~/.shared-memory/<project-slug>/`

Use this for decisions, conventions, glossary, user preferences (private), etc.

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
