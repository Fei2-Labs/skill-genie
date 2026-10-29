# Block Catalog — ecommerce-golive-check

The eight blocks in full. Each block names its **owning skill**, how to run it,
and what evidence proves a pass. The conductor reads the owning skill, runs it,
and records a verdict per `gate-schema.md`.

---

## Block 1 — Payment & checkout

**Owner:** `cross-layer-payment-provider-migration`

| Check | Pass evidence | Severity |
|-------|---------------|----------|
| Add-to-cart → checkout → provider → return works end to end | Screenshot/trace of a completed test order | 🔴 Blocking |
| Success, failure, and cancel returns all land on a correct page | 3 return URLs each verified | 🔴 Blocking |
| Amount / currency / tax / shipping computed correctly | Order total matches line items + rules | 🔴 Blocking |
| Refund path exists and is executable | Refund tested or documented | 🟠 High |
| Front-of-store copy names no unfamiliar processor | Grep of checkout/sales copy | 🟡 Medium |

Processor names only where legally required (terms/privacy) or where the customer
is visibly redirected to the hosted page. Use generic wording ("encrypted payment
service provider") elsewhere.

## Block 2 — Order webhook, status & confirmation email

**Owner:** `real-signed-webhook-replay-verification` (+ inline real-inbox email test)

| Check | Pass evidence | Severity |
|-------|---------------|----------|
| Webhook endpoint verifies signature | Real signed replay accepted; tampered payload rejected | 🔴 Blocking |
| `order_created` / `payment_succeeded` transitions order state | DB/state shows order moved to paid | 🔴 Blocking |
| Order confirmation email reaches the customer on a real test order | Email **received in a real inbox** from test order #N — not a mail-API 200 / "queued" | 🔴 Blocking |
| Confirmation email content correct + sender authenticated | Email shows right order #, line items, total, delivery/returns info; SPF/DKIM/DMARC pass; not in spam | 🟠 High |
| Failures retry or alert; no silent drop (orders or emails) | Retry/alert path shown | 🟠 High |

Use a **real signed** webhook replay, never a mock — a mock proves nothing about
signature verification. For the confirmation email, a mail-API `200` or a
"queued" status is **not** proof of delivery (repo lesson: a mailer whose live
send was never tested): place a real test order and confirm the email actually
arrives in a real inbox, from the correct authenticated sender, with the right
order details.

## Block 3 — Feature completeness

**Owner:** `nuxt-app-feature-gap-audit` + `audit-feature-claims-with-evidence`

| Check | Pass evidence | Severity |
|-------|---------------|----------|
| No fake data / stubs / placeholder on a shipping page | Grep + page walk | 🔴 Blocking |
| No auth gaps (protected endpoints require login) | Unauth request returns 401/redirect | 🔴 Blocking |
| No dead links / orphan endpoints | Link crawl | 🟠 High |
| Stock / out-of-stock state correct | Out-of-stock product shows correctly | 🟠 High |

## Block 4 — Legal compliance

**Owner:** `web-compliance-builder` (AUDIT mode if the site already exists)

| Check | Pass evidence | Severity |
|-------|---------------|----------|
| Required pages present per classification | Each required page returns 200 with real content | 🔴 Blocking |
| Each item labelled Legal / Platform / Best-practice / Risk-based | Gap table | — |
| No Mismatch (page contradicts actual practice) | Gap table shows no Mismatch | 🔴 Blocking |
| High-risk triggers escalated to "Legal review required" | Escalation list | 🟠 High |

Required-page set is computed from facts, not assumed. Typical ecommerce set:
Privacy, Cookie, Terms, Refund/Return, Shipping; add Subscription terms if
recurring billing, marketplace seller terms if multi-vendor.

## Block 5 — GDPR/DSGVO consent + Art. 13

**Owner:** `landing-launch-check` Phase 5

| Check | Pass evidence | Severity |
|-------|---------------|----------|
| Cookie banner appears on first visit | Fresh-session screenshot | 🔴 Blocking |
| "Accept all" / "Essential only" equally prominent | No dark pattern in banner | 🔴 Blocking |
| No third-party tag fires before consent | Network trace pre-consent | 🔴 Blocking |
| Consent recorded with timestamp, withdrawable | `/cookie-settings` works | 🟠 High |
| Privacy policy has all 8 Art. 13 elements | Keyword scan (controller, legal basis, retention, rights, supervisory authority e.g. IMY, processors, transfers, contact) | 🔴 Blocking |

## Block 6 — CRO conversion audit

**Owner:** `psychology-master` — `scripts/conversion_audit.py` + `references/conversion-optimization.md`

| Check | Pass evidence | Severity |
|-------|---------------|----------|
| Above-the-fold: value-prop headline, hero, CTA, social proof | Screenshot audit | 🟠 High |
| CTA action-oriented / first-person / specific / high-contrast | CTA copy + contrast | 🟠 High |
| Forms minimal, single-column, inline validation, progress on multi-step | Form walk | 🟡 Medium |
| Pricing: anchoring, tiers, charm pricing, value stack | Pricing page review | 🟡 Medium |
| Objection handling + friction reduced | Funnel walk | 🟡 Medium |
| **Ethics: no deception, no dark patterns, urgency/scarcity is real** | Scarcity claims cross-checked against reality | 🔴 Blocking |

CRO findings are mostly High/Medium — they cost conversions, they do not block a
legal launch. The ONE Blocking CRO item is the ethics gate: a fake countdown or
invented "only 2 left" is both a dark pattern and, in the EU, a potential UCPD
violation.

## Block 7 — Responsive adaptation (3 viewports)

**Owner:** `web-verify` (local); escalate to `ui-ux-pro-max` / `web-accessibility-audit` for depth

| Check | Pass evidence | Severity |
|-------|---------------|----------|
| Real-device screenshots at mobile ≤480, tablet 768–1024, desktop ≥1280 | 3 screenshots per key page | 🟠 High |
| Touch targets sized; images don't overflow; nav usable on small screens | Mobile screenshot review | 🟠 High |
| **Checkout completes on all three viewports** | Checkout tested per viewport | 🔴 Blocking |
| Accessibility: contrast, focus order, alt text | a11y audit | 🟡 Medium |

A store whose checkout is broken on mobile is not launch-ready — mobile is the
majority of ecommerce traffic, so that single item is Blocking.

## Block 8 — SEO / AEO / GEO

**Owner:** `landing-launch-check` Phase 2–4 (+ remote `seo-aeo-audit`)

| Check | Pass evidence | Severity |
|-------|---------------|----------|
| Per-locale title / description / canonical / hreflang | Each locale served correct meta | 🔴 Blocking (wrong-locale meta) |
| JSON-LD (Organization / WebSite / Product / FAQPage) | Valid JSON-LD present | 🟠 High |
| sitemap / robots present; auth pages not indexed | sitemap 200, robots disallows /login etc. | 🟠 High |

Wrong-locale meta (a Swedish store serving English `<title>` to Google.se) is
Blocking because it breaks indexing in the target market.

---

## Release hygiene (Step 2, not a numbered block)

| Check | Pass evidence | Severity |
|-------|---------------|----------|
| Deployed commit == served commit | `web-verify` parity check | 🔴 Blocking |
| No real infra identifiers in public artifacts | Identifier-class scan (IPs, instance/app/company names, abs paths) | 🔴 Blocking |
| CI green for the release commit | CI run link | 🟠 High |
| Secrets read at runtime, not hardcoded | Grep for hardcoded keys | 🔴 Blocking |
