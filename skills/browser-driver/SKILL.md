---
name: "browser-driver"
description: "Attach to the user's OWN already-logged-in system browser over the Chrome DevTools Protocol (CDP) with Playwright, so automation reuses their existing session and avoids re-logging-in with 2FA. Use this ONLY when a fresh/headless browser won't do because the task needs the user's live login — e.g. 'do this in my browser', 'use my existing session/login', 'I'm already signed in, don't make me log in again', driving a console/dashboard behind 2FA while they watch. Do NOT use for ordinary browsing, scraping public pages, headless tests, or any automation that doesn't need their real session — use the agent's built-in browser tool / Playwright or chrome-devtools MCP / computer-use for those. Covers launching Chrome/Edge/Brave with a remote-debugging port, per-step one-shot Playwright scripts, screenshot-audited steps, shadow-DOM/overlay handling, handing control back at Touch ID/security-key/QR walls, one-time-secret capture, and cleanup. Own browser, own accounts, never to bypass auth."
license: "MIT"
metadata: {"version":"1.0.0","category":"automation","tags":["browser-automation","cdp","playwright","chromium","web-automation","dashboard"],"license":"MIT","hermes":{"tags":["browser-automation","cdp","playwright","chromium","web-automation","dashboard"]}}
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Browser Driver (system browser over CDP)

Drive the user's **own, already-logged-in** browser via CDP + Playwright. The user watches every step; you screenshot after each mutating action so both you and the user can audit.

## Why the system browser, not a fresh Playwright Chromium

A fresh Playwright profile has no sessions — the user would re-log-in with 2FA from scratch. The user's own Chromium browser already holds the session, so there is zero login friction. You attach to it over a debug port; you do not replace it.

## When to use this — and when NOT to (avoid tool conflict)

This skill exists for exactly **one** thing the other browser tools cannot do: **attach to the user's real browser and its existing login**. Reach for it only when *all* of these hold:

- The task needs the user's **existing session / login** (would otherwise require logging in, often with 2FA), AND
- A fresh or headless browser profile would land on a login screen, AND
- The user wants it done in **their own** browser, typically watching live.

Signals: "do it in my browser", "use my login / my session", "I'm already signed in", "don't make me log in again", a console/dashboard behind SSO+2FA.

**Do NOT use this skill — defer to the agent's built-in browser tooling — for:**

- ordinary browsing, fetching, or scraping of public or unauthenticated pages,
- headless end-to-end tests or CI automation,
- anything where a clean throwaway profile is fine (no real login needed),
- when the agent already has a browser tool / Playwright MCP / chrome-devtools MCP / computer-use that satisfies the task without the user's live session.

If the built-in tooling can do it, use that and stop — do not load this skill's reference files. Only load `references/*` once you have actually committed to driving the system browser, so an irrelevant browser task costs ~0 extra tokens (just this short description).

## Scope boundary (read first)

Only ever drive the **user's own** browser, **own** sessions, **own** accounts, with their knowledge and present consent. Never use this to bypass authentication, defeat a security control, or reach an account that is not theirs. Identity walls (Touch ID, security key, liveness/QR) are handed back to the user — never attempt to defeat or proxy them.

## Workflow

0. **Check where the agent runs vs where the browser is.** If you (the agent) run on the same machine as the user's logged-in browser, proceed normally. If you run on a remote host (VPS) and the browser is on the user's **local** machine, you must bridge the CDP port over an SSH reverse tunnel first — `references/remote-over-tunnel.md`. If the only browser is a headless one on the VPS, there is no existing user session to reuse and this skill does not apply.
1. **Pick the browser + port.** Any Chromium-based browser works (Chrome, Edge, Brave). Choose a non-default debug port (e.g. 9223) to avoid clashes.
2. **Launch with the debug port** so tabs/session restore — `references/launch-and-drive.md`.
3. **Probe** the port until it answers, then attach.
4. **Drive one step at a time** with short, one-shot scripts that connect fresh, act, screenshot, and detach — `references/launch-and-drive.md`.
5. **Read the screenshot** after every mutating step. That is how you "see" the page and how the user audits.
6. **Handle selectors** for modern SPAs (shadow DOM, overlays, display-vs-internal names) — `references/selectors-and-handoffs.md`.
7. **Hand control to the user at identity walls**, then poll for completion — `references/selectors-and-handoffs.md`.
8. **Capture one-time secrets** straight to a file, never to chat — `references/selectors-and-handoffs.md`.
9. **Clean up**: restart the browser normally so no open debug port lingers — `references/selectors-and-handoffs.md`.

## Core rules

- **One-shot scripts, not a long-lived process.** A long-running Playwright process dies with the shell. Connect fresh per step with `connectOverCDP`, act, then `browser.close()` (this only detaches — the user's browser stays open).
- **Screenshot every mutating step** and Read the PNG before the next action. No blind clicking.
- **Locators over `querySelectorAll`.** Playwright locators pierce shadow DOM; raw `document.querySelectorAll` inside `page.evaluate` does not.
- **DOM-click through overlays.** When something "intercepts pointer events", `locator.evaluate(el => el.click())` fires a DOM click and skips hit-testing; `force: true` is often not enough.
- **Stop at identity walls.** Click up to the wall, tell the user exactly what to do, then poll page text or a source-of-truth API until it clears.
- **Secrets shown once go to a file, never to chat.** Regex the value out of the page text into a temp file, store it in the user's password manager, then shred the temp file.

## Reference files (load on demand)

- `references/launch-and-drive.md` — launch-with-debug-port sequence (and why `open --args` is unreliable right after quit), the probe, and the per-step one-shot script pattern with screenshot auditing.
- `references/selectors-and-handoffs.md` — SPA selector gotchas (shadow DOM, overlays, display vs internal names), identity-wall handoff + polling, one-time-secret capture, cleanup, and a stdout-corruption gotcha.
- `references/remote-over-tunnel.md` — when the agent is remote (VPS) and the browser is on the user's local machine: bridge the CDP port over a loopback-only SSH reverse tunnel; security rules for unauthenticated CDP; when this skill does not apply (headless VPS, no user session).
