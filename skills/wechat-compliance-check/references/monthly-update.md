# Monthly word-list update procedure

This document is the complete procedure for the monthly agent job. It may
research and propose additions, but it may not delete, reorder, downgrade, or
rewrite existing word-list entries. The update script enforces that boundary;
this procedure must not bypass it.

## Schedule and context

Run on day 3 of each month at 09:00 in `Europe/Stockholm`, with a fresh,
non-persistent agent session and a one-hour timeout. The job needs the skill's
normal context because it researches web sources. No credential value, provider
response body, or private path belongs in a notification.

## Procedure

1. Research approximately the previous 35 days: WeChat official violation
   notices and announcements, platform policy pages, and clearly attributed
   community reports. Record a URL and collection date for every candidate. Do
   not invent a source or treat a search snippet as a source.
2. Ask Jev once for every candidate. Record a Score distribution for evidence
   reliability and a Noul for whether an existing entry or regex already covers
   it. Preserve the complete probabilities and confidence. A candidate without
   a validated Jev assessment is not eligible for the updater.
3. Write an array of candidate objects to `candidates.json` using the contract
   accepted by `scripts/update_wordlist.py`. Include the verified Jev record,
   not only a caller-supplied `evidence_score`.
4. Create `auto/wordlist-YYYY-MM` from `origin/main`; do not work on `main`.
5. Run:

   ```bash
   python3 skills/wechat-compliance-check/scripts/update_wordlist.py \
     --candidates candidates.json --run-id monthly-YYYY-MM
   ```

   If it fails or adds zero entries, do not commit or push. Notify the exact
   stage and reason. The updater restores the original file after a failed
   write or validation.
6. Run the word-list validator and the complete offline test suite. If either
   fails, do not commit or push.
7. Commit only the additive word-list change with:
   `chore(wechat-compliance-check): monthly wordlist update YYYY-MM (+N)`.
   Push only `auto/wordlist-YYYY-MM`. Never merge it to `main` and never publish
   the skill automatically.
8. Notify the user with the number added, rejection counts by reason, branch,
   run ID, and at most the three highest-scoring additions with their source
   URLs. On failure report the stage and a local reason, never raw provider
   bodies.

Research failure, missing credentials, provider failure, invalid Jev output,
zero candidates, updater failure, tests failure, or push failure all stop the
job without changing the word list on disk. Human review remains required for
merge and publication.
