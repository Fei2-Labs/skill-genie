#!/bin/bash
set -euo pipefail

DOTFILES_DIR="$(cd "$(dirname "$0")" && pwd)"
RULES_DIR="$DOTFILES_DIR/rules"
SKILLS_DEST="$HOME/.agents/skills"
KIRO_DIR="$HOME/.kiro/steering"
CLAUDE_FILE="$HOME/.claude/CLAUDE.md"
CODEX_FILE="$HOME/.codex/AGENTS.md"
SKILLGENIE_BIN_PATH=""

FULL=false
COPY_MODE=false
RULES_ONLY=false
SKILLS_ONLY=false

for arg in "$@"; do
  case "$arg" in
    --full) FULL=true ;;
    --copy) COPY_MODE=true ;;
    --rules-only) RULES_ONLY=true ;;
    --skills-only) SKILLS_ONLY=true ;;
  esac
done

if $FULL; then
  echo "⚠ Full mode: ~/.agents/skills/ will be cleared and rebuilt."
  read -p "Continue? [y/N] " confirm
  [[ "$confirm" =~ ^[Yy]$ ]] || exit 0
fi

if $COPY_MODE; then
  echo "ℹ Copy mode: skills will be copied (not symlinked)"
fi

# ── 0. Backup existing configs (first run only) ──────────────────────────────
BACKUP_DIR="$HOME/.skill-genie-backup"
if [[ ! -d "$BACKUP_DIR" ]]; then
  echo "→ Backing up existing configs to $BACKUP_DIR..."
  mkdir -p "$BACKUP_DIR"
  [[ -d "$HOME/.kiro/steering" ]] && cp -R "$HOME/.kiro/steering" "$BACKUP_DIR/kiro-steering" 2>/dev/null
  [[ -f "$HOME/.claude/CLAUDE.md" ]] && cp "$HOME/.claude/CLAUDE.md" "$BACKUP_DIR/CLAUDE.md" 2>/dev/null
  [[ -d "$HOME/.claude/skills" ]] && cp -R "$HOME/.claude/skills" "$BACKUP_DIR/claude-skills" 2>/dev/null
  [[ -f "$HOME/.config/codex/instructions.md" ]] && cp "$HOME/.config/codex/instructions.md" "$BACKUP_DIR/codex-instructions.md" 2>/dev/null
  [[ -d "$HOME/.codex/skills" ]] && cp -R "$HOME/.codex/skills" "$BACKUP_DIR/codex-skills" 2>/dev/null
  [[ -d "$HOME/.agents/skills" ]] && cp -R "$HOME/.agents/skills" "$BACKUP_DIR/agents-skills" 2>/dev/null
  echo "  ✓ Backup saved (restore with: cp -R $BACKUP_DIR/* ~/)"
fi

# Helper: link or copy a skill directory to a destination
install_skill() {
  local src="$1" dest="$2"
  if $COPY_MODE; then
    rm -rf "$dest"
    cp -R "$src" "$dest"
  else
    ln -sfn "$src" "$dest"
  fi
}

# Ensure skills.yaml exists
if [[ ! -f "$DOTFILES_DIR/skills.yaml" ]]; then
  if [[ -f "$DOTFILES_DIR/skills.yaml.example" ]]; then
    cp "$DOTFILES_DIR/skills.yaml.example" "$DOTFILES_DIR/skills.yaml"
    echo "ℹ Created skills.yaml from example. Edit it to customize your remote skills."
  fi
fi

