#!/bin/bash
set -euo pipefail

DOTFILES_DIR="$(cd "$(dirname "$0")" && pwd)"
RULES_DIR="$DOTFILES_DIR/rules"
SKILLS_DEST="$HOME/.agents/skills"
KIRO_DIR="$HOME/.kiro/steering"
CLAUDE_FILE="$HOME/.claude/CLAUDE.md"
CODEX_FILE="$HOME/.config/codex/instructions.md"
SKILLGENIE_BIN_PATH=""

FULL=false
if [[ "${1:-}" == "--full" ]]; then
  FULL=true
  echo "⚠ Full mode: ~/.agents/skills/ will be cleared and rebuilt."
  read -p "Continue? [y/N] " confirm
  [[ "$confirm" =~ ^[Yy]$ ]] || exit 0
fi

# ── 1. Kiro: symlink individual rule files ────────────────────────────────────
echo "→ Setting up Kiro rules..."
mkdir -p "$KIRO_DIR"
for f in "$RULES_DIR"/*.md; do
  ln -sf "$f" "$KIRO_DIR/$(basename "$f")"
done
echo "  ✓ Kiro: symlinked $(ls "$RULES_DIR"/*.md | wc -l | tr -d ' ') rule files"

# ── 2. Claude Code: concatenate rules into single file ────────────────────────
echo "→ Setting up Claude Code rules..."
mkdir -p "$(dirname "$CLAUDE_FILE")"
cat "$RULES_DIR"/router.md "$RULES_DIR"/session-sync.md \
    "$RULES_DIR"/workflow-tools.md "$RULES_DIR"/stack-and-deployment.md \
    "$RULES_DIR"/external-tools.md > "$CLAUDE_FILE"
echo "  ✓ Claude Code: $CLAUDE_FILE"

# ── 3. Codex: concatenate rules into single file ──────────────────────────────
echo "→ Setting up Codex rules..."
mkdir -p "$(dirname "$CODEX_FILE")"
cp "$CLAUDE_FILE" "$CODEX_FILE"
echo "  ✓ Codex: $CODEX_FILE"

# ── 4. Skills: sync from manifest ────────────────────────────────────────────
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
  ln -sf "$skill_dir" "$SKILLS_DEST/$skill_name"
done
echo "  ✓ Local skills linked from skill-genie"

# 4b. Remote skills (read from skills.yaml)
CACHE_DIR="$HOME/.cache/skill-genie-remotes"
mkdir -p "$CACHE_DIR"

python3 - "$DOTFILES_DIR/skills.yaml" "$CACHE_DIR" "$SKILLS_DEST" <<'PYTHON'
import sys, os, subprocess
from pathlib import Path

try:
    import yaml
except ImportError:
    print("  ⚠ pyyaml not installed, skipping remote skills (pip3 install pyyaml)")
    sys.exit(0)

manifest = Path(sys.argv[1])
cache_dir = Path(sys.argv[2])
dest = Path(sys.argv[3])

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
  TRELLIS_SKILLS="$(npm root -g)/@mindfoldhq/trellis/dist/templates/codex/skills"
  if [[ -d "$TRELLIS_SKILLS" ]]; then
    for skill in start brainstorm check check-cross-layer update-spec before-dev break-loop finish-work; do
      [[ -d "$TRELLIS_SKILLS/$skill" ]] && ln -sf "$TRELLIS_SKILLS/$skill" "$SKILLS_DEST/$skill"
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
    ln -sfn "$real_skill" "$native_dir/$skill_name" 2>/dev/null || true
  done
  linked_agents="$linked_agents $agent_name"
}

command -v codex &>/dev/null && link_to_native "$HOME/.codex/skills" "codex" || true
command -v claude &>/dev/null && link_to_native "$HOME/.claude/skills" "claude" || true
command -v antigravity &>/dev/null && link_to_native "$HOME/.gemini/antigravity/skills" "antigravity" || true
command -v cursor &>/dev/null && link_to_native "$HOME/.cursor/skills" "cursor" || true
command -v gh &>/dev/null && [[ -d "$HOME/.github" ]] && link_to_native "$HOME/.github/skills" "copilot" || true

if [[ -z "$linked_agents" ]]; then
  echo "  – No additional agents detected, skipping"
else
  echo "  ✓ Skills linked to:$linked_agents"
fi

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
