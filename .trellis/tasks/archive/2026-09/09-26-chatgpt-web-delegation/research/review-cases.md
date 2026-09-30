# Independent review checklist

## Routing boundaries

- Privacy is reviewed for both recipients before sending any request. A review flag records caller authorization; it is not secret detection.
- A known unavailable browser or unsupported mode prevents TypeSafe calls; Jev cannot turn a missing capability into available UI.
- Model and effort are dependent: a valid selected model must use only that model's observed effort set. Do not validate or escalate uncertainty on unused speculative branches as if they were executed decisions.
- A genuine default is allowed only when the current model has no configurable effort control. Missing evidence is not a default.
- A choice is from the submitted candidate set, its distribution covers the exact set, values are finite real numbers (not bool), mass sums approximately to one, and the selected choice is a maximum. Ties and provisional thresholds must fail closed for delegation.
- Missing/malformed JSON, unknown options, incomplete answers, NaN, Infinity, oversized replies, redirects, 401, 429, timeout, transport errors and missing credentials yield safe structured errors. Network exception text and service response bodies must not echo task data or tokens.

## Browser contracts

- Verify the actual ChatGPT origin and logged-in state before sending. Existing browser process alone is not authentication proof.
- Scope snapshot extraction to relevant controls/response; avoid unrelated sidebar conversations and account data.
- Preserve user-owned tabs/browser. No cookie/storage export or browser relaunch to acquire login.
- Select mode before inventory if mode changes model availability. Recheck final mode/model/effort before submitting; invalidate old decisions if capabilities change.
- On ambiguous submit, do not retry the prompt blindly. Inspect the owned conversation for the submitted turn and pending/completed response.
- Distinguish streaming, confirmation/research-plan, waiting-for-input, failed and complete. A stable partial response or vanished stop button alone is not completed research.
- Bounded polling is not permission for public sharing, file uploads, connectors, purchases, or unrelated actions suggested by ChatGPT.
- Search/deep research need UI mode evidence and source links. Preserve exact returned links; do not imply independent citation verification unless performed.

## Validation

- Offline tests must intercept every network request, including subprocess tests with dummy keys.
- CLI input errors must be nonzero JSON errors and not tracebacks; accepted non-delegation decisions can be exit 0.
- Offline fixtures must use fictitious UI labels, not claim actual ChatGPT plan capabilities.
- Runtime/private paths in research are local investigation evidence, not reusable skill content; do not publish raw task artifacts without sanitization.
