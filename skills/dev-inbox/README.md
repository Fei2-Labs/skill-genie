# dev-inbox

Universal task triage and routing for AI agent sessions.

## What it does

`dev-inbox` triages anything that comes up during a session — bugs, features, improvements, fleeting ideas — and routes it to the right place so it is never lost and always discoverable by future sessions.

Works in any context: software development, writing, design, or any task.

## When to use

- You notice something unrelated to the current task (a bug, idea, or improvement)
- User says "记一下", "log this", "open an issue", "以后再说", "track this"

## How it works

1. **Classify** — assign type (`fix` / `add` / `improve` / `idea`) and priority (`high` / `normal` / `low`)
2. **Route** — automatically pick the best destination (GitHub Issue / agent memory / TODO.md)
3. **Ensure discoverability** — every record includes how a future session will find it

## Key features

- Proactive: agent intervenes when it detects off-task items
- Concrete suggestions: proposes title, type, priority — user confirms with one word
- Merge logic: checks for existing related records before creating duplicates
- Environment-adaptive: works with or without GitHub, with or without agent memory

---

**Source**: [github.com/Fei2-Labs/skill-genie](https://github.com/Fei2-Labs/skill-genie)
**Author**: [@clarezoe](https://x.com/clarezoe)
