# Resolving fork/upstream conflicts

Read after the conflicts are in the tree and `sync-upstream.sh` has classified
them. Ordered by how much damage getting it wrong causes.

## Resolve by class, not by file

Going file-by-file makes each conflict a fresh decision and produces
inconsistency across a 30-file merge. Decide the *class* once — per the policy in
`.fork-sync.yml` — then apply it. The classes worth naming:

| Class | Policy | Why |
|---|---|---|
| Security / auth / sandbox | **fork wins** | The fork's hardening is usually the reason the fork exists. Adopt upstream only where it does not touch the hardened behavior. |
| Generated files, baselines, lockfiles | **take upstream, then regenerate** | Hand-merging generated content produces a file matching neither source. |
| App/UI structure | **upstream wins, re-apply fork fixes** | Upstream churns structure; carrying a fork's structural variant means re-resolving it every sync. Keep the *fixes*, not the structure. |
| Config schemas / enums | **union, then reconcile** | Both sides usually add values. See below — this is the most-missed case. |
| Docs | **union** | Two sides documenting different things is not a conflict, it is two paragraphs. |

## The union case — where most fork merges go wrong

When both sides only **add** independent entries to the same list, set, dict, or
import block, those additions are two requirements, not two candidates. Take
both. Choosing one silently drops whatever the other side added.

```python
# <<<<<<< HEAD  (fork)
    "run-coordinator",          # fork added this
# =======
    "kiro_pids.txt",            # upstream added this
    "kiro_pids.lock",
# >>>>>>> upstream
```

Both are entries on a sensitive-path list. Taking either side alone leaves a real
path unprotected. **Resolution: keep all of them.**

The same shape appears in import blocks (each side imports different symbols the
file now uses), capability sets, error-code tables, and i18n glossaries. Check
whether the dropped side's names are still referenced *elsewhere in the file* —
if they are, you have just created a `NameError` that only fires on the branch
nobody tested.

Where it is *not* a union: when the two sides change **the same** entry's value,
or when one side's implementation supersedes the other's. Then it is a real
choice, and the policy table decides.

## Textually clean is not semantically correct

**The single most expensive failure mode in this whole procedure**, because
nothing in git or the type checker reports it.

Shape: your fork adds feature A. Upstream adds feature B. Both edit the same
function, in different places. Git merges both hunks without a conflict. Both
features are present and neither works, because the wiring that connected one
half to the other was in a line neither hunk owned.

A real instance: upstream added a helper that resolved a folder-inherited project
value; the fork owned the block that assigned the session's project. The merge
kept both. Nothing assigned the resolved value — the helper's result was computed
and dropped. No conflict, no type error, no lint. Only a test that asserted the
end-to-end behavior caught it.

Three others from the same merge, all textually clean:

- A function was defined **twice** (both sides added their own copy at different
  offsets). Python takes the last definition — so the Windows-aware variant
  silently lost to the earlier one, on every platform.
- A backend gained a capability descriptor from upstream but the fork's separate
  process-marker registry never learned about it, so its processes became
  unreapable orphans.
- A UI banner was added by both sides in different places, so it rendered twice —
  and the test that looked for "the" banner found two and failed confusingly.

**Therefore, after resolving each file:**

1. Read the **whole function**, not the conflict region. The bug lives in the
   lines the markers did not cover.
2. `grep` for duplicate definitions of anything either side added:
   ```bash
   grep -oE "^(async def|def|class) [A-Za-z_][A-Za-z0-9_]*" FILE | sort | uniq -d
   ```
   (Expect false positives from code inside string literals — check before acting.)
3. Ask: *did either side add something that needs registering somewhere else?* A
   new backend, provider, handler, or capability usually has two or three
   registries that must agree.
4. Confirm every name the surviving code references is still imported, and every
   import is still used.

## Verify with the suite, then triage honestly

A resolved merge is not finished until the full suite has run and **every**
failure is in one of three buckets:

**Real regression** — the merge broke it. Fix in-branch before merging. If the fix
is not obvious, that is a signal the resolution was wrong, not that the test is
wrong.

**Stale expectation** — behavior changed on purpose and the assertion did not
follow. Update the assertion *and say why in the commit*. Two traps:
- A test pinning an exact source string (`inspect.getsource` substring checks) is
  usually pinning a security invariant. Read what it guards before editing it.
- A test asserting a fork divergence (e.g. "this set contains exactly X") will
  fail when upstream widens the set. That failure is the test **doing its job** —
  update the expected value, keep the assertion.

**Environmental** — fails on the merge base too. **Prove it:**
```bash
git stash && git checkout "$(git merge-base HEAD @{u})"
<re-run the failing test>
git checkout - && git stash pop
```
Only after it fails identically there may you set it aside.

Two discipline rules that matter more than they look:

- **Never skip a failure because it "looks environmental."** That instinct is how
  a real regression ships. The merge-base run costs a minute.
- **A failure appearing identically across several unrelated PRs indicts the
  branch, not the PRs.** If three independent dependency bumps fail the same way,
  stop rebasing them and go fix the default branch.

## Baselines and generated files

- Regenerate; never hand-merge. Take upstream's version, run the generator.
- **Use the project's own interpreter/runner**, spelled out in
  `.fork-sync.yml` → `toolchain`. A bare `python3` can be a system 3.9 while the
  project runs 3.12; the baseline it writes is silently wrong, and it will pass
  locally before failing in CI — or pass both and encode garbage.
- Regenerate **after** the tests pass, so the baseline records the state you
  actually verified.

## Operational traps

- **Update a PR branch once.** Repeated "update branch" clicks stack merge
  commits and trip commit-count hygiene gates. One failing check becomes two.
- **Do not push the fork's default branch directly**, even when nothing blocks
  it. The PR exists so the full matrix runs.
- **Distinguish a red *gate* from a red *repo setting*.** Checks that need
  credentials or a repo feature the fork lacks (license scanning, model-backed
  review) fail closed on every PR and are not yours to fix in a merge. Record them
  in `known_red` so the next sync does not re-investigate — and re-verify
  occasionally, because a stale entry masks a real failure.

## Close the loop

Every sync teaches something. Put it back in `.fork-sync.yml`:

- Fixed a real regression → add the pin test that would have caught it.
- Made a judgment call on a conflict class → record it as policy so the next sync
  inherits the decision.
- Found a permanently-red check → list it with its reason and its fix.
- Discovered an undefended divergence → write the test, then record it.

A sync that resolves conflicts and updates nothing has paid the full cost and
kept none of the value. The manifest is the fork's memory; prose in a commit
message is not.
