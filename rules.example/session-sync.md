# Session and sync

Rules for how sessions start: reading project files, checking git upstream, handling handoffs.

- At the start of every session, read the machine-wide private memory index when
  it exists:
  ```bash
  [ -f ~/.shared-memory/global/MEMORY.md ] && cat ~/.shared-memory/global/MEMORY.md
  ```
  Load an individual global memory only when its index description is relevant
  to the task.
- At the start of every session in a git repository, enable real-time worktree
  memory when the shared-memory skill is installed:
  ```bash
  if [ -x ~/.agents/skills/shared-memory/templates/link_shared_memory.sh ]; then
    ~/.agents/skills/shared-memory/templates/link_shared_memory.sh
  fi
  ```
  Then read `.trellis/shared/handoffs/CURRENT` and the matching `INDEX.md` when
  they exist before looking for branch-local handoffs. This setup is idempotent:
  sibling worktrees resolve to the same git-common-dir runtime store.
- After fixing a bug or when the user points out a mistake, write a concise lesson-learned memory: what went wrong, root cause, and how to avoid it. Before writing, search existing memories for related content. If a conflict or overlap is found, show both the existing memory and the proposed update to the user and ask which to keep, merge, or replace.

<!-- Generate with: skillgenie read init-rules -->
