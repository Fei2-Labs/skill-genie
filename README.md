# 🧞 Skill Genie

> ⚠️ **WARNING**: This setup modifies agent configuration files on your system (`~/.claude/`, `~/.codex/`, `~/.kiro/`, `~/.agents/`, etc.). **Back up your existing configs before running `setup.sh`.** This is a personal configuration repo — provided as-is with no warranty. The author is not responsible for any data loss, broken configs, or unintended side effects. Use at your own risk.

Your AI agent environment, in one repo. Skills, rules, agents, and a single command to set it all up.

## Why

Every AI coding agent (Claude Code, Codex, Kiro, Cursor, Gemini) has its own config location, its own skills format, its own way of loading rules. You end up with scattered configs across machines that drift apart.

Skill Genie fixes this:
- **One repo** — all your skills, rules, and agents version-controlled together
- **One command** — `./setup.sh` distributes everything to the right places
- **Every agent** — native path support for OpenClaw, Hermes, Devin, OpenCode, Kiro, Codex, Claude Code, Gemini Antigravity, Cursor, Windsurf, GitHub Copilot, and GitHub Copilot CLI/app

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
| Custom agents | `~/.agents/agents/` + native agent paths | Only for selected agents |
| Skills | `~/.agents/skills/` + native agent paths | Only for detected agents |
| CLI tool | `skillgenie` in PATH | Always |

## Modes

```bash
./setup.sh                # Full setup: rules + skills (symlink)
./setup.sh --copy         # Full setup: rules + skills (copy files)
./setup.sh --rules-only   # Only update rules
./setup.sh --skills-only  # Only update skills
./setup.sh --agents       # Pick agents to install
./setup.sh --agents all   # Install all agents
./setup.sh --agents-only  # Only update agents
./setup.sh --full         # Clean slate + symlink
./setup.sh --full --copy  # Clean slate + copy
```

## Structure

```
skills/             Reusable AI agent skills (each with SKILL.md)
rules.example/      Example agent rules (copy to rules/ and customize)
agents/             Agent definitions (copy to ~/.agents/agents/ and native paths)
skills.yaml.example Third-party skill sources (copy to skills.yaml to customize)
skillgenie          CLI tool for listing and reading skills
setup.sh            One-command environment setup
```

## skillgenie CLI

```bash
skillgenie list            # List all skills in this repo
skillgenie read <name>     # Print a skill's full instructions
skillgenie validate        # Check AgentSkills/OpenClaw/Hermes compatibility
skillgenie status          # Show install status per runtime
skillgenie install <name>  # Install a specific skill (local ./skills/)
skillgenie install --all   # Install all local skills
skillgenie update <name>   # Re-install a skill after editing it
skillgenie sync            # Pull all remote repos in skills.yaml -> ~/.agents/skills/
skillgenie sync --global   # Also link synced skills into every native runtime dir
skillgenie sync --clean    # Wipe cache and re-clone every remote repo
```

## Customization

On first run, `setup.sh` creates `skills.yaml` from `skills.yaml.example`. Edit your local `skills.yaml` to add or remove third-party sources:

```yaml
remote:
  # Remote repo — cloned to ~/.local/share/skill-genie-remotes/, pulled on subsequent syncs
  - repo: owner/repo-name
    path: path/to/skills
    pick:
      - skill-folder-name

  # Local checkout — use an existing repo directly (no clone, no duplicate copy)
  - local: /Users/you/Projects/some-repo
    path: .claude/skills
    pick:
      - some-skill
```

Your `skills.yaml` is gitignored — it won't be overwritten by updates.

Custom agents live in `agents/`. Run `./setup.sh --agents` to pick which ones to install, `./setup.sh --agents all` to install all of them, or `./setup.sh --agents-only` to refresh just agents.

To generate personalized agent rules, tell your agent:
```
skillgenie read init-rules
```

## Agent Compatibility

Rules and skills are only installed for agents detected on your machine. Rules are symlinked — edit once, all agents see the change immediately.

