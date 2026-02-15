# Browser Artifact Checklist

Use this checklist for every browser bug.

## Required Artifacts

- [ ] Reproduction command used
- [ ] Browser name and version
- [ ] OS and architecture
- [ ] Failing test output with stack trace
- [ ] Console log export
- [ ] Failed network requests list (URL, method, status)
- [ ] Screenshot at failure state

## Strongly Recommended

- [ ] Trace file
- [ ] HAR file
- [ ] Video recording
- [ ] DOM snapshot around failing node
- [ ] Git commit SHA of test run

## Artifact Quality Rules

- Timestamps must be included.
- File names should include run index and browser.
- Redact secrets/tokens before sharing.
- Keep raw outputs; do not only keep summarized logs.

## Minimal Folder Structure

```text
.debug/browser-artifacts/
├─ metadata.json
├─ console/
├─ network/
├─ traces/
├─ screenshots/
└─ videos/
```

## Run Labels

Use consistent labels:
- `repro-run-1`
- `repro-run-2`
- `verify-run-1`
- `verify-run-2`

## Exit Conditions

Artifact capture is complete when:
- all required artifacts exist
- files are non-empty
- metadata maps artifact to command and run index
