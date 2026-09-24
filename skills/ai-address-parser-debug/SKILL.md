---
name: "ai-address-parser-debug"
description: "Diagnose and fix an AI-powered address-parsing feature that breaks in production: trace the UI error to its backend route, separate the root request/provider failure from secondary enrichments (Jev judgment, geocoding/postcode lookup), probe the configured model on the same endpoint/model/auth/payload the app uses, verify the model is actually callable on that account (a model-list entry is not proof), pick a right-sized fallback that still meets the task, then update the running app's config (rbw-retrieved Dokploy credentials, only the target env var changed, all others preserved) and redeploy with behavior-level verification instead of a bare HTTP 200. Use when an AI parsing/autofill feature 500s in prod, when a model starts failing behind a self-hosted proxy, or when asked to fix the address parsing of a deployed store. Never print secrets into chat, never claim success from a website HTTP 200, always distinguish Dokploy instances and rbw entries before writing."
license: "MIT"
metadata: {"version":"1.0.0","category":"developer-tools","tags":["ai-address-parser","debugging","incident-response","llm","model-compatibility","dokploy","rbw","env-vars","deployment"],"license":"MIT","hermes":{"tags":["ai-address-parser","debugging","incident-response","llm","model-compatibility","dokploy","rbw","env-vars","deployment"]}}
allowed-tools: Read, Write, Edit, Bash
---

# AI Address Parser — Debug & Fix

Diagnose a deployed AI-powered address-parsing feature that is returning errors,
then fix it at the model/config layer and verify the real feature works — not just
that the site returns HTTP 200.

Companion to the [`ai-address-parser`](../ai-address-parser/SKILL.md) skill: that one
documents how to *build* the feature, this one documents how to *fix it in production*
when it breaks. Resolved incident this derives from: `<app-name>` on the
`<dokploy-instance-name>` instance — `LLM_BASE_URL` pointing at a self-hosted
proxy, `LLM_MODEL` unset so the code defaulted to a model the account could not
actually call, authenticated probes failing for that model (502) while an
available one returned 200, and the fix being a single env var change + redeploy.

---

## Step 1: Trace the UI error to the backend route

Reproduce the error in the UI, open the network/devtools, and read the failing
request path. Do not guess which endpoint is broken from the UI text alone.

- Find the failing `fetch`/XHR: note its URL, method, and status.
- Map that URL to a backend route (server route / Nitro handler / cloud function).
- Read that handler's code to find what it calls *first* in the error path: the LLM
  provider call, or something else entirely (database, cache, another API).

Only after confirming the failing backend route is the AI call, continue. If the
error originates in a non-AI path, debug that separately — this skill is about the
model/provider layer.

## Step 2: Separate the provider call from secondary enrichments

An address-parsing flow is often composite. Before touching any config, classify
every downstream call the failing route makes:

- **Primary:** the LLM chat-completions request that turns the free-text blob into
  structured fields. This is the route this skill fixes.
- **Secondary enrichments** — these may fail *independently* and must not be confused
  with a model problem:
  - judgment / re-format passes (e.g. a Jev/TypeSafe call),
  - geocoding or postcode lookup (a separate API),
  - any database or CRM lookup.

Diagnose the enrichment by calling it directly with the same payload the route uses.
Its own error (timeout, quota, bad key, schema change) is a different bug: fix the
enrichment, not the model config. Only the primary LLM call's failure leads to
Step 3.

## Step 3: Probe the model exactly the way the app does

Do **not** probe with a convenient tool or a different protocol than the app uses —
the bug lies in the mismatch, and a "close enough" probe hides it. Replay the same
call as the app:

- same endpoint (`POST {base_url}/chat/completions`),
- same `model`,
- same auth path (the bearer token the server reads — from server-side config, never
  from the client),
- same JSON payload shape (messages, `response_format: {type:'json_object'}`, no
  `temperature` if the app omits it — some providers reject its presence with a 400).

Return the provider's verbatim status/body for each tested model. Repro:
Claude returned **502**, while an available model (gpt-5.6-luna style alias) returned
**200** on the identical payload — proving the config, not the proxy, was broken.

## Step 4: Verify model compatibility with the actual account

A model appearing in a provider's `/models` list is **not** proof it can be called:
listings can advertise models that 404/502 in practice, and the account's permission
profile decides what is actually callable.

- Confirm the model is absent from (or failing on) the auth token the app uses.
- Probe each candidate with the app's real payload (Step 3).
- The decisive test is a successful authenticated chat-completions call, never a
  list entry.
- Use synthetic or fully redacted address data for probes by default. Never send
  real customer addresses or other personal data to an external provider unless
  the data-processing authorization and provider trust boundary are already
  confirmed.

## Step 5: Pick a right-sized fallback for the user's task

Choose the replacement model that fits the user's actual need, not the most powerful
one available. For address parsing the bar is: reliable JSON extraction, tolerant of
messy free text, not necessarily bleeding-edge reasoning. Rules:

- Prefer a model the account demonstrably calls OK (Step 4) that keeps the existing
  JSON-mode payload working (response format support, no `temperature` requirement).