| Agent | Detection | Rules | Skills |
|-------|-----------|-------|--------|
| Kiro | `kiro` in PATH or `~/.kiro/` exists | `~/.kiro/steering/*.md` (all topic files) | `~/.kiro/skills/` + `~/.agents/skills/` |
| OpenClaw | `openclaw` in PATH or `~/.openclaw/` exists | Reads linked/global rules on demand | `~/.openclaw/skills/` + `~/.agents/skills/` |
| Hermes | `hermes` in PATH or `~/.hermes/` exists | Reads linked/global rules on demand | `~/.hermes/skills/` + `~/.agents/skills/` |
| OpenCode | `opencode` in PATH or `~/.config/opencode/` exists | Reads project/global rules on demand | `~/.config/opencode/skills/` + `~/.agents/skills/` |
| Devin (CLI + Desktop) | `devin` in PATH, or `~/.config/devin/`, `~/.devin/`, `~/.devin-next/` exists | Reads project/global rules on demand | `~/.config/devin/skills/` + `~/.agents/skills/` |
| Claude Code | `claude` in PATH or `~/.claude/` exists | `~/.claude/CLAUDE.md` → `router.md` | `~/.claude/skills/` |
| Codex | `codex` in PATH or `~/.codex/` exists | `~/.codex/AGENTS.md` → `router.md` | `~/.codex/skills/` |
| Windsurf _(legacy)_ | `~/.codeium/windsurf/` exists | `~/.codeium/windsurf/memories/global_rules.md` → `router.md` | `~/.codeium/windsurf/skills/` |
| Windsurf Next _(legacy)_ | `~/.codeium/windsurf-next/` exists | `~/.codeium/windsurf-next/memories/global_rules.md` → `router.md` | `~/.codeium/windsurf-next/skills/` |
| Gemini Antigravity | `antigravity` in PATH | — | `~/.gemini/antigravity/skills/` |
| Cursor | `cursor` in PATH | — | `~/.cursor/skills/` |
| GitHub Copilot | `gh` in PATH + `~/.github/` exists | — | `~/.github/skills/` |
| GitHub Copilot CLI/app | `copilot` in PATH or `~/.copilot/` exists | `~/.copilot/copilot-instructions.md` / `AGENTS.md` | `~/.copilot/skills/` + `~/.agents/skills/` |

> **Windsurf → Devin Desktop:** the Windsurf editor was rebranded to Devin Desktop (Cognition, June 2026). Devin Desktop and the Devin CLI both load global skills from `~/.config/devin/skills/` — covered by the **Devin** target. The legacy `~/.codeium/windsurf*` paths are kept for installs still on the old brand during the transition.

## Skill Compatibility

Skills in `skills/` follow the AgentSkills `SKILL.md` shape used by Claude Code, OpenClaw, Hermes, OpenCode, Kiro, Devin, Codex, Cursor, Windsurf, and other local skill-aware agents:

- Every skill directory has a root `SKILL.md`.
- Frontmatter includes single-line `name`, `description`, and `license` fields.
- `metadata` is a single-line JSON object so OpenClaw's embedded parser can read it, including `metadata.version`.
- Tags are stored in `metadata.tags` and mirrored to `metadata.hermes.tags`.
- `allowed-tools`, when present, is a single-line comma-separated value for Claude Code compatibility.
- Skill names must match their directory and use lowercase letters, digits, and single hyphens.
- Descriptions must stay at or below 1024 characters for OpenCode and Kiro compatibility.

Run `skillgenie validate` before committing skill changes.

Topic rule files (session-sync, workflow-tools, etc.) are installed to `~/.agents/rules/` and loaded on demand via `cat` when the agent needs them. This keeps context small.

## Tab Completion (zsh)

`setup.sh` installs zsh completions automatically. If tab completion doesn't work, add to `~/.zshrc`:

```bash
fpath=(~/.zsh/completions $fpath)
autoload -Uz compinit && compinit
```

Then restart your terminal. Supports: `skillgenie <tab>` for commands, `skillgenie read <tab>` for skill names.

## Agent-Driven Install

> **For AI agents**: If you are an AI assistant reading this README, fetch and follow [`install.md`](https://raw.githubusercontent.com/Fei2-Labs/skill-genie/main/install.md) directly — it contains step-by-step instructions written for you.

For humans — paste this into your agent's chat:

```
Read https://raw.githubusercontent.com/Fei2-Labs/skill-genie/main/install.md and follow the instructions.
```

## License

MIT © Feifei Kosonen

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Fei2-Labs/skill-genie&type=Date)](https://star-history.com/#Fei2-Labs/skill-genie&Date)
