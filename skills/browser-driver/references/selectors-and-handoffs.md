# Selectors, handoffs, secrets, cleanup

## SPA selector gotchas

Modern dashboards render with web components and overlays. Patterns that work:

- **Shadow DOM: use Playwright locators, not raw `querySelectorAll`.**
  `document.querySelectorAll(...)` inside `page.evaluate` **misses** anything inside a shadow root, and many SPAs render panels as web components. Playwright locators pierce shadow DOM automatically:
  ```js
  page.getByRole('button', { name: 'Save' })
  page.getByText('Some label', { exact: true })
  page.locator('tr', { hasText: 'Row label' })
  ```

- **Overlays intercept clicks: fire a DOM click.**
  Even when the target is visible, an overlay can "intercept pointer events". `force: true` is often not enough. Bypass hit-testing with a real DOM click:
  ```js
  await page.getByRole('button', { name: 'Confirm' })
            .evaluate(el => el.click())
  ```

- **Scoped sub-element clicks.** To click a specific control inside a specific row:
  ```js
  await page.locator('tr', { hasText: 'The row' })
            .getByText('Edit', { exact: true })
            .click()
  ```

- **Display name ≠ internal name.** The label a user sees in the UI may differ from the underlying API/field name (spacing, casing, punctuation). Match on the **visible** text for clicks; do not assume the internal identifier renders verbatim.

## Identity walls — hand control to the user

Touch ID, security keys, and phone/QR liveness flows **cannot and must not** be automated. Drive up *to* the wall, then hand off:

1. Click through everything up to the prompt.
2. Tell the user exactly what to do, in plain words ("approve the Touch ID prompt", "scan the QR code with your phone").
3. **Poll for completion** instead of guessing:
   - watch the page text change:
     ```js
     // loop with short sleeps between checks
     const text = await page.evaluate(() => document.body.innerText)
     ```
   - or check a source-of-truth API/CLI for the same state, which is more reliable than scraping.
4. Only continue once the state actually flipped.

## One-time secrets

Some values (API keys, tokens) are shown **once** in the page. Handle them without leaking:

- Pull the value out of the page text straight into a file — never echo it to chat or logs:
  ```js
  const text = await page.evaluate(() => document.body.innerText)
  const m = text.match(/<expected-pattern>/)
  require('fs').writeFileSync('secret.txt', m[0])
  ```
- Move it into the user's password manager (whatever they use), then **shred the temp file**:
  ```bash
  # store via the user's password-manager CLI, then:
  shred -u secret.txt   # or: rm -P secret.txt
  ```
- Do not paste the secret back into the conversation, even truncated.

## Cleanup

When done, **restart the browser normally** (quit, reopen without the debug flag). An open remote-debugging port lets *any* local process control the logged-in browser, so do not leave it running.

```bash
osascript -e 'quit app "Microsoft Edge"'; sleep 2
open -a "Microsoft Edge"
```

## Gotcha: stdout corruption from hooks/plugins

Some environments inject extra lines into command stdout (e.g. a plugin hint banner). That corrupts strict parsers — `JSON.parse` / `json.load` can fail on the very first character. Defenses:

- Parse with tolerant patterns (`grep -o '<regex>'`) instead of strict JSON parsing, or
- Write the output to a file and re-read just the part you need, or
- Strip known banner lines before parsing.
