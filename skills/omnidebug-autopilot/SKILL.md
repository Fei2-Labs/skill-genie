---
name: omnidebug-autopilot
description: Autonomous end-to-end debugging skill for any codebase, language, and framework. Detects stack, reproduces failures, isolates root cause, applies minimal safe fixes, and verifies with tests/build/lint without user interruption.
license: MIT
metadata:
  version: 1.0.0
  category: debugging
---

# OmniDebug Autopilot

// TODO: split SKILL.md into smaller modules/components

Universal debugging skill for apps, services, libraries, and scripts across mainstream stacks.
Default mode is autonomous execution: find root cause and ship a verified fix without pausing for user input.

## Quick Start

Use this skill when requests include:
- "debug this"
- "fix this bug"
- "why is this failing"
- "find root cause"
- "auto fix"

Execution contract:
1. Detect language, framework, package manager, and test runner.
2. Reproduce the failure with a single deterministic command.
3. Collect evidence from logs, traces, network, and failing tests.
4. Isolate the smallest root cause (code, config, env, data, dependency, race, permissions).
5. Apply the minimum correct fix.
6. Re-run verification gates until green.

## Non-Interruption Policy

- Do not ask follow-up questions during normal debugging.
- Continue autonomously through analysis, patching, and verification.
- Only stop when blocked by missing secrets, unavailable infrastructure, or destructive action risk.
- If blocked, use the safest fallback and continue as far as possible.

## Mainstream Debug Process

### Phase 1: Triage

- Capture exact error text and failing command.
- Use debugging tools first: console logs and network requests before code edits.
- Identify regression window from recent diffs if available.
- Determine scope: runtime error, failing test, build failure, performance issue, or security defect.

### Phase 2: Reproduction

- Create one reproducible command.
- Remove noise by disabling unrelated jobs and minimizing input.
- Prefer deterministic seeds and controlled timing.
- Confirm failure reproduces at least twice.
- Browser-specific reproducibility rules:
  - Pin browser (`chromium`/`firefox`/`webkit`), viewport, locale, and timezone.
  - Freeze test data and seed values.
  - Disable retries during repro.
  - Persist traces, screenshots, videos, and HAR files.

### Phase 3: Evidence Collection

Collect only relevant artifacts:
- Console and application logs
- Test output with stack traces
- Network failures and status codes
- Runtime metrics (latency, memory, CPU) when performance related
- Config/env differences between working and failing contexts
- Browser artifacts bundle:
  - Devtools console log export
  - Failed request waterfall with request/response metadata
  - Reproduction trace and screenshot at failure frame
  - Browser/version and OS metadata

### Phase 4: Root Cause Analysis

Use this chain:
1. Symptom statement
2. Immediate fault location
3. Underlying mechanism
4. Trigger condition
5. Why safeguards missed it

Root cause must be a single falsifiable statement tied to evidence.

### Phase 5: Fix Strategy

- Prefer the smallest change that resolves cause, not symptom masking.
- Keep public API behavior stable unless the bug requires a behavior correction.
- Add or update tests that fail before and pass after fix.
- Avoid temporary bypasses (`@ts-ignore`, disabled tests, silent catches).

### Phase 6: Verification Gates

All applicable gates must pass:
- Unit, integration, and e2e tests
- Lint and static analysis
- Type checks
- Build and package
- Relevant runtime smoke check

If any gate fails, loop back to Phase 4.

## Browser Reproduction Module

Use these scripts for browser bug reproduction and fix validation:

```bash
# 1) Reproduce failure deterministically (expected to fail)
python scripts/repro_browser_issue.py \
  --project-root . \
  --repro-cmd "pnpm exec playwright test tests/bug.spec.ts --project=chromium --workers=1 --retries=0" \
  --expect fail \
  --runs 2

# 2) Capture browser debugging artifacts into one bundle
python scripts/capture_browser_artifacts.py --project-root . --output-dir .debug/browser-artifacts

# 3) Verify fix deterministically (expected to pass)
python scripts/verify_browser_fix.py \
  --project-root . \
  --verify-cmd "pnpm exec playwright test tests/bug.spec.ts --project=chromium --workers=1 --retries=0" \
  --runs 2 \
  --signature-file .debug/browser-repro/repro_report.json
```

Supported frameworks: Playwright, Cypress, Selenium, WebdriverIO.
Use project-native commands first; scripts only orchestrate repeatable debug workflow.

## Stack Detection and Default Commands

| Stack | Detect Signals | Verify Commands |
|------|----------------|----------------|
| Node.js / TypeScript | `package.json`, `tsconfig.json` | `pnpm test`, `pnpm lint`, `pnpm typecheck`, `pnpm build` |
| Python | `pyproject.toml`, `requirements.txt` | `pytest -q`, `ruff check .`, `mypy .` |
| Go | `go.mod` | `go test ./...`, `go vet ./...` |
| Rust | `Cargo.toml` | `cargo test`, `cargo clippy -- -D warnings` |
| Java/Kotlin | `build.gradle`, `pom.xml` | `./gradlew test`, `./gradlew build` or `mvn test` |
| Ruby | `Gemfile` | `bundle exec rspec`, `bundle exec rubocop` |
| PHP | `composer.json` | `composer test`, `vendor/bin/phpunit` |
| .NET | `*.sln`, `*.csproj` | `dotnet test`, `dotnet build` |
| Swift (iOS/macOS) | `Package.swift`, `*.xcodeproj` | `swift test` or `xcodebuild test` |

Pick commands from project scripts first; use defaults only if scripts are missing.

## Auto-Fix Heuristics

Prioritize fixes in this order:
1. Incorrect logic or branching
2. Null and undefined handling at source
3. Async and concurrency ordering
4. Contract and schema mismatch
5. Config and environment mismatch
6. Dependency incompatibility
7. Resource, path, or permission issues

For each candidate fix:
- Estimate blast radius
- Choose the lowest-risk valid option
- Verify with targeted tests, then full gates

## Guardrails

- Never claim success without passing verification.
- Never skip tests to make status green.
- Never introduce permanent production `console.log` noise.
- Never hardcode secrets or private endpoints.
- Preserve existing style and architecture conventions.

## Completion Criteria

A task is complete only when all are true:
- Reproduction exists for the original failure
- Root cause statement is evidence-backed
- Fix addresses root cause directly
- Verification gates pass
- Regression coverage is added or updated

## Output Format

Return concise sections:
1. Root cause
2. Applied fix
3. Verification commands and results
4. Remaining risk (if any)

## Resources

- `references/browser-repro-playbook.md`
- `references/browser-artifact-checklist.md`
- `scripts/repro_browser_issue.py`
- `scripts/capture_browser_artifacts.py`
- `scripts/verify_browser_fix.py`
