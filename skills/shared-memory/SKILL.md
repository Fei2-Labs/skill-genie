---
name: "shared-memory"
description: "Read and write project memory that ANY AI agent can find (Claude Code, Cursor, Codex, OpenClaw, Aider, ...). Defines a portable on-disk convention in the project repo plus a private layer for personal notes, and an optional real-time runtime layer (`.trellis/shared`) that parallel git worktrees share. Use when saving project knowledge that should survive across tools, when you suspect another agent's memory might be relevant, or when coordinating handoffs across worktrees."
license: "MIT"
allowed-tools: "Bash, Read, Write, Edit, Glob, Grep"
metadata: {"version":"1.1.3","category":"cross-agent-coordination","triggers":["save to shared memory","remember this for all agents","what do agents know about this project","load project memory","shared memory","cross-agent memory","where is the project memory","find memory from other agents","global memory","worktree shared memory","cross-worktree handoff","agent shared state"],"license":"MIT","tags":["shared-memory","cross-agent-coordination","project-memory","workflow","worktree","handoff"],"hermes":{"tags":["shared-memory","cross-agent-coordination","project-memory","workflow","worktree","handoff"]}}
---

# Shared Memory — cross-agent project knowledge

Most agent tools store memory in their own private location: Claude Code uses
`~/.claude/projects/<slug>/memory/`, Cursor uses `.cursorrules`, Codex reads
`AGENTS.md`, etc. None of them read each other's stores. This skill defines a
**single on-disk convention** so any agent that knows about it — and any human
running `cat` — can read project memory written by any other agent.

It also defines an optional **runtime layer** for a different concern: what
agents in parallel git worktrees of the same repository are doing right now.
Durable knowledge and runtime state use separate storage and separate
mutation rules; see § Layer 3 and § Operation 7.

## The convention — two layers

### Layer 1 — `.agents/memory/` inside the repo (SHARED, git-tracked)

```
<repo>/
├── .agents/
│   └── memory/
│       ├── MEMORY.md                  ← index, every agent reads this first
│       ├── glossary-terms.md
│       ├── project-vision.md
│       ├── engineering-cost-discipline.md
│       └── ...
```

- **Lives in git.** Anyone who clones the repo gets the memory.
- **All agents read it.** Bridge files (see § Cross-agent advertisement)
  make sure Cursor / Codex / Claude / Aider / OpenClaw all find this dir.
- **Public.** If the repo is public, the memory is public. Do NOT put
  customer lists, prices paid, personal email, account credentials, or
  anything that should not appear on GitHub here.

### Layer 2 — `~/.shared-memory/<project-slug>/` (PRIVATE, machine-local)

```
~/.shared-memory/
├── acme-app/
│   ├── MEMORY.md
│   ├── personal-preferences.md
│   ├── gh-auth-account.md            ← which github user runs which repo
│   ├── customer-list.md
│   └── feedback-incidents.md
├── another-project/
│   └── ...
```

- **Not in git.** Stays on your machine, follows you only via Dropbox /
  iCloud / Time Machine.
- **All agents read it** — same convention, same index format, just a
  different known path.
- **Private.** Buyer lists, paid amounts, personal email, GitHub account
  trivia, vibe-coding preferences, all go here.

`<project-slug>` = the repo directory's basename, lowercased. For
`~/Dropbox/My Apps/Acme-App` → slug is `acme-app`. Skill
auto-derives via `basename "$PWD" | tr '[:upper:]' '[:lower:]'`.

### Optional — `~/.shared-memory/global/` (PRIVATE, machine-wide)

Same structure and privacy rules as Layer 2, but not tied to one project:
operating preferences and lessons that apply across every repository on
this machine. Read its `MEMORY.md` index at session start; load entries on
demand.

### Layer 3 — `.trellis/shared/` (RUNTIME, per repository, not in git)

```
<git-common-dir>/trellis-shared/       ← one store per repository
├── handoffs/                          ← cross-worktree handoff files
├── knowledge/                         ← append-only runtime discoveries
├── agents/                            ← one append-only log per agent
└── events/                            ← timestamped event stream

<worktree>/.trellis/shared  →  symlink to the store above
```

- **Real-time.** Every worktree of the repository links to the same store,
  so a handoff written in one worktree is visible in its siblings at once,
  without a commit or merge.
- **Not in git.** `.trellis/shared` is gitignored; the store lives inside
  the git common dir and never leaves the machine.
- **Operational, not durable.** Coordination state only. Long-lived
  knowledge still belongs in Layer 1 or Layer 2.

Full specification:
[references/worktree-shared-framework.md](references/worktree-shared-framework.md).

## Memory file format

Every memory file is plain Markdown. Header:

