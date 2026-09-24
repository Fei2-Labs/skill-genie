---
name: "git-worktree-decision"
description: "Decide whether a piece of work deserves its own git worktree, before creating one. Use when about to start work that would disturb a dirty or warm working tree, when an urgent fix interrupts work in progress, when launching concurrent/parallel agent sessions on one repo, when tempted to `git stash` or `git switch` to make room, or when worktrees have accumulated and you need to know which should never have existed. Covers the concurrency test, the shared-external-state blocker that makes worktrees backfire, and the teardown commitment. Not a worktree how-to: mechanics, per-worktree ports, and dependency symlinking are out of scope."
license: "MIT"
metadata: {"version":"1.0.0","category":"engineering","license":"MIT","tags":["git","worktree","decision","parallel-agents","workflow","engineering-judgment"],"hermes":{"tags":["git","worktree","decision","parallel-agents","workflow","engineering-judgment"]}}
---

# When to create a git worktree

Every guide about worktrees explains **how** to make one. Almost none says **when**,
so the tool gets used as a reflex — and the cost lands later, as four half-set-up
checkouts holding branches you can't delete and can't remember.

This skill is only the decision. Make it before you type `git worktree add`.

## The one-line test

> **Do two working states of this repo need to be live at the same time?**

Live at the same time — not "both exist", not "both matter this week". If one can
finish, or even just pause cleanly, before the other starts, you want `git switch`,
not a worktree.

## What a worktree actually buys

A second working tree over the **same object store and the same branch namespace**.
That single sentence contains everything that makes the decision:

| Isolated | **Not** isolated |
|---|---|
| Working files, index, `HEAD` | Branch namespace — one branch, one worktree, enforced |
| Build outputs, caches, `node_modules` | The stash (`git stash` is repo-global) |
| Uncommitted/dirty state | Remotes, config, hooks, refs, objects |
| Per-tree tool state | **Everything outside git** — ports, databases, containers, daemons, `.env` singletons |

The right column is where worktrees go wrong. Not knowing it is how people create
one to run tests in parallel and then discover both runs are fighting over the same
dev database.

## Decide in four questions

Run them in order and stop at the first that answers.

**1. Is anything running or warm in the current tree?**
A reproduction you finally got, a debugger attached, a 6-minute build cache, a test
suite mid-run, a long `git bisect`. `git switch` throws that away and `git stash`
hides it somewhere repo-global you will forget. **→ Worktree.**

**2. Will two lines of work be edited concurrently — by two people, two agents, or you and a long job?**
**→ Worktree.** See the always-case below.

**3. Do I need both states visible at once?**
Diffing a regression against the last good tag, porting a fix between major
versions, running old and new side by side to compare output. Nothing sequential
gives you this. **→ Worktree.**

**4. Otherwise → no worktree.**
Switch the branch. Sequential work on a clean tree is what branches are for, and
the checkout you already have is set up.

## The always-case: concurrent agent sessions

**Two agents editing one checkout is not a slowdown, it is a correctness failure.**
They overwrite each other's edits with no conflict marker — git never sees it,
because it never reached the index. Worse, each agent's test run observes the
other's half-written files, so *both* results are noise: a green run proves nothing
and a red run points at the wrong cause.

So: **concurrent sessions always get a fresh branch and a fresh worktree, never
shared `main`.** This is the one case where you skip the cost/benefit entirely —
the shared-tree option isn't slower, it's invalid.

Corollary for a single agent: if you are about to spawn parallel work on one repo,
decide the worktree layout *before* launching, not after the first collision.

## The blocker check (do this before `worktree add`)

A worktree duplicates files. It does **not** duplicate the world those files talk to.
Before creating one, name every singleton the work touches:

- a **fixed port** in a committed config
- a **dev database** or a shared schema/migration state
- a **named container**, volume, or `docker compose` project
- a **daemon / watcher / language server** bound to one absolute path
- an `.env` with a token that only one session may hold at a time
- a **lockfile outside the repo** (global package cache, license daemon)

If any exist, the worktree gives you two checkouts racing over one resource, and the
failures look like flaky tests rather than like what they are. Two honest ways out:

- **Parameterize the singleton** (per-worktree port, per-worktree DB name / compose
  project) — this is the real setup cost of worktrees, and it is worth paying once
  per repo if you will do this often; or
- **Don't use a worktree.** Sequence the work instead. A worktree whose external
  state collides is worse than the branch switch it replaced.

Deciding "I'll sort it out when it breaks" is choosing the flaky-test outcome.

## Don't create one when

- The change is trivial and the tree is clean — just switch.
- You're **already** on the right branch in the current tree.
- The work is short and setup is long (a large install, migrations, a codegen step).
  Setup cost is per-worktree; if setup exceeds the task, the worktree *is* the task.
- You only want to *look* at another branch: `git show`, `git diff`, `git log -p`,
  or `git restore --source` read other commits without a second tree.
- The repo has heavy submodules — they are not shared and must be re-initialized
  per worktree. Weigh that before, not after.

## Teardown is part of the decision

Creating a worktree commits you to removing it. An abandoned one keeps its branch
checked out, which silently blocks `git branch -d`, keeps stale build output on
disk, and makes `git worktree list` useless as a picture of what's in flight.

So decide up front, in one sentence: **what event ends this worktree?** ("Merged",
"spike answered", "the agent run finishes.") If you can't name the end, you're not
making a worktree — you're making a second permanent checkout, and should say so
deliberately.

Then actually do it:

```bash
git worktree list                 # what exists, and is any of it finished?
git worktree remove <path>        # removes the tree; refuses if dirty
git worktree prune                # clears records of trees deleted by hand
```

Sweep at the natural boundary — end of session, or right after a merge. Not "later".

## Decision record

| Situation | Worktree? | Why |
|---|---|---|
| Concurrent agents / people, one repo | **Always** | Shared tree corrupts edits and invalidates both test runs |
| Urgent fix while mid-debug, tree warm | **Yes** | Preserves the reproduction and the cache |
| Long build/test/bisect holding the tree | **Yes** | The tree is occupied; you need a second one |
| Compare two versions side by side | **Yes** | Sequential checkout can't show both |
| Review a colleague's branch, keep yours running | **Yes** | Both states must be live |
| Throwaway spike with a named end | **Yes** | Isolation is the point; teardown is cheap |
| Sequential work, clean tree | No | `git switch` |
| Trivial single-file edit | No | Setup exceeds the change |
| Already on that branch here | No | Nothing to isolate |
| Just reading another commit | No | `git show` / `git diff` / `git log -p` |
| Work depends on an un-parameterized singleton | No — **fix the singleton first** | Two trees, one port/DB ⇒ flaky failures |

## Mechanics are deliberately out of scope

Once the decision is *yes*, the setup problems — copying `.env`, linking or
installing dependencies, assigning a deterministic port per worktree, sweeping stale
trees — are solved work with existing tools. Crib from prior art rather than
reinventing; keep this skill about the choice.
