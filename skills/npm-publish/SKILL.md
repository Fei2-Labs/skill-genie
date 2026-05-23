---
name: npm-publish
description: Publish an NPM package to the registry, handling authentication via browser-based login with 2FA/security key support.
version: 1.0.0
triggers:
  - "publish to npm"
  - "npm publish"
  - "publish package"
  - "deploy to npm"
---

# NPM Publish Skill

Publish an NPM package to the registry. Handles authentication including 2FA and security key (WebAuthn) flows.

## Prerequisites

- Node.js 22+ and npm installed
- Package.json with correct name, version, and `prepublishOnly` script
- Password manager CLI (optional, for retrieving credentials)

## Process

### Step 1: Verify Package Readiness

```bash
npm run build:hooks   # or whatever build step exists
npm test              # ensure tests pass
```

- [ ] Build succeeds
- [ ] Tests pass

### Step 2: Check NPM Authentication

```bash
npm whoami
```

- If this returns a username → already authenticated, skip to Step 5.
- If this returns `E401` → need to authenticate, continue to Step 3.

### Step 3: Retrieve Credentials (Optional)

If the user has a password manager CLI, retrieve credentials:

**rbw (Bitwarden):**
```bash
rbw get npmjs.com          # returns password
rbw get --full npmjs.com   # returns username + password + URIs
```

**Other password managers** — ask the user how to retrieve their NPM credentials:
- `pass`: `pass show npmjs.com`
- `1password`: `op item get "npmjs.com" --fields label=username,label=password`
- `gopass`: `gopass show npmjs.com`
- Custom: ask user for their CLI command

Extract:
- **Username** from the full output
- **Password** from the first line of output

### Step 4: Browser-Based Login (REQUIRED for 2FA/Security Key)

NPM requires browser-based authentication when 2FA or security keys are enabled. **Use the user's default browser**, not a test/headless browser.

#### 4a: Start npm login (opens browser for 2FA)

```bash
npm login
```

This prints a URL like:
```
https://www.npmjs.com/login?next=/login/cli/<uuid>
```

#### 4b: Open the login URL in the user's default browser

```bash
open "<the-login-url>"
```

On macOS, `open` uses the user's default browser with all their existing sessions, cookies, and extensions — including security key/WebAuthn support.

#### 4c: Automate credential entry (optional, if no existing browser session)

If the user is NOT already logged into npmjs.com in their browser, use Playwright with the user's Chrome profile to fill credentials:

```bash
npx playwright install chromium   # first time only
```

Then run a script like:

```javascript
import { chromium } from 'playwright';
import { writeFileSync } from 'fs';
import { homedir } from 'os';
import { join } from 'path';
import { execSync } from 'child_process';

// Get credentials from password manager or user
const NPM_USER = '<username from password manager>';
const NPM_PASS = '<password from password manager>';

// Use user's Chrome — NOT headless, NOT test browser
// channel: 'chrome' uses the system Chrome installation
const browser = await chromium.launch({ headless: false, channel: 'chrome' });
const context = await browser.newContext();
const page = await context.newPage();

await page.goto('https://www.npmjs.com/login');
await page.waitForLoadState('networkidle');

// Fill username
const usernameInput = page.locator('input#username, input[name="username"], input[type="text"]').first();
await usernameInput.waitFor({ timeout: 10000 });
await usernameInput.fill(NPM_USER);

// Fill password
const passwordInput = page.locator('input#password, input[name="password"], input[type="password"]').first();
await passwordInput.waitFor({ timeout: 5000 });
await passwordInput.fill(NPM_PASS);

// Click sign in
const signInBtn = page.locator('button[type="submit"], button:has-text("Sign In"), button:has-text("Log In")').first();
await signInBtn.click();

// Wait for user to complete 2FA/security key in the browser
console.log('Waiting for 2FA/security key authentication...');

const result = await Promise.race([
  page.waitForURL('**/dashboard**', { timeout: 300000 }).then(() => 'dashboard'),
  page.waitForURL('**/login/cli/**', { timeout: 300000 }).then(() => 'cli-callback'),
  page.waitForURL('**/~**', { timeout: 300000 }).then(() => 'profile'),
]).catch(() => 'timeout');

console.log('Login result:', result, 'URL:', page.url());

// After successful login, create an automation token via the NPM API
if (result !== 'timeout') {
  const tokenResult = await page.evaluate(async () => {
    const res = await fetch('/-/npm/v1/tokens', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ password: '<NPM_PASS>', readonly: false, cidr_whitelist: [] }),
    });
    return res.json();
  });

  if (tokenResult && tokenResult.token) {
    const npmrcPath = join(homedir(), '.npmrc');
    writeFileSync(npmrcPath, `//registry.npmjs.org/:_authToken=${tokenResult.token}\n`);
    console.log('Token written to .npmrc!');
  }
}

// Verify authentication
try {
  const whoami = execSync('npm whoami 2>&1').toString().trim();
  console.log('npm whoami:', whoami);
} catch (e) {
  console.log('npm whoami failed — manual intervention needed');
}

await browser.close();
```

**Key points:**
- `channel: 'chrome'` uses the user's installed Chrome (with security key support)
- `headless: false` — MUST be visible for WebAuthn/security key prompts
- The user only needs to tap their security key — everything else is automated
- After login, create an NPM automation token and write it to `~/.npmrc`

#### 4d: Verify authentication

```bash
npm whoami
```

Must return the correct username before proceeding.

### Step 5: Publish

```bash
npm publish --access public
```

For scoped packages (`@scope/name`), `--access public` is required on first publish.

**If publish fails with E403:**
- Check if the package version already exists: `npm view <package>@<version>`
- Bump version if needed
- Check scope permissions: `npm access list packages`

**If publish fails with E404:**
- The NPM scope may not exist or user lacks permission
- Verify: `npm org ls <scope-name>` or check on npmjs.com

### Step 6: Verify

```bash
npm view <package-name> version
```

Confirm the published version matches.

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| E401 Unauthorized | Not logged in | Run Step 4 |
| E403 Forbidden | Version already published or no permission | Bump version or check scope access |
| E404 Not Found | Scope doesn't exist or no publish rights | Create scope on npmjs.com or request access |
| WebAuthn not working in Playwright | Headless mode or wrong browser | Use `channel: 'chrome'` + `headless: false` |
| Token expired | NPM tokens have limited lifetime | Re-run Step 4 |

## Security Notes

- **NEVER** hardcode credentials in scripts committed to git
- Use password manager CLI to retrieve credentials at runtime
- The `npm-login.mjs` script should be created as a temp file and deleted after use
- Add `npm-login.mjs` to `.gitignore`
- Automation tokens should be scoped to publish-only when possible
