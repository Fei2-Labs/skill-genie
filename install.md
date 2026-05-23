# Skill Genie Install Guide

Skill Genie gives coding agents access to a curated set of AI skills, global rules, and project templates through a single setup command.

## Copy This Prompt

```text
I want you to install Skill Genie for managing AI agent skills.
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
1. Symlink global rules to your agent's config directory
2. Sync skills from `skills.yaml` into `~/.agent/skills/`
3. Link the `skillgenie` CLI to your PATH

## Modes

| Command | Behavior |
|---------|----------|
| `./setup.sh` | Safe — adds/updates without removing existing skills |
| `./setup.sh --full` | Full rebuild — clears `~/.agent/skills/` first |

## Agent-Specific Setup

### Claude Code

After running `setup.sh`, rules are at `~/.claude/CLAUDE.md`. Skills are available via `skillgenie list` and `skillgenie read <name>`.

### Kiro

After running `setup.sh`, rules are symlinked as individual files in `~/.kiro/steering/`. Skills are available via `skillgenie list` and `skillgenie read <name>`.

### Codex

After running `setup.sh`, rules are at `~/.config/codex/instructions.md`. Skills are available via `skillgenie list` and `skillgenie read <name>`.

### Other Agents

Skills are in `~/.agent/skills/<name>/SKILL.md`. Any agent that can read files can use them directly:
```bash
cat ~/.agent/skills/<name>/SKILL.md
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
rm -rf ~/skill-genie ~/.agent/skills ~/.cache/skill-genie-remotes
# Remove symlinks:
rm -f ~/.kiro/steering/router.md ~/.kiro/steering/session-sync.md \
      ~/.kiro/steering/workflow-tools.md ~/.kiro/steering/stack-and-deployment.md \
      ~/.kiro/steering/external-tools.md
rm -f ~/.claude/CLAUDE.md
rm -f ~/.config/codex/instructions.md
```
