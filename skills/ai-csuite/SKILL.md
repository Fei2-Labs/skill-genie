---
name: "ai-csuite"
description: "Runs a script-backed AI C-Suite strategic debate for SaaS teams. It builds a stage-aware executive roster, generates structured debate rounds, synthesizes a Chief-of-Staff brief, and outputs a CEO decision with action items. Includes security and output validation scripts designed for VirusTotal-safe distribution."
license: "MIT"
allowed-tools: "Read, Write, Edit, Bash, Glob, Grep, Task"
metadata: {"version":"2.1.2","mode":"prompt-plus-scripts","runtime":"python3-stdlib","license":"MIT","tags":["strategy","executive-debate","saas","decision-support"],"hermes":{"tags":["strategy","executive-debate","saas","decision-support"]}}
---

# AI C-Suite Multi-Agent Framework

Use this skill when the user needs a strategic decision on product, engineering, pricing,
go-to-market, hiring, operations, or competitive response.

The user's topic is: **$ARGUMENTS**

## Runtime Contract

This skill is operational via local scripts in `scripts/`:
- `prepare_session.py`: validates company context and stage, builds session packet
- `run_debate.py`: generates full multi-round debate + CEO decision
- `validate_output.py`: validates required output sections and fields
- `security_scan.py`: checks for suspicious code patterns for release safety
- `jev.py`: optional TypeSafe judgments, inert unless `--jev` is passed

No hidden network execution, no obfuscation, and no credential reads are required.

## Optional Jev Judgments

By default every judgment in this skill is deterministic: topic classification is
keyword matching, consensus is a vote count, confidence is a fixed `7`, and the
escalation rules below are documented but not checked. Passing `--jev` to
`run_debate.py` replaces those with real judgments from TypeSafe's Jev model.

```bash
python3 scripts/run_debate.py --topic "$ARGUMENTS" --company-file config/company.yaml --output logs/latest-decision.md --jev
```

What Jev decides, in two requests:

1. Topic category (`Choice` over the six decision areas).
2. After round 1 positions exist: consensus (`Choice` over the positions actually
   argued), reversibility (`Choice`), CEO confidence (`Score`, mapped to 0-10),
   and the five escalation rules (one `Noul` each, run in parallel).

Escalations at probability `>= 0.5` are rendered into the CEO brief risk flags
with their probability. Tune that threshold against real decisions rather than
treating it as a fixed rule.

Requires `TYPESAFE_API_KEY` in the environment. Without `--jev` the skill never
touches the network.

Fallback is total, and the output is byte-identical to a run without `--jev`.
A missing key, an unreachable or slow endpoint, a rejected key, a rate limit, a
malformed body, or a well-formed answer with an out-of-range or wrong-typed value
all degrade to the deterministic path with a warning; none of them fail the run.
Validation is atomic — a single bad field discards the whole verdict, so a run
never mixes judged values with static ones.

`scripts/test_jev_fallback.py` exercises 25 failure modes and asserts each one
reproduces the baseline output exactly. Run it after touching `jev.py`.

## Required Inputs

Load company context from:
- `config/company.yaml`

If missing, ask the user for:
- company name + product line
- stage: `solo | pre-seed | seed | series-a`
- ARR or MRR
- runway (months)
- team size
- constraints list

## Stage Profiles

| Stage | Debate Agents | Rounds |
|---|---|---|
| solo | CEO, CTO, CPO, CFO, CoS | 2 |
| pre-seed | CEO, CTO, CPO, CoS, CV | 2 |
| seed | CEO, CTO, CPO, CMO, CRO, CoS, CV | 3 |
| series-a | CEO, CTO, CPO, CFO, CMO, CRO, COO, CSA, CISO, CoS, CV | 3 |

Data brief agents are always:
- `CV` for customer signals
- `CFO` for financial constraints

If `CV` or `CFO` are not in the debate roster for that stage, they still provide pre-round data.

## Squads

| Squad | Members | Lead |
|---|---|---|
| Strategy | CEO, CFO, COO, CoS | CFO |
| Product | CTO, CPO, CSA, CISO | CPO |
| Growth | CMO, CRO, CV | CRO |

Intra-squad challenges are direct. Cross-squad challenges are mediated by CoS.

## Execution Steps

1. Security pre-check:
```bash
python3 scripts/security_scan.py .
```

2. Build session packet:
```bash
python3 scripts/prepare_session.py --topic "$ARGUMENTS" --company-file config/company.yaml
```

3. Run full debate:
```bash
python3 scripts/run_debate.py --topic "$ARGUMENTS" --company-file config/company.yaml --output logs/latest-decision.md
```

4. Validate output integrity:
```bash
python3 scripts/validate_output.py --file logs/latest-decision.md
```

5. Present result to user and ask:
- accept
- challenge
- rerun with constraints

## Debate Protocol

Use this exact order:
1. Pre-round Data Brief (`CV` + `CFO`)
2. Round 1 independent positions (`3-5` sentences each)
3. Optional human checkpoint
4. Round 2 rebuttals and challenges (`3-5` sentences each)
5. Round 3 convergence (`2-3` sentences, only 3-round stages)
6. CoS synthesis to CEO Brief
7. CEO decision with action owners

## Mandatory Output Shape

The final output must include:
- `DATA BRIEF (Pre-Round)`
- `CEO BRIEF`
- `CEO DECISION`
- `DECISION`
- `RATIONALE`
- `WHAT I WEIGHED`
- `OVERRIDES`
- `NEXT STEPS`
- `REVIEW TRIGGER`
- `CONFIDENCE`
- `REVERSIBILITY`

## Escalation Rules

Always enforce:
1. CISO legal/compliance risk must appear in CEO Brief
2. CFO runway risk under 6 months must include explicit severity
3. CV contradiction with consensus must be shown in brief
4. Deadlock after final round must show both sides
5. Radical position flips must be flagged

Rules 1, 2, 3, 4 and a groupthink check are evaluated automatically under `--jev`.
Without `--jev` they are your responsibility when presenting the result.

## Consensus Mechanics

Each role opens with its own category-specific position, so Round 1 is genuinely
contested rather than the same recommendation repeated. Consensus is a weighted
pick: a role whose remit covers the category counts double. When the top two
positions tie, the brief reports a deadlock and states that the CEO is breaking
the tie rather than ratifying agreement. Roles that lost are named under
`Key Tensions`, and a debate with no dissent says so explicitly instead of
presenting unanimity as strength.

## Quality Guardrails

1. Round 1 cannot be uniform agreement
2. No vague recommendations
3. Claims must tie to role or company context
4. CEO must state tradeoffs
5. CoS must probe for groupthink if consensus appears too early

## VirusTotal Safety Profile

Distribution-safe expectations:
- plaintext markdown and Python source only
- no encoded payloads, no runtime decoding
- no `eval`/`exec`/shell injection behavior
- no automatic outbound network calls; the only outbound call is to
  `api.typesafe.ai`, reached solely via stdlib `urllib` and solely when the
  operator passes `--jev`
- reads `TYPESAFE_API_KEY` from the environment only on that opt-in path, and
  never logs or writes it
- only local read/write in skill directory (`config/`, `logs/`)

## Compatibility

- Claude Code (via .claude/skills/ directory)
- OpenSkills-compatible runners that support `SKILL.md`
