# Journal - clarezoe (Part 1)

> AI development session journal
> Started: 2026-09-24

---



## Session 1: Create, secure and publish ai-address-parser-debug skill

**Date**: 2026-09-24
**Task**: Create, secure and publish ai-address-parser-debug skill
**Branch**: `main`

### Summary

Authored a production debug playbook skill, de-identified real infrastructure before first commit, added data-protection and production-change guardrails, installed across 13 runtimes, pruned 14 dangling links, and diagnosed the Dashboard agent-kind 409.

### Main Changes

## What was done

Created, security-hardened, installed, committed and pushed the `ai-address-parser-debug`
skill — a reusable diagnosis-and-fix playbook distilled from a resolved production
incident in an AI-powered address-parsing feature.

Handoff taken over: `.trellis/handoffs/2026-09-24-16-04.md` (now `done`).

### Artifact

`skills/ai-address-parser-debug/SKILL.md` — 9-step workflow plus guardrails:
trace UI error to backend route; separate the root provider failure from secondary
enrichments; probe the configured model on the same endpoint/model/auth/payload;
verify the model is actually callable on the account (a model-list entry is not
proof); pick a right-sized fallback; update only the target env var while preserving
all others; redeploy and verify real feature behavior rather than a bare HTTP 200.

Companion to the existing `skills/ai-address-parser` skill (build vs. fix-in-prod).

### Security remediation (the substantive part of the session)

The first draft embedded real infrastructure identifiers. Since this is a PUBLIC
repo, those were removed before any commit — nothing leaked into git history.

- Real public IP, Dokploy instance name and app name → placeholders
  (`<dokploy-instance-name>`, `<app-name>`). Proxy and store domains removed.
- Two guardrails added after a static safety review:
  1. external probes must use synthetic or fully de-identified address data —
     never real customer addresses;
  2. production changes require an explicit confirmation gate showing target app,
     variable name and redacted change state before write/redeploy.
- Verified zero credential values, no destructive commands, no `config/`,
  `scripts/` or `logs/` payload files that could ride along (the failure mode that
  previously leaked `company.yaml` through a skill package).

### Install / validation

- Installed via `skillgenie update --global` into all 13 runtimes.
- Ran `setup.sh --agents` after discovering the default run does NOT import agents;
  `dev-inbox-planner` and `kirocrew-debugger` linked into `~/.agents/agents`.
- `skillgenie doctor --fix --prune` removed 14 dangling `edit-article` /
  `obsidian-vault` links across 7 runtimes; all installed skills now resolve.
- `skillgenie validate` clean for this skill (the 4 remaining failures pre-date it).

### Diagnosis: "selected agent choice is not available"

Not an install problem. Backend resolves `dev-inbox-planner` as `agent_kind=template`
and starts it successfully; the same name submitted as `member` produces exactly that
409. The Dashboard was submitting the wrong kind from stale pre-install frontend
state. Fix is a hard refresh / new chat, not a reinstall.

## Commit

`27c5950 feat(skills): add ai-address-parser-debug` — single file, pushed to
`origin/main`.

## Not done / deliberately left alone

- 15 pre-existing dirty paths (`3mf-print-editor`, `npm-publish`,
  `research-to-wechat`, untracked skill dirs and tooling dirs) — untouched,
  not part of this task.
- `skills.yaml` remains gitignored by design (names the private
  `Fei2-Labs/agent-skills` repo); public counterpart is `skills.yaml.example`.
- Paused parallel stream `.trellis/handoffs/2026-06-18-13-57.md` — author a
  "when to create a git worktree" decision rule/skill. Still paused, not executed.

## Lessons

- `setup.sh` does not sync agents unless `--agents` is passed. "Full sync complete"
  was an inaccurate claim until that flag was run.
- `skillgenie doctor --prune` alone only reports; pruning requires `--fix --prune`.
- A skill authored from a real incident inherits that incident's identifiers.
  De-identify before the first commit, while it is still untracked and free.


### Git Commits

