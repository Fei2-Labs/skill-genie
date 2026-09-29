# ChatGPT Web Delegation Contract

## 1. Scope / Trigger

This spec governs `skills/chatgpt-web-delegation/`.

Trigger: the skill adds a Python command that validates a browser capability snapshot, sends three independent Jev Choice questions, and returns a typed routing receipt. It does not drive a browser or call ChatGPT API.

## 2. Signatures

### CLI

```text
python3 scripts/route.py < reviewed-request.json
python3 scripts/route.py --example-input
python3 scripts/route.py --example-output
```

Input: one UTF-8 JSON object on stdin.

Output: one JSON object on stdout. Errors use nonzero exit codes and contain only a stable error code and safe message.

### TypeSafe API

```text
POST https://api.typesafe.ai/v1/systemone
Authorization: Bearer $TYPESAFE_API_KEY
Content-Type: application/json
```

Request contains `model: "jev-latest"`, structured `state`, and keyed `questions`.

## 3. Contracts

### Input

Required fields:

- `task_summary`: non-empty sanitized string, at most 12,000 characters.
- Direct `route_task()` callers and CLI input both enforce a serialized UTF-8 input limit of 64 KiB before validation or network access. Unknown fields do not bypass this limit.
- `mode`: one of `chat`, `search`, `research`.
- `disclosure_reviewed`: boolean `true`; caller confirms both Jev and ChatGPT transfers.
- `ui.snapshot_fresh`: `true`.
- `ui.origin`: exactly `https://chatgpt.com`.
- `ui.authenticated`: `true`.
- `ui.selected_mode`: same value as `mode`.
- `ui.models`: one to 32 observed models. Each model has unique `id`, `description`, `effort_control`, and a valid effort list.
- `ui.mode_compatibility[mode]`: unique IDs referring only to observed models; list must not be empty.

Model effort contract:

- `effort_control: "available"` requires one or more unique observed efforts.
- `effort_control: "none"` requires an empty effort list. Code may select only `default_no_effort_control`.

### Jev questions

One request contains these independent Choice questions:

- `route`: `delegate`, `keep_local`, `clarify`.
- `model`: compatible observed model IDs plus `no_suitable_model`.
- One speculative effort question per compatible observed model. No effort question is needed for `no_suitable_model`.

Each consumed Choice answer must include `choice`, probabilities for exactly every offered option, and finite `confidence` from 0 through 1. Probabilities must be finite, non-negative, at most 1, sum to 1 within `1e-6`, and have a maximum at `choice`. Tied maxima are valid distributions but resolve to `clarify`. Low confidence and insufficient lead also resolve to `clarify`, including when a sentinel is selected.

Non-delegation consumes only `route`. A suitable, unambiguous delegation route additionally consumes `model`; only an unambiguous observed model requires its effort answer. Missing or malformed unused branches do not invalidate a result. Duplicate JSON keys and nesting exceeding the JSON parser's recursion limit are rejected globally.

### Result

Successful result contains `ok: true`, effective `route`, `action`, and `receipt` with all consumed decisions, probability spreads, confidence, requested mode, and provisional thresholds. Selected model and effort appear only after consuming the effort branch; unconsumed decisions are omitted.

`route: "delegate"` additionally contains `selection`. `keep_local` and `clarify` contain `action: "no_web_action"` and never authorize browser work.

### Environment and ownership boundary

- Every account, credential, browser session, endpoint, and local configuration belongs to the user invoking the skill. Never embed or inherit the skill author's key, vault entry, filesystem path, browser profile, CDP port, or other machine-specific setting.
- `TYPESAFE_API_KEY` is required only for Jev requests. Read it from the current process environment at request time, so repeated calls use the current caller's value rather than a value captured at import or installation time. Never print, persist, or include it in errors. No vault access belongs in `route.py`.
- Browser attachment is outside `route.py`; the agent must discover and authorize the invoking user's browser tool, session, and endpoint at runtime. A missing prerequisite is a concrete failure, never a fallback to another user's configuration.