```markdown
---
name: glossary-terms
description: One-line summary used by future agents to decide relevance.
metadata:
  type: reference         # user | feedback | project | reference | engineering
  scope: shared           # shared (Layer 1), private (Layer 2) or global
  created: 2026-05-24
  updated: 2026-05-24
---

# Body

Plain Markdown. Link to other memories with [[their-name]].
```

All `MEMORY.md` indexes follow the same pattern:

```markdown
# Project memory index

Each line points at one memory file. ~150 chars max — agents truncate
after line 200 to bound context cost.

- [Glossary](glossary-terms.md) — one-line hook
- [Vision](project-vision.md) — one-line hook
...
```

`MEMORY.md` has NO frontmatter — it's an index, not a memory.

## Skill operations

### Operation 1 — Locate memory at session start

When the user starts a session OR mentions a project topic that suggests
memory might exist:

```bash
# Project root (or anywhere inside the project tree)
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
SLUG="$(basename "$REPO_ROOT" | tr '[:upper:]' '[:lower:]')"

# Layer 1 (shared, in-repo)
SHARED_DIR="$REPO_ROOT/.agents/memory"

# Layer 2 (private, home)
PRIVATE_DIR="$HOME/.shared-memory/$SLUG"

# Optional machine-wide private layer
GLOBAL_DIR="$HOME/.shared-memory/global"

# Read the indexes (if present)
[ -f "$SHARED_DIR/MEMORY.md" ] && cat "$SHARED_DIR/MEMORY.md"
[ -f "$PRIVATE_DIR/MEMORY.md" ] && cat "$PRIVATE_DIR/MEMORY.md"
[ -f "$GLOBAL_DIR/MEMORY.md" ] && cat "$GLOBAL_DIR/MEMORY.md"

# Layer 3 (runtime), when this worktree is linked
[ -L "$REPO_ROOT/.trellis/shared" ] && ls -1 "$REPO_ROOT/.trellis/shared/handoffs" 2>/dev/null || true
```

Do not load every individual memory file — only the indexes. Pull individual
files on demand when their description matches the current question.

### Operation 2 — Write a new memory

```
Question 1: Is this memory shared, private or global?
  - shared  → goes in <repo>/.agents/memory/, ENTERS GIT
  - private → goes in ~/.shared-memory/<slug>/, STAYS LOCAL
  - global  → goes in ~/.shared-memory/global/, STAYS LOCAL, all projects

Question 2: What type?
  - user        — facts about the person you're collaborating with
  - feedback    — corrections or validated approaches from the user
  - project     — facts about the project goals / state / decisions
  - reference   — pointers to external systems or accounts
  - engineering — cross-cutting code conventions
```

Active coordination state (who is doing what right now, handoffs between
worktrees) is not a memory; write it to Layer 3 instead (Operation 6).

Sensitive-content gate before writing to `shared`:

```text
Block save if the body contains any of:
  - email address (regex: \b\w[\w.+-]*@\w[\w.-]+\.\w+\b)
  - monetary amount with currency ($X, €X, ¥X, CNY)
  - "customer", "buyer", "subscriber" + name
  - GitHub PAT / SSH private key patterns
  - phone number
Re-prompt user: "This looks sensitive — save as PRIVATE instead?"
```

After writing the file, update the matching `MEMORY.md` with one line:
`- [Title](filename.md) — one-line hook`.

### Operation 3 — Cross-agent advertisement

When `.agents/memory/` is first created in a repo, add bridge mentions
so other agents find it automatically:

| Agent | File | Snippet to ensure exists |
|---|---|---|
| Codex / Aider / generic | `AGENTS.md` (root) | Section "## Shared memory" with line pointing at `.agents/memory/MEMORY.md` |
| Claude Code | `CLAUDE.md` (root) — only if used | Same section |
| Cursor | `.cursorrules` | Single line: `Shared memory lives at .agents/memory/MEMORY.md — read it before answering.` |
| OpenClaw | `<PROJECT>.md` or whatever the project uses | Same section |

The skill should grep each bridge file for `.agents/memory/` and add the
section if missing. Idempotent — never duplicate.

### Operation 4 — Migrate from a single-agent store

When invoked with the phrase "migrate memory from Claude Code" or similar:

