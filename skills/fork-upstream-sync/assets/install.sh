#!/usr/bin/env bash
# Bootstrap upstream-sync into a fork.
#
#   install.sh [--upstream <url>] [--force]
#
# Does the mechanical half of setup: installs the driver and workflow, detects
# the toolchain, harvests gate commands out of the repo's existing CI, spots
# baseline-shaped generated files, and scaffolds .fork-sync.yml around what it
# found.
#
# It deliberately does NOT invent the `divergences:` list. What this fork changed
# on purpose, and which test defends each change, cannot be read off the
# filesystem — that is the agent's job (see SKILL.md → "Setup"). Every scaffolded
# entry is marked TODO so an unfilled manifest is obvious rather than plausible.
set -uo pipefail
shopt -s extglob

BOLD=$'\033[1m'; DIM=$'\033[2m'; RED=$'\033[31m'; GRN=$'\033[32m'; YEL=$'\033[33m'; OFF=$'\033[0m'
die()  { printf '%s\n' "${RED}error:${OFF} $*" >&2; exit 1; }
ok()   { printf '%s\n' "${GRN}✓${OFF} $*"; }
info() { printf '%s\n' "${DIM}·${OFF} $*"; }
warn() { printf '%s\n' "${YEL}!${OFF} $*"; }
head_(){ printf '\n%s\n' "${BOLD}$*${OFF}"; }

UPSTREAM_URL=""; FORCE=false
while [ $# -gt 0 ]; do
  case "$1" in
    --upstream) UPSTREAM_URL=${2:-}; shift 2 ;;
    --force)    FORCE=true; shift ;;
    -h|--help)  sed -n '2,16p' "$0"; exit 0 ;;
    *) die "unknown option: $1" ;;
  esac
done

ASSETS=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
command -v git >/dev/null || die "git not found"
git rev-parse --git-dir >/dev/null 2>&1 || die "not a git repository"
cd "$(git rev-parse --show-toplevel)" || die "cannot reach repo root"
ROOT=$(pwd)
info "repo: $ROOT"

command -v yq >/dev/null || warn "yq not installed — the driver needs it: brew install yq"

# ── upstream remote ─────────────────────────────────────────────────────────
head_ "Upstream remote"
if git remote get-url upstream >/dev/null 2>&1; then
  UPSTREAM_URL=$(git remote get-url upstream)
  ok "already configured: $UPSTREAM_URL"
else
  if [ -z "$UPSTREAM_URL" ] && command -v gh >/dev/null; then
    UPSTREAM_URL=$(gh repo view --json parent \
      -q 'if .parent then "https://github.com/" + .parent.owner.login + "/" + .parent.name + ".git" else "" end' 2>/dev/null || true)
    [ -n "$UPSTREAM_URL" ] && info "detected the fork parent via gh: $UPSTREAM_URL"
  fi
  if [ -n "$UPSTREAM_URL" ]; then
    git remote add upstream "$UPSTREAM_URL" && ok "added remote upstream → $UPSTREAM_URL"
  else
    warn "no upstream remote and none detected. Add it, then re-run:"
    printf '    git remote add upstream <url>\n'
  fi
fi

DEFAULT_BRANCH=$(git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null | sed 's|^origin/||')
[ -n "$DEFAULT_BRANCH" ] || DEFAULT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
UPSTREAM_BRANCH=$DEFAULT_BRANCH
info "fork branch: $DEFAULT_BRANCH"

# ── toolchain detection ─────────────────────────────────────────────────────
head_ "Toolchain"
PY=""
for c in .venv/bin/python3 venv/bin/python3 .venv/bin/python env/bin/python3; do
  [ -x "$c" ] && { PY=$c; break; }
done
if [ -n "$PY" ]; then ok "python: $PY"
elif [ -f pyproject.toml ] || [ -f setup.py ] || compgen -G "*.py" >/dev/null 2>&1; then
  PY="python3"; warn "python project but no venv found — set toolchain.python yourself."
  warn "  A bare python3 can be a system version whose generated output differs."
fi