# Ensure rules/ exists
if [[ ! -d "$RULES_DIR" ]] || [[ -z "$(ls "$RULES_DIR"/*.md 2>/dev/null)" ]]; then
  if [[ -d "$DOTFILES_DIR/rules.example" ]]; then
    mkdir -p "$RULES_DIR"
    cp "$DOTFILES_DIR/rules.example"/*.md "$RULES_DIR/"
    echo "ℹ Created rules/ from examples (placeholder only)."
    echo "  → To generate personalized rules, tell your agent: skillgenie read init-rules"
  fi
fi

# ── 1. Kiro: symlink individual rule files ────────────────────────────────────
if ! $SKILLS_ONLY; then

# Install topic files to fixed location for all agents to read on demand
RULES_GLOBAL="$HOME/.agents/rules"
mkdir -p "$RULES_GLOBAL"
for f in "$RULES_DIR"/*.md; do
  [[ "$(basename "$f")" == "README.md" ]] && continue
  ln -sf "$f" "$RULES_GLOBAL/$(basename "$f")"
done

if command -v kiro &>/dev/null || [[ -d "$KIRO_DIR" ]]; then
  echo "→ Setting up Kiro rules..."
  mkdir -p "$KIRO_DIR"
  # Backup and remove non-symlink files (user's old manual configs)
  for f in "$KIRO_DIR"/*.md; do
    [[ -e "$f" ]] || continue
    [[ -L "$f" ]] && continue
    echo "  ⚠ Found existing file: $(basename "$f") — backing up to $BACKUP_DIR/"
    mkdir -p "$BACKUP_DIR"
    mv "$f" "$BACKUP_DIR/"
  done
  for f in "$RULES_DIR"/*.md; do
    ln -sf "$f" "$KIRO_DIR/$(basename "$f")"
  done
  echo "  ✓ Kiro: symlinked $(ls "$RULES_DIR"/*.md | wc -l | tr -d ' ') rule files"
fi

# ── 2. Claude Code: symlink router rules ──────────────────────────────────────
if command -v claude &>/dev/null || [[ -d "$HOME/.claude" ]]; then
  echo "→ Setting up Claude Code rules..."
  mkdir -p "$(dirname "$CLAUDE_FILE")"
  ln -sf "$RULES_DIR/router.md" "$CLAUDE_FILE"
  echo "  ✓ Claude Code: $CLAUDE_FILE"
fi

# ── 3. Codex: symlink router rules ───────────────────────────────────────────
if command -v codex &>/dev/null || [[ -d "$HOME/.codex" ]]; then
  echo "→ Setting up Codex rules..."
  mkdir -p "$(dirname "$CODEX_FILE")"
  ln -sf "$RULES_DIR/router.md" "$CODEX_FILE"
  echo "  ✓ Codex: $CODEX_FILE"
fi

# ── 3b. Windsurf: symlink router rules ───────────────────────────────────────
WINDSURF_RULES="$HOME/.codeium/windsurf/memories/global_rules.md"
if [[ -d "$HOME/.codeium/windsurf" ]]; then
  echo "→ Setting up Windsurf rules..."
  mkdir -p "$(dirname "$WINDSURF_RULES")"
  ln -sf "$RULES_DIR/router.md" "$WINDSURF_RULES"
  echo "  ✓ Windsurf: $WINDSURF_RULES"
fi

WINDSURF_NEXT_RULES="$HOME/.codeium/windsurf-next/memories/global_rules.md"
if [[ -d "$HOME/.codeium/windsurf-next" ]]; then
  echo "→ Setting up Windsurf Next rules..."
  mkdir -p "$(dirname "$WINDSURF_NEXT_RULES")"
  ln -sf "$RULES_DIR/router.md" "$WINDSURF_NEXT_RULES"
  echo "  ✓ Windsurf Next: $WINDSURF_NEXT_RULES"
fi

fi # end !SKILLS_ONLY

# ── 4. Skills: sync from manifest ────────────────────────────────────────────
if ! $RULES_ONLY; then

echo "→ Syncing skills..."
mkdir -p "$SKILLS_DEST"

if $FULL; then
  echo "  Clearing $SKILLS_DEST..."
  rm -rf "$SKILLS_DEST"/*
fi

# 4a. Local skills (in this repo)
SKILLGENIE_PATH="$DOTFILES_DIR/skills"

for skill_dir in "$SKILLGENIE_PATH"/*/; do
  skill_name="$(basename "$skill_dir")"
  [[ -f "$skill_dir/SKILL.md" ]] || continue
  install_skill "$skill_dir" "$SKILLS_DEST/$skill_name"
done
echo "  ✓ Local skills linked from skill-genie"

