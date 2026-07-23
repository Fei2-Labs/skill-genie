# Worktree shared framework specification

## Goal

Provide real-time shared state across git worktrees in the same repository without requiring commits or merges for handoff visibility.

## Canonical runtime root

- Runtime root: `<git-common-dir>/trellis-shared/`
- Worktree pointer: `<repo>/.trellis/shared` -> symlink to runtime root

## Required structure

```text
<git-common-dir>/trellis-shared/
├── handoffs/
├── knowledge/
├── agents/
└── events/
```

## Data ownership and write model

- `agents/<agent>.jsonl`: append-only; only that agent writes.
- `events/YYYY/MM/DD.jsonl`: append-only event stream.
- `handoffs/*.md`: owned by a stream; mutable by owning stream.
- `knowledge/*`: append-only blocks or timestamped files.

## Timestamp and identity conventions

- Timestamps: ISO 8601 with timezone (for example `2026-07-23T01:34:00+02:00`)
- Agent IDs: lowercase kebab-case (`claude-code`, `codex`, `kiro`, `devin`, `custom-agent`)

## Boundary with durable memory

Durable knowledge and runtime state are separate:

- Durable shared knowledge -> `.agents/memory/` (git-tracked)
- Durable private knowledge -> `~/.shared-memory/<slug>/` (local)
- Runtime cross-worktree state -> `.trellis/shared/` (symlinked runtime root)

Do not replace committed specs/tasks with runtime files.

## Setup checklist

1. Run:
   ```bash
   bash skills/shared-memory/templates/link_shared_memory.sh
   ```
2. Confirm:
   ```bash
   ls -l .trellis/shared
   ```
3. Ensure `.gitignore` contains:
   ```gitignore
   .trellis/shared
   ```
4. Test in another worktree by creating a file under `.trellis/shared/handoffs/` and reading it from sibling worktree.
5. Install a session-start rule that runs the linker in each new agent session.
   The link is per worktree, while the runtime root is shared per repository.

## Security notes

- Never store credentials, private keys, tokens, or `.env` content.
- Treat runtime files as local shared operational context, not secure storage.
