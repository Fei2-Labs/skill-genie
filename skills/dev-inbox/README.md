# dev-inbox

Universal task triage and routing for AI agent sessions.

## What it does

`dev-inbox` triages anything that comes up during a session — bugs, features, improvements, fleeting ideas — and routes it to the right place so it is never lost and always discoverable by future sessions.

Works in any context: software development, writing, design, or any task.

## When to use

- A message contains multiple requests that need to be separated before work starts
- You notice something unrelated to the current task (a bug, idea, or improvement)
- User says "记一下", "log this", "open an issue", "以后再说", "track this"
- A resumed or compacted session mentions a requested item that was never recorded

## How it works

1. **Atomize** — split multi-topic messages into active, blocking, and unrelated/deferred items
2. **Classify** — assign type (`fix` / `add` / `improve` / `idea`) and priority (`high` / `normal` / `low`)
3. **Route** — automatically pick the best destination (GitHub Issue / agent memory / TODO.md)
4. **Recover** — after resume or compaction, persist requested-but-unrecorded items before continuing
5. **Ensure discoverability** — every record includes how a future session will find it

## Key features

- Proactive: agent intervenes when it detects off-task items
- Explicit requests: records after deduplication without asking for confirmation again
- Proactive inference: proposes title, type, and priority for one-word confirmation
- Merge logic: checks for existing related records before creating duplicates
- Environment-adaptive: works with or without GitHub, with or without agent memory

---

**Source**: [github.com/Fei2-Labs/skill-genie](https://github.com/Fei2-Labs/skill-genie)
**Author**: [@clarezoe](https://x.com/clarezoe)