# 4b. Remote skills (read from skills.yaml)
CACHE_DIR="$HOME/.cache/skill-genie-remotes"
mkdir -p "$CACHE_DIR"

python3 - "$DOTFILES_DIR/skills.yaml" "$CACHE_DIR" "$SKILLS_DEST" "$COPY_MODE" <<'PYTHON'
import sys, os, subprocess, shutil
from pathlib import Path

try:
    import yaml
except ImportError:
    print("  ⚠ pyyaml not installed, skipping remote skills (pip3 install pyyaml)")
    sys.exit(0)

manifest = Path(sys.argv[1])
cache_dir = Path(sys.argv[2])
dest = Path(sys.argv[3])
copy_mode = sys.argv[4] == "true"

data = yaml.safe_load(manifest.read_text())
remotes = data.get("remote", [])

for entry in remotes:
    repo = entry["repo"]
    base_path = entry.get("path", "")
    picks = entry.get("pick", [])
    repo_dir = cache_dir / repo.replace("/", "_")

    if not repo_dir.exists():
        print(f"  Cloning {repo}...")
        subprocess.run(["git", "clone", "--depth", "1", f"https://github.com/{repo}.git", str(repo_dir)],
                       capture_output=True)
    else:
        subprocess.run(["git", "-C", str(repo_dir), "pull", "--quiet"], capture_output=True)

    for skill in picks:
        skill_name = os.path.basename(skill)
        skill_path = repo_dir / base_path / skill if base_path else repo_dir / skill
        if skill_path.is_dir():
            link = dest / skill_name
            if copy_mode:
                if link.exists() or link.is_symlink():
                    shutil.rmtree(link, ignore_errors=True)
                shutil.copytree(skill_path, link, symlinks=True)
            else:
                link.unlink(missing_ok=True)
                link.symlink_to(skill_path)
        else:
            print(f"  ⚠ Not found: {repo}/{skill}")

print("  ✓ Remote skills synced")
PYTHON

# ── 4c. Optional skills (only if tool is installed) ───────────────────────────
echo "→ Checking optional tool skills..."

# Trellis
if command -v trellis &>/dev/null; then
  # Derive the package root from the trellis binary so this works regardless of
  # install method (nvm, Homebrew, pnpm). Fall back to the npm global root.
  TRELLIS_SKILLS=""
  TRELLIS_BIN="$(readlink -f "$(command -v trellis)" 2>/dev/null || true)"
  if [[ -n "$TRELLIS_BIN" ]]; then
    TRELLIS_CANDIDATE="$(dirname "$TRELLIS_BIN")/../dist/templates/codex/skills"
    [[ -d "$TRELLIS_CANDIDATE" ]] && TRELLIS_SKILLS="$TRELLIS_CANDIDATE"
  fi
  [[ -z "$TRELLIS_SKILLS" ]] && TRELLIS_SKILLS="$(npm root -g)/@mindfoldhq/trellis/dist/templates/codex/skills"
  if [[ -d "$TRELLIS_SKILLS" ]]; then
    for skill in start brainstorm check check-cross-layer update-spec before-dev break-loop finish-work; do
      [[ -d "$TRELLIS_SKILLS/$skill" ]] && install_skill "$TRELLIS_SKILLS/$skill" "$SKILLS_DEST/$skill"
    done
    echo "  ✓ trellis skills linked"
  else
    echo "  ⚠ trellis installed but skills path not found"
  fi
else
  echo "  – trellis not found, skipping"
fi

# ── 5. Native agent skill paths (only if agent is installed) ──────────────────
echo "→ Linking skills to detected agent paths..."

linked_agents=""

