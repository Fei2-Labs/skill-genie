# Checklist Framework

Evidence-led, not prose-led. Every item binds to verifiable evidence and an owner. Only **Blocking** items are lifted into the go-live gate.

## Gating-item schema

```yaml
gating_checklist_item:
  id: string
  severity: Blocking | High risk | Medium risk | Best practice
  class: Legal requirement | Platform requirement | Best practice | Risk-based recommendation
  requirement: string
  why_it_matters: string
  applies_when: string
  evidence_needed:
    - string
  pass_fail_status: Pass | Fail | Partial | Unknown
  source:
    name: string
    citation: string
    review_date: YYYY-MM-DD
  owner: Legal | Product | Engineering | Marketing | Operations | Content | Founder
  review_frequency: Launch-only | Quarterly | Semi-annual | Annual | On-change
  notes: string
  legal_review_required: true | false
```

Rendered row:

| Severity | Requirement | Why it matters | Applies when | Evidence needed | Status | Source | Owner | Review frequency |
|---|---|---|---|---|---|---|---|---|
| Blocking | Non-essential cookies must not fire before consent in EU/UK flows | Unlawful tracking can invalidate consent and trigger complaints/enforcement | EU/UK visitors + analytics/ads pixels active | CMP config; tag audit; screenshots; test logs | Fail | ePrivacy / ICO / EDPB | Engineering | Quarterly |

## Generation workflow (deterministic)

1. **Requirement extraction** — convert law/platform/best-practice rules into checklist items.
2. **Applicability filter** — keep only items triggered by the intake facts.
3. **Severity scoring** — Blocking / High risk / Medium risk / Best practice.
4. **Evidence binding** — require screenshot, URL, config export, platform field, or sample email/SMS copy.
5. **Owner assignment** — Product / Legal / Engineering / Marketing / Ops / Content / Founder.
6. **Pass/fail** — Pass / Fail / Partial / Unknown.
7. **Lawyer escalation** — attach legal-review reason where triggered.
8. **Gating extraction** — lift only Blocking items into the go-live gate.

## Checklist schemas (one per surface)

Generate the subset triggered by the business. Each uses the gating-item fields above.

- **Homepage / landing page** — policy links present & reachable; consent banner loads; no pre-consent tags; accurate claims.
- **Footer** — PP, CP, ToS, RR, SP, contact, "Do Not Sell or Share" (CA), accessibility link — findable before and during checkout.
- **Product page** — price-promo basis (EU prior-price), tax/duty clarity, shipping origin & timing, digital-content waiver notice.
- **Cart & checkout** — total/all-in price, mandatory-fee disclosure, terms acceptance, withdrawal/cancellation info, no hidden charges.
- **Account creation** — privacy notice at collection, deletion path, retention, age check if relevant.
- **Consent banner** — symmetrical Accept/Reject, preferences, reject-equals-accept, consent logging, no pre-consent firing.
- **Email capture form** — consent statement, channel scope, sender ID, link to PP, double-opt-in where required.
- **Subscription sign-up** — what renews, frequency, price, billing timing, cancellation path, express informed consent, pre-renewal notice.
- **App homepage** — privacy-policy link, subscription clarity, support/contact, deletion path reference.
- **App store listing** — privacy-policy URL, App Privacy Details / Data safety mapping, account-deletion declaration, sensitive-permission justification, kids/health checks.
- **Seller onboarding** (marketplace) — trader identity/KYC, traceability fields, prohibited-goods acceptance, complaint-route acknowledgement.
- **Final launch gating** — all Blocking items Pass; legal-review queue cleared or accepted; disclaimer present.
- **Red-flag report** — see below.

## Red-flag report

Surface every escalation trigger with its label. Stop being template-first and become issue-spotting-first whenever any fire:

| Trigger | Label |
|---|---|
| Health / medical / diagnostic / fitness-with-health-claims | Legal review required |
| Biometrics (face/voice/fingerprint) | Legal review required |
| Children or likely child-access | Legal review required |
| Financial products / lending / payments / insurance / investments | Legal review required |
| Employment / hiring / screening / worker scoring | Legal review required |
| AI scoring or materially impactful AI | Legal review required |
| Marketplace / UGC with user posts or sellers | Legal review required |
| SMS marketing / autodialling / lead resale | Legal review required |
| Cross-border store with unclear seller identity / origin / duties / return address | High risk or Blocking |
| Reliance on a generic "template" page not matching actual practice | High risk |

## Severity guidance

- **Blocking** — unlawful processing, missing mandatory consumer info, platform-rejection cause, deceptive cross-border fulfilment. Must Pass before launch.
- **High risk** — likely complaint/enforcement/dispute vector; fix before or immediately after launch.
- **Medium risk** — should fix; schedule.
- **Best practice** — trust/quality improvement.
