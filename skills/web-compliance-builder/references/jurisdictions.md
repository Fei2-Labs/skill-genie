# Jurisdictions

Region-by-region rule summary and trigger logic. Baseline jurisdiction set: **EU/EEA, UK, US baseline + California, Canada, Australia**. When a fact sits near a boundary, emit **Needs verification**, **Jurisdiction-specific**, or **Legal review required**.

Territorial scope is fact-driven, not address-driven: GDPR/UK GDPR can apply by *targeting* or *monitoring* people in-region even without a local establishment. If the user is unsure whether they "target" EU/UK or are merely accessible there, assume **moderate exposure** and mark **Needs verification**.

## EU / EEA

- **Privacy (GDPR).** Applies when processing personal data of people in the EU/EEA, including extra-territorial targeting/monitoring. Output: Privacy Policy, layered notices, lawful-basis mapping, data-subject-rights section, processor/transfer disclosures.
- **Cookies / similar tech (ePrivacy, Art. 5(3)).** Non-essential cookies, pixels, SDKs, fingerprinting, web storage → prior consent. Output: Cookie Policy, banner, consent categories, pre-consent tag-blocking, consent logs. Banner must not fire non-essential tags before consent.
- **Consumer sales / withdrawal (Consumer Rights Directive).** Distance contracts for goods/services/digital content → 14-day withdrawal right with exceptions. Digital content needs an explicit waiver to start before the period ends. Output: Returns/Withdrawal page, model withdrawal language, digital-content waiver.
- **Price-reduction disclosures (Omnibus).** Discount/strike-through claims → must reference the prior lowest price in the last 30 days. Output: product-page price-promo checklist + evidence.
- **Withdrawal-function directive (EU) 2023/2673.** Applies from **19 Jun 2026**. On/near that date verify country-by-country. **Needs verification.**
- **Accessibility (European Accessibility Act + WCAG 2.2).** Covered EU-facing e-commerce / services. Output: Accessibility Statement + WCAG remediation checklist (the checklist is the real control). Boundary cases → **Needs verification**.
- **AI transparency (EU AI Act).** AI products, chatbots, synthetic media, high-risk use. Output: AI disclosure, human-review notice, claims substantiation, training-data/privacy flag. **High change risk.**
- **Marketplace / platform (DSA).** Multi-vendor marketplace or UGC platform → trader traceability/KYC, complaint flow, illegal-content & moderation rules, dark-pattern limits.
- **Children / special-category data.** Child-consent age varies by member state (13–16) → **Jurisdiction-specific**; parental-consent logic. Special-category data → **Legal review required**.
- **Processor contracts (Art. 28).** SaaS acting as processor → DPA, subprocessors annex, security & assistance clauses, SCC/transfer flag.

## United Kingdom

- **UK GDPR + ICO guidance.** UK personal-data processing → UK-facing Privacy Policy, UK rights, ICO-aligned notice structure.
- **PECR.** Non-essential cookies + electronic direct marketing → consent / soft-opt-in logic, reject-equals-accept banner UI, unsubscribe language. **High change risk.**
- **Distance selling / cancellation (CCRs).** Online consumer contracts → cancellation-rights section, model cancellation form/process, no hidden limits.
- **Subscriptions (DMCCA regime).** Reminders, easy exit, renewal cooling-off — **Needs verification**: treat as a *future* UK regime, not current mandatory baseline. Government response updated 2 Apr 2026; commencement expected later. Monitor monthly until commenced.
- **Children's Code (Age-Appropriate Design).** Service likely accessed by children → children's notice, age-appropriate design checklist, high-privacy defaults.
- **Accessibility.** Risk-based for most commercial sites; legal for public-sector bodies.

## United States (baseline + California)

- **FTC baseline.** Deception / dark patterns / CAN-SPAM (commercial email) / ROSCA (negative-option billing). CAN-SPAM footer: sender ID, postal address, working unsubscribe.
- **California (CCPA/CPRA) as default state-privacy baseline.** Point-of-collection notice, rights, "Do Not Sell or Share" link, GPC handling, sensitive-PI section. CPPA dark-pattern rules → symmetrical consent UI, no misleading button hierarchy. **High change risk.**
- **Global Privacy Control (GPC).** Ad-supported sites must honor the browser opt-out signal.
- **California ARL (auto-renewal).** Clear recurring-charge disclosure, express consent, easy cancellation.
- **COPPA.** Child-directed services or knowingly collecting from under-13s → children's notice + verifiable parental consent. Rule amended 2025. No generic-policy-only fix.
- **Other states.** Not exhaustively codified — mark US state expansion **Jurisdiction-specific**. Telemarketing/SMS (TCPA) and federal negative-option rules are actively changing → **Needs verification**.

## Canada

- **PIPEDA.** Private-sector commercial activity → privacy notice + safeguards baseline.
- **CASL.** Commercial electronic messages (email/SMS) → consent language, sender ID, unsubscribe flow. Among the strictest consent regimes.
- **Competition Act / drip pricing.** All-in price disclosure.
- **Provincial consumer law.** Many refund/cancellation rights are **provincial** → warn the user; do not fake nationwide certainty.

## Australia

- **Privacy Act (APPs).** Covers many businesses, including some small businesses despite the general exemption → APP-style Privacy Policy, overseas-disclosure section, complaints contact, covered/not-covered warning. Reform in progress → periodic review.
- **Spam Act.** Email/SMS/MMS/IM marketing → consent, unsubscribe, sender ID.
- **Australian Consumer Law (ACL).** Consumer guarantees cannot be waived → Refund/Returns policy must not contradict statutory guarantees; product-page disclaimer checks.

## Terminology differences (watch for)

- "Personal data" (EU/UK) ≈ "personal information" (US/CA/AU).
- "Controller/processor" (EU/UK) ≈ "business/service provider" (California).
- "Cookie consent" (EU/UK, opt-in) vs "opt-out of sale/share" (California) — different legal model, do not conflate.
- "Withdrawal" (EU) ≈ "cancellation" (UK) ≈ "cooling-off".
