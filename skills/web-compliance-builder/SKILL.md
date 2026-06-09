---
name: "web-compliance-builder"
description: "Classify a web business, then identify, draft, and checklist the compliance pages, notices, disclosures, user flows, and launch gates it needs. Use when the user wants a Privacy Policy, Cookie Policy / banner, Terms of Service, Refund/Return Policy, Shipping Policy, Subscription Terms, Acceptable Use Policy, DPA outline, Accessibility Statement, AI disclosure, children/age notice, marketing-consent language, marketplace seller terms, GDPR/UK-GDPR/PECR/CCPA/CPRA/PIPEDA/CASL/Australian Privacy Act compliance, App Store / Google Play / Shopify / ad-platform requirements, a website compliance requirements matrix, a launch/go-live checklist, or a red-flag report. Also audits existing sites (审计/review/合规检查): existing pages or a URL → gap report + fixes. Covers ecommerce, dropshipping, digital products, subscriptions, SaaS, app landing pages, marketplaces, affiliate/lead-gen, AI products, newsletters, and cross-border stores. Classifies first; never drafts generic policies blind. Not legal advice."
license: "MIT"
metadata: {"version":"1.1.0","category":"legal-compliance","tags":["compliance","privacy-policy","gdpr","ccpa","cookies","terms-of-service","ecommerce","saas"],"license":"MIT","hermes":{"tags":["compliance","privacy-policy","gdpr","ccpa","cookies","terms-of-service","ecommerce","saas"]}}
allowed-tools: Read, Write, Edit, AskUserQuestion, Bash, Glob, Grep
---

# web-compliance-builder

A **fact-driven compliance classifier**, a **modular document generator**, and an **evidence-based release gate**. Classify the business first; map facts to obligations; emit only what the facts trigger; label every item by who requires it; surface uncertainty instead of hiding it.

## Purpose

Help users identify, draft, review, and checklist the compliance pages, notices, disclosures, user flows, and launch controls needed for websites, stores, SaaS products, apps, landing pages, and marketplaces.

Built for: ecommerce stores · dropshipping stores · digital-product stores · subscription / membership sites · B2C and B2B SaaS · mobile app homepages / landing pages · marketplaces and multi-vendor platforms · affiliate and lead-generation sites · AI product websites · newsletter / email-capture pages · cross-border stores.

## What this skill does

- Classify the business model **before drafting anything**.
- Determine target regions and likely legal exposure.
- Identify data collection, cookies, pixels, analytics, advertising, and SDK usage.
- Identify product and transaction types (goods, digital, services, subscriptions, in-app).
- Detect high-risk domains and sensitive data.
- Generate the required-pages list, page outlines, and first-draft text.
- Generate page-level and go-live checklists with evidence fields.
- Mark unresolved issues that need legal review.
- Produce a blocking launch-gate with pass/fail evidence.

## What this skill must NOT do

- Present generic privacy policies or terms without first classifying the business.
- Treat all outputs as legal requirements.
- Claim jurisdiction-wide certainty where rules are state- or country-specific.
- Give legal advice.
- Hide uncertainty.
- Assume a platform template (Shopify/Apple/Google) is legally sufficient on its own.
- Claim a page is complete without checking the actual facts of the business.

## Mandatory workflow (in order)

1. Identify business type — `references/business-types.md`.
2. Identify target markets and user regions — `references/jurisdictions.md`.
3. Identify data collection and tracking.
4. Identify transaction model: refunds, subscriptions, shipping, taxes, payment methods.
5. Identify high-risk domains and sensitive data.
6. Generate the required-pages list — `references/page-requirements.md`.
7. Generate page-level outlines.
8. Generate first-draft text — `references/policy-templates.md`.
9. Generate the page-level compliance checklist — `references/checklist-framework.md`.
10. Generate the final go-live checklist.
11. Mark legal-review issues.
12. Produce a blocking gating checklist.

Run the questionnaire first (`scripts/compliance_questionnaire.py` for the layered question set). Populate the structured intake object — it is the single source of truth for every downstream output. Then feed it to `scripts/checklist_generator.py` for the deterministic page + gating output. Scripts assemble; they do **not** interpret law on their own.

## Two modes: BUILD vs AUDIT

- **BUILD (default)** — greenfield. The mandatory workflow above generates the pages a site *needs*. Use when the user is creating a site/store/app or has no compliance pages yet.
- **AUDIT** — review an *existing* site. Use when the user says 审计 / audit / review my existing site / 合规检查现有网站 / "check what's wrong with my policies" / pastes existing Privacy Policy / ToS / Cookie pages or a URL. Do **not** draft from scratch first — diagnose the gap.

Pick AUDIT when existing pages/URL are provided or the user asks to review/check an existing site. Otherwise BUILD. Both still start with classification (steps 1–5) — you cannot audit without knowing the business type, regions, data, and transactions. Full audit procedure: `references/audit-workflow.md`.

