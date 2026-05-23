# 🧞 Skill Genie

Your AI agent environment, in one repo. Skills, rules, templates, and a single command to set it all up.

## Why

Every AI coding agent (Claude Code, Codex, Kiro, Cursor, Gemini) has its own config location, its own skills format, its own way of loading rules. You end up with scattered configs across machines that drift apart.

Skill Genie fixes this:
- **One repo** — all your skills, rules, and templates version-controlled together
- **One command** — `./setup.sh` distributes everything to the right places
- **Every agent** — native path support for Codex, Claude Code, Gemini Antigravity, Cursor, and GitHub Copilot

## Quick Start

```bash
git clone https://github.com/Fei2-Labs/skill-genie.git ~/skill-genie
cd ~/skill-genie
./setup.sh
```

That's it. Your agent environment is ready.

## What Gets Installed

| What | Where |
|------|-------|
| Agent rules | `~/.kiro/steering/`, `~/.claude/CLAUDE.md`, `~/.config/codex/instructions.md` |
| Skills | `~/.agents/skills/` + native paths (`~/.codex/skills/`, `~/.claude/skills/`, etc.) |
| CLI tool | `skillgenie` in your PATH |

## Modes

```bash
./setup.sh              # Symlink mode (default): fast, edits sync instantly
./setup.sh --copy       # Copy mode: copies files, no dependency on source paths
./setup.sh --full       # Clean slate + symlink
./setup.sh --full --copy # Clean slate + copy
```

## Structure

```
skills/             Reusable AI agent skills (each with SKILL.md)
rules/              Global agent behavior rules (split by topic)
templates/          Project AGENTS.md starters for different stacks
skills.yaml.example Third-party skill sources template (copy to skills.yaml to customize)
skillgenie          CLI tool for listing and reading skills
setup.sh            One-command environment setup
```

## skillgenie CLI

```bash
skillgenie list            # List all skills in this repo
skillgenie read <name>     # Print a skill's full instructions
skillgenie status          # Show install status per runtime
skillgenie install <name>  # Install a specific skill
skillgenie install --all   # Install all skills
```

## Customization

On first run, `setup.sh` creates `skills.yaml` from `skills.yaml.example`. Edit your local `skills.yaml` to add or remove third-party sources:

```yaml
remote:
  - repo: owner/repo-name
    path: path/to/skills
    pick:
      - skill-folder-name
```

Your `skills.yaml` is gitignored — it won't be overwritten by updates.

## Agent Compatibility

| Agent | Rules | Skills |
|-------|-------|--------|
| Kiro | `~/.kiro/steering/*.md` (individual files) | `~/.agents/skills/` |
| Claude Code | `~/.claude/CLAUDE.md` (concatenated) | `~/.claude/skills/` |
| Codex | `~/.config/codex/instructions.md` (concatenated) | `~/.codex/skills/` |
| Gemini Antigravity | — | `~/.gemini/antigravity/skills/` |
| Cursor | — | `~/.cursor/skills/` |
| GitHub Copilot | — | `~/.github/skills/` |

## Agent-Driven Install

Tell your agent:

```
Read https://raw.githubusercontent.com/Fei2-Labs/skill-genie/main/install.md and follow the instructions.
```

## License

MIT © Feifei Kosonen

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Fei2-Labs/skill-genie&type=Date)](https://star-history.com/#Fei2-Labs/skill-genie&Date)
