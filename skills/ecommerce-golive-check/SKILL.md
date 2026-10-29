---
name: "ecommerce-golive-check"
description: "Pre-launch go-live gate for an ecommerce / online store. Orchestrates the existing specialist skills into one ordered, evidence-based checklist with a BLOCKING launch gate: payment & checkout end-to-end, order webhook signature + status flow, feature completeness (no stubs / fake data / auth gaps), legal compliance (GDPR/DSGVO cookie consent, required policy pages, Art. 13 elements) via web-compliance-builder, CRO conversion audit via psychology-master, responsive adaptation on mobile / tablet / desktop via web-verify, SEO/AEO/GEO, deployed-vs-served parity, and release hygiene (no real infra identifiers, CI green, secrets read at runtime). Use when the user says 电商上线检查 / go-live check / 上线前检查 / pre-launch audit / 发布清单 for a store, or wants to verify an ecommerce site is ready to launch. Classifies the store first; marks every item Blocking / High / Medium / Low; produces a pass/fail gate, not prose. Not legal advice."
license: "MIT"
metadata: {"version":"1.1.0","category":"launch-qa","license":"MIT","tags":["ecommerce","go-live","launch","audit","checklist","gdpr","dsgvo","cro","responsive","payments","webhook","seo"],"hermes":{"tags":["ecommerce","go-live","launch","audit","checklist","gdpr","dsgvo","cro","responsive","payments","webhook","seo"]}}
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
---

# ecommerce-golive-check

An **orchestration** skill. It does not re-implement checks — it sequences the
repo's existing specialist skills into one ordered pre-launch flow and rolls
their findings up into a single **blocking go-live gate**.

The deliverable is a **gate (pass/fail with evidence), not a report**. A store is
"launch-ready" only when every Blocking item passes with recorded evidence.

## When to use

- The user says 电商上线检查 / 上线前检查 / go-live check / pre-launch audit /
  发布清单 for a store, shop, or ecommerce site.
- A store was built (often on a shared app layer) and needs a final sign-off
  before it takes real orders and real money.
- Auditing an existing live store for launch-readiness gaps.

Not for: a pure marketing landing page with no transactions — use
`landing-launch-check` directly. This skill calls `landing-launch-check` for the
SEO/compliance block, then adds the ecommerce-only blocks (payment, webhook,
order flow, CRO, responsive) on top.

## Delegated skills (the orchestra)

This skill is the conductor. Each block below is OWNED by a specialist skill —
read and run that skill for the block, then record its verdict here. Never
re-derive a check this skill already delegates.

| Block | Owned by | Lives in |
|-------|----------|----------|
| Legal compliance (classify, policies, GDPR/DSGVO, cookie consent) | `web-compliance-builder` | repo |
| GDPR Art. 13 + cookie-banner live behavior + SEO/AEO/GEO | `landing-launch-check` | repo |
| CRO conversion audit (funnel, CTA, forms, pricing, trust, ethics) | `psychology-master` | repo |
| Responsive adaptation (mobile / tablet / desktop) + a11y | `web-verify` (local); `ui-ux-pro-max`, `web-accessibility-audit` (remote) | repo + skills.yaml |
| Payment & checkout, settlement, refunds, readiness gate | `cross-layer-payment-provider-migration` | installed (auto/) |
| Order webhook signature + status flow + confirmation email delivery | `real-signed-webhook-replay-verification` (+ inline real-inbox email test) | installed (auto/) |
| Feature completeness (stubs, fake data, auth gaps, dead links) | `nuxt-app-feature-gap-audit` / `audit-feature-claims-with-evidence` | installed (auto/) |
| Ad pixel consent-gating + conversion events | `verify-consent-gated-ad-pixel-launch` | installed (auto/) |
| Deployed-vs-served parity, real-device screenshots | `web-verify` / `verify-and-ship-visual-data-fix` | repo + installed |

If a delegated skill is not installed, mark its block **Needs-skill** in the
gate (not silently skipped) and tell the user which one to install.

## Mandatory workflow (in order)

### Step 0 — Classify the store first

Never run checks blind. Establish, via `web-compliance-builder` step 1–5 and the
questionnaire (`scripts/intake.py` here, or
`web-compliance-builder/scripts/compliance_questionnaire.py`):

- Business model: own-stock / dropshipping / digital goods / subscription / marketplace / cross-border
- Target markets (which drives GDPR vs CCPA vs PIPEDA…)
- Payment provider(s) and whether checkout is hosted or embedded
- Data collected, cookies, pixels, analytics, SDKs
- Fulfilment & returns model (who ships, where returns go)

The intake object is the single source of truth for every downstream block.

### Step 1 — Run each block through its owning skill

Run the eight blocks below. For each, read the owning skill, run it, and record:
**status (Pass / Fail / Warning / Needs-skill) · evidence · severity · fix**.

1. **Payment & checkout** → `cross-layer-payment-provider-migration`
   - Add-to-cart → checkout → provider → success/fail/cancel return all land correctly
   - Amount, currency, tax, shipping computed right; refund path exists
   - Front-of-store copy does not name unfamiliar processors (generic wording)
