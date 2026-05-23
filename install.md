# Skill Genie Install Guide

Skill Genie sets up your AI coding agent environment: skills, global rules, and project templates — in one command.

## Copy This Prompt

```text
I want you to set up my AI agent environment with Skill Genie (skills, rules, and templates).
Read the official install guide here: https://raw.githubusercontent.com/Fei2-Labs/skill-genie/main/install.md
Use only the section for your current client.
Before cloning repos or writing config files, summarize the exact commands you plan to run and ask me to confirm.
```

## Safety Rule For Agents

Use this page as documentation only. Before cloning repos, writing config files, or running install commands, summarize the exact files and commands you plan to use and ask the user to confirm.

## Requirements

- git
- python3 (with pyyaml: `pip3 install pyyaml`)
- bash

## Install

```bash
git clone https://github.com/Fei2-Labs/skill-genie.git ~/skill-genie
cd ~/skill-genie
./setup.sh
```

This will:
1. Detect which agents are installed on your machine
2. Install global rules only for detected agents
3. Sync skills from `skills.yaml` into detected agent paths
4. Detect optional tools (e.g. trellis) and link their skills
5. Link the `skillgenie` CLI to your PATH

## Modes

| Command | Behavior |
|---------|----------|
| `./setup.sh` | Symlink mode (default): fast, edits sync instantly |
| `./setup.sh --copy` | Copy mode: copies files, no dependency on source paths |
| `./setup.sh --full` | Clean slate + symlink |
| `./setup.sh --full --copy` | Clean slate + copy |

## Agent-Specific Setup

`setup.sh` auto-detects installed agents. Only detected agents get configured:

### Claude Code

Detected if `claude` is in PATH or `~/.claude/` exists. Rules written to `~/.claude/CLAUDE.md`, skills to `~/.claude/skills/`.

### Kiro

Detected if `kiro` is in PATH or `~/.kiro/` exists. Rules symlinked to `~/.kiro/steering/`, skills to `~/.agents/skills/`.

### Codex

Detected if `codex` is in PATH or `~/.config/codex/` exists. Rules written to `~/.config/codex/instructions.md`, skills to `~/.codex/skills/`.

### Gemini Antigravity

Detected if `antigravity` is in PATH. Skills to `~/.gemini/antigravity/skills/`.

### Cursor

Detected if `cursor` is in PATH. Skills to `~/.cursor/skills/`.

### Other Agents

Skills are also available at `~/.agents/skills/<name>/SKILL.md`. Any agent that can read files can use them directly:
```bash
cat ~/.agents/skills/<name>/SKILL.md
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

## Verify

```bash
skillgenie list              # List all available skills
skillgenie read <name>       # Print a skill's content
skillgenie status            # Show install status per runtime
```

## Uninstall

```bash
rm -rf ~/skill-genie ~/.agents/skills ~/.cache/skill-genie-remotes
# Remove symlinks:
rm -f ~/.kiro/steering/router.md ~/.kiro/steering/session-sync.md \
      ~/.kiro/steering/workflow-tools.md ~/.kiro/steering/stack-and-deployment.md \
      ~/.kiro/steering/external-tools.md
rm -f ~/.claude/CLAUDE.md
rm -f ~/.config/codex/instructions.md
```
