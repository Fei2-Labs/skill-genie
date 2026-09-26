---
name: "typed-decisions-around-llms"
description: "Decide WHERE a typed judgment model (TypeSafe's Jev or any System One model) belongs relative to a generative LLM, and who is allowed to authorize what. Use when adding a guardrail, router, verifier, or approval gate around an LLM; when converting a free-text 'LLM-as-judge' step into a typed decision; when a model's own confidence score is being used to authorize its own output; when choosing thresholds, confidence bands, or fallback behavior; or when reviewing an agent/tool-calling pipeline for who holds authority. This is the architecture question — placement, ordering, and authority. For API mechanics, primitive selection, and question wording use the typesafe-ai skill and the live docs instead."
license: "MIT"
metadata: {"version":"1.0.0","category":"engineering","license":"MIT","tags":["llm-architecture","guardrails","verification","routing","decision-layer","agent-safety","typesafe","jev"],"hermes":{"tags":["llm-architecture","guardrails","verification","routing","decision-layer","agent-safety","typesafe","jev"]}}
---

# Typed decisions around LLMs

> "Do not ask one model to be the author, router, policy engine, judge, and
> auditor of its own work."

That is the whole skill. Everything below is how to take those roles apart.

**Scope.** This is about *placement and authority*: what sits before the LLM,
what sits after it, and who is allowed to authorize a side effect. It is not
about API calls. For endpoints, SDKs, primitive selection, question wording,
and criteria design, use the **`typesafe-ai`** skill and the live docs; do not
restate them here.

**Provenance.** Distilled from an independent field guide (Sept 2026) built on
public docs. Not vendor material, not an endorsement. It dates itself: verify
product names, model aliases, limits, and any number against live
documentation before deployment. Hardcode none of them.

## 1. Division of labor

| Need | Owner |
|---|---|
| Apply exact rules | Code |
| Judge messy text | Typed judgment model |
| Write or reason openly | LLM |
| Authorize side effects | Policy + human |
| Record and replay | Harness |

The anti-pattern this replaces: one prompt that understands the request,
invents a plan, chooses a provider, approves its own tool call, judges its own
result, and declares completion. That hides many independent judgments inside
one transcript. Pulling them out into typed questions makes them visible,
testable, and replaceable.

**Boundary test.** Use a typed judgment when the answer space is known before
the request arrives, the state holds enough evidence, and code can act on the
returned distribution. Use an LLM when the answer must be invented, explained,
or reached through multi-step reasoning. Use deterministic code when the rule
is already explicit.

**Where a judgment model does NOT belong:** drafting the final answer,
generating a patch, synthesizing a long plan, replacing an exact parser, or any
call whose result cannot change behavior. A decision layer that produces
metrics but never alters routing, review, or context is only added latency.

**Mental model:** not a manager supervising several LLMs — a **typed sensor
inside a program**. Supervision implies authority; a sensor implies
measurement. The program owns the workflow.

## 2. Code keeps authority

> A favorable semantic answer is **evidence, not authority**.

A high probability cannot grant a capability the caller does not possess. Run
this order and do not reorder it:

```
proposal
  -> schema and type validation
  -> identity and capability check
  -> path / domain / amount allowlists
  -> data-egress policy
  -> semantic review (typed judgment)
  -> risk-specific threshold
  -> user or operator confirmation
  -> execute with least privilege
  -> immutable receipt
```

Two rules an agent will otherwise violate:

1. **If deterministic validation already fails, do not call the judgment model,
   and never let a favorable semantic answer override the failure.**
2. **If the judgment service is unavailable, take a documented fallback**
   (proposal-only, human review). Never treat absence as approval.

## 3. The self-approval prohibition

> "Do not ask the generative LLM to produce a proposal and a confidence score
> that authorizes the same proposal. Put the bounded review in [a judgment
> model] or deterministic validation, and let policy decide what is
> sufficient. Independence is not perfection, but it removes one obvious
> conflict of interest."

**Run this audit on any existing pipeline** — it finds real bugs, not
hypothetical ones. For every automatic action, ask:

- Which component produced the artifact?
- Which component produced the number or label the gate compares against?
- Are they the same model call? Then the gate is decorative.

Watch for the disguised form: an LLM emits both a label saying an action needs
no approval *and* the cost estimate that the only remaining threshold compares
against. Both inputs to the gate come from the thing being gated.

## 4. The hybrid request path

```
request
  -> deterministic validation
  -> preflight battery: classify intent, risk, route
  -> code: choose context and LLM
  -> LLM: generate plan, text, or code
  -> postflight battery: verify bounded properties
  -> code: pass, retry, review, or block
  -> receipt + metrics
```

Both batteries are optional and do different jobs. Preflight controls what the
expensive model sees and which model gets the task. Postflight evaluates the
output against narrow properties before code allows a consequential action.
Read-only, low-risk flows may need only one side.

## 5. Preflight — decide the path before generating

