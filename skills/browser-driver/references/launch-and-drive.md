# Launch and drive

## Launch the browser with a remote-debugging port

The goal: get the user's existing browser (with its sessions) listening on a CDP port, without losing their open tabs.

1. **Quit the browser first** so it can relaunch with the debug flag. Example (macOS):
   ```bash
   osascript -e 'quit app "Microsoft Edge"'
   sleep 3
   ```
   Use the right app name for the chosen browser ("Google Chrome", "Brave Browser", etc.).

2. **Launch the binary directly** with the debug port. Do **not** rely on `open -a "<App>" --args --remote-debugging-port=...` right after a quit — there is a race where the app has not fully exited, so it either does not start or silently drops the flag. Launch the executable directly and detach it:
   ```bash
   nohup "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge" \
     --remote-debugging-port=9223 --restore-last-session \
     >/dev/null 2>&1 &
   ```
   `--restore-last-session` brings the user's tabs back, so they lose nothing. Pick a non-default port (9223 etc.) to avoid clashes with anything already on 9222.

   Binary paths per browser (macOS):
   - Chrome: `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`
   - Edge: `/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge`
   - Brave: `/Applications/Brave Browser.app/Contents/MacOS/Brave Browser`

3. **Probe until it answers** before attaching:
   ```bash
   until curl -s http://127.0.0.1:9223/json/version >/dev/null; do sleep 0.5; done
   ```

## Per-step one-shot script pattern

A long-lived Playwright process dies when the shell that started it exits. So connect fresh for **each** step: attach, act, screenshot, detach. Use `playwright-core` (it attaches to an existing browser; it does not download Chromium).

```js
import { chromium } from 'playwright-core'

const browser = await chromium.connectOverCDP('http://localhost:9223')
const ctx = browser.contexts()[0]                 // the user's real context, with sessions
const page = ctx.pages().find(p => p.url().includes('example.com'))
                ?? ctx.pages()[0]

// ... act on the page ...

await page.screenshot({ path: 'step.png' })
await browser.close()   // detaches CDP only — the user's browser stays open
```

Run it with `node step.mjs` (or via your runtime's ESM loader). Keep each step in its own short script; do not try to hold one process open across steps.

## Screenshot-audited stepping

After every **mutating** action (click, type, submit, navigation), take a screenshot and Read the PNG before deciding the next move. This is how you perceive the page state and how the user audits what you did. Never chain blind clicks.

Naming the screenshots per step (`01-open.png`, `02-form.png`, …) makes the audit trail readable.

## Finding the right page/tab

The user may have many tabs. Select the target deterministically:

```js
const page = ctx.pages().find(p => p.url().includes('the-target-host'))
```

If the tab is not open yet, open it explicitly with `ctx.newPage()` then `page.goto(url)`, and screenshot to confirm the session carried over (you should land logged-in, not on a login screen).