### AUDIT workflow (replaces steps 6–12 when auditing)

1. Steps 1–5 above (classify business, regions, data, transactions, risk).
2. Inventory existing pages the user provided (PP, CP, ToS, RR, SP, banner, etc.) and capture each page's actual content/claims.
3. Compute the **required** set from facts (same as BUILD step 6).
4. For each required item, judge status: **Present-OK** / **Present-Inadequate** / **Missing** / **Mismatch** (page contradicts actual practice — the worst, per the red-flag rules).
5. For present pages, run the per-page **failure-mode** checks in `references/page-requirements.md` and the live-behavior checks in `references/checklist-framework.md` (e.g. pre-consent tag firing, buried reject button, hidden return address).
6. Output a **gap report** (see audit output below) + the red-flag report + a remediation gating checklist (Blocking gaps first).
7. Mark legal-review issues and uncertainty labels as in BUILD.

Feed the intake object — now including `existing_pages` and `mode: "audit"` — to `scripts/checklist_generator.py --audit` for the deterministic required-vs-existing gap table.

## The four labels (apply to EVERY requirement)

- **Legal requirement** — comes from a statute / regulator / official legal text.
- **Platform requirement** — comes from a distribution or payments channel that can block publication, ads, or selling (Apple, Google Play, Shopify, Google/Meta/TikTok Ads, Amazon).
- **Best practice** — reduces risk / improves trust; not always mandatory.
- **Risk-based recommendation** — operationally wise default given the facts.

This separation keeps outputs honest. Many things users think are "mandatory" are only platform rules or wise defaults (e.g. an accessibility statement is not universally mandatory, but accessibility itself can be a legal requirement for EAA-covered EU services; an AI disclosure is legally required only in some scenarios).

## Required disclaimer (append to every substantive output)

> This output is not legal advice. Compliance requirements vary by jurisdiction, business model, and actual operational practice. High-risk, regulated, sensitive-data, or cross-border businesses should have final materials reviewed by qualified counsel. This skill provides drafting support, issue spotting, and checklisting only.

## Escalation — auto-mark "Legal review required" if the business

- Targets children, or is likely accessed by children.
- Processes health, biometric, financial, employment, or precise-location data.
- Offers AI systems with material user impact (scoring, decisions, synthetic media).
- Operates a marketplace or UGC platform.
- Uses aggressive subscription / trial-to-paid flows.
- Relies on cross-border fulfilment with unclear seller identity or return location.
- Combines multiple jurisdictions with conflicting requirements.
- Plans to rely on consent as the legal basis for complex profiling.
- Processes customer data as a SaaS processor without a DPA framework.
- Operates in a regulated vertical.

## Uncertainty labels

When the law or platform layer is unsettled, surface one of these automatically: **Needs verification** (rule changing / effective-date edge), **Jurisdiction-specific** (state/country implementation varies), **Legal review required** (high-risk trigger). Re-check these before launch.

## Evidence-first checklisting

Every checklist item carries: requirement · why it matters · applies when · evidence needed · pass/fail · source · owner · review frequency. See `references/checklist-framework.md` and the gating schema there. Lift only **Blocking** items into the go-live gate.

## Audit output (AUDIT mode only)

When auditing an existing site, default output is:

1. **Gap report** — table of `Required item · Class · Status (Present-OK / Present-Inadequate / Missing / Mismatch) · Finding · Fix`. One row per required item.
2. **Red-flag report** — Mismatch and high-risk findings first (page contradicting actual practice ranks Blocking).
3. **Remediation gating checklist** — Blocking gaps to fix before the site is compliant, evidence-bound.
4. **Needs-verification / Legal-review** — surfaced as in BUILD.

Do not silently re-draft pages during an audit. Report the gap; offer to draft/fix only after the gap report, or when the user asks.

## Reference files (load on demand)

- `references/jurisdictions.md` — region-by-region rules, triggers, terminology, verification flags (EU/EEA, UK, US baseline + California, Canada, Australia).
- `references/business-types.md` — business taxonomy, data/transaction patterns, default pages, common red flags.
- `references/page-requirements.md` — page-by-page decision matrix: when each page is required / recommended / inapplicable, mandatory sections by trigger and region.
- `references/policy-templates.md` — modular clause library and policy skeletons.
- `references/checklist-framework.md` — page-level + launch + red-flag checklist schemas and the gating-item schema.
- `references/audit-workflow.md` — AUDIT mode: how to inventory existing pages, grade present/missing/inadequate/mismatch, run failure-mode + live-behavior checks, and produce the gap report.
- `references/source-register.md` — source inventory with jurisdiction, last-checked date, review cadence, change risk, and affected modules.

## Scripts

- `scripts/compliance_questionnaire.py` — prints the layered questionnaire and emits an empty structured intake object to fill.
- `scripts/checklist_generator.py` — transforms the filled intake object (JSON) into a required-pages list and gating checklist rows. Deterministic; no legal interpretation.