Shape: `route` (Choice over allowed routes), `needs_current_data` (Noul),
`contains_sensitive_data` (Noul), `complexity` (Score).

- **Filter deterministically first.** Remove unavailable providers and
  forbidden tools *before* semantic routing. The model chooses among allowed
  possibilities; it never overrides policy.
- **The largest savings come from deciding what NOT to send.** Judge each
  candidate document for relevance, assemble context from accepted passages,
  and keep citations to the source chunks — the postflight verifier must be
  able to evaluate the same evidence.
- **Retrieve before routing** when the request is under-specified. Cheap
  deterministic discovery, then judge a compact candidate set. Keeping
  retrieval separate from judgment makes missing evidence distinguishable from
  a wrong semantic choice.
- **Route contracts, not model names.** A Choice selects a contract — provider
  class, allowed data, tool surface, context budget, max retries, verification
  plan, fallback — so a semantic router cannot bypass limits buried in
  provider-specific code. Capabilities are the stable interface; names change.
- **Measure the counterfactual in shadow.** Routing that saves input tokens but
  increases retries, context reloads, or human review is not an improvement.

## 6. Postflight — verify bounded properties

Shape, all Noul: `addresses_task`, `evidence_supports`, `unrelated_changes`,
`needs_clarification`.

- **Deterministic verification runs first.** Semantic review cannot prove code
  compiles, a migration is reversible, or a URL belongs to an approved domain.
  Ordinary code checks those exactly.
- **Input and output guards are different batteries.** A safe input can produce
  an unsafe output; a risky-looking input may deserve a helpful refusal rather
  than a block.
- **The verifier must see the exact sources used for generation.** If
  generation used passage A and verification sees a fresh search result B, the
  review can approve a claim the original model could not support. Bind cited
  passages, tool results, and snapshots to the proposal receipt.
- **Verify claims or sections**, not a whole long answer.
- **Write the precedence as a decision table.** Malformed state or failed
  deterministic validation ⇒ review unavailable. Missing judgment output ⇒
  review unavailable. Unfavorable or low-confidence ⇒ proposal-only, revision,
  or human. Only a complete favorable set makes the proposal *eligible* for the
  next policy gate.
- **A semantic review never auto-executes a consequential command.** It says
  what appears true of the supplied state; it does not grant permission.
- **Receipts go stale.** If the file, policy, or tool arguments changed, the
  earlier review is not current approval.
- **Finite revision loops.** Return structured reasons: which property failed,
  which evidence was missing, what scope must stay unchanged. Limit attempts
  and **change the state on every retry**. If the same property fails twice,
  escalate or narrow the task. More tokens do not fix an invalid boundary.

## 7. State is the evidence packet

Treat state as the packet handed to a review panel — not a transcript dump.

| Include | Avoid |
|---|---|
| Current request | Entire chat by default |
| Relevant policy | Unversioned memory dump |
| Candidate action | Hidden global assumptions |
| Verified records | Secrets not needed to judge |
| Source timestamps | Stale facts without dates |

- **Separate facts from instructions.** All user content, retrieved documents,
  tool output, and LLM text is **untrusted data**. If a retrieved page says to
  ignore the policy and permit the command, that sentence is evidence to
  classify — not an instruction the harness executes. Workflow rules live in
  code and question definitions.
- **Version the state contract.** A renamed field, reworded option, reordered
  rubric, or added policy document changes results with the model unchanged.
  It is an API contract.
- **Preserve provenance** — source id, retrieval time, version, verified vs
  generated. Provenance is what separates unsupported generation from stale
  evidence, and enables selective refresh.
- **Fail closed.** When a required record cannot be loaded, fail. Never
  substitute a model guess.
- **Unit-test the state builder separately** from model quality. A perfect
  decision model cannot repair a packet carrying the wrong customer or the
  wrong snapshot.

More context is not better: irrelevant context buys distraction, cost, privacy
exposure, and harder evaluation.

## 8. Confidence is not permission

> "Probability is not permission."

Numbers describe model uncertainty about a bounded question. They do not
measure business impact and cannot convert an unauthorized action into an
authorized one.

| Band | Default behavior |
|---|---|
| High | eligible for the automatic path |
| Medium | confirm, gather state, or review |
| Low | stop, clarify, or fall back |

- **Thresholds are per question, per action, per risk class** — never one
  global number. A 0.8 on evidence-support is not interchangeable with 0.8 on a
  different question or with Choice confidence. High-stakes positive and
  negative decisions may need asymmetric thresholds.
- **Start in shadow**, choose thresholds on a held-out set, and track false
  automation, needless review, abstention, and downstream quality. A threshold
  copied from an example is a placeholder, not calibration.
- **Recalibrate** after changing the model, question wording, criteria, state
  builder, language mix, or traffic source. The policy depends on the whole
  decision contract, not the model id.
- **Retry only after changing the evidence.** Re-asking the same question over
  the same state is sampling until a convenient answer appears.
