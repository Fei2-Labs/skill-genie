# Issue: orphan / parallel handoffs are invisible once `CURRENT` is set

Resolved on 2026-05-22 in local skill copies under:

- `handoff/SKILL.md`
- `session-handoff/SKILL.md`
- `handoff-receiver/SKILL.md`

Resolution summary:

- added `status: open` at handoff creation time
- introduced `CURRENT` plus `INDEX.md` as the default routing model
- changed prior active streams from implicit replacement to explicit `paused`
- limited `handoff-receiver` to `CURRENT + INDEX.md` in the common path
- reserved extra file reads for rows already marked `orphan` or index drift

The original issue text was resolved and archived here to preserve context
without leaving it in the active skill directory.
