# Research: Read-only ChatGPT web delegation, skills, browser automation, and validation

- **Query**: Read-only repository/browser capability research for the ChatGPT web delegation skill. Identify existing skill format/examples, browser automation tools and authenticated-session reuse (including user-owned browser constraints), relevant tests and validation, and any installed ChatGPT web integrations. Do not expose credentials or read secret values.
- **Scope**: mixed (internal repository, local installed tooling, and live local browser metadata)
- **Date**: 2026-09-26

## Findings

### Files Found

| File Path | Description |
|---|---|
| `<repo-root>/skills/browser-driver/SKILL.md` | Existing user-owned browser/CDP skill. Frontmatter, trigger conditions, scope boundary, one-shot Playwright workflow, screenshot auditing, identity-wall handoff, cleanup, and reference links. |
| `<repo-root>/skills/browser-driver/references/launch-and-drive.md` | CDP launch/probe sequence and Playwright `connectOverCDP` example. |
| `<repo-root>/skills/browser-driver/references/selectors-and-handoffs.md` | Shadow-DOM/locator and overlay patterns, identity-wall handoff/polling, secret-handling and debug-port cleanup. |
| `<repo-root>/skills/browser-driver/references/remote-over-tunnel.md` | Same-host versus remote-agent/local-browser cases and loopback-only SSH reverse-tunnel constraints. |
| `<repo-root>/skills/omnidebug-autopilot/SKILL.md` | Existing browser test/reproduction workflow, supported frameworks, verification gates and browser-specific determinism rules. |
| `<repo-root>/skills/omnidebug-autopilot/references/browser-repro-playbook.md` | Pin browser/environment, run reproduction twice, capture artifacts, and re-verify exact command. |
| `<repo-root>/skills/omnidebug-autopilot/references/browser-artifact-checklist.md` | Required browser artifacts and redaction rules. |
| `<repo-root>/README.md` | Repository skill distribution and compatibility conventions. |
| `<repo-root>/skillgenie` | Validator implementation and CLI wiring. |
| `<repo-root>/skills/ai-csuite/SKILL.md` | Existing Jev-backed decision pattern and explicit fallback behavior. |
| `<repo-root>/skills/ai-csuite/scripts/test_jev_fallback.py` | Adversarial Jev fallback test covering 25 failure modes. |
| `<repo-root>/skills/ai-csuite/scripts/test_debate_divergence.py` | Test enforcing non-uniform independent positions and named tensions. |
| `<caller-skill-root>/skills/agent-browser/SKILL.md` | Installed browser automation CLI documentation: snapshots/refs, state persistence, named sessions, CDP attach, content boundaries, domain allowlist, action policy, and cleanup. |
| `<caller-skill-root>/skills/playwright-cli/SKILL.md` | Installed Playwright CLI documentation: storage state, CDP attach, detach, snapshots, sessions, and browser interaction. |
| `<caller-skill-root>/skills/agents-sdk/references/browse-the-web.md` | Installed Cloudflare browser-binding reference; describes fresh browser sessions, not reuse of a user's authenticated browser. |
| `<caller-skill-root>/skills/.system/openai-docs/SKILL.md` | Installed OpenAI docs skill; it is for official OpenAI developer documentation/API/product questions, not a ChatGPT web-session integration. |
| `<caller-skill-root>/skills/baoyu-post-to-wechat/scripts/wechat-agent-browser.ts` | Existing script-backed authenticated web workflow using a named `agent-browser` session; useful pattern for session naming and login-state checks, but it targets WeChat and is not a ChatGPT integration. |
| `<repo-root>/.trellis/tasks/09-26-chatgpt-web-delegation/prd.md` | Task requirements: ChatGPT website only, no API/auth extraction, Jev decisions, ordinary/search/research modes, observable status/evidence, and offline-test expectations. |

### Skill format and validation

- Repository skills are directories with a root `SKILL.md`; README documents this at `<repo-root>/README.md:136-148`.
- The repository's standard header is single-line YAML frontmatter containing `name`, `description`, and `license`, with one-line JSON `metadata`; tags are mirrored under `metadata.hermes.tags` (`README.md:138-146`). Existing browser-driver header is at `<repo-root>/skills/browser-driver/SKILL.md:1-7`.
- `skillgenie` parses frontmatter using a simple regex (`<repo-root>/skillgenie:145-173`), requires `name` and `description`, enforces lowercase hyphenated name matching the directory and a 64-character name limit (`skillgenie:269-289`), rejects block scalars and non-single-line frontmatter syntax (`skillgenie:290-294`), and requires single-line JSON `metadata` with `version` and `hermes` (`skillgenie:295-309`).
- Validation is available as `./skillgenie validate [skill]`; CLI wiring and compatibility wording are at `<repo-root>/skillgenie:826-836`. Verified command result on 2026-09-26: `./skillgenie validate` passed all 36 checked skills.
- `browser-driver` alone validates: `./skillgenie validate browser-driver` passed.
- `skills.yaml` declares local skills as auto-included (`<repo-root>/skills.yaml:4-5`).
- `browser-driver/agents/openai.yaml` exists and contains display metadata/default prompt (`<repo-root>/skills/browser-driver/agents/openai.yaml:1-5`), but `functions.Read` verified no corresponding `agents/openai.yaml` in `skills/ai-csuite` (not a repository requirement).

