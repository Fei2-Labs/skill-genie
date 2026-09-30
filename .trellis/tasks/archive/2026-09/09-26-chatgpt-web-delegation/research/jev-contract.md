# Jev contract and routing constraints

Sources consulted 2026-09-26: [HTTP API](https://docs.typesafe.ai/api.md), [Choice](https://docs.typesafe.ai/primitives/choice.md), [Score](https://docs.typesafe.ai/primitives/score.md), [State](https://docs.typesafe.ai/concepts/state.md), [Confidence](https://docs.typesafe.ai/confidence.md).

- `POST https://api.typesafe.ai/v1/systemone`; bearer authentication; body `{ "model": "jev-latest", "state": {...}, "questions": { "id": { "type": "choice", "instructions": ..., "criteria": {"option": "description"} } } }`. `questions` is a keyed object, not an array. `state` is shared by independent questions.
- Choice returns `choice`, `probabilities` and `confidence`. Probabilities sum to 1; confidence reflects concentration, not truth or permission. Near ties need a deterministic non-delegation or explicit clarification policy.
- Score is an ordered list of 2–10 semantic levels; response score is a probability-weighted position. A single model/effort choice fits Choice better than Score unless ranking several independently acceptable candidates.
- Give the three decisions their own questions. Model and effort questions should state the counterfactual premise that delegation is appropriate, since questions run independently. Never send user prompt text containing credentials, private account details, or sensitive data without checking authorization. Never use Jev to determine whether a model/effort option exists in the live page or whether an authenticated session works; check the browser UI.
- HTTP errors `401`, `422`, `429`, `529` must be distinguished. `429`/`529` may be retried with bounded exponential backoff. Missing key, malformed response or incomplete answers must not silently become a ChatGPT API call or an invented decision.
- Candidate taxonomy and threshold must be grounded in observed ChatGPT UI and representative tests; the docs provide no universal confidence threshold.
