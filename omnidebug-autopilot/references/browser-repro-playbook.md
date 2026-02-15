# Browser Reproduction Playbook

Goal: produce deterministic reproduction for frontend/browser bugs before patching.

## Step 1: Lock Environment

- Pin browser target: `chromium`, `firefox`, or `webkit`.
- Pin viewport (for example `1280x720`).
- Pin locale and timezone.
- Disable retries and parallel workers during reproduction.
- Freeze network/data inputs when possible.

## Step 2: Single Repro Command

Create one command that fails reliably.

Examples:
- Playwright:
  - `pnpm exec playwright test tests/bug.spec.ts --project=chromium --workers=1 --retries=0`
- Cypress:
  - `pnpm exec cypress run --spec cypress/e2e/bug.cy.ts --browser chrome`
- Selenium/WebdriverIO:
  - use project test command with one test file and one worker.

## Step 3: Run Twice Minimum

- A reproduction is valid only if it fails at least 2 times with same signature.
- Signature means same core error class and stack segment.
- If signatures differ, mark issue as flaky and stabilize test input first.

## Step 4: Capture Artifacts

Collect:
- Console logs
- Network request failures and status codes
- Trace file if available
- Screenshot at failure frame
- Video (optional but helpful)
- Browser and OS metadata

## Step 5: Root Cause Mapping

Map the failure from symptom to cause:
1. Symptom shown in UI or assertion
2. Failing request or event
3. Fault location in source
4. Data or timing trigger
5. Missing guard/test that allowed regression

Root cause statement must be falsifiable and tied to at least one artifact.

## Step 6: Fix and Re-Verify

- Apply smallest safe fix.
- Re-run same repro command twice; both runs must pass.
- Re-run full suite gates (lint/type/test/build).
- Confirm previous signature does not appear in outputs.

## Anti-Patterns

- Debugging by random changes without deterministic repro.
- Enabling retries to hide failures during root-cause stage.
- Fixing UI symptom while backend/request bug remains.
- Claiming success without re-running the exact repro command.
