# IDE Global Rules

This file is the router. Read the relevant topic note before changing behavior in that area.

## Universal rules
- Read `AGENTS.md` first.
- Never push unless the user explicitly asks.
- If an `upstream` remote exists, fetch and report new commits at session start, then wait for approval before merging.
- Prefer CLI tools over MCP when both can do the job.
- Ask one minimal clarifying question before architecture, data model, permissions, flow, or irreversible changes.
- Keep replies concise; do not create docs, changelogs, or summaries unless the user asks.

## Topic notes
- Session and sync: `IDE Global Rules - session-sync.md`
- Workflow and tools: `IDE Global Rules - workflow-tools.md`
- Stack and deployment: `IDE Global Rules - stack-and-deployment.md`
- External tools and skills: `IDE Global Rules - external-tools.md`