---
name: "fork-upstream-sync"
description: "Sync a long-lived fork with its upstream without losing fork-specific divergences. Use when pulling upstream changes into a fork, resolving a fork/upstream merge, setting up automated upstream sync, or when an upstream merge silently reverted fork behavior. Covers merge-not-rebase, per-repo divergence manifests, conflict-class resolution policy, semantic (not just textual) merge verification, and three-bucket test-failure triage. Not for ordinary same-repo merges or rebasing a feature branch."
license: "MIT"
metadata: {"version":"1.0.0","category":"developer-tools","license":"MIT","tags":["git","fork","upstream-sync","merge","conflict-resolution","automation"],"hermes":{"tags":["git","fork","upstream-sync","merge","conflict-resolution","automation"]}}
---

# Fork ⇄ Upstream Sync

Keeping a fork current is not a git problem, it is a **divergence-preservation**
problem. `git merge` tells you whether two texts combine; it cannot tell you
whether your fork still behaves the way you built it to. Those are different
questions, and the second one is the one that bites.

Use this skill for any fork you carry deliberate changes in — a de-branded OSS
fork, a hardened internal build, a fork with features upstream rejected.

## The five rules

**1. Merge, never rebase.** Fork commits stay in history where a merge preserves
them. Rebase replays them onto upstream, multiplying conflicts and destroying the
record of which upstream sync introduced what.

**2. Land through a PR, never a direct push.** A textually clean merge routinely
hides semantic breakage (see rule 3). The PR is what makes the full CI matrix
adjudicate before it reaches your default branch.

**3. Textually clean ≠ semantically correct.** This is the rule people learn the
expensive way. The failure mode: your fork adds feature A, upstream adds feature
B, both touch the same function, git merges both hunks without conflict — and the
result is two features that each compile and neither connects. Real instance: a
folder-inherited project value was *computed* by the upstream half and *assigned*
by the fork half, the merge kept both blocks, and nothing wired the computation to
the assignment. No conflict marker. No type error. Just a silently dead feature.
**A merge is not done when the markers are gone. It is done when the suite is
green and every failure is accounted for.**

**4. An undefended divergence is a divergence you will lose.** Every deliberate
fork behavior needs a test that fails when upstream overwrites it. Without one,
the loss is invisible until a user reports it. With one, the next merge goes red
on the exact line. Recording the divergence in prose (a doc, a comment, a commit
message) does not defend it — only an assertion does.

**5. Never let automation resolve a conflict.** Automation's job is fetch, trial
merge, classify, run gates, open the PR. Choosing a side in a security or
authorization conflict is judgment; a script that guesses there fails toward
whichever side happens to be listed second.

## Prerequisites

```bash
command -v yq || brew install yq   # reads .fork-sync.yml; required
command -v gh || brew install gh   # opens the PR; optional but expected
gh auth status                     # must be authenticated for --push
```

## Onboarding a fork (once)

Run the installer from the target repo. It adds the `upstream` remote (detecting
the fork parent via `gh` when possible), installs the driver and the scheduled
workflow, detects the toolchain, harvests candidate gate commands out of the
repo's existing CI, spots baseline-shaped generated files, and scaffolds
`.fork-sync.yml` around what it found:

```bash
bash <skill>/assets/install.sh            # or: --upstream <url>, --force
```

It leaves `TODO` markers for everything a script cannot know. **Fill those in —
that is the actual onboarding work**, and it is what makes this fork's syncs
safe. Two sections matter most:

**`conflict_policy`** — put the security / auth / sandbox surfaces first, as
`fork_wins` + `keystone: true`. A wrong resolution there is a vulnerability, not
a bug. Globs are shell `case` patterns: `@(a|b)` for alternation, **never**
`{a,b}` (that matches the literal string, and the paths it was meant to cover
report as `unclassified` — silently).

**`divergences`** — the load-bearing section. Enumerate candidates from the
fork's own commits, then read what each one changed:

