---
name: "dokploy-deploy"
description: "Deploy or rebuild applications on a Dokploy instance via the tRPC API. Handles authentication, finding the target service, triggering deploy/rebuild, and verifying the deployment."
license: "MIT"
metadata: {"version":"1.0.0","category":"deployment","license":"MIT","tags":["dokploy","deployment","trpc","docker"],"hermes":{"tags":["dokploy","deployment","trpc","docker"]}}
---

# Dokploy Deploy

Deploy or rebuild an application on a Dokploy instance without touching the Dokploy web UI.

## When to use

- User asks to deploy, redeploy, or rebuild an app on Dokploy
- Code has been pushed but Dokploy didn't auto-deploy (webhook misconfigured, CI secret missing, etc.)
- Need to verify a deployment completed and the live site reflects the latest code

## Prerequisites

1. **Dokploy URL** — the panel hostname (e.g. `dokploy.shuttleup.se`)
2. **Credentials** — stored in `rbw` under a key like `<project>-dokploy`. The entry contains:
   - `username`: email for login
   - `password`: login password
   - `uri`: the Dokploy panel URL
3. **Application ID** — the Dokploy service ID (e.g. `7FAexyVPdsg9uJaw9ezBF`). See "Finding the application ID" below.

## Security rules (NEVER skip)

- **Never display the password in chat output.** When reading from `rbw`, pipe directly to a variable or file:
  ```bash
  DOKPLOY_PASS=$(rbw get <rbw-key> 2>/dev/null)
  ```
  Do NOT `echo "$DOKPLOY_PASS"` or run `rbw get <rbw-key>` without redirecting output to `/dev/null`.
  To confirm the password was retrieved, check the variable length:
  ```bash
  echo "password length: ${#DOKPLOY_PASS}"
  ```
- Never write the password to any tracked file, temp file, or log.
- The password lives only in the shell session variable for the duration of the login flow.

## Authentication flow

Dokploy uses httpOnly cookies for auth. The easiest way is to use the Puppeteer MCP to log in via the browser, then use `fetch()` from within that browser context to call the tRPC API (cookies are sent automatically with `credentials: 'include'`).

### Step 1: Log in via Puppeteer

```
puppeteer_navigate → https://<dokploy-url>/
puppeteer_fill   → input[name='email'], <email>
puppeteer_fill   → input[name='password'], <password>
puppeteer_click  → button[type='submit']
```

Verify login by checking the URL changed to `/dashboard/...`:
```js
// puppeteer_evaluate
(() => window.location.href.includes('dashboard'))()
```

### Step 2: Find the application ID (if not known)

Navigate to the projects page and read the service links:

```
puppeteer_navigate → https://<dokploy-url>/dashboard/projects
```

```js
// puppeteer_evaluate — extract service links
(() => {
  const links = document.querySelectorAll('a');
  const result = [];
  links.forEach(a => {
    const text = a.textContent.trim();
    const href = a.getAttribute('href') || '';
    if (href.includes('/services/application/')) {
      const match = href.match(/\/application\/([A-Za-z0-9_-]+)/);
      result.push({ name: text.slice(0, 60), appId: match ? match[1] : '' });
    }
  });
  return JSON.stringify(result, null, 2);
})()
```

Pick the service that matches the target app name (e.g. "landing", "match", "club").

### Step 3: Trigger deploy via tRPC

From within the Puppeteer browser context (already authenticated):

```js
// puppeteer_evaluate
(async () => {
  const r = await fetch('/api/trpc/application.deploy?batch=1', {
    method: 'POST',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      '0': { json: { applicationId: '<APP_ID>' } }
    })
  });
  const data = await r.json();
  return JSON.stringify({ status: r.status, data: JSON.stringify(data).slice(0, 500) }, null, 2);
})()
```

For **rebuild** instead of deploy, use `application.rebuild`:
```js
fetch('/api/trpc/application.rebuild?batch=1', { ... same body ... })
```

A `200` status with `result.data.json: null` means the deploy was triggered successfully.

### Step 4: Wait for build and verify

Docker builds typically take 30-120 seconds. Wait, then verify the live site:

```bash
sleep 60
curl -s https://<target-url>/ | grep -o '<expected-pattern>' | sort | uniq -c
```

Example: verify a URL changed from `admin.shuttleup.se` to `club.shuttleup.se`:
```bash
curl -s https://shuttleup.se/ | grep -o 'admin.shuttleup\|club.shuttleup' | sort | uniq -c
```

## Alternative: checking service configuration

To inspect the service's Git source, Dockerfile path, and env vars without deploying:

```
puppeteer_navigate → https://<dokploy-url>/dashboard/project/<projectId>/environment/<envId>/services/application/<appId>
puppeteer_evaluate → read input values (buildPath, dockerfile, dockerContextPath, etc.)
```

Key fields to verify:
- `buildPath` — should be `/` (repo root)
- `dockerfile` — path to Dockerfile (e.g. `apps/landing/Dockerfile`)
- `dockerContextPath` — should be `.` (repo root)
- Trigger Type — `On Push` for auto-deploy
- Branch — `main`

## Troubleshooting

- **404 on tRPC call**: The API path may differ between Dokploy versions. Intercept `window.fetch` to discover the correct path:
  ```js
  // puppeteer_evaluate — install interceptor before clicking UI buttons
  const origFetch = window.fetch;
  window._apiCalls = [];
  window.fetch = function(...args) { window._apiCalls.push(args[0]); return origFetch.apply(this, args); };
  ```
  Then click the Deploy/Rebuild button in the UI and read `window._apiCalls`.

- **Deploy triggered but site unchanged**: Check if the build failed — go to the Logs tab in the Dokploy UI, or check if env vars are correct (especially `NUXT_PUBLIC_*` vars that control URLs).

- **Auto-deploy not working**: Dokploy's "On Push" trigger requires a GitHub webhook configured in the Dokploy service settings. If only CI `DOKPLOY_*_WEBHOOK_URL` secrets exist, those are a separate path. Check which mechanism the other working services use.
