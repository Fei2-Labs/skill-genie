# OmniDebug Autopilot

Autonomous root-cause debugging skill for modern codebases.

`omnidebug-autopilot` gives an AI agent a strict, repeatable debug workflow:

1. reproduce the issue deterministically
2. isolate the true root cause
3. apply the smallest valid fix
4. verify with hard quality gates

It includes a browser-first module for deterministic UI bug reproduction, artifact capture, and fix verification.

## Why This Skill

Debugging often fails because teams patch symptoms, skip reproducibility, or accept false-green checks.

This skill enforces:
- deterministic reproduction before edits
- evidence-backed root-cause statements
- minimum blast-radius fixes
- verification loops until green
- no-interruption default execution for autonomous agents

## Core Capabilities

- Stack-aware debugging across Node.js, Python, Go, Rust, Java/Kotlin, Ruby, PHP, .NET, Swift
- Root-cause-first analysis chain
- Browser debugging artifact pipeline
- Verification gates for test, lint, typecheck, build, and smoke checks
- Ordered auto-fix heuristics by risk/likelihood

## Main Workflow

### Phase 1: Triage
- Capture exact failure text and command
- Inspect logs/network before code changes
- Identify likely regression window

### Phase 2: Reproduction
- Create a deterministic repro command
- Remove noise (parallelism, retries, random data)
- Confirm reproducibility (minimum 2 runs)

### Phase 3: Evidence Collection
- Gather logs, stack traces, failing requests
- Capture env/runtime differences
- For browser bugs, capture trace/screenshot/network metadata

### Phase 4: Root Cause Analysis
Build one falsifiable cause statement using:
- symptom
- immediate fault location
- underlying mechanism
- trigger condition
- missing safeguard

### Phase 5: Fix Strategy
- Apply smallest valid root-cause fix
- Preserve public behavior unless bug requires correction
- Reject bypass hacks as final fix

### Phase 6: Verification
- Run targeted checks first
- Run full project gates
- If any gate fails, return to Phase 4

## Browser Debugging Module

### Included Scripts
- `scripts/repro_browser_issue.py`
- `scripts/capture_browser_artifacts.py`
- `scripts/verify_browser_fix.py`

### Standard Browser Flow

```bash
# 1) Reproduce browser failure (expect fail)
python scripts/repro_browser_issue.py \
  --project-root . \
  --repro-cmd "pnpm exec playwright test tests/bug.spec.ts --project=chromium --workers=1 --retries=0" \
  --expect fail \
  --runs 2

# 2) Capture artifacts
python scripts/capture_browser_artifacts.py \
  --project-root . \
  --output-dir .debug/browser-artifacts

# 3) Verify fix (expect pass)
python scripts/verify_browser_fix.py \
  --project-root . \
  --verify-cmd "pnpm exec playwright test tests/bug.spec.ts --project=chromium --workers=1 --retries=0" \
  --runs 2 \
  --signature-file .debug/browser-repro/repro_report.json
```

Supported ecosystems:
- Playwright
- Cypress
- Selenium
- WebdriverIO

## Script Reference

### `repro_browser_issue.py`
- Re-runs repro command and checks deterministic signature
- Outputs: run logs + `repro_report.json`
- Exit codes: `0` success, `10` reproducibility failure

### `capture_browser_artifacts.py`
- Collects screenshots, traces, HAR/video/log artifacts into one bundle
- Outputs: artifact tree + `manifest.json`
- Exit codes: `0` success, `10` empty capture (unless `--allow-empty`)

### `verify_browser_fix.py`
- Re-runs verification command and checks old failure signature is absent
- Outputs: run logs + `verify_report.json`
- Exit codes: `0` success, `11` verification failure

## References

- `references/browser-repro-playbook.md`
- `references/browser-artifact-checklist.md`

## Folder Structure

```text
omnidebug-autopilot/
├─ SKILL.md
├─ README.md
├─ references/
│  ├─ browser-repro-playbook.md
│  └─ browser-artifact-checklist.md
└─ scripts/
   ├─ repro_browser_issue.py
   ├─ capture_browser_artifacts.py
   └─ verify_browser_fix.py
```

## Guardrails

- Never claim success without passing verification
- Never skip tests to force green state
- Never hardcode secrets/endpoints
- Never ship temporary bypasses as final fixes
- Keep fixes minimal and architecture-compatible

## License

MIT