1. List entries in `~/.claude/projects/<slug>/memory/MEMORY.md`.
2. For each, classify as shared vs private using the sensitive-content gate.
3. Copy to the right layer; update both `MEMORY.md` indexes.
4. Leave the original in place (don't delete) — Claude Code keeps using
   it; other agents now pick up the shared copies via Layer 1/2.

Migration is per-memory, not bulk. Ask the user once per ambiguous file;
batch the clear-cut ones.

### Operation 5 — Enable the runtime layer for worktrees

From inside the repository, run:

```bash
bash skills/shared-memory/templates/link_shared_memory.sh
```

Script contract:

- Resolves the absolute git common dir.
- Creates `trellis-shared/{handoffs,knowledge,agents,events}`.
- On first setup, when the shared handoff directory is empty, copies
  existing branch-local `.trellis/handoffs/` into it and rewrites paths in
  `CURRENT` / `INDEX.md`. The originals are left in place.
- Creates the `.trellis/shared` symlink if missing; a second run is a no-op.
- Fails loudly when `.trellis/shared` exists and is not the expected link.
- Never `rm -rf` user content implicitly.

Also ensure `.gitignore` has:

```gitignore
.trellis/shared
```

The link is per worktree, while the store is shared per repository, so each
new worktree needs the linker once. Installing this skill does not make a
client run it automatically: install the Skill Genie session-start rules
(`rules.example/session-sync.md`) to run the idempotent linker at the start
of every session, before handoffs are read.

### Operation 6 — Write runtime state (Layer 3)

| Kind | Location | Write rule |
|---|---|---|
| Handoffs | `.trellis/shared/handoffs/YYYY-MM-DD-<stream>-<agent>.md` | Mutable only by the owning stream; others add notes in their own files |
| Agent logs | `.trellis/shared/agents/<agent>.jsonl` | One JSON object per line; append-only; only that agent writes |
| Events | `.trellis/shared/events/YYYY/MM/DD.jsonl` | Append-only timestamped entries |
| Runtime knowledge | `.trellis/shared/knowledge/` | Append-only blocks or timestamped files |

Timestamps use ISO 8601 with a timezone offset. Agent IDs are lowercase
kebab-case (`claude-code`, `codex`, `kiro`, `devin`, `custom-agent`).

### Operation 7 — Layer boundaries

Before every write:

1. Long-lived, reusable project knowledge? → Layer 1 or Layer 2 (or global).
2. Active coordination, handoff or runtime state? → Layer 3.
3. Secret or credential? → refuse; see § What stays out of shared memory.

Never mix layers in one file. Do not treat `.trellis/shared/` as a
replacement for committed specs or tasks.

## What stays out of shared memory

Even when "shared" is chosen, refuse to save:

- API keys, tokens, passwords, private keys, .env contents.
- Personally identifying customer data (names + transaction amounts).
- In-flight credentials of any external service.
- Anything the user wraps in `[sensitive] ... [/sensitive]` blocks in
  their prompt.

If the user insists, route to PRIVATE layer instead and warn that
Dropbox / iCloud sync still propagates those files to other devices.

The same list applies to Layer 3. Runtime files are shared operational
context, not secure storage.

## Conflict resolution

If `.agents/memory/<name>.md` exists AND `~/.shared-memory/<slug>/<name>.md`
exists:

- They are DIFFERENT memories with the same slug → rename one.
- They are the SAME content drift → shared layer wins; update private
  to match (and re-classify if the content drifted into sensitive
  territory).

Never silently merge.

## Anti-patterns

- ❌ Writing to ONLY a tool-specific store (e.g. only Claude Code's
  `~/.claude/projects/...`) when the memory is shareable.
- ❌ Putting personal preferences in `.agents/memory/` — they pollute
  git history and travel with every repo clone forever.
- ❌ Letting bridge files diverge — if `AGENTS.md` says memory lives at
  one path and `.cursorrules` says another, agents desync.
- ❌ Generating placeholder index entries with descriptions like "this
  file" or "see body" — descriptions must contain enough keywords for
  future agents to know when to load.
- ❌ Writing handoffs only under branch-local `.trellis/handoffs/` when the
  runtime layer is enabled — sibling worktrees will not see them.
- ❌ Overwriting another agent's runtime file instead of appending or
  writing to your own per-agent file.

## Implementation hints

- `git rev-parse --show-toplevel` is the safest project-root resolver;
  fall back to `pwd` when not in a git repo.
- The skill's own files should never be written into `.agents/memory/`
  — meta-recursion bad.
- `mkdir -p` both layers on first write; don't fail if either is missing.
- Resolve the runtime store with `git rev-parse --git-common-dir`, not
  `--git-dir`: the latter differs per worktree.

## Cross-references

- Claude-Code-specific memory (legacy): `~/.claude/projects/<slug>/memory/`
- Sessions handoff convention: `.trellis/handoffs/`, or
  `.trellis/shared/handoffs/` when the runtime layer is enabled (orthogonal
  to Layers 1 and 2 — handoffs are conversation summaries, not memories)
- `session-handoff` writes handoff artifacts; `handoff-receiver` resumes from
  the active handoff. Both prefer `.trellis/shared/handoffs/` when present.
- ADR template / context docs / glossaries — repo docs that ARE shared
  memory in spirit, just unstructured. The skill respects them; it
  doesn't duplicate.
