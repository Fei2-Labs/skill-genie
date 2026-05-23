#!/bin/bash
set -euo pipefail

DOTFILES_DIR="$(cd "$(dirname "$0")" && pwd)"
RULES_DIR="$DOTFILES_DIR/rules"
SKILLS_DEST="$HOME/.agent/skills"
KIRO_DIR="$HOME/.kiro/steering"
CLAUDE_FILE="$HOME/.claude/CLAUDE.md"
CODEX_FILE="$HOME/.config/codex/instructions.md"
SKILLGENIE_BIN_PATH=""

FULL=false
if [[ "${1:-}" == "--full" ]]; then
  FULL=true
  echo "⚠ Full mode: ~/.agent/skills/ will be cleared and rebuilt."
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
SKILLGENIE_PATH="$DOTFILES_DIR"

for skill_dir in "$SKILLGENIE_PATH"/*/; do
  skill_name="$(basename "$skill_dir")"
  [[ -f "$skill_dir/SKILL.md" ]] || continue
  ln -sf "$skill_dir" "$SKILLS_DEST/$skill_name"
done
echo "  ✓ Local skills linked from skill-genie"

# 4b. Remote skills (clone repos and symlink picked skills)
CACHE_DIR="$HOME/.cache/dotfiles-skills"
mkdir -p "$CACHE_DIR"

sync_remote() {
  local repo="$1" path="${2:-}" shift_args=("${@:3}")
  local repo_dir="$CACHE_DIR/$(echo "$repo" | tr '/' '_')"

  if [[ ! -d "$repo_dir" ]]; then
    echo "  Cloning $repo..."
    git clone --depth 1 "https://github.com/$repo.git" "$repo_dir" 2>/dev/null
  else
    git -C "$repo_dir" pull --quiet 2>/dev/null || true
  fi

  for skill in "${shift_args[@]}"; do
    local skill_name="$(basename "$skill")"
    local skill_path="$repo_dir"
    [[ -n "$path" ]] && skill_path="$skill_path/$path"
    skill_path="$skill_path/$skill"

    if [[ -d "$skill_path" ]]; then
      ln -sf "$skill_path" "$SKILLS_DEST/$skill_name"
    else
      echo "  ⚠ Not found: $repo/$skill"
    fi
  done
}

# Matt Pocock
sync_remote "mattpocock/dotfiles" "skills" \
  "engineering/design-an-interface" "personal/edit-article" \
  "misc/git-guardrails-claude-code" "misc/migrate-to-shoehorn" \
  "personal/obsidian-vault" "deprecated/qa" \
  "deprecated/request-refactor-plan" "misc/scaffold-exercises" \
  "misc/setup-pre-commit" "engineering/ubiquitous-language"

# Warp oz-skills
sync_remote "warpdotdev/oz-skills" "" \
  "analysis-artifacts" "ci-fix" "create-pull-request" \
  "dbt-model-index" "docs-update" "github-bug-report-triage" \
  "github-issue-dedupe" "scheduler" "seo-aeo-audit" \
  "slack-qa-investigate" "terraform-style-check" \
  "web-accessibility-audit" "web-performance-audit"

echo "  ✓ Remote skills synced"

# ── 5. skillgenie CLI ─────────────────────────────────────────────────────────
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