NODE_RUNNER=""
if [ -f pnpm-lock.yaml ]; then NODE_RUNNER=pnpm
elif [ -f yarn.lock ]; then NODE_RUNNER=yarn
elif [ -f package-lock.json ] || [ -f package.json ]; then NODE_RUNNER=npm
fi
[ -n "$NODE_RUNNER" ] && ok "node runner: $NODE_RUNNER"

TC_EXTRA=""
if [ -n "$PY" ] && grep -rqs "platform linux\|--platform linux" ./*.md docs 2>/dev/null; then
  TC_EXTRA="--platform linux"
  info "docs mention mypy --platform linux; carried into typecheck_extra_args"
fi

# ── harvest gate commands from existing CI ──────────────────────────────────
head_ "Gates found in existing CI"
GATES_YAML=""
add_gate() { GATES_YAML+="  - name: \"$1\"$'\n'    run: \"$2\"$'\n'"; }
gate_lines=()
if [ -d .github/workflows ]; then
  # Any `python3 scripts/check_*.py` / `bash scripts/*-lint.sh` style invocation
  # already trusted by this repo's CI is a gate worth re-running on a sync.
  while IFS= read -r cmd; do
    [ -n "$cmd" ] || continue
    gate_lines+=("$cmd")
  done < <(grep -rhoE '(python3?|bash) +(scripts|tools)/[A-Za-z0-9_./-]+(\.py|\.sh)' \
             .github/workflows 2>/dev/null | sort -u | head -12)
fi
if [ ${#gate_lines[@]} -gt 0 ]; then
  for g in "${gate_lines[@]}"; do printf '    %s\n' "$g"; done
  ok "${#gate_lines[@]} candidate gate command(s) — scaffolded, review them"
else
  info "none auto-detected; fill gates: yourself"
fi

# ── baseline-shaped generated files ─────────────────────────────────────────
head_ "Generated files that must be regenerated, not hand-merged"
base_files=()
while IFS= read -r f; do
  f=${f#./}
  case "$f" in */node_modules/*|*/.git/*|*/dist/*) continue ;; esac
  base_files+=("$f")
done < <(find . -maxdepth 3 \
           \( -name '*baseline*' -o -name '*.gen.ts' -o -name '*.generated.*' -o -name '*.lock' \) \
           -type f 2>/dev/null | head -12)
if [ ${#base_files[@]} -gt 0 ]; then
  for f in "${base_files[@]}"; do printf '    %s\n' "$f"; done
  ok "${#base_files[@]} candidate(s) — add each one's regen command"
else
  info "none detected"
fi

# ── install driver + workflow ───────────────────────────────────────────────
head_ "Installing"
mkdir -p scripts .github/workflows
for pair in "sync-upstream.sh:scripts/sync-upstream.sh" "sync-upstream.yml:.github/workflows/sync-upstream.yml"; do
  src=${pair%%:*}; dst=${pair##*:}
  if [ -e "$dst" ] && ! $FORCE; then
    warn "$dst exists — left alone (--force to overwrite)"
  else
    cp "$ASSETS/$src" "$dst" && ok "$dst"
  fi
done
chmod +x scripts/sync-upstream.sh 2>/dev/null || true

# ── scaffold the manifest ───────────────────────────────────────────────────
if [ -e .fork-sync.yml ] && ! $FORCE; then
  warn ".fork-sync.yml exists — left alone (--force to overwrite)"
else
  {
    cat <<YAML
# Upstream-sync manifest. Procedure: the fork-upstream-sync skill.
#
# SCAFFOLDED by install.sh — every TODO below is a real gap, not boilerplate.
# The mechanical parts (toolchain, candidate gates, generated files) were
# detected; the judgment parts (conflict policy, divergences) were not, because
# they cannot be read off the filesystem.

upstream:
  remote: upstream
  url: ${UPSTREAM_URL:-TODO}
  branch: $UPSTREAM_BRANCH
  fork_branch: $DEFAULT_BRANCH
  sync_branch: "sync/upstream-{date}"

# Globs are shell \`case\` patterns: use @(a|b) for alternation, NOT {a,b}.
# First match wins — narrow/high-stakes first, broad/structural last.
# policy: fork_wins | upstream_wins | union | upstream_then_regen | manual
conflict_policy:
  # TODO: put this fork's security/auth/sandbox surfaces here FIRST, as
  #       fork_wins + keystone: true. Those are the files where a wrong
  #       resolution is a vulnerability rather than a bug.
  # - glob: "src/**/@(security|auth|sandbox).py"
  #   policy: fork_wins
  #   keystone: true

  - glob: "docs/**"
    policy: union
  - glob: "*.md"
    policy: union
