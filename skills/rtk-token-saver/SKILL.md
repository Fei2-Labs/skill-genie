---
name: "rtk-token-saver"
description: "Use rtk to reduce token usage from common shell, git, search, file-reading, test, build, and lint commands while preserving raw-output fallbacks when exact output is required."
license: "MIT"
metadata: {"version":"1.0.2","category":"developer-tools","triggers":["rtk","reduce tokens","large command output","compact shell output","token savings"],"license":"MIT","tags":["developer-tools","token-savings","shell-output","cli"],"hermes":{"tags":["developer-tools","token-savings","shell-output","cli"]}}
---

# RTK Token Saver

Use this skill when a task involves shell commands that may produce large output, especially repository inspection, git history, diffs, search, file reading, tests, linting, builds, logs, containers, or package manager output.

RTK is a CLI proxy that filters and compresses command output before it enters the agent context. Prefer RTK when compact output is enough to make the next decision. Use raw commands when exact bytes, full JSON, full logs, cryptographic material, or complete unmodified output is required.

## Activation Rules

Use RTK by default for:
- Directory listings and tree-like exploration.
- Git status, diffs, logs, pull, push, and GitHub CLI summaries.
- Search commands across large repositories.
- Reading large files when a concise view is sufficient.
- Test, lint, typecheck, and build commands where failures are the main signal.
- Docker, Kubernetes, AWS, package manager, and log output that may be noisy.

Do not use RTK when:
- The user explicitly asks for raw or complete output.
- The next step requires exact formatting, exact bytes, or complete structured data.
- A command output will be parsed programmatically by another command.
- Security-sensitive values may be exposed; avoid reading secrets at all.
- RTK is not installed or the relevant RTK wrapper fails. Fall back to the native command and keep output scoped.

## Install and Verify

Before relying on RTK, check whether it is available:

```bash
which rtk
rtk --version
rtk gain
```

If RTK is missing, do not install it silently. Report that RTK is unavailable and run the native command with the narrowest safe scope.

## Command Mapping

### Repository and File Exploration

Prefer:

```bash
rtk ls .
rtk find "*.ts" .
rtk read path/to/file.ts
rtk read path/to/file.ts -l aggressive
rtk smart path/to/file.ts
```

Instead of broad raw commands such as:

```bash
ls -laR .
find . -type f
cat path/to/large-file.ts
```

### Search

Prefer:

```bash
rtk grep "pattern" .
rtk grep "functionName" src
```

Use native grep, ripgrep, or repository search tools when exact match behavior, line ranges, or complete output is required.

### Git

Prefer:

```bash
rtk git status
rtk git diff
rtk git diff --stat
rtk git log -n 10
rtk gh pr list
rtk gh pr view 42
```

Use raw git commands when applying patches, generating exact diffs for review, or feeding output into another tool.

### Tests, Lint, Typecheck, and Build

Prefer RTK wrappers for high-noise checks:

```bash
rtk test npm test
rtk jest
rtk vitest
rtk pytest
rtk cargo test
rtk go test
rtk lint
rtk tsc
rtk next build
rtk cargo clippy
rtk ruff check
```

If a compact failure summary is not enough to fix the issue, rerun the smallest failing command natively with flags that show the exact failure.

### Logs and Services

Prefer:

```bash
rtk docker ps
rtk docker logs <container>
rtk docker compose ps
rtk kubectl pods
rtk kubectl logs <pod>
rtk aws logs get-log-events
rtk log path/to/app.log
```

Use raw output only when full logs are required for auditing, exact reproduction, or external attachment.

## Workflow

1. Check whether RTK is installed when the task would benefit from compact command output.
2. Use the RTK command that corresponds to the native command.
3. Inspect the compact output and decide the next smallest action.
4. If RTK hides information needed for correctness, rerun the native command with the narrowest scope that exposes the missing detail.
5. Record validation commands exactly, including whether RTK or native output was used.

## Guardrails

- Never use RTK as an excuse to skip validation.
- Never claim a test, lint, typecheck, or build passed unless the command exit status succeeded.
- Do not use RTK for commands whose output must be consumed exactly by a script or parser.
- Do not run broad commands just because RTK compresses output; keep command scope targeted.
- Respect project-specific tool preferences. If a project provides a preferred test or lint command, wrap that command with RTK only when compact output is appropriate.

## Completion Output

When RTK was used for important work, summarize:
- The RTK commands run.
- Whether any native command was rerun for exact output.
- Final validation status.
