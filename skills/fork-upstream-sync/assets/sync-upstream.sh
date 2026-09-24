#!/usr/bin/env bash
# Upstream-sync driver. Does the deterministic half of a fork sync: fetch, trial
# merge, classify conflicts against .fork-sync.yml, run gates, regenerate
# baselines. It deliberately NEVER resolves a conflict — that is judgment, and a
# script that guesses picks whichever side is listed second.
#
#   ./scripts/sync-upstream.sh            fetch, report, trial merge
#   ./scripts/sync-upstream.sh --gates    after resolving: gates + baselines + tests
#   ./scripts/sync-upstream.sh --report   read-only: what would change, no branch
#   ./scripts/sync-upstream.sh --push     push the branch and open the PR
#
# Reads .fork-sync.yml from the repo root. Needs: git, yq, gh.
set -uo pipefail
# Policy globs are matched with `case`, which does NOT do brace expansion: a
# pattern written `{a,b}.py` matches the literal string "{a,b}.py" and every path
# it was meant to cover silently reports as unclassified. extglob gives config
# authors real alternation via `@(a|b)`.
shopt -s extglob

CFG=".fork-sync.yml"
BOLD=$'\033[1m'; DIM=$'\033[2m'; RED=$'\033[31m'; GRN=$'\033[32m'; YEL=$'\033[33m'; OFF=$'\033[0m'

die()  { printf '%s\n' "${RED}error:${OFF} $*" >&2; exit 1; }
info() { printf '%s\n' "${DIM}·${OFF} $*"; }
ok()   { printf '%s\n' "${GRN}✓${OFF} $*"; }
warn() { printf '%s\n' "${YEL}!${OFF} $*"; }
head_() { printf '\n%s\n' "${BOLD}$*${OFF}"; }

