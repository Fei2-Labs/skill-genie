# Source Register

Source inventory governing the rules engine. Each row: source · region · business types · why it matters · last checked · review cadence · change risk · affected modules. When a source changes, update the affected modules in `policy-templates.md` / `checklist-framework.md` and re-run scenario tests.

Sources treated as checked on **9 June 2026** unless the source itself shows a more specific effective/update date. This register is the maintenance backbone — extend it so every legal/platform rule used in the skill has its own row.

## Legal sources

| Source | Region | Business types | Why it matters | Last checked | Review cadence | Change risk | Affects |
|---|---|---|---|---|---|---|---|
| GDPR (official text) | EU/EEA | all | privacy scope, transparency, rights, processor contracts | 2026-06-09 | quarterly | medium | PP, DPA, matrix |
| ICO UK GDPR guidance | UK | all | UK privacy notices, accountability | 2026-06-09 | quarterly | medium | PP, rights, lawyer triggers |
| ePrivacy Directive / EDPB Art. 5(3) consent | EU/EEA | sites with tracking | cookies, pixels, similar tech | 2026-06-09 | quarterly | high | CP, banner, consent logic |
| ICO PECR (cookies + e-marketing) | UK | tracking / email / SMS | cookie + direct-marketing rules | 2026-06-09 | quarterly | high | CP, banner, marketing language |
| CCPA statute + CPPA regs | California/US | US-exposed consumer sites | point-of-collection, rights, sale/share, dark patterns | regs effective 2026-01-01; checked 2026-06-09 | quarterly | high | PP, opt-out, rights pages |
| California GPC guidance | California/US | ad-supported sites | global opt-out signal handling | 2026-06-09 | quarterly | medium | opt-out page, footer checklist |
| FTC CAN-SPAM / ROSCA | US | email marketing / subscriptions | email footer, negative-option billing | 2026-06-09 | semi-annual | medium | marketing language, ST |
| PIPEDA | Canada | all | privacy baseline | 2026-06-09 | semi-annual | medium | PP, risk notes |
| CASL + ISED consent guidance | Canada | newsletter / lead-gen / stores | email/SMS consent + unsubscribe | 2026-06-09 | semi-annual | medium | marketing language |
| OAIC small-business guidance | Australia | AU-facing sites | Privacy Act coverage determination | 2026-06-09 | semi-annual | high | PP, risk notes |
| ACCC refunds guidance (ACL) | Australia | stores / subscriptions | statutory guarantees, refund limits | 2026-06-09 | semi-annual | low | RR, checkout copy |
| Spam Act | Australia | marketing senders | email/SMS consent, unsubscribe, sender ID | 2026-06-09 | semi-annual | low | marketing language |
| EU Consumer Rights Directive / UK CCRs | EU/UK | stores, subscriptions, digital | withdrawal, pre-contract info, digital waiver | 2026-06-09 | semi-annual | medium | RR, ToS, checkout |
| EU Omnibus price-reduction rule | EU/EEA | stores with promos | prior-30-day price disclosure | 2026-06-09 | semi-annual | medium | product-page checklist |
| UK DMCCA subscription regime | UK | subscriptions | future-state implementation warning | govt response updated 2026-04-02 | monthly until commenced | high | ST, risk report |
| EU withdrawal-function directive (EU) 2023/2673 | EU/EEA | online traders w/ withdrawal right | applies from 2026-06-19 | checked 2026-06-09 | monthly during rollout | high | withdrawal UI checklist |
| COPPA (amended 2025) | US | child-directed services | children's privacy + parental consent | 2026-06-09 | quarterly | medium | CH, parental-consent logic |
| UK Children's Code | UK | services likely accessed by children | age-appropriate design | 2026-06-09 | semi-annual | medium | CH, high-privacy defaults |
| EU AI Act / Commission AI transparency | EU/EEA | AI sites / AI-enabled | transparency obligations + timelines | 2026-06-09 | quarterly | high | AI notice, risk report |
| European Accessibility Act + WCAG 2.2 | EU/EEA + wider | stores, SaaS, apps | accessibility duties + statement | 2026-06-09 | semi-annual | medium | ACC, gating checklist |
| GDPR Art. 28 (processor contracts) | EU/EEA + UK | SaaS processors | DPA, subprocessors, transfers | 2026-06-09 | semi-annual | medium | DPA |
| DSA (official text) | EU/EEA | marketplaces, UGC, platforms | trader traceability, dark patterns, obligations | 2026-06-09 | quarterly | high | MP, complaint flows |
| P2B Regulation | EU/EEA (+UK relevance) | marketplaces w/ business sellers | seller terms, ranking transparency, complaints | 2026-06-09 | semi-annual | medium | seller ToS, ranking notice |
| INFORM Consumers Act | US | high-volume marketplaces | seller verification + public disclosures | 2026-06-09 | semi-annual | low | seller onboarding, MP |

## Platform sources

| Source | Platform | Why it matters | Last checked | Review cadence | Change risk | Affects |
|---|---|---|---|---|---|---|
| Apple App Review Guidelines / App Privacy | Apple | privacy-policy URL, Kids, subscriptions, App Privacy Details | 2026-06-09 (living doc) | monthly | high | app notes, PP, ST |
| Google Play User Data / Data safety / account deletion | Google Play | in-app privacy, data safety, deletion | 2026-06-09 | monthly | high | app notes, PP, deletion |
| Shopify customer-privacy tools | Shopify | cookie banner, privacy page, opt-out page | 2026-06-09 | quarterly | medium | PP, CP, footer checklist |
| Google Ads policies | Google Ads | landing-page destination, customer-data/enhanced conversions | 2026-06-09 | quarterly | high | ads note, PP, pixel checklist |
| Meta Ads / Business Tools policies | Meta | pixel/CAPI/custom audiences, sensitive-data prohibition, consent | 2026-06-09 | quarterly | high | CP, PP, pixel checklist |
| Amazon seller policies | Amazon | returns/refunds consistency, listing policy | 2026-06-09 | quarterly | medium | RR, seller note |
| TikTok Shop rules | TikTok Shop | returns/refunds/shipping-after-sale | 2026-06-09 | quarterly | high | RR, SP note |
| Google Merchant Center / Shopping | Google | return + shipping fields, product-listing | 2026-06-09 | quarterly | medium | SP, product checklist |

## Review cadence by change risk

| Change risk | Examples | Cadence |
|---|---|---|
| High | CPPA regs, Apple/Google Play policies, AI Act guidance, UK subscription implementation, DSA guidance | monthly–quarterly |
| Medium | GDPR/ICO guidance, PIPEDA, OAIC guidance, Google/Meta ad policies | quarterly–semi-annual |
| Low | GDPR core text, CAN-SPAM, ROSCA, UK CCRs, ACL guarantees | semi-annual–annual |

## Open limitations (keep marked)

- **US privacy law** — California + US federal baseline only; other states not exhaustively codified → **Jurisdiction-specific**.
- **US subscription law** — ROSCA + California ARL as baseline; broader federal negative-option in a **Needs verification** track.
- **Canada consumer returns** — many refund/cancellation rights are provincial → warn, don't fake nationwide certainty.
- **Accessibility** — EAA application can depend on service scope/local implementation → boundary cases **Needs verification**.
- **EU withdrawal function** — (EU) 2023/2673 applies from 2026-06-19; verify country-by-country in the immediate post-application period.
