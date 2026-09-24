---
name: "right-sized-solution"
description: "Pick the simplest solution that fits the user's ACTUAL constraints before building — and pivot when a dead-end undercuts the approach, instead of over-engineering, following an issue/spec literally, or shipping-and-flagging the heavy path. Use BEFORE implementing any feature, fix, or issue — especially when reaching for a 'standard'/heavyweight pattern (CI, auto-update, queues, microservices, frameworks, infra), when an issue/ticket prescribes a solution, or the moment you notice a constraint that makes part of the planned work dead weight ('this won't work without X')."
license: "MIT"
metadata: {"version":"1.0.0","category":"engineering","license":"MIT","tags":["engineering-judgment","scoping","anti-over-engineering","yagni","decision"],"hermes":{"tags":["engineering-judgment","scoping","anti-over-engineering","yagni","decision"]}}
---

# Right-sized solution: fit the constraints, pivot on dead-ends

A reflex to run BEFORE and DURING implementation so you build the simplest thing that actually solves the user's problem — not the textbook-complete version, and not the issue's literal wording.

## The two failure modes this prevents
1. **Spec-literal over-engineering.** An issue/ticket/user says "do it with electron-updater + GitHub Releases + CI" (or "add a queue", "use microservices", "set up a framework"). You implement exactly that — the conventional heavyweight pattern — without checking whether it fits the real setup. The stated solution is a *hypothesis*, not a mandate.
2. **Ship-and-flag the dead-end.** Mid-build you hit a constraint that guts the approach's value ("mac auto-update won't relaunch without code-signing"; "the org has Actions disabled"; "this needs a paid tier"). You note it as a caveat and ship the heavy thing anyway, or you defer to the obstacle ("user must enable X"). That flag was a signal to *pivot*, not a footnote.

## Before you implement — the fit check (30 seconds)
Ask, in order:
1. **What's the user's ACTUAL need?** State it in one plain sentence, stripped of the proposed mechanism. ("Know when there's a newer version" — not "have electron-updater auto-download a signed DMG from CI.")
2. **What's their real setup/constraints?** Who builds and deploys this? Solo dev or a team? What infra/auth/signing/secrets actually exist? What scale? One user or thousands? Self-hosted or managed?
3. **What's the SIMPLEST thing that meets the need under those constraints?** Start from the floor (a script, a button, a config line, a manual step, an existing tool) and only add weight when the simple version genuinely can't meet the need. Default to the simplest tier; justify every step up.
4. **If the simple version fits, propose it** — even when the issue/user named a heavier approach. One line: "The issue says CI+auto-update, but given you build from source solo and have no signing, a one-button 'check for updates' (GitHub API vs build sha) covers the real need with none of that. Want that instead?"

## During implementation — the pivot trigger
The moment you would write or say a sentence like:
- "This won't actually work without **\<signing / a paid plan / admin access / Actions enabled / a cert / a server\>**…"
- "Note: \<big chunk\> is dead weight until X is set up."
- "The user will need to manually enable X for this to function."

**STOP. That is a pivot trigger, not a caveat to ship with.** Re-run the fit check: does a different, lighter approach deliver the actual need WITHOUT the blocking dependency? If yes, switch to it (or surface the choice). Don't:
- ship the heavy path with the limitation flagged, or
- defer to "you go enable X" when a path that needs no X exists.

## Heuristics
- **The floor first.** A shell script, a single button, a cron line, a config flag, an existing CLI, or a manual step often *is* the answer. Reach for CI/services/frameworks/queues only when the simple version provably can't meet the stated need.
- **Constraints shrink the design space — use them.** "No signing", "solo dev", "no budget", "org policy off", "must be offline" each often eliminate the heavy option entirely and point straight at the light one.
- **One blocked dependency that gates most of the value = wrong approach, not bad luck.** Re-pick.
- **Match scale.** Building for thousands of users when there's one (or vice-versa) is the same error in two directions.
- **A spec is a hypothesis.** Push back with the lighter alternative when it fits better; that's not scope-dodging, it's right-sizing.

## Anti-patterns (don't)
- Implementing the issue's prescribed mechanism without questioning fit.
- Treating a value-gutting limitation as a release note instead of a redesign trigger.
- "Doing it properly" = adding infra/abstraction the situation doesn't warrant.
- Asking the user to set up heavy prerequisites when a no-prereq path exists.

## One-line test
> "If I strip away the proposed mechanism, what's the user's bare need — and what's the lightest thing that meets it under their real constraints?" Build that.
