# Implementation plan

## Ordered checklist

1. Read task manifests, PRD, design, research, and adjacent `browser-driver`, `typesafe-ai` and existing Jev helper before code changes. Respect `main` clean baseline except the task artifacts. Create feature branch before editing tracked code; no commit or push without the Trellis Phase 3.4 gate.
2. Add `skills/chatgpt-web-delegation/SKILL.md` with repo metadata. Cover invocation, privacy preflight, current browser/auth probe, model/effort discovery, three Jev decisions with full probability spread, browser execution per mode, citations, failure and cleanup. Link to existing `browser-driver` for authenticated attach; no ChatGPT API.
3. Add minimal `scripts/route.py` using standard Python library. Read one JSON request from stdin; validate disclosure and UI candidates; call Jev only after deterministic validation. Restrict outgoing destination to TypeSafe, cap request/response size and timeout, suppress secrets and raw HTTP bodies from errors, validate all answer distributions, and provide machine-readable results. Keep browser operations out of the script. Exit nonzero with safe error codes on Jev failures and malformed results.
4. Add `scripts/test_route.py` with offline HTTP mocks: delegate/chat, search, research, keep-local, low confidence/ties, no suitable model/effort, unavailable UI options, sensitive disclosure, bad input, missing key, HTTP/network/timeout/malformed answer. Ensure rejected inputs send no network request and errors never contain credential values. Run Python syntax checks and full `./skillgenie validate`.
5. Check live browser feasibility on currently attached user-owned session using only snapshots and task-owned tab. Prior probe returned ChatGPT `Log in`; do not send a test message in that context. If authenticated session remains unavailable, record precise blocker and skip actual generation, without claiming web flow verified.
6. Run full-scope `trellis-check`, inspect doc consistency and privacy boundaries, update specs only if genuinely new repository conventions discovered, then follow Trellis commit plan review. No publish or install as part of this task.

## Validation

- `python3 -m unittest discover -s skills/chatgpt-web-delegation/scripts -p 'test_*.py' -v`
- `python3 -m py_compile skills/chatgpt-web-delegation/scripts/route.py skills/chatgpt-web-delegation/scripts/test_route.py`
- `./skillgenie validate chatgpt-web-delegation` and `./skillgenie validate`
- Manual browser smoke: only if an authenticated ChatGPT web session is reachable in the user's own browser; verify actual selected model/effort and each available mode via UI evidence. Otherwise report skipped with observed login or attach failure.

## Review gates

- No external prompt submission until the exact task content is checked for sensitive data.
- No Jev verdict bypasses observed UI availability, user consent, or privacy policy.
- No fallback to ChatGPT API; no credential extraction, browser storage export, or session hijack.
- Generated docs/code must contain no private infrastructure identifiers or credentials.
- Phase 3.4 commit only with explicit one-shot plan confirmation; never push by default.
