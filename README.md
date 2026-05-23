# 🧞 Skill Genie

Your AI agent environment, in one repo. Skills, rules, and a single command to set it all up.

## Why

Every AI coding agent (Claude Code, Codex, Kiro, Cursor, Gemini) has its own config location, its own skills format, its own way of loading rules. You end up with scattered configs across machines that drift apart.

Skill Genie fixes this:
- **One repo** — all your skills and rules version-controlled together
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

| What | Where | Condition |
|------|-------|-----------|
| Agent rules | Agent-specific config dirs | Only for detected agents |
| Skills | `~/.agents/skills/` + native agent paths | Only for detected agents |
| CLI tool | `skillgenie` in PATH | Always |

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
rules.example/      Example agent rules (copy to rules/ and customize)
skills.yaml.example Third-party skill sources (copy to skills.yaml to customize)
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

Rules and skills are only installed for agents detected on your machine.

| Agent | Detection | Rules | Skills |
|-------|-----------|-------|--------|
| Kiro | `kiro` in PATH or `~/.kiro/` exists | `~/.kiro/steering/*.md` | `~/.agents/skills/` |
| Claude Code | `claude` in PATH or `~/.claude/` exists | `~/.claude/CLAUDE.md` | `~/.claude/skills/` |
| Codex | `codex` in PATH or `~/.config/codex/` exists | `~/.config/codex/instructions.md` | `~/.codex/skills/` |
| Gemini Antigravity | `antigravity` in PATH | — | `~/.gemini/antigravity/skills/` |
| Cursor | `cursor` in PATH | — | `~/.cursor/skills/` |
| GitHub Copilot | `gh` in PATH + `~/.github/` exists | — | `~/.github/skills/` |

## Agent-Driven Install

Tell your agent:

```
Read https://raw.githubusercontent.com/Fei2-Labs/skill-genie/main/install.md and follow the instructions.
```

## License

MIT © Feifei Kosonen

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Fei2-Labs/skill-genie&type=Date)](https://star-history.com/#Fei2-Labs/skill-genie&Date)
