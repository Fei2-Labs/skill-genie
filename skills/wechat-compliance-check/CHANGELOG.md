# Changelog

All notable changes to `wechat-compliance-check` will be documented here.

## 1.1.0 - 2026-09-29

### Added

- Standard-library `scripts/compliance_scan.py` with strict word-list parsing,
  deterministic `[ALWAYS]`/`[REGEX]` gates, contextual Jev questions, and a
  whole-document variant check.
- Standard-library `scripts/update_wordlist.py` with verified-evidence input,
  additive-only assertions, source metadata, threshold filtering, and a per-run
  addition cap.
- Versioned gate policy and monthly research/update procedure.
- Offline tests for standalone execution, strict parsing, fail-closed provider
  handling, response validation, logging boundaries, and forged evidence.

### Changed

- Documentation now describes exit codes and the actual guarantee boundary:
  zero hits against the current word list is not a guarantee of WeChat approval.
- Existing word-list entries remain unchanged, including overlapping terms and
  broad category labels.
