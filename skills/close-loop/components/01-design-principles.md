## Design principles

- Treat memory as a system, not a dump: working, episodic, semantic, procedural.
- Write memory only with evidence and confidence.
- Prefer idempotent actions and deterministic outputs.
- Keep high-impact side effects gated.
- Keep memory auditable, reversible, and minimally invasive.

## Execution policy

- Default is execution mode: perform actions directly.
- Ask exactly one minimal question only when blocked by unclear irreversible operations.
- Only push, deploy, or publish externally when explicitly requested in this session or preapproved by project policy.
- Support `dry-run` mode to compute all actions and memory writes without side effects.

## Action gate matrix

| Action | Allowed | Ask | Blocked |
|---|---|---|---|
| Commit | Local repo changed and message is clear | Unclear scope for staged files | Repo locked or no write permission |
| Push | Explicit user request or explicit project policy | Ambiguous policy status | User says no push |
| Deploy | Explicit user request or explicit deploy policy | Deployment target unclear | No deploy script/skill or user says no deploy |
| Publish | Explicit user request | Platform/schedule ambiguous | No user approval |

## Memory design abstraction (ALMA-inspired)

Treat memory policy as a design tuple `M = (U, D, R)`:

- `U` update policy: extraction, filtering, consolidation, retention.
- `D` data schema: record fields, TTL, status, provenance links.
- `R` retrieval policy: ranking, conflict handling, and context assembly.

Required interfaces:

- `general_update(session_artifacts)` for write-path logic.
- `general_retrieve(query_context)` for read-path logic.

## Evaluation modes

- `static`: replay fixed evidence without further writes; use to evaluate candidate policy safely.
- `dynamic`: allow updates during sequential tasks; use after static checks pass.

## Autonomous strategy modes

| Mode | Goal | Behavior |
|---|---|---|
| `safe` | Minimize risk | Deterministic writes, static-only checks, no exploration |
| `balanced` | Balance quality and speed | Static checks first, limited dynamic updates |
| `openclaw` (`adaptive` alias) | Maximize autonomous adaptation | Archive-driven exploration, dynamic updates, bounded self-reflection |

Alias normalization:

- If input mode is `adaptive`, normalize to canonical mode `openclaw`.
- Output uses canonical value `openclaw` in machine-readable JSON.

## Auto-selection policy (no manual choice by default)

The AI must choose mode automatically from context signals:

| Signal | Low | Medium | High |
|---|---|---|---|
| Memory risk | stable memory state | minor contradictions | sensitive domain or repeated conflicts |
| Environment volatility | repeated tasks | moderate task drift | frequent distribution shifts |
| Optimization pressure | routine session | moderate improvement need | explicit performance/cost pressure |

Decision rules:

1. If `memory risk` is high, choose `safe`.
2. Else if `environment volatility` or `optimization pressure` is high, choose `openclaw`.
3. Else choose `balanced`.

Only ask the user when irreversible external actions are blocked by policy ambiguity.