| Hash | Message |
|------|---------|
| `27c5950` | (see git log) |

### Testing

- [OK] (Add test results)

### Status

[OK] **Completed**

### Next Steps

- None - task complete

---

## Session 2: Worktree decision skill, then a repo-wide identifier leak

**Date**: 2026-09-24 / 25
**Task**: Resume the paused worktree handoff; publish; then contain a leak it exposed
**Branch**: `main`

### Summary

Took over a handoff paused since 2026-06-18 and shipped the
`git-worktree-decision` skill, published it to ClawHub, and fixed a
misspelled CLI name in the tracked rules template. Verifying an unrelated
registry artifact then surfaced real identifiers inside tracked files of
this PUBLIC repo, which turned the session into a containment exercise:
redact, then rewrite history across all branches, then rename two remote
branches whose names carried a person's name.

### Main Changes

| Commit | Change |
|------|--------|
| `e872aa2` | `git-worktree-decision` skill (the paused handoff's deliverable) |
| `64defbd` | rules.example: corrected the ClawHub CLI binary name |
| `1fdf93f` | Replaced real identifiers in two skills with placeholders |
| (history) | `git-filter-repo` over 294 commits; force-pushed `main` |

Published `git-worktree-decision@1.0.0` to ClawHub (scan `scanner.llm.clean`).
Renamed two remote branches whose names embedded a personal name, a company
name, and a username, preserving 5 unmerged commits, then deleted the old
names. Full pre-rewrite backup: `~/skill-genie-backup-*.bundle`.

### Lessons

- **A rule can encode its own failure.** The publishing rule named a CLI
  binary that does not exist, and its last line said to skip and inform the
  user when that binary is missing. Every agent following it looked up the
  wrong name, landed in the skip branch, and reported a missing tool.
  Publishing had silently never run. A graceful-degradation clause turns a
  typo into permanent silence — when a rule has a skip path, verify the
  condition that triggers it, not just the happy path.

- **A denylist is itself sensitive.** While reporting a scan I printed the
  list of terms being scanned for. That list is an enumeration of real
  identifiers; echoing it leaked exactly what it exists to protect. Keep it
  in a mode-600 file, match against it, and report hits as redacted spans —
  never the pattern set.

- **Redact-and-commit is not removal.** Two files this session had already
  been "fixed" by a follow-up commit. `-S` search across all branches still
  found the originals in history. A new commit hides a value from the tip;
  only a rewrite removes it.

- **Binary blobs defeat text scanning.** `.pyc` files embed the compiler's
  absolute source path, so they carried a home-directory path that
  `git grep` cannot see and `--replace-text` cannot fix. They needed
  `--invert-paths`. Any scan that only greps text is blind to this class.

- **Branch names are unscanned surface.** Two remote branches carried a real
  name and a username. Branch names live outside commit content, so every
  pre-push content scan this project has run was structurally incapable of
  catching them. Scan refs, not just diffs.

- **Check ownership before assuming a published copy is yours.** Two skill
  names in the registry belong to other authors. The affected skills here
  were never published at all — the remediation item did not exist.

### Git Commits

| Hash | Message |
|------|---------|
| `e872aa2` | feat(skills): add git-worktree-decision |
| `64defbd` | fix(rules.example): ClawHub CLI name |
| `1fdf93f` | fix(skills): replace real identifiers with placeholders |

Earlier hashes recorded in Session 1 are invalid: the rewrite changed every
commit id in this repo.

### Testing

- [OK] `skillgenie validate` → 35/35 compatible
- [OK] Denylist scan across all 5 remote branches → 0 hits
- [OK] `-S` scan across full rewritten history (294 commits) → 0 hits
- [OK] ClawHub publication verified visible, not assumed from exit code

### Status

[OK] **Completed** — containment done; residual risk below

### Next Steps

- Old objects may remain reachable on GitHub by full SHA until GC; a Support
  ticket would be needed to force collection.
- Clones on other machines cannot fast-forward across the rewrite and must
  be re-cloned or hard-reset.