YAML
    for f in "${base_files[@]:-}"; do
      [ -n "${f:-}" ] || continue
      printf '  - glob: "%s"\n    policy: upstream_then_regen\n' "$f"
    done

    cat <<'YAML'

# TODO — the most important section. Every deliberate difference from upstream,
# and THE TEST THAT DEFENDS IT. An entry with pinned_by: null is a change some
# future sync will silently revert; prose does not fail a build.
#
# Derive these from: the repo's own AGENTS.md / CONTRIBUTING.md, its custom CI
# gate scripts, and `git log --oneline upstream/HEAD..HEAD` (every fork-only
# commit is a candidate).
divergences: []
  # - id: <short-slug>
  #   what: "<the behavior that differs>"
  #   why: "<why it differs — the reason a future merge must not undo it>"
  #   pinned_by: "<test path::name>"   # null = undefended, write the test
  #   decided: <YYYY-MM-DD>

YAML

    cat <<YAML
# Spell the interpreter out. A bare python3/node can resolve to a system version
# whose generated output differs — a baseline written by the wrong one is
# silently wrong and still passes locally.
toolchain:
  python: "${PY}"
  node: "${NODE_RUNNER}"
  typecheck_extra_args: "${TC_EXTRA}"

gates:
  - name: "no conflict markers"
    run: "! git grep -n '^<<<<<<<' -- ':!*.md' ':!.fork-sync.yml'"
YAML
    for g in "${gate_lines[@]:-}"; do
      [ -n "${g:-}" ] || continue
      nm=$(basename "${g##* }"); nm=${nm%.*}
      # {python} so the manifest's own toolchain wins over whatever CI hardcoded.
      printf '  - name: "%s"   # TODO verify\n    run: "%s"\n' \
        "$nm" "$(printf '%s' "$g" | sed 's|^python3\{0,1\} |{python} |')"
    done

    cat <<'YAML'

baselines:   # TODO: each generated file above needs its regen command
  # - path: "<file>"
  #   regen: "{python} scripts/<generator>.py"

tests:
  focused: ""   # TODO: the divergence-pinning tests — fastest useful signal
  full: ""      # TODO
  frontend: ""

# Checks that fail for reasons unrelated to any change, so a real failure is
# never mistaken for one of them. Each needs a REASON, or it becomes a permanent
# excuse. Re-verify occasionally: a stale entry masks a genuine failure.
known_red: []

# Test-failure classes proven environmental — PROVE with a merge-base run first.
environmental_failures: []
YAML
  } > .fork-sync.yml
  ok ".fork-sync.yml scaffolded"
fi

# ── report ──────────────────────────────────────────────────────────────────
todos=$(grep -c 'TODO' .fork-sync.yml 2>/dev/null || echo 0)
head_ "Next"
cat <<EOF
  .fork-sync.yml has ${BOLD}${todos}${OFF} TODO marker(s). The scaffold covers what a
  script can know; the rest is judgment and is what makes this fork's syncs safe:

  1. ${BOLD}conflict_policy${OFF} — put the security/auth/sandbox surfaces first, as
     fork_wins + keystone. A wrong call there is a vulnerability, not a bug.
  2. ${BOLD}divergences${OFF} — the load-bearing section. Start from:
       git log --oneline upstream/$UPSTREAM_BRANCH..$DEFAULT_BRANCH
     Each fork-only commit is a candidate; for each, name the test that fails if
     upstream overwrites it. No test ⇒ pinned_by: null ⇒ you will lose it.
  3. ${BOLD}gates / baselines / tests${OFF} — verify the scaffolded commands run.

  Then dry-run, and confirm nothing you care about lands in "unclassified":
     ./scripts/sync-upstream.sh --report
EOF