### Browser automation and authenticated-session reuse

- The repository's closest fit is `browser-driver`: it explicitly attaches to the user's own, already-logged-in Chromium browser over CDP and says a fresh Playwright profile has no sessions (`<repo-root>/skills/browser-driver/SKILL.md:9-16`). It must only be used when the task needs the user's existing login and a clean profile would land at login (`SKILL.md:17-34`).
- Its explicit scope boundary is own browser/own sessions/own accounts, with knowledge and present consent; it forbids bypassing authentication and hands Touch ID/security-key/liveness/QR identity walls back to the user (`SKILL.md:36-38`). This directly covers the user-owned-browser constraint requested by the task.
- Local browser reuse sequence: choose non-default debug port, launch/relaunch browser with restored session, probe CDP, attach, perform one step per short script, screenshot after each mutating step, and detach (`SKILL.md:40-60`; `references/launch-and-drive.md:3-20`, `27-50`). The Playwright example uses a caller-provided loopback CDP endpoint, selects the real context/page, screenshots, then detaches (`launch-and-drive.md:32-50`).
- Browser-driver warns not to leave the unauthenticated CDP port open; cleanup is a normal browser restart (`<repo-root>/skills/browser-driver/references/selectors-and-handoffs.md:63-70`).
- Remote-agent case is explicitly differentiated: same host needs no tunnel; remote agent plus local browser needs a loopback-only SSH reverse tunnel; headless browser on a VPS has no existing user session for this skill (`remote-over-tunnel.md:1-12`). CDP has no authentication, so the reference requires loopback binding, SSH key auth, immediate teardown, and no public/shared forwarding (`remote-over-tunnel.md:28-35`).
- For selectors, Playwright locators pierce shadow DOM while raw `querySelectorAll` in page evaluation does not; DOM-click is documented for overlay interception (`selectors-and-handoffs.md:3-29`). Identity-wall behavior is click-to-wall, tell the user exactly what to do, then poll page text or a source-of-truth state instead of guessing (`selectors-and-handoffs.md:31-44`).
- Installed `agent-browser` documentation gives a different authenticated-session model: save/load state (`<caller-skill-root>/skills/agent-browser/SKILL.md:134-149`), named persistent sessions with optional encryption at rest (`:151-171`), and explicit CDP attach/auto-connect (`:198-207`). It also supports named parallel sessions (`:186-196`). The docs state security restrictions are opt-in (`:269-271`), with content-boundaries (`:273-284`), domain allowlist (`:286-294`), and action policy (`:296-309`).
- Installed `playwright-cli` supports storage state (`<caller-skill-root>/skills/playwright-cli/SKILL.md:116-145`), attaching to Chrome/Edge by CDP endpoint and detaching without closing the external browser (`:281-299`), named persistent sessions (`:377-393`), and snapshot-driven interactions (`:314-375`).
- The installed `agent-browser` executable is not on PATH in this environment. A bundled Playwright CLI is present at `<caller-playwright-cli>`, version `0.1.21`; `playwright-cli` is also available via that Kiro path. No `agent-browser` command was found on PATH.
- A running Brave browser was verified via process listing with a user-owned-looking separate profile and CDP port `<observed-cdp-port>`, and `<loopback-cdp-endpoint>/json/version` returned browser metadata `Chrome/153.0.8010.37`, protocol `1.3`; no credentials or page contents were read. The endpoint exposed only `newtab` and a service worker when `json/list` was inspected, so an authenticated ChatGPT page was not verified as open.
- Existing WeChat script pattern uses a named session (`SESSION = 'wechat-post'`) and consistently invokes `agent-browser --session ...` (`<caller-skill-root>/skills/baoyu-post-to-wechat/scripts/wechat-agent-browser.ts:6-7`, `23-50`), checks URL/login state and waits for user QR login rather than extracting credentials (`:122-146`). This is an existing authenticated web workflow, but it is WeChat-specific and not evidence of ChatGPT support.

### Tests and validation

