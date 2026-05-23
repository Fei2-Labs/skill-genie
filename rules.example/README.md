# Rules

This directory contains example agent rule files. Copy to `rules/` and customize:

```bash
cp -r rules.example/ rules/
```

## File structure

| File | Purpose |
|------|---------|
| `router.md` | Minimal top-level rules (always loaded) |
| `session-sync.md` | Session start, git sync, handoff behavior |
| `workflow-tools.md` | Tool preferences, debugging, verification |
| `stack-and-deployment.md` | Tech stack, deployment, project structure |
| `external-tools.md` | Third-party tools, skills discovery |

## How they're loaded

- **Kiro**: Each file is symlinked individually to `~/.kiro/steering/`
- **Claude Code / Codex**: All files are concatenated into a single rules file

## Tips

- Keep each file focused on one topic
- Rules should be universal (not project-specific) — project rules belong in AGENTS.md
- Total size across all files ideally under 4KB to minimize context usage