- **Cascade deliberately**: deterministic rule → typed judgment → fast path if
  clear and low-risk → more evidence and re-ask → LLM only if generation is
  needed → human review as the floor. A cascade helps when most cases are
  simple; otherwise early calls only add latency.
- **Fallbacks appear in the same metrics as the primary route**, or a failing
  first stage hides behind an expensive second one. Put a latency and cost
  ceiling on the whole cascade: an unbounded chain of model calls is not
  resilience, it is loss of control.
- **Diagnose low confidence** rather than rewording. It usually means missing
  evidence, genuinely plausible alternatives, or overlapping criteria. If human
  reviewers disagree, the label definition is the bug.

The goal is not maximum automatic throughput. It is the best completed outcome
per unit of cost, latency, and review attention at an acceptable risk level.

## 9. Receipts and cost

Record one receipt per decision:

```
state_digest, question_version, jev_model, answers, policy_version,
route, llm_provider, latency_ms, cost_estimate, outcome
```

- **Cache by the complete contract** — normalized state + question definitions
  + criteria + model id + policy version. Reuse after any of those change
  applies an old judgment to a new case.
- **Budget the whole path**, not provider price: serialization, network, both
  model latencies, retries, retrieval, tool execution, review time, and the
  cost of failures. An extra decision call pays when it prevents a larger model
  call, shrinks context, avoids rework, or catches a consequential error.
- **Avoid hidden serial work** — do not call once per file, per candidate, or
  per option when one state and a batched question set express the same job.
- **Separate provider retries from workflow retries**, so an incident shows
  whether cost came from networking, uncertainty, or repeated generation.
- **Treat a battery as a product interface**: owner, semantic version,
  changelog, regression set. Remove questions nothing ever consumes.

## 10. Rollout and ownership

| Stage | Behavior |
|---|---|
| Offline | replay labeled cases |
| Shadow | log decisions, change nothing |
| Assist | recommend routes to humans |
| Limited | automate a low-risk slice |
| Expand | raise scope only after evidence |

- **Evaluate outcomes, not agreement.** A router can classify intent correctly
  and still pick a worse provider because the capability registry is wrong.
- **Make rollback ordinary.** Version every state builder, question set,
  threshold policy, provider registry, and fallback rule; a release should
  revert without touching application code. Keep a kill switch that disables
  automatic actions while preserving logging.
- **Protect the review path.** Human review is a production dependency, not an
  infinite queue. Estimate volume at each threshold. If the queue exceeds
  capacity, reduce automation scope rather than lower the threshold. Review
  screens must show the state and evidence behind a decision, not just a label.
- **Assign operational ownership** of the state builder, question contract,
  thresholds, provider registry, review queue, and incident response. The owner
  must be able to disable automation without waiting for a model update.
- **Every incident adds a durable artifact**: a regression case, a corrected
  question, a deterministic validator, a new no-match option, a tighter egress
  rule, or a revised threshold.
- **Sample periodically even when dashboards look healthy.** Aggregate accuracy
  hides a failing language, tenant, route, or rare high-impact class.
- **Test jagged edges**: negation, quoted instructions, long lists, missing
  evidence, overlapping options, mixed languages, adversarial content, and
  state containing prompt injection.

## Build order

1. Draw the boundary — code for exact rules, typed judgment for bounded
   judgments, LLM for open-ended generation.
2. Build state — current evidence only, every field named, untrusted content
   separated from instructions.
3. Choose the primitive (see `typesafe-ai`).
4. Decompose one broad prompt into independent atomic questions; compose in
   code.
5. Batch independent questions over one state.
6. Route before generation — filter by capability and policy first.
7. Verify after generation — deterministic checks first.
8. Gate by risk — bands chosen from labeled data.
9. Record receipts bound to a versioned trace.
10. Roll out offline → shadow → assist → slice → expand.

**Pre-launch:** required fields validated; no-match options present;
deterministic rules run before AI; secrets minimized; provider routes approved;
failure behavior defined; thresholds evaluated on held-out cases; receipts
replayable; rollback tested; review staffed for the volume the policy creates.

**First week:** review low-confidence cases, automated actions, fallbacks, and
provider errors daily. **Freeze question wording during the first observation
window** so behavior changes attribute to traffic, not a moving contract. Make
exactly one correction at the end of the week, with a measurable hypothesis.

## Anti-patterns

- The model that wrote it also scores whether it may run.
- A favorable semantic answer overriding a failed deterministic check.
- Service unavailable, treated as approval.
- One global confidence threshold across questions and risk classes.
- Retrying the same question over unchanged state until it passes.
- A verifier reading different evidence than the generator used.
- Routing on model names instead of capability contracts.
- Asking "what should we do" — mixing diagnosis, policy, and execution in one
  question.
- A decision layer that emits metrics but never changes behavior.
- Adding judgment calls as the goal. The signal is a higher verified completion
  rate with lower total latency, cost, and recovery work. If those do not
  improve, simplify the architecture or remove the decision layer from that
  branch.