```bash
git log --oneline upstream/<branch>..<fork-branch>
```

Also mine the repo's `AGENTS.md` / `CONTRIBUTING.md` (a rule written there is
usually a divergence someone already lost once) and any past incident where an
upstream merge broke something. For each entry, name the test that fails if
upstream overwrites it. **No test ⇒ `pinned_by: null` ⇒ you will lose it** — so
either write the test now or record the gap honestly.

Then dry-run and confirm nothing you care about is `unclassified`:

```bash
./scripts/sync-upstream.sh --report
```

## Running a sync

```bash
./scripts/sync-upstream.sh          # fetch, report, trial-merge
./scripts/sync-upstream.sh --gates  # after resolving: gates + baselines + tests
./scripts/sync-upstream.sh --push   # push the branch, open the PR
```

The scheduled workflow does the same unattended: PR when the merge is clean,
**issue** (never a PR) when it is not, because a conflicted merge needs a person
before it needs a branch.

### Clean merge

The script pushes the branch and opens the PR. Read the diff for rule-3 hazards
anyway (any function both sides touched), then let CI decide.

### Conflicted merge

The script lists conflicts already classified by your manifest and flags which
ones touch declared-keystone paths. Then:

1. **Resolve by class**, per the manifest — not file by file, and not by picking
   whichever side looks newer.
2. **Prefer the union** when both sides *add* independent entries to the same
   list, set, or import block. This is the single most common shape in a fork
   merge and the one most often mis-resolved: two additions to a
   sensitive-paths list are two requirements, not a choice. Take both.
3. **Read the whole function after resolving**, not just the conflict region.
   Rule 3's failure mode lives in the lines the conflict markers did *not* cover.
4. **After every file**: `git add`, then confirm it parses.
5. Full detail and worked examples: `references/conflict-judgment.md`.

## Verifying (the part that actually catches the bugs)

Run `--gates`, then triage **every** failure into exactly one bucket:

| Bucket | Meaning | Action |
|---|---|---|
| **Real regression** | The merge broke it | Fix in-branch before merging |
| **Stale expectation** | Code intentionally changed; assertion did not | Update the assertion, state why in the commit |
| **Environmental** | Fails on the pre-merge commit too | Leave alone — prove it by checking out the merge base and re-running |

Rules for the triage:

- **Never skip a failure because it "looks environmental."** Prove it with a
  merge-base run. This is the whole difference between the three buckets.
- **A failure appearing on several PRs at once indicts the branch, not the PRs.**
  If three unrelated dependency bumps fail identically, the default branch is
  broken; stop rebasing PRs and fix the branch.
- **Regenerate baselines with the project's own toolchain**, never a bare
  `python3`/`node` that may resolve to a system version. A baseline written by the
  wrong interpreter is silently wrong and passes locally.
- **Update a PR branch once.** Repeated update/sync clicks stack merge commits and
  trip commit-count hygiene gates — turning one problem into two.

## Closing the loop

Whatever you learned this sync goes back into `.fork-sync.yml`:

- Fixed a real regression? Add the pin test that would have caught it (rule 4).
- Resolved a conflict class by judgment? Record that judgment as policy.
- Found a check that is permanently red for infra reasons? List it, so the next
  sync does not re-investigate it.

The manifest is the fork's memory. A sync that resolves conflicts without
updating it has paid the cost and kept none of the value.

## Bundled files

| File | Purpose |
|---|---|
| `assets/install.sh` | Onboards a fork: remote, driver, workflow, scaffolded manifest |
| `assets/fork-sync.config.yml` | Fully-commented manifest reference (the installer emits a shorter scaffold) |
| `assets/sync-upstream.sh` | Deterministic driver: fetch, classify, gates |
| `assets/sync-upstream.yml` | Scheduled workflow: PR when clean, issue when not |
| `references/conflict-judgment.md` | Resolution policy per conflict class, with worked examples |