## 4. Validation & Error Matrix

| Condition | Stable error code | Network call | Browser action |
|---|---|---:|---:|
| Invalid JSON, wrong type, duplicate candidate, or schema violation | `invalid_input` | No | No |
| Input exceeds 64 KiB | `input_too_large` | No | No |
| Disclosure flag is not `true` | `disclosure_not_reviewed` | No | No |
| Snapshot is stale or mode changed | `ui_stale` | No | No |
| Requested mode has no compatible observed model | `ui_unavailable` | No | No |
| Origin is not exact ChatGPT origin | `wrong_origin` | No | No |
| Snapshot is not authenticated | `not_authenticated` | No | No |
| Missing Jev key | `missing_key` | No | No |
| Jev redirect | `redirect_rejected` | Attempted endpoint only | No |
| Jev 401 / 422 | `http_401` / `http_422` | Yes | No |
| Jev 429 / 529 after bounded retries | `http_429` / `http_529` | Yes | No |
| Jev timeout, transport failure, oversized or malformed response | Stable transport code | Yes | No |
| Missing consumed answer, unknown choice, non-finite probability, non-maximal choice, bad sum, duplicate JSON key, or excessive nesting | `invalid_response` | Yes | No |
| Tied maximum, or route probability, lead, or confidence below provisional thresholds | `clarify` result | Yes | No |
| `keep_local`, `clarify`, `no_suitable_model`, or `no_suitable_effort` | Non-delegation result | Yes | No |

The helper never falls back to ChatGPT API or invents model/effort values.

Transport limits: 64 KiB serialized request, 256 KiB response, 20-second socket timeout, and at most three attempts for 429/529. Socket timeout is not a total wall-clock deadline. The agent must impose an external process deadline (documented example: GNU `timeout 75s`) and treat termination or absent JSON as failure, never delegation. Direct Python callers must impose their own deadline. Only helper-generated errors guarantee a JSON response.

## 5. Good / Base / Bad Cases

- Good: fresh authenticated snapshot, reviewed sanitized task, compatible observed model, unambiguous Jev answers. Return `delegate` and exact observed model/effort.
- Base: Jev selects `keep_local`, `clarify`, or a verified default effort. Return safe non-delegation or explicit default; do not silently substitute.
- Bad: login wall, stale capability snapshot, sensitive content without specific authorization, malformed Jev answer, or ambiguous submit state. Stop and report stable observable failure. Do not send prompt or retry an ambiguous browser submit.

## 6. Tests Required

`python3 -m unittest discover -s skills/chatgpt-web-delegation/scripts -p 'test_*.py' -v` must assert:

- route, model, and selected-model-only effort decisions;
- default effort and sentinel non-delegation behavior;
- low confidence and near ties clarify, including selected effort sentinels;
- unused branches do not invalidate non-delegation or uncertain-model results;
- duplicate-key and excessively nested JSON produce safe CLI/response errors;
- real redirect handler rejects 301/302/303/307/308 and closes the response;
- invalid input and unavailable UI make no network call;
- missing key, redirect, timeout, HTTP status, oversized, malformed, and non-byte responses map to safe errors;
- error output excludes task secrets and API keys;
- consecutive requests read the current caller's `TYPESAFE_API_KEY`, rather than an import-time or author-owned value;
- a missing key raises `missing_key` and the network opener is never called;
- CLI examples remain offline and use fictitious labels;
- Python compilation and `./skillgenie validate` pass.

Live browser verification is conditional. If no authenticated browser exists, report skipped with observed attach or login blocker. Never claim live model, effort, Search, or Deep research availability from fixtures.

## 7. Wrong vs Correct

### Wrong

```text
Send full browser conversation to Jev, choose a hardcoded model alias, then call ChatGPT API when browser attach fails.
```

### Correct

```text
Review minimized text, verify fresh visible UI, pass only observed capability labels to Jev, re-check UI, then use visible ChatGPT controls once.
```

Jev output is routing data, not authorization, browser proof, or fact verification.
