---
name: "claude-agent-sdk-auth"
description: "Run Claude Code / the Claude Agent SDK headless or programmatically, and authenticate it with the user's Claude Pro/Max SUBSCRIPTION (no API key) — including on a REMOTE server or in CI. Use when: running `claude -p` / the Agent SDK (`@anthropic-ai/claude-agent-sdk`, `claude-agent-sdk`) non-interactively; making a remote/CI machine or a spawned agent use the local subscription instead of a metered API key; deciding between API key, subscription OAuth, `CLAUDE_CODE_OAUTH_TOKEN`, and a proxy; or wiring `CLAUDE_CODE_OAUTH_TOKEN` / `ANTHROPIC_AUTH_TOKEN` / `apiKeyHelper`. Covers `claude setup-token`, the auth precedence order, headless entry points, and the key fact that the Agent SDK is NOT an HTTP server."
license: "MIT"
metadata: {"version":"1.0.0","category":"developer-tools","license":"MIT","references":["https://code.claude.com/docs/en/headless","https://code.claude.com/docs/en/authentication","https://code.claude.com/docs/en/agent-sdk/typescript","https://code.claude.com/docs/en/agent-sdk/python","https://code.claude.com/docs/en/agent-sdk/hosting"],"tags":["claude-code","agent-sdk","authentication","oauth","subscription","headless","ci"],"hermes":{"tags":["claude-code","agent-sdk","authentication","oauth","subscription","headless","ci"]}}
---

# Claude Agent SDK / Claude Code — headless auth with a subscription

Goal: run Claude Code (or the Claude Agent SDK) **non-interactively**, authenticated by the user's Claude **Pro/Max subscription** rather than a metered Anthropic API key — locally, in CI, on a remote 24/7 server, or inside a spawned agent. Verify any binding against the docs in the frontmatter `references` before writing code; do not guess flags.

## The one fact that kills the wrong design first
**The Claude Agent SDK / Claude Code is NOT an HTTP server.** It is a client/agent runtime: the SDK spawns a local `claude` CLI subprocess over stdin/stdout, and that subprocess calls `api.anthropic.com` directly. It does **not** listen on a network port. So you **cannot** point another process's `ANTHROPIC_BASE_URL` at "the SDK" — there is nothing serving an Anthropic-API-compatible endpoint. If you need an HTTP endpoint, you build your own wrapper around `query()` (your code listens, calls the SDK internally), or you use a token (below) instead. Source: Agent SDK Hosting docs.

## Headless / programmatic entry points
- CLI: `claude -p "<prompt>"` (a.k.a. `--print`) → non-interactive, result to stdout.
- Output: `--output-format text|json|stream-json` (`stream-json` is newline-delimited JSON for real-time streaming; pair with `--verbose`).
- SDK: TypeScript `@anthropic-ai/claude-agent-sdk` `query()` async generator; Python `claude-agent-sdk` `query()` / `ClaudeSDKClient` (long-running sessions).

## Authentication precedence (what `claude` checks, first match wins)
1. Cloud provider env (`CLAUDE_CODE_USE_BEDROCK`, …)
2. `ANTHROPIC_AUTH_TOKEN` — bearer token, sent as `Authorization: Bearer <token>`; the intended slot for an **LLM gateway / proxy**.
3. `ANTHROPIC_API_KEY` — Console API key (metered).
4. `apiKeyHelper` — a script whose stdout is the credential (dynamic).
5. **`CLAUDE_CODE_OAUTH_TOKEN`** — a long-lived **subscription** OAuth token (see `setup-token`).
6. Subscription OAuth from `/login` — the interactive Claude Code login. Stored on macOS in the Keychain, on Linux in `~/.claude/.credentials.json` (mode 0600) as `claudeAiOauth: { accessToken, refreshToken, expiresAt, scopes, subscriptionType }`. Auto-refreshed by Claude Code.

A stale `ANTHROPIC_API_KEY` in the environment **shadows** the subscription (slot 3 beats slot 5/6) — unset it if you mean to use the subscription. Likewise an empty `ANTHROPIC_API_KEY=""` still wins its slot.

## THE primitive: `claude setup-token` (use a subscription on a remote / in CI)
```bash
# On a machine where you're logged into Claude Code (interactive, opens a browser):
claude setup-token
# → prints a ~1-year, INFERENCE-ONLY OAuth token bound to your subscription.
#   It is NOT saved anywhere; copy it.
```
Then anywhere else (remote server, CI, a spawned agent), with **no dependency on the original machine being online**:
```bash
export CLAUDE_CODE_OAUTH_TOKEN=<token>
claude -p "do the task"     # or drive the Agent SDK — uses the subscription
```
This is the supported, documented way to "borrow a subscription" off-box. It is genuinely independent of the origin machine (unlike any Mac-side relay), so it works for 24/7 / unattended agents.

**Caveats:**
- Token is **inference-only** and lasts ~**1 year** — re-run `setup-token` to renew. Cannot establish Remote Control sessions.
- **`--bare` mode does NOT read `CLAUDE_CODE_OAUTH_TOKEN`.** If a script uses `claude --bare`, authenticate with `ANTHROPIC_API_KEY` or an `apiKeyHelper` instead. (Plain `claude -p` and the SDK read it fine.)
- Do not log it; treat it as a credential (store mode 0600, inject via env only).

## Decision guide
- **Remote/CI agent should use the subscription, unattended:** `claude setup-token` once → set `CLAUDE_CODE_OAUTH_TOKEN` on the remote. Simplest, no proxy, origin machine can be offline. **Default choice.**
- **You need an actual HTTP endpoint to point `ANTHROPIC_BASE_URL` at** (e.g. a gateway that adds telemetry/routing, or a relay holding the subscription so the token never leaves one box): run a thin proxy that forwards `/v1/messages` to `api.anthropic.com` and attaches the subscription OAuth as `Authorization: Bearer <accessToken>` **plus** `anthropic-beta: oauth-2025-04-20` (subscription OAuth requires that beta header on `/v1/messages`; it is NOT `x-api-key`). The remote then uses `ANTHROPIC_AUTH_TOKEN`=<a gate token> + `ANTHROPIC_BASE_URL`=<proxy>. This keeps the OAuth on one box but requires that box online. Prefer `setup-token` unless you specifically need the gateway.
- **API-key / Console billing is fine:** just set `ANTHROPIC_API_KEY` — simplest, but metered, not the subscription.
- **"Use the SDK itself as the LLM server":** does not exist — see the top section.

## Reading the local subscription token directly (when not using `setup-token`)
`~/.claude/.credentials.json` → `.claudeAiOauth.accessToken` (+ `refreshToken`, `expiresAt`). Usable directly as a `Bearer` for short-lived calls, but you must implement refresh against the OAuth token endpoint when `expiresAt` passes — which is exactly the fragile part `setup-token` / Claude Code already handle. Prefer not to hand-roll refresh.

## Quick checklist for "make X use the subscription headlessly"
1. Is X another machine / CI / a spawned agent that must work unattended? → `claude setup-token` → `CLAUDE_CODE_OAUTH_TOKEN` env. Done.
2. Does X call `claude --bare`? → that flag ignores the OAuth token; use an API key or `apiKeyHelper`.
3. Is a stale `ANTHROPIC_API_KEY` set in the env? → unset it, or it shadows the subscription.
4. Need a real Anthropic-compatible HTTP endpoint? → build/point a proxy (Bearer + `anthropic-beta: oauth-2025-04-20`); the SDK is not that endpoint.
