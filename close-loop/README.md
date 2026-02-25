# close-loop

High-signal end-of-session memory and shipping workflow for users, LLMs, and autonomous bots.

## Purpose

`close-loop` turns session wrap-up into a deterministic operating procedure:

1. close repo/task state cleanly,
2. produce reliable memory updates,
3. apply low-risk self-improvements,
4. queue publishable artifacts.

It is designed for low human overhead and supports autonomous mode selection.

## Who should use this

- User: says `wrap up`, `close session`, `end session`, or `/wrap-up`.
- LLM agent: executes the 4 phases and emits both human + JSON artifacts.
- `openclaw` bot: runs the adaptive strategy path (`openclaw` canonical mode; `adaptive` alias).

## Entry points

- Main workflow: `SKILL.md`
- Policy and mode logic: `components/01-design-principles.md`
- Ship actions: `components/02-phase-1-ship-state.md`
- Memory engine: `components/03-phase-2-memory.md`
- Output contract: `components/04-phase-3-4-and-output.md`
- Output template: `assets/templates/wrap-report-template.md`
- Framework references: `references/memory-frameworks.md`

## Quick run

1. Trigger with `wrap up` or equivalent phrase.
2. Apply action gates and auto-select strategy mode.
3. Run phases in strict order:
   - Phase 1: Ship State
   - Phase 2: Consolidate Memory
   - Phase 3: Review and Apply Improvements
   - Phase 4: Publish Queue
4. Emit two outputs:
   - Artifact A: human-readable report
   - Artifact B: machine-readable JSON

## Strategy modes

Supported mode inputs:

- `safe`
- `balanced`
- `openclaw`
- `adaptive` (alias; normalized to `openclaw`)

Canonical output mode values:

- `safe`, `balanced`, `openclaw`

Mode intent:

- `safe`: deterministic and conservative; static checks only.
- `balanced`: quality/speed compromise; bounded dynamic checks.
- `openclaw`: adaptive archive exploration with bounded autonomous retries.

## Auto-selection behavior

`close-loop` compares all strategies before choosing:

1. run static replay for `safe`, `balanced`, `openclaw`,
2. compute score: `strategyScore = utilityGain - riskPenalty - costPenalty`,
3. select highest non-violating strategy,
4. keep alternatives in output.

Tie-break rule:

- if margin is < 5%, prefer lower-risk strategy.

Human interaction policy:

- no manual mode question by default,
- ask only when irreversible external actions are policy-ambiguous.

## Memory persistence and retrieval

Memory model:

- working (ephemeral),
- episodic,
- semantic,
- procedural.

Write pipeline:

1. extract candidates,
2. verify provenance/dedupe/contradictions,
3. run static checks,
4. apply score/confidence/TTL/sensitivity gates,
5. write only accepted records.

Persistence targets:

- Native IDE memory store if available.
- If native memory is unavailable, persist session memory under:
  - `docs/memory/<YYYY-MM-DD_HHMM>-session.md`
- Project rule/config memory may also update:
  - `CLAUDE.md`
  - `.claude/rules/*`
  - `CLAUDE.local.md` (private/local context)

How the model reaches memory in future runs:

- by reading persisted files and/or host-provided native memory injection.
- `close-loop` itself is policy; persistence layer determines storage backend.

## Safety model

- Action gates for `commit`, `push`, `deploy`, `publish`.
- Prompt-injection and poisoning resistance in memory candidate filtering.
- Contradictions are not overwritten; conflicting records become `needs-review`.
- `openclaw` uses bounded reflection retries and cost/token budgets.

## Required output contract

Artifact A (human report sections):

1. Ship State
2. Mode Decision
3. Memory Writes
4. Findings (applied)
5. No action needed
6. Publish queue
7. Blocked items

Artifact B (JSON) includes:

- selected strategy input + canonical strategy
- candidate mode comparison
- memory evaluation and archive update
- safety block
- KPIs (noise, reuse, correction, precision, token overhead, cost per useful write, decision confidence)

Use:

- `assets/templates/wrap-report-template.md`

## Recommended bot behavior (`openclaw`)

For long or shifting tasks:

1. normalize `adaptive` to `openclaw`,
2. run static baseline first,
3. run dynamic checks only after static pass,
4. promote archive candidate only if utility and efficiency both improve,
5. fallback to `balanced` or `safe` on repeated failures.

## Troubleshooting

- No memory updates appear:
  - check provenance/score/TTL/sensitivity gates; rejected writes should show in report.
- Mode seems too conservative:
  - inspect `modeSelection` penalties and `decisionConfidence`.
- Memory cost too high:
  - inspect `retrievedTokenSize`, `endToEndMemoryCost`, and `costPerUsefulWrite`.
- Conflicting memory persists:
  - review `needs-review` records and evidence links before promotion.