- Stay as close as possible to the intended capability — a small fast model for a
  structured extraction is right-sized; a huge frontier model is only justified if
  the parse quality genuinely needs it.
- Record *why* the fallback was chosen (the probing evidence), so the choice is
  auditable and can be revisited when the preferred model becomes callable.

## Step 6: Get deployment credentials from rbw safely

rbw may not be on PATH inside the agent's shell. Locate it first:

```bash
command -v rbw || ls "$HOME/.local/bin/rbw" "$HOME/.cargo/bin/rbw" 2>/dev/null || find "$HOME" -maxdepth 4 -name rbw -type f 2>/dev/null
```

A common failure is that the credential lives outside the current session's PATH but
is already exported in the environment — check for an existing variable before any
fetch (e.g. if the repo `.env` defines a `*_KEY`, read that value into a var, never
echo it).

- Identify the exact **password-store entry name** that matches the target Dokploy
  instance (`<dokploy-instance-name>` in the resolved incident), and the **field** within it
  that holds the API key (`<api-key-field>`).
- **Never let rbw output reach the chat.** Pipe it straight into a shell variable and
  use the variable only:

  ```bash
  DOKPLOY_KEY=$(rbw get --full "<dokploy-instance-name>" 2>/dev/null | sed -n 's/^<api-key-field>: //p')
  test -n "$DOKPLOY_KEY"
  ```

  The key lives in a named custom field, so `--full` plus a field-name extraction
  is required — a bare `rbw get <entry>` reads only the password field. `sed -n`
  matches the field label, so the secret never reaches stdout on its own line.
  Check length (`${#DOKPLOY_KEY}`), never the value. Pipe the value to the
  consuming process; never print it, echo it, or write it to any file.

## Step 7: Inspect the Dokploy instance & app BEFORE writing anything

Guard: distinguish the target instance and credential entry precisely before any call
— updating env vars on the wrong app/host is a real failure mode this skill exists to
prevent.

- Confirm which Dokploy instance the app belongs to (`<dokploy-instance-name>` is a
  *different* control plane from other Dokploy endpoints —
  do not assume the same one every time).
- Inspect the current application and its environment **before** any mutation:
  read the app's current env (via the Dokploy API / UI), list the docker-compose or
  container env, and diff it against what the code expects.
- Verify which env vars are actually controlling the model: find `LLM_BASE_URL` and
  note whether `LLM_MODEL` is set or unset across the runtime/app. In the resolved
  incident `LLM_MODEL` was unset, so the code fell back to a default model the account
  couldn't call.

## Step 8: Update only the target variable, preserving every other env var

- Before any write or redeploy, show the user the target app, the exact variable
  name, the old/new state (values redacted), and the planned effect, then obtain
  explicit confirmation. Do not treat a diagnosis, a model probe, or a previous
  request to investigate as authorization to change production.
- Fetch the app's **full current env** first (via the Dokploy instance's API/UI).
- Mutate **only** the target key (`LLM_MODEL`), keeping byte-for-byte every other
  variable (`LLM_BASE_URL`, the API/token keys, NUXT/EXPRESS/public vars, secrets).
- Apply the change through the instance's own API path used by the existing
  `dokploy-deploy` skill pattern (authenticated tRPC/browser session with cookies, or
  the matching instance's documented endpoint). Re-read the env after applying to
  prove the target changed and nothing else did, and that no secret value ever
  touched the chat.

## Step 9: Redeploy and verify deployment state AND actual feature behavior

- Trigger a redeploy/rebuild of the app on that instance.
- Verify the deployment converged: the service is running and the env update is
  reflected (read back the container/runtime env).
- **Then verify the feature, never the site.** An HTTP 200 from the website proves
  the site is up, which it already was — it proves nothing about the parser. Re-run
  the address-parsing flow end-to-end (paste a messy address blob, submit, read the
  structured fields back), with the same probe payload the app uses (Step 3) until it
  returns a successful parse. Only then is the fix confirmed.
- Report: env var changed (old state → new state, no values), deployment
  convergence, the end-to-end parse result, and the deciding probe evidence.

---

## Guardrails (never skip)

- **Never expose secret values.** No token, password, or API key in chat, tool output,
  files, or logs. rbw output goes straight to a variable; check length, never content.
- **Do not claim the feature works from a website HTTP 200.** Verify the actual parse
  behavior end-to-end before declaring resolution.
- **Distinguish instances and credential entries.** The app/dokploy-instance/rbw-entry
  triple must be confirmed together before any write — the wrong combination has
  already caused the wrong-app updates this skill exists to prevent.
- **Separate the primary from enrichments before changing config.** A broken
  geocoder or Jev call must not be "fixed" by switching the model.
- **Model list presence ≠ callable.** Always prove with an authenticated
  chat-completions call using the app's own payload.
- **Protect address data.** Use synthetic or fully redacted fixtures for external
  probes; real customer data requires an explicitly confirmed, authorized trust
  boundary.
- **Require confirmation before production changes.** No environment update or
  redeploy without explicit approval of the exact target and variable change.
- Skill contains no credential values; it only documents how to fetch them safely.