- Repository-level validation is verified: `./skillgenie validate` passed all 36 skills on 2026-09-26.
- Existing Jev fallback test is verified: `python3 skills/ai-csuite/scripts/test_jev_fallback.py` passed all 25 failure modes and identical-baseline assertions. The test cases include network failures, HTTP 401/429/500, malformed payloads, missing keys, and wrong types (`<repo-root>/skills/ai-csuite/scripts/test_jev_fallback.py:1-80`).
- Existing Jev divergence test is verified: `python3 skills/ai-csuite/scripts/test_debate_divergence.py` passed; it checks multiple independent stances, non-uniform concessions, named `Key Tensions`, and stance coverage (`<repo-root>/skills/ai-csuite/scripts/test_debate_divergence.py:1-55`).
- No repository-native ChatGPT/browser delegation tests, package manifest, Playwright config, or project test suite were found. `get_context.py --mode packages` reported `Single-repo project (no packages configured)`. The only test-like repository files outside an unrelated temporary security-review checkout are the two `ai-csuite` tests above.
- Browser debugging references require deterministic browser/project settings: pin browser/viewport/locale/timezone, disable retries and parallel workers, freeze data where possible, run repro at least twice, and collect console/network/trace/screenshot artifacts (`omnidebug-autopilot/SKILL.md:103-127`; `browser-repro-playbook.md:5-39`). The artifact checklist requires reproduction command, browser/OS, failing output, console logs, failed requests, screenshot, and redaction of secrets (`browser-artifact-checklist.md:1-28`). These are documented validation patterns, not tests for ChatGPT delegation.

### Installed ChatGPT/OpenAI integrations

- No installed skill or file explicitly named `chatgpt` was found under the checked installed roots `<caller-skill-root>/skills`, `<caller-claude-skill-root>`, `<caller-opencode-config>/skills`, `<caller-openclaw-config>/skills`, and `<caller-codex-config>/skills`.
- Installed OpenAI-related material is `/.system/openai-docs` and other generic `openai.yaml`/asset files; the OpenAI docs skill is explicitly for current official OpenAI developer documentation/API/product questions and prioritizes docs MCP, not ChatGPT web control (`<caller-skill-root>/skills/.system/openai-docs/SKILL.md:1-19`). It is not verified as a ChatGPT web integration.
- `<caller-codex-config>/config.toml` contains OpenAI/Codex plugin and ChatGPT-project path strings, but this is configuration metadata rather than proof of a ChatGPT web automation integration. The inspected lines include `openai-bundled` plugins and `chatgpt-projects` paths; no credential values were read. Treat this as a local Codex/OpenAI integration reference, not a verified web-session delegate.
- Selected agent configs contain generic OpenAI-compatible provider entries (`<caller-opencode-config>/opencode.json`, `<caller-opencode-config>/opencode.jsonc`, `<caller-openclaw-config>/openclaw.json`), but these indicate API/provider configuration and do not establish ChatGPT webpage integration. Per task boundary, no secret values were read.
- The currently running Brave CDP target list showed only a `newtab` page and a service worker; no ChatGPT hostname was observed. Therefore an authenticated ChatGPT session is **not verified** in the inspected browser endpoint.

### Related specs

- `<repo-root>/.trellis/spec/` does not exist in this checkout; `get_context.py --mode packages` reports no packages. No package/layer-specific spec was found.
- `<repo-root>/.trellis/tasks/09-26-chatgpt-web-delegation/prd.md` is the relevant task PRD. Its requirements at lines 5-22 specify ChatGPT web only, no API/auth extraction, Jev decisions, three interaction modes, observable success/failure/evidence, and offline validation expectations.

## Verified vs unverified

### Verified

- Repository format and validator rules, including successful validation of all 36 existing skills.
- Existing `browser-driver` user-owned CDP workflow and security constraints.
- Installed `playwright-cli` version `0.1.21`; `agent-browser` absent from PATH.
- Running Brave CDP metadata at loopback port `<observed-cdp-port>` and browser version/protocol; target list had only newtab/service worker.
- Existing Jev tests and both passing results.
- No explicit ChatGPT-named skill found in the checked installed skill trees.
- No ChatGPT hostname observed in the inspected CDP target list.

### Unverified / not found

- No ChatGPT webpage interaction was performed; no authenticated ChatGPT session was proven reachable.
- No repository-native tests or fixtures for ChatGPT delegation were found.
- Generic OpenAI/Codex configuration references do not verify a ChatGPT web integration.
- Browser profile directories were only enumerated; cookies, local storage, credentials, and other secret/session values were not read.
- No external web documentation was required to establish the repository-local capabilities; the installed references above are the relevant local sources.

## Caveats / Not Found

- The process list also showed other Brave instances and ports, including an unrelated temporary browser; no attempt was made to attach, navigate, or mutate any browser because the request was read-only and credentials/session contents were out of scope.
- A CDP endpoint is unauthenticated and grants control to local reachability; any implementation must preserve loopback-only binding and detach/clean up promptly. The repository's browser-driver reference treats this as a non-negotiable constraint.
- Page content from any future ChatGPT session would be untrusted data, not agent instructions; this is required by the task PRD but is not currently implemented or tested in this checkout.