command -v git >/dev/null || die "git not found"
command -v yq  >/dev/null || die "yq not found — install it: brew install yq
       (Linux: see https://github.com/mikefarah/yq#install)
       yq reads .fork-sync.yml, which is where this fork's policy lives."
command -v gh  >/dev/null || warn "gh not found — --push will push the branch but not open the PR"
git rev-parse --git-dir >/dev/null 2>&1 || die "not a git repository"
cd "$(git rev-parse --show-toplevel)" || die "cannot reach repo root"
[ -f "$CFG" ] || die "$CFG not found. Copy it from the skill's assets/ and fill it in."

q() { yq -r "$1 // \"\"" "$CFG" 2>/dev/null; }

UPSTREAM_REMOTE=$(q '.upstream.remote'); UPSTREAM_REMOTE=${UPSTREAM_REMOTE:-upstream}
UPSTREAM_BRANCH=$(q '.upstream.branch'); UPSTREAM_BRANCH=${UPSTREAM_BRANCH:-main}
FORK_BRANCH=$(q '.upstream.fork_branch'); FORK_BRANCH=${FORK_BRANCH:-main}
# The default is a separate assignment on purpose. Inline as
# ${SYNC_TMPL:-sync/upstream-{date}} bash closes the expansion at the FIRST `}`,
# so the trailing `}` becomes literal text appended even when the value came
# from the config — yielding a branch literally named "...-20260831}".
SYNC_TMPL=$(q '.upstream.sync_branch')
[ -n "$SYNC_TMPL" ] || SYNC_TMPL='sync/upstream-{date}'
SYNC_BRANCH=${SYNC_TMPL/'{date}'/$(date +%Y%m%d)}

PY=$(q '.toolchain.python'); NODE=$(q '.toolchain.node')
TC_EXTRA=$(q '.toolchain.typecheck_extra_args')

# Substitute {python}/{node}/{fork_branch}/{typecheck_extra_args} in a command.
expand() {
  local s=$1
  s=${s//\{python\}/$PY}; s=${s//\{node\}/$NODE}
  s=${s//\{fork_branch\}/$FORK_BRANCH}; s=${s//\{typecheck_extra_args\}/$TC_EXTRA}
  printf '%s' "$s"
}

# ── the policy any conflicted path resolves under, first match wins ──────────
policy_for() {
  local path=$1 n i glob pol keystone
  n=$(yq -r '.conflict_policy | length // 0' "$CFG" 2>/dev/null)
  for ((i = 0; i < n; i++)); do
    glob=$(yq -r ".conflict_policy[$i].glob // \"\"" "$CFG")
    [ -n "$glob" ] || continue
    # shellcheck disable=SC2254  # glob is a pattern on purpose
    case "$path" in
      $glob)
        pol=$(yq -r ".conflict_policy[$i].policy // \"manual\"" "$CFG")
        keystone=$(yq -r ".conflict_policy[$i].keystone // false" "$CFG")
        printf '%s\t%s' "$pol" "$keystone"; return ;;
    esac
  done
  printf 'manual\tfalse'
}

require_clean_tree() {
  git diff --quiet && git diff --cached --quiet \
    || die "working tree is dirty. Commit or stash first — a sync must start clean."
}

# ── gates / baselines / tests ───────────────────────────────────────────────
run_gates() {
  local n i name cmd failed=0
  head_ "Gates"
  n=$(yq -r '.gates | length // 0' "$CFG")
  [ "$n" -eq 0 ] && info "none declared in $CFG"
  for ((i = 0; i < n; i++)); do
    name=$(yq -r ".gates[$i].name // \"gate $i\"" "$CFG")
    cmd=$(expand "$(yq -r ".gates[$i].run // \"\"" "$CFG")")
    [ -n "$cmd" ] || continue
    printf '  %s … ' "$name"
    if out=$(bash -c "$cmd" 2>&1); then printf '%s\n' "${GRN}pass${OFF}"
    else
      printf '%s\n' "${RED}FAIL${OFF}"
      printf '%s\n' "$out" | tail -25 | sed 's/^/      /'
      failed=1
    fi
  done
  return $failed
}

regen_baselines() {
  local n i path cmd
  head_ "Baselines"
  n=$(yq -r '.baselines | length // 0' "$CFG")
  [ "$n" -eq 0 ] && { info "none declared"; return 0; }
  warn "regenerating with ${PY:-<toolchain.python unset>} — a wrong interpreter writes a silently wrong baseline"
  for ((i = 0; i < n; i++)); do
    path=$(yq -r ".baselines[$i].path // \"\"" "$CFG")
    cmd=$(expand "$(yq -r ".baselines[$i].regen // \"\"" "$CFG")")
    [ -n "$cmd" ] || continue
    printf '  %s … ' "$path"
    if out=$(bash -c "$cmd" 2>&1); then ok ""; else
      printf '%s\n' "${RED}FAIL${OFF}"; printf '%s\n' "$out" | tail -15 | sed 's/^/      /'
    fi
  done
}

run_tests() {
  local key=$1 cmd
  cmd=$(expand "$(q ".tests.$key")")
  [ -n "$cmd" ] || { info "tests.$key not declared"; return 0; }
  head_ "Tests ($key)"
  info "$cmd"
  bash -c "$cmd"
}

print_known_red() {
  local n i chk reason
  n=$(yq -r '.known_red | length // 0' "$CFG")
  [ "$n" -eq 0 ] && return 0
  head_ "Known-red (NOT evidence of a problem in this merge)"
  for ((i = 0; i < n; i++)); do
    chk=$(yq -r ".known_red[$i].check // \"\"" "$CFG")
    reason=$(yq -r ".known_red[$i].reason // \"no reason recorded\"" "$CFG")
    printf '  %-38s %s\n' "$chk" "${DIM}$reason${OFF}"
  done
  warn "re-verify occasionally: an entry whose cause is fixed now MASKS a real failure"
}

print_divergences() {
  local n i id what pin unpinned=0
  n=$(yq -r '.divergences | length // 0' "$CFG")
  head_ "Divergences to preserve ($n)"
  if [ "$n" -eq 0 ]; then
    warn "none declared — then nothing defends this fork's behavior on merge. Fill in $CFG."
    return 0
  fi
  for ((i = 0; i < n; i++)); do
    id=$(yq -r ".divergences[$i].id // \"?\"" "$CFG")
    what=$(yq -r ".divergences[$i].what // \"\"" "$CFG")
    pin=$(yq -r ".divergences[$i].pinned_by // \"\"" "$CFG")
    if [ -z "$pin" ] || [ "$pin" = "null" ]; then
      printf '  %s %-26s %s\n' "${RED}unpinned${OFF}" "$id" "$what"; unpinned=1
    else
      printf '  %s %-26s %s\n' "${GRN}pinned  ${OFF}" "$id" "${DIM}$pin${OFF}"
    fi
  done
  [ "$unpinned" -eq 1 ] && warn "an unpinned divergence is one this sync can silently revert — write the test"
  return 0
}

# ── modes ───────────────────────────────────────────────────────────────────
case "${1:-}" in
  --gates)
    run_gates; gates_rc=$?
    regen_baselines
    run_tests focused
    print_known_red
    head_ "Triage every failure into exactly one bucket"
    cat <<'EOF'
  real regression   the merge broke it            → fix in-branch, do not merge
  stale expectation code changed on purpose       → update the assertion, say why
  environmental     fails on the merge base too   → PROVE IT:
                      git stash && git checkout $(git merge-base HEAD @{u}) &&
                      <re-run the failing test> && git checkout - && git stash pop

  Never skip a failure because it "looks environmental" — prove it or fix it.
  Several PRs failing IDENTICALLY indicts the branch, not the PRs.
EOF
    exit $gates_rc ;;

  --push)
    br=$(git rev-parse --abbrev-ref HEAD)
    [ "$br" != "$FORK_BRANCH" ] || die "refusing to push $FORK_BRANCH directly — sync lands via PR"
    git grep -qn '^<<<<<<<\|^>>>>>>>' && die "conflict markers still present"
    git push -u origin "$br" || die "push failed"
    command -v gh >/dev/null || { ok "pushed $br — open the PR manually (gh not found)"; exit 0; }
    gh pr create --base "$FORK_BRANCH" --head "$br" \
      --title "merge: sync ${UPSTREAM_REMOTE}/${UPSTREAM_BRANCH}" \
      --body "$(cat <<EOB
Automated upstream sync. **Do not merge on a green tick alone** — a textually
clean merge can still leave two features unwired (see the fork-upstream-sync
skill, rule 3). Read the diff for any function both sides touched.

Divergences that must survive: see \`.fork-sync.yml\`.
Checks known-red for infrastructure reasons: see \`.fork-sync.yml\` → \`known_red\`.
EOB
)" || warn "branch pushed; PR creation failed — open it manually"
    exit 0 ;;

  --report|"") : ;;
  -h|--help) sed -n '2,16p' "$0"; exit 0 ;;
  *) die "unknown option: $1" ;;
esac

# ── default / --report: fetch and assess ────────────────────────────────────
report_only=false; [ "${1:-}" = "--report" ] && report_only=true

head_ "Fetching ${UPSTREAM_REMOTE}/${UPSTREAM_BRANCH}"
git fetch "$UPSTREAM_REMOTE" "$UPSTREAM_BRANCH" 2>&1 | sed 's/^/  /' \
  || die "fetch failed — is the '$UPSTREAM_REMOTE' remote configured?"

UP="${UPSTREAM_REMOTE}/${UPSTREAM_BRANCH}"
behind=$(git rev-list --count "HEAD..${UP}")
ahead=$(git rev-list --count "${UP}..HEAD")

if [ "$behind" -eq 0 ]; then ok "already current with $UP (fork is $ahead ahead)"; exit 0; fi
info "$behind upstream commit(s) to take; this fork is $ahead ahead"

head_ "Incoming (newest 15)"
git log --oneline --no-decorate "HEAD..${UP}" | head -15 | sed 's/^/  /'

print_divergences

head_ "Trial merge"
require_clean_tree
base=$(git rev-parse HEAD)
orig_branch=$(git rev-parse --abbrev-ref HEAD)

# `git merge-tree --write-tree` probes the merge WITHOUT touching the working
# tree. Exit 0 = clean, exit 1 = conflicts. Two parsing traps, both of which
# silently produce garbage rather than an error:
#
#   * Reading the exit code the wrong way round reports a conflicted merge as
#     clean — so the two branches stay explicit below.
#   * The --name-only output is THREE sections: the tree OID (line 1), the
#     conflicted paths, a BLANK LINE, then human-readable "Auto-merging ..." /
#     "CONFLICT (content): ..." messages. Stripping only line 1 leaves those
#     messages in the path list, where they match no policy glob and every
#     conflict reports as "unclassified". Cut at the blank line.
if probe=$(git merge-tree --name-only --write-tree "$base" "$UP" 2>/dev/null); then
  conflicts=""
else
  conflicts=$(printf '%s\n' "$probe" | tail -n +2 | sed '/^$/q' | grep -v '^$' || true)
  # Exit 1 with nothing named means merge-tree could not analyse it at all
  # (unrelated histories, or a git too old for this flag). Do not call that clean.
  [ -n "$conflicts" ] || die "merge-tree could not analyse the merge. Check git version (needs 2.38+) and that the histories are related."
fi

if [ -z "$conflicts" ]; then
  ok "merges clean"
  if $report_only; then info "--report: stopping before creating a branch"; exit 0; fi
  git checkout -b "$SYNC_BRANCH" >/dev/null 2>&1 || git checkout "$SYNC_BRANCH" >/dev/null 2>&1
  if ! git merge --no-edit "$UP" 2>&1 | tail -5 | sed 's/^/  /'; then
    # The probe said clean and the real merge disagreed: never leave a
    # half-merged tree behind for the next command to trip over.
    git merge --abort 2>/dev/null || true
    git checkout "$orig_branch" >/dev/null 2>&1 || true
    git branch -D "$SYNC_BRANCH" >/dev/null 2>&1 || true
    die "probe said clean but the merge conflicted — aborted and restored $orig_branch. Re-run to re-classify."
  fi
  ok "merged onto $SYNC_BRANCH"
  warn "clean ≠ correct. Read every function both sides touched before pushing."
  info "next: ./scripts/sync-upstream.sh --gates    then    ./scripts/sync-upstream.sh --push"
  exit 0
fi

n=$(printf '%s\n' "$conflicts" | grep -c . || true)
warn "$n conflicted path(s) — classified below, NOT resolved (that is judgment)"
head_ "Conflicts by policy"
keystones=0
while IFS= read -r f; do
  [ -n "$f" ] || continue
  IFS=$'\t' read -r pol ks <<<"$(policy_for "$f")"
  if [ "$ks" = "true" ]; then
    printf '  %s %-46s %s\n' "${RED}keystone${OFF}" "$f" "$pol"; keystones=$((keystones + 1))
  elif [ "$pol" = "manual" ]; then
    printf '  %s %-46s %s\n' "${YEL}unclassified${OFF}" "$f" "$pol"
  else
    printf '  %-8s %-46s %s\n' "" "$f" "$pol"
  fi
done <<<"$conflicts"

[ "$keystones" -gt 0 ] && warn "$keystones keystone path(s) — each needs a deliberate read, never a default"

cat <<EOF

${BOLD}To proceed${OFF}
  git checkout -b $SYNC_BRANCH
  git merge $UP                 # leaves the conflicts in the tree
  # resolve BY POLICY above; prefer the union when both sides only ADD entries
  # read the whole function afterwards, not just the marked region
  ./scripts/sync-upstream.sh --gates
  ./scripts/sync-upstream.sh --push

Any path shown as ${YEL}unclassified${OFF} is missing from $CFG — add it once you
have decided, so the next sync inherits the decision instead of re-deriving it.
EOF