2. **Order webhook, status & confirmation email** → `real-signed-webhook-replay-verification` (+ inline email-delivery test)
   - Webhook endpoint verifies signature (real signed replay, not a mock)
   - `order_created` / `payment_succeeded` actually transitions order state
   - **Order confirmation email actually reaches the customer on a real test order** — received in a real inbox, NOT just a mail-API `200` / "queued" (a queued send is not a delivered email)
   - Confirmation email has correct order details (order number, line items, total, delivery/returns info) and an authenticated sender (SPF/DKIM/DMARC pass, not landing in spam)
   - Failures retry or alert; no silent dropped orders and no silently dropped emails
3. **Feature completeness** → `nuxt-app-feature-gap-audit` + `audit-feature-claims-with-evidence`
   - No fake data / stubs / placeholder content on a shipping page
   - No auth gaps (endpoints that should require login do)
   - No dead links / orphan endpoints; stock / out-of-stock state correct
4. **Legal compliance** → `web-compliance-builder` (AUDIT mode if the site exists)
   - Required pages present per classification (Privacy, Cookie, ToS, Refund/Return, Shipping, Subscription terms)
   - Each item labelled Legal / Platform / Best-practice / Risk-based
   - Gap report with Present-OK / Inadequate / Missing / **Mismatch**
   - Auto-escalate "Legal review required" on high-risk triggers
5. **GDPR/DSGVO consent + Art. 13** → `landing-launch-check` Phase 5
   - Cookie banner on first visit; "Accept all" and "Essential only" equally prominent (no dark pattern)
   - **No third-party tag fires before consent**
   - Privacy policy carries all 8 Art. 13 elements (controller, legal basis, retention, rights, supervisory authority, processors, transfers, contact)
6. **CRO conversion audit** → `psychology-master` (`conversion_audit.py` + `references/conversion-optimization.md`)
   - Above-the-fold: value-prop headline, hero, CTA, social proof
   - CTA: action-oriented, first-person, specific, high-contrast, anxiety reducers
   - Forms: minimal fields, single column, inline validation, progress on multi-step
   - Pricing: anchoring, tiers, charm pricing, value stack
   - Objection handling + friction (cognitive/emotional/physical/social)
   - **Ethics gate**: no deception, no dark patterns; urgency/scarcity must be real
7. **Responsive adaptation (3 viewports)** → `web-verify` (+ `ui-ux-pro-max` / `web-accessibility-audit`)
   - Real-device screenshots at mobile (≤480), tablet (768–1024), desktop (≥1280)
   - Touch targets sized, images don't overflow, nav usable on small screens
   - **Checkout flow completes on all three**
   - Accessibility: contrast, focus order, alt text
8. **SEO / AEO / GEO** → `landing-launch-check` Phase 2–4 (+ remote `seo-aeo-audit`)
   - Per-locale title / description / canonical / hreflang (no leaked wrong-locale meta)
   - JSON-LD (Organization / WebSite / Product / FAQPage) for AI search citation
   - sitemap / robots; auth pages not indexed

### Step 2 — Deployed-vs-served parity + release hygiene

- `web-verify`: the commit deployed is the commit served (no "it's only on a branch")
- No real infrastructure identifiers in any public artifact (prod IPs, instance/app names, company name, absolute paths)
- CI exists and is green for the release commit
- Secrets read at runtime, never hardcoded

### Step 3 — Roll up into the blocking gate

Run `scripts/gate.py` with the recorded block verdicts (JSON). It produces:

1. **Summary table** — block × status × severity
2. **Blocking gate** — every Blocking item with pass/fail + evidence; ANY
   Blocking fail ⇒ **NOT launch-ready**
3. **Remediation list** — ordered by severity
4. **Needs-verification / Legal-review** — surfaced, not hidden
5. **Disclaimer** — this is not legal advice

## Severity → gate mapping

| Severity | Examples | Gate effect |
|----------|----------|-------------|
| 🔴 Blocking | payment can't complete, webhook unverified, order confirmation email never reaches the customer, tag fires pre-consent, missing required legal page, checkout broken on mobile, wrong-locale meta, real infra identifier in public artifact | Fails the gate |
| 🟠 High | missing JSON-LD, weak CTA, inadequate (present-but-thin) policy, no refund path shown | Fix before launch; recorded as waiver if overridden |
| 🟡 Medium | suboptimal pricing layout, minor a11y, medium form friction | Fix after launch |
| 🟢 Low | cosmetic, future improvement | Backlog |

A Blocking fail cannot be waived silently. If the user chooses to launch anyway,
`gate.py` records it as an explicit **waiver with reason**, so the gate output
still tells the truth.

## Scripts

- `scripts/intake.py` — prints the ecommerce-specific intake questionnaire and
  emits an empty structured intake object (JSON) to fill. Superset of
  `web-compliance-builder`'s intake with payment/webhook/fulfilment fields.
- `scripts/gate.py` — takes the filled intake + per-block verdicts (JSON) and
  emits the summary table, the blocking gate, and the remediation list.
  Deterministic; assembles, does not interpret law or judge CRO itself.

## Reference files (load on demand)

- `references/block-catalog.md` — the eight blocks in full: every check, its
  owning skill, how to run it, and what evidence proves a pass.
- `references/gate-schema.md` — the verdict JSON schema `gate.py` consumes and
  the pass/fail rules.

## Required disclaimer (append to every gate output)

> This output is not legal advice. Compliance and launch-readiness vary by
> jurisdiction, business model, and actual operational practice. High-risk,
> regulated, sensitive-data, or cross-border stores should have final materials
> reviewed by qualified counsel. This skill orchestrates issue-spotting,
> checklisting, and gating only.
