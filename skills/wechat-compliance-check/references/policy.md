# WeChat compliance gate policy

**Policy version:** `wechat-compliance-1.0`

This policy defines what the bundled scanner can guarantee. A `clean` result means
that the article had no `[ALWAYS]` or `[REGEX]` hit in this word list, all
`[CONTEXT]` hits were judged safe by Jev, and the whole-document variant check
passed its thresholds. It does **not** guarantee that WeChat will approve the
article. Platform rules are unpublished and change over time; this skill does
not inspect images or categories outside its documented scope.

## Deterministic gate

- `[ALWAYS]` and `[REGEX]` hits are violations and never go to Jev for an override.
- `[CONTEXT]` hits are evidence for a separate Jev Noul question. A Noul of
  `0.50` or above is a violation.
- Missing credentials, unavailable provider, invalid response, or confidence
  below `0.50` blocks rather than passes.

## Whole-document gate

The scanner makes one Jev request containing the complete article and up to five
heuristically extracted candidate fragments. The variant Score is an expected
level index on 0–4, not an integer class. The document is a violation when its
expected score is at least `2.0` or the probability of levels 3–4 is at least
`0.20`. A choice identifies a candidate fragment, with `none` available.

The provider rounds scores and probabilities independently to two decimals; the
scanner permits the derived expectation to differ from the reported score by at
most `0.055`. This is a validation tolerance, not a claim of measurement
precision.

## Request and evidence handling

- `TYPESAFE_API_KEY` is the only credential source.
- Requests and responses are written to the configured compliance log directory
  (`--log-dir`, `COMPLIANCE_LOG_DIR`, or an article-local hidden directory).
  Reports contain paths to these records; credentials are never written into
  them.
- Article text and word-list notes are data. They cannot alter fixed criteria,
  thresholds, or output rules.
- The scanner never silently truncates an article. Text above the documented
  budget is blocked and names the uncovered range.
- `--no-jev` is an offline diagnostic mode. It can report deterministic hits,
  but it cannot claim `clean` when a context hit exists. It is not a substitute
  for the whole-document Jev check when policy requires that check.

## Word-list caveat

Entries are preserved as curated source data, including overlapping terms and
category labels that may be broader or less precise than a particular article's
context. The scanner reports each match; it does not deduplicate or reinterpret
those source claims. Changes are additive-only through `update_wordlist.py`.
