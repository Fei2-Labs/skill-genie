---
name: close-loop
description: End-of-session workflow for shipping changes, consolidating memory, applying self-improvements, and preparing publishable outputs with safety gates.
license: MIT
metadata:
  version: 2.0.0
  category: session-memory
---

# Close Loop

Use this skill when the user says "wrap up", "close session", "end session", "close out this task", or invokes `/wrap-up`.

Run four phases in order and return one consolidated inline report.

## Design principles

- Treat memory as a system, not a dump: working, episodic, semantic, procedural.
- Write memory only with evidence and confidence.
- Prefer idempotent actions and deterministic outputs.
- Keep high-impact side effects gated.

## Execution policy

- Default is execution mode: perform actions directly.
- Ask exactly one minimal question only when blocked by unclear irreversible operations.
- Only push, deploy, or publish externally when explicitly requested in this session or preapproved by project policy.

## Phase 1: Ship State

1. Find touched repos and run `git status` in each.
2. If uncommitted changes exist, commit with descriptive messages.
3. If push is allowed by policy, push to remote; otherwise report ready-to-push commands.
4. Validate file placement and naming conventions for files created in this session.
5. Move misplaced document files (`.md`, `.docx`, `.pdf`, `.xlsx`, `.pptx`) to the correct docs location when applicable.
6. Detect deploy scripts/skills and run only if deploy is approved.
7. Reconcile task tracking: close completed items, flag stale or orphaned items.

## Phase 2: Consolidate Memory

Extract candidate learnings from the full session transcript and classify each item:

| Type | Meaning | Default target |
|---|---|---|
| Working | Short-lived execution context | Do not persist after report |
| Episodic | What happened in this session | Auto memory |
| Semantic | Stable project facts and conventions | `CLAUDE.md` or project rules |
| Procedural | Reusable workflow patterns | `.claude/rules/` or skill docs |

Use this write filter:

`score = novelty + stability + reuse + evidence - sensitivity`

- Each factor is scored `0..2`.
- Persist only when `score >= 5`.
- Require provenance for every persisted item: source step, evidence snippet, confidence.
- Deduplicate against existing memory before writing.
- Never persist secrets, tokens, private keys, or personal sensitive data.

## Phase 3: Review and Apply Improvements

Review the session for actionable findings:

- Skill gap
- Friction
- Missing knowledge
- Automation opportunity

Apply low-risk improvements immediately:

1. Update relevant `CLAUDE.md` or scoped rule files.
2. Save stable insights to memory with confidence labels.
3. Draft skill or hook specs for repetitive patterns.
4. Commit improvement changes separately from feature commits when possible.

If the session is routine with no actionable findings, state: `Nothing to improve`.

## Phase 4: Publish Queue

Scan the session for publishable material:

- Debugging story with clear lesson
- Reusable technical pattern
- Milestone or release-worthy update
- Educational walkthrough

If suitable content exists:

1. Create draft(s) under `Drafts/<slug>/<Platform>.md`.
2. Propose the best first post and schedule spacing for the rest.
3. Do not auto-post unless explicitly requested.

If nothing is suitable, state: `Nothing worth publishing from this session`.

## Output contract

Return one concise report with these sections:

1. `Ship State`
2. `Memory Writes`
3. `Findings (applied)`
4. `No action needed`
5. `Publish queue`
6. `Blocked items` (only if any)

Every memory write must include:

- destination
- item text
- confidence (`low`, `medium`, `high`)
- evidence source

Use `assets/templates/wrap-report-template.md` as the default report skeleton.

## Guardrails

- Do not claim deployment if no deploy command was run.
- Do not claim push if push was gated.
- Do not create extra summary files unless the user asks.
- Keep edits scoped to requested outcomes.

## Framework alignment

- InfiAgent: infinite-horizon state and cross-session continuity.
- Letta + LangGraph: explicit memory blocks and typed state separation.
- A-MEM: selective memory formation and consolidation.
- Rowboat: event-threaded orchestration and observability.
- AgentSys and A-MemGuard: memory integrity and poisoning defenses.

## Resources

- `references/memory-frameworks.md`
- `assets/templates/wrap-report-template.md`
