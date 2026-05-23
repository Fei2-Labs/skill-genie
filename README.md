# Skill Genie

AI agent environment in one repo: skills, global rules, project templates, and a setup script.

## Quick start

```bash
git clone https://github.com/Fei2-Labs/skill-genie.git ~/skill-genie
~/skill-genie/setup.sh
```

## Modes

| Command | Behavior |
|---------|----------|
| `./setup.sh` | Safe — adds/updates skills without removing existing ones |
| `./setup.sh --full` | Full rebuild — clears `~/.agents/skills/` and reinstalls from manifest only |

> If you already have skills in `~/.agents/skills/`, the default mode won't touch them. Use `--full` for a clean slate.

## Structure

```
skills/             → Reusable AI agent skills (each with SKILL.md)
rules/              → Global agent behavior rules (split by topic)
templates/          → Project AGENTS.md templates
skills.yaml         → Third-party skill sources (editable config)
skillgenie          → CLI: list, read, install, status
setup.sh            → One-command environment setup
```

## Agent compatibility

| Agent | How rules are loaded |
|-------|---------------------|
| Kiro | Symlinks individual files to `~/.kiro/steering/` |
| Claude Code | Concatenates into `~/.claude/CLAUDE.md` |
| Codex | Concatenates into `~/.config/codex/instructions.md` |

## skillgenie CLI

```bash
skillgenie list              # List available skills
skillgenie read <name>       # Print a skill's SKILL.md
skillgenie install <name>    # Install to detected runtimes
skillgenie install --all     # Install all skills
skillgenie status            # Show install status per runtime
```

## What's included

- **Skills** — Reusable task instructions for AI agents (local + third-party)
- **Rules** — Global behavior configuration for Kiro, Claude Code, Codex
- **Templates** — Project-level AGENTS.md starters for different tech stacks
- **CLI** — `skillgenie` for discovering and reading skills

## Skills sources

1. **Local** — Skills in this repo (dirs with `SKILL.md`)
2. **Remote** — Third-party repos declared in `skills.yaml`
3. **Bundled** — Registry-installed skills (not managed here)

## License

MIT © Feifei Kosonen