link_to_native() {
  local native_dir="$1" agent_name="$2"
  mkdir -p "$native_dir"
  local real_native real_dest
  real_native="$(readlink -f "$native_dir" 2>/dev/null || echo "$native_dir")"
  real_dest="$(readlink -f "$SKILLS_DEST" 2>/dev/null || echo "$SKILLS_DEST")"
  # Already points to primary skills dir
  [[ "$real_native" == "$real_dest" ]] && linked_agents="$linked_agents $agent_name(✓)" && return
  for skill in "$SKILLS_DEST"/*/; do
    local skill_name real_skill
    skill_name="$(basename "$skill")"
    real_skill="$(readlink -f "$skill" 2>/dev/null || echo "$skill")"
    [[ -d "$real_skill" ]] || continue
    [[ -f "$real_skill/SKILL.md" ]] || continue
    install_skill "$real_skill" "$native_dir/$skill_name" 2>/dev/null || true
  done
  linked_agents="$linked_agents $agent_name"
}

command -v codex &>/dev/null && link_to_native "$HOME/.codex/skills" "codex" || true
command -v claude &>/dev/null && link_to_native "$HOME/.claude/skills" "claude" || true
if command -v kiro &>/dev/null || [[ -d "$HOME/.kiro" ]]; then
  link_to_native "$HOME/.kiro/skills" "kiro"
fi
if command -v openclaw &>/dev/null || [[ -d "$HOME/.openclaw" ]]; then
  link_to_native "$HOME/.openclaw/skills" "openclaw"
fi
if command -v hermes &>/dev/null || [[ -d "$HOME/.hermes" ]]; then
  link_to_native "$HOME/.hermes/skills" "hermes"
fi
if command -v opencode &>/dev/null || [[ -d "$HOME/.config/opencode" ]]; then
  link_to_native "$HOME/.config/opencode/skills" "opencode"
fi
# Devin CLI + Devin Desktop (formerly Windsurf); both read ~/.config/devin/skills
if command -v devin &>/dev/null || [[ -d "$HOME/.config/devin" ]] || [[ -d "$HOME/.devin" ]] || [[ -d "$HOME/.devin-next" ]]; then
  link_to_native "$HOME/.config/devin/skills" "devin"
fi
command -v antigravity &>/dev/null && link_to_native "$HOME/.gemini/antigravity/skills" "antigravity" || true
command -v cursor &>/dev/null && link_to_native "$HOME/.cursor/skills" "cursor" || true
command -v gh &>/dev/null && [[ -d "$HOME/.github" ]] && link_to_native "$HOME/.github/skills" "copilot" || true
# GitHub Copilot CLI + Copilot app (both load personal Agent Skills from ~/.copilot/skills)
if command -v copilot &>/dev/null || [[ -d "$HOME/.copilot" ]]; then
  link_to_native "$HOME/.copilot/skills" "copilot-cli"
fi
[[ -d "$HOME/.codeium/windsurf" ]] && link_to_native "$HOME/.codeium/windsurf/skills" "windsurf" || true
[[ -d "$HOME/.codeium/windsurf-next" ]] && link_to_native "$HOME/.codeium/windsurf-next/skills" "windsurf-next" || true

if [[ -z "$linked_agents" ]]; then
  echo "  – No additional agents detected, skipping"
else
  echo "  ✓ Skills linked to:$linked_agents"
fi

fi # end !RULES_ONLY

# ── 6. skillgenie CLI ─────────────────────────────────────────────────────────
echo "→ Linking skillgenie to PATH..."
SKILLGENIE_BIN="$DOTFILES_DIR/skillgenie"
if [[ -f "$SKILLGENIE_BIN" ]]; then
  chmod +x "$SKILLGENIE_BIN"
  if [[ -d /opt/homebrew/bin ]]; then
    ln -sf "$SKILLGENIE_BIN" /opt/homebrew/bin/skillgenie
  elif [[ -d "$HOME/.local/bin" ]]; then
    mkdir -p "$HOME/.local/bin"
    ln -sf "$SKILLGENIE_BIN" "$HOME/.local/bin/skillgenie"
  fi
  echo "  ✓ skillgenie linked"
fi

echo ""
echo "✅ Done. All rules and skills are in place."

# ── 7. Zsh completions ────────────────────────────────────────────────────────
if [[ -f "$DOTFILES_DIR/completions/_skillgenie" ]]; then
  mkdir -p "$HOME/.zsh/completions"
  ln -sf "$DOTFILES_DIR/completions/_skillgenie" "$HOME/.zsh/completions/_skillgenie"
fi
