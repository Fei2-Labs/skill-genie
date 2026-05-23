# Session and sync

- Read `AGENTS.md` first.
- If an `upstream` remote exists, run `git fetch upstream` at session start and report any new commits with `git log HEAD..upstream/main --oneline`.
- If upstream has changes, stop after reporting them and wait for approval before merging.
- Never push unless the user explicitly asks.
- When important state is accumulating, capture a compact session memory note with the current state, constraints, and next step.
- If architecture, data model, permissions, flows, or an irreversible operation is unclear, ask one minimal question and do not modify files until clarified.
- For handoffs, use the session-handoff skill; use the compact handoff only when the user explicitly asks for it.