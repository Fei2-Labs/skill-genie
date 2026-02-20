# close-loop

End-of-session workflow for shipping work cleanly and retaining high-value memory.

## What it does

- Runs a 4-phase wrap-up: Ship State, Consolidate Memory, Review & Apply, Publish Queue.
- Uses typed memory buckets: working, episodic, semantic, procedural.
- Applies a persistence filter to reduce noisy memory writes.
- Enforces safety gates for push, deploy, and publish actions.

## Use this skill when

- You want to end a coding session with clean repo state.
- You want structured memory updates instead of ad-hoc notes.
- You want repeatable self-improvement and publication triage.

## Files

- `SKILL.md` - Main instructions and execution contract.
- `references/memory-frameworks.md` - Framework references and update checklist.
- `assets/templates/wrap-report-template.md` - Output template for session wrap reports.

## Quick usage

Trigger phrases:

- `wrap up`
- `close session`
- `end session`
- `/wrap-up`

Execution order:

1. Ship State
2. Consolidate Memory
3. Review and Apply Improvements
4. Publish Queue

## Design goals

- High signal memory only
- Deterministic end-of-session behavior
- Minimal irreversible actions without approval
- Clear output contract with evidence and confidence labels
