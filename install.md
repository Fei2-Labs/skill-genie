# Skill Genie Install Guide

Skill Genie sets up your AI coding agent environment: skills and global rules — in one command.

## Copy This Prompt

```text
I want you to set up my AI agent environment with Skill Genie (skills and rules).
Read the official install guide here: https://raw.githubusercontent.com/Fei2-Labs/skill-genie/main/install.md
Use only the section for your current client.
Before cloning repos or writing config files, summarize the exact commands you plan to run and ask me to confirm.
```

## Safety Rule For Agents

Use this page as documentation only. Before cloning repos, writing config files, or running install commands, summarize the exact files and commands you plan to use and ask the user to confirm.

## Requirements

- git
- python3 (with pyyaml: `pip3 install pyyaml`)
- bash (or Git Bash on Windows)

### Windows Prerequisites

> **For AI agents on Windows**: Before proceeding, check if the required tools are available. If any are missing, guide the user through installation:

| Tool | Check | Install |
|------|-------|---------|
| git | `git --version` | Download from https://git-scm.com/download/win (includes Git Bash) |
| python3 | `python --version` or `python3 --version` | Download from https://www.python.org/downloads/ or run `winget install Python.Python.3` |
| bash | `bash --version` | Included with Git for Windows; alternatively use WSL (`wsl --install`) |
| pyyaml | `python -m pip show pyyaml` | `pip install pyyaml` |

On Windows, run all setup commands inside **Git Bash** (installed with Git for Windows) or **WSL**. PowerShell and CMD are not supported.

## Install

```bash
git clone https://github.com/Fei2-Labs/skill-genie.git ~/skill-genie
cd ~/skill-genie
./setup.sh
```

This will:
1. Detect which agents are installed on your machine
2. Install global rules only for detected agents
3. Sync agents from `agents/` into the shared registry and detected agent paths
4. Sync skills from `skills.yaml` into detected agent paths
5. Detect optional tools (e.g. trellis) and link their skills
6. Link the `skillgenie` CLI to your PATH

## Modes

| Command | Behavior |
|---------|----------|
| `./setup.sh` | Full setup: rules + skills (symlink, default) |
| `./setup.sh --copy` | Full setup: rules + skills (copy files) |
| `./setup.sh --rules-only` | Only update rules |
| `./setup.sh --skills-only` | Only update skills |
| `./setup.sh --agents` | Interactive agent picker |
| `./setup.sh --agents all` | Install all agents |
| `./setup.sh --agents-only` | Only update agents |
| `./setup.sh --full` | Clean slate + symlink |
| `./setup.sh --full --copy` | Clean slate + copy |

## Agent-Specific Setup

`setup.sh` auto-detects installed agents. Only detected agents get configured:

### Claude Code

Detected if `claude` is in PATH or `~/.claude/` exists. Rules written to `~/.claude/CLAUDE.md`, skills to `~/.claude/skills/`.

Custom agents from `agents/` are linked to `~/.claude/agents/` when present.

### OpenClaw

Detected if `openclaw` is in PATH or `~/.openclaw/` exists. Skills to `~/.openclaw/skills/` and the shared `~/.agents/skills/` root.

### Hermes

Detected if `hermes` is in PATH or `~/.hermes/` exists. Skills to `~/.hermes/skills/` and the shared `~/.agents/skills/` root.

### Kiro

Detected if `kiro` is in PATH or `~/.kiro/` exists. Rules symlinked to `~/.kiro/steering/`, skills to `~/.kiro/skills/` and `~/.agents/skills/`.

Custom agents from `agents/` are linked to `~/.kiro/agents/` when present.

### Codex

Detected if `codex` is in PATH or `~/.codex/` exists. Rules written to `~/.codex/AGENTS.md`, skills to `~/.codex/skills/`.

Custom agents from `agents/` are linked to `~/.codex/agents/` when present.

### OpenCode

Detected if `opencode` is in PATH or `~/.config/opencode/` exists. Skills to `~/.config/opencode/skills/` and the shared `~/.agents/skills/` root.

### Devin (CLI + Desktop)

Detected if `devin` is in PATH or `~/.config/devin/` exists. Skills to `~/.config/devin/skills/`; Devin also detects repo-local `.agents/skills/` files.

### Gemini Antigravity

Detected if `antigravity` is in PATH. Skills to `~/.gemini/antigravity/skills/`.

### Cursor

Detected if `cursor` is in PATH. Skills to `~/.cursor/skills/`.

Custom agents from `agents/` are linked to `~/.cursor/agents/` when present.

### Other Agents

Skills are also available at `~/.agents/skills/<name>/SKILL.md`. Any agent that can read files can use them directly:
```bash
cat ~/.agents/skills/<name>/SKILL.md
```

Agents are also available at `~/.agents/agents/<name>.md`. Any agent that can read files can use them directly:
```bash
cat ~/.agents/agents/<name>.md
```

## Customization

Edit `skills.yaml` to add or remove third-party skill sources:

```yaml
remote:
  - repo: owner/repo-name
    path: path/to/skills    # base path inside the repo
    pick:
      - skill-folder-name   # relative to path
```

Then re-run `./setup.sh` to sync.

Edit files under `agents/` to add or remove custom agent definitions. Then re-run `./setup.sh --agents` or `./setup.sh --agents-only` to sync them.

## Verify

```bash
skillgenie list              # List all available skills
skillgenie read <name>       # Print a skill's content
skillgenie validate          # Check AgentSkills/OpenClaw/Hermes compatibility
skillgenie status            # Show install status per runtime
```

## Uninstall

```bash
rm -rf ~/skill-genie ~/.agents/skills ~/.agents/agents ~/.cache/skill-genie-remotes
# Remove symlinks:
rm -f ~/.kiro/steering/router.md ~/.kiro/steering/session-sync.md \
      ~/.kiro/steering/workflow-tools.md ~/.kiro/steering/stack-and-deployment.md \
      ~/.kiro/steering/external-tools.md
rm -f ~/.claude/CLAUDE.md
rm -rf ~/.claude/agents ~/.codex/agents ~/.kiro/agents ~/.copilot/agents
rm -f ~/.config/codex/instructions.md
```
