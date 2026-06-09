# web-compliance-builder research and build specification

## Executive build brief

The strongest design choice for **web-compliance-builder** is to make it a **classification engine first, drafting engine second**. The skill should not start by writing a generic privacy policy. It should first determine the product type, regions targeted, data categories, tracking stack, transaction model, platform dependencies, and high-risk triggers, then map those facts to concrete outputs: required pages, missing disclosures, mandatory user flows, platform-facing requirements, and a launch-blocking checklist. That design is directly supported by the way the main regimes work: GDPR / UK GDPR depend on the nature of processing and territorial scope; ePrivacy / PECR depend on whether non-essential cookies or similar tracking are used; consumer-law obligations depend on whether the site sells goods, services, digital content, or subscriptions; marketplace rules depend on whether third-party sellers are involved; and app-store rules depend on app data practices and monetisation model. citeturn0search0turn0search1turn2search0turn2search2turn4search4turn21search0turn9search4turn11search0turn11search11

For this skill, the most reliable baseline jurisdiction set is: **EU/EEA, UK, California/U.S. baseline, Canada, and Australia**. That covers the specific laws the brief asked for and also gives enough structure to detect when the skill must escalate to **Jurisdiction-specific** or **Legal review required** mode. The key privacy and marketing baselines within that set are GDPR, UK GDPR + PECR, CCPA/CPRA, PIPEDA, CASL, Australia’s Privacy Act / ACL / Spam Act, and sector-specific or high-risk overlays for children, health, AI, and marketplaces. citeturn0search0turn0search1turn2search2turn24search0turn24search1turn24search2turn0search3turn20search0turn20search8turn1search0turn1search1turn1search2

The biggest practical lesson from current law and platform policy is that the skill must separate four labels in every output item: **Legal requirement**, **Platform requirement**, **Best practice**, and **Risk-based recommendation**. That distinction matters because several things users think are “mandatory” are only platform rules or operationally wise defaults. Examples: an accessibility statement is not universally mandatory, but accessibility itself can be a legal requirement for covered EU-facing services and is a major enforcement and litigation risk elsewhere; an AI disclosure notice is a legal requirement only in some scenarios, but a strong risk-control measure in many more; Shopify’s built-in privacy tools are helpful, but they do not replace legal analysis; Apple and Google store-listing disclosures are platform requirements even when the underlying website would not have needed the same format. citeturn6search1turn6search4turn6search9turn7search0turn7search1turn8search2turn11search2turn11search7turn16search0turn17search6

This report treats sources as checked on **9 June 2026** unless a source itself shows a more specific update or effective date. Items marked **Needs verification**, **Jurisdiction-specific**, or **Legal review required** should be re-checked before launch, and the skill should surface those labels automatically when conditions are met.

## Regulatory and platform map

### Core legal and platform map

The table below is the legal and platform backbone that the skill should encode into its rules engine.

| Topic | Requirement class | Region | Applies when | What the skill should generate or check | Update signal | Source |
|---|---|---:|---|---|---|---|
| Privacy notice / point-of-collection notice | Legal requirement | EU/EEA | Site or app processes personal data of people in the EU / EEA, including extra-territorial targeting or monitoring | Privacy Policy; layered notices; lawful-basis mapping; data subject rights section; processor / transfer disclosures | Stable text, but guidance evolves; periodic review | citeturn0search0turn30search0 |
| Privacy notice / transparency | Legal requirement | UK | UK personal data processing | UK-facing Privacy Policy; UK rights; ICO-aligned notice structure | Ongoing ICO guidance; periodic review | citeturn0search1turn0search5 |
| Cookies / similar technologies consent | Legal requirement | EU/EEA | Non-essential cookies, pixels, SDKs, fingerprinting, web storage, or similar device access | Cookie Policy; cookie banner; consent categories; blocking logic; consent logs; per-tool mapping | Needs periodic review | citeturn2search0turn3search0turn3search1 |
| Cookies / similar technologies under PECR | Legal requirement | UK | Non-essential cookies or similar technologies | UK cookie banner copy; reject-equal-to-accept UI checks; PECR checklist | Needs periodic review | citeturn2search2turn3search3turn3search15 |
| State privacy rights / opt-out / GPC | Legal requirement | California and some U.S. states | If the business is subject to CCPA/CPRA or similar state privacy laws, especially where “sale/share” or targeted advertising is used | “Do Not Sell or Share” page / link; privacy rights language; GPC handling; sensitive PI section | High change risk; periodic review | citeturn24search0turn24search1turn24search2turn24search3 |
| Dark-pattern limits for privacy choices | Legal requirement | California | Privacy rights interfaces, opt-outs, consent choices | Symmetrical consent UI checks; reject misleading button hierarchy; evidence screenshots | High change risk; periodic review | citeturn29search2turn29search6 |
| Commercial email marketing | Legal requirement | U.S. federal baseline | Commercial email is sent | CAN-SPAM footer elements; unsubscribe workflow; postal address; sender identification checks | Stable baseline | citeturn5search1turn20search2turn20search6 |
| Commercial email / SMS marketing | Legal requirement | UK | Direct marketing by electronic mail / texts | PECR consent / soft-opt-in logic; unsubscribe language; audience-type logic | Needs periodic review | citeturn20search3turn3search3 |
| Commercial electronic messages | Legal requirement | Canada | Commercial email, SMS, some other electronic messages to / from Canada | CASL consent language; sender identification; unsubscribe flow | Stable law; periodic review for guidance | citeturn20search0turn20search8turn20search12 |
| Privacy law coverage | Legal requirement | Canada | Private-sector commercial activity in Canada | PIPEDA privacy notice and safeguards baseline; province warning flag | Stable but province overlays vary | citeturn0search3turn0search7turn0search11 |
| Privacy law coverage | Legal requirement | Australia | Business covered by Privacy Act, including some small businesses despite general exemption | APP-style Privacy Policy; overseas disclosure section; complaints contact; covered/not-covered warning | Reform risk; periodic review | citeturn1search0turn1search8 |
| Email / SMS marketing | Legal requirement | Australia | Marketing emails / SMS / MMS / instant messages | Consent wording; unsubscribe checks; sender identification | Stable baseline | citeturn1search2turn1search6 |
| Refunds / guarantees | Legal requirement | Australia | Consumer sale of goods or services | Refund / Returns Policy must not waive statutory guarantees; product-page disclaimer checks | Stable baseline | citeturn1search1 |
| Distance selling / withdrawal | Legal requirement | EU/EEA | Consumer distance contracts for goods, services, digital content, with exceptions | Returns / Withdrawal page; standard withdrawal language; digital-content waiver language | Stable, but implementations vary | citeturn4search0turn4search4turn25search12 |
| Price reduction disclosures | Legal requirement | EU/EEA | Discount claims / strike-through pricing | Product-page price-promo checklist; evidence of prior 30-day price | Periodic review | citeturn4search1 |
| Distance selling / cancellation | Legal requirement | UK | Online / distance consumer contracts | Cancellation-rights section; standard cancellation form / process; no hidden limitations | Stable baseline | citeturn21search0turn21search4turn25search10 |
| Subscription contract reforms | Legal requirement | UK | Consumer subscriptions | **Needs verification**: prepare for reminders, easy exit, renewal cooling-off, but mark as future UK regime rather than current mandatory baseline on 9 June 2026 | Government response updated 2 Apr 2026; spring 2027 expected by government response context | citeturn22search0turn23view0 |
| Online negative-option charges | Legal requirement | U.S. federal baseline | Recurring online billing, post-transaction upsells, trial-to-paid flows | Clear recurring-payment disclosures; express informed consent; easy cancellation design; evidence logs | U.S. subscription law requires periodic review | citeturn5search0turn5search12turn4search3 |
| Children’s privacy | Legal requirement | U.S. | Child-directed services or services knowingly collecting from under-13s | Children’s Privacy Notice; parental-consent flow; no generic policy-only solution | COPPA rule amended in 2025; periodic review | citeturn5search3turn5search7turn5search11 |
| Children’s code | Legal requirement | UK | Online service likely to be accessed by children | Children’s notice; age-appropriate design checklist; high-privacy defaults; escalation | Stable code, active enforcement relevance | citeturn31search0turn31search4 |
| Child consent threshold | Legal requirement | EU/EEA | Consent-based information-society service offered directly to a child | Country-specific child-consent-age question; parental-consent logic | **Jurisdiction-specific** | citeturn31search1turn31search5 |
| Processor contract / DPA | Legal requirement | EU/EEA and UK | SaaS / vendor acts as processor for customer data | DPA outline; subprocessors annex; security and assistance clauses; SCC / transfer flag | Stable baseline; transfer tools need review | citeturn30search0turn30search1turn30search2turn30search3 |
| Accessibility | Legal requirement or risk-based depending scope | EU/EEA; U.S.; UK | EU-facing e-commerce / covered services, public bodies, or any site wanting lower risk and higher trust | Accessibility Statement; WCAG 2.2 checklist; escalation if covered by EAA or public-sector rules | Needs periodic review | citeturn6search1turn6search2turn6search4turn6search9 |
| AI transparency | Legal requirement or risk-based depending use case | EU/EEA; UK/U.S. consumer-protection context | AI product, chatbot, synthetic media, high-risk AI use, or AI claims in marketing | AI disclosure notice; human-review notice; claims substantiation; training-data/privacy flag | High change risk; periodic review | citeturn7search0turn7search1turn8search0turn8search1turn8search2turn8search7turn7search3 |
| Marketplace operator obligations | Legal requirement | EU/EEA | Multi-vendor marketplace / platform with traders selling to consumers | Seller onboarding KYC/trader-traceability; complaint flow; marketplace terms; seller-display fields | Needs periodic review | citeturn9search4turn10search0turn10search5turn19search0 |
| High-volume third-party seller verification | Legal requirement | U.S. | Online marketplace covered by INFORM Consumers Act | Seller verification workflow; public seller disclosures; evidence retention | Stable baseline | citeturn9search1turn9search5 |

### Platform requirement map

The skill also needs a separate platform map, because platform approval often fails before any regulator contacts the merchant.

| Platform | Requirement class | Applies when | What the skill should output | Update signal | Source |
|---|---|---|---|---|---|
| Apple App Store | Platform requirement | Any iOS app / app page | Privacy Policy URL in App Store Connect and within app; App Privacy Details; if subscriptions, clear pre-purchase subscription information; Kids Category restrictions; health/medical claims scrutiny | living document; high review frequency | citeturn16search0turn16search3turn32view3turn32view2turn32view0turn32view1 |
| Google Play | Platform requirement | Android app | Privacy Policy link in listing and in-app for sensitive-data or children’s apps; Data safety disclosures; account deletion if account creation exists; prominent in-app disclosure / consent where data use is outside user expectation | frequent policy changes | citeturn17search6turn17search13turn11search1turn17search4turn17search11 |
| Shopify | Platform requirement with legal-assist tooling | Shopify store | Store policies pages; footer / checkout links; customer privacy settings; cookie banner; data-sharing opt-out page; GPC / opt-out support considerations | product evolves; review periodically | citeturn11search2turn11search7turn18search2turn18search6 |
| Google Ads | Platform requirement | Paid traffic from Google Ads | Landing-page destination checks; customer-data / enhanced-conversion review; privacy-disclosure reminder | frequent policy review | citeturn10search2turn12search0turn10search6 |
| Meta Ads / Meta Business Tools | Platform requirement | Meta Pixel, CAPI, Custom Audiences, retargeting | Sensitive-data prohibition flag; pixel ownership check; consent / notice check; Meta-specific tracking note | frequent policy review | citeturn14search13turn14search17turn14search5 |
| Amazon marketplace seller | Platform requirement | Amazon seller page / seller-fulfilled orders | Return / refund handling consistent with Amazon policy; seller-code checks; account and listing policy note | periodic review | citeturn9search2turn9search6turn18search5 |
| TikTok Shop | Platform requirement | TikTok Shop seller | Returns / refunds / shipping-after-sale note tied to TikTok Shop rules | frequent policy review | citeturn9search3 |
| Google Merchant Center / Shopping | Platform requirement | Product feeds / Shopping ads / free listings | Return policy and shipping information fields; product-listing checklist | periodic review | citeturn18search0turn11search17 |

### What this means for skill logic

The skill should use the following baseline rule:

> If a requirement comes from a statute / regulator / official legal text, classify it as **Legal requirement**. If it comes from a distribution or payments channel that can block publication, ad delivery, or selling privileges, classify it as **Platform requirement**. If it reduces dispute risk or improves trust but is not always mandatory, classify it as **Best practice** or **Risk-based recommendation**.

That single rule keeps the outputs honest, which is critical because the skill must explicitly avoid pretending that every page is equally mandatory.

## Decision logic and requirements matrices

### Business-type to compliance mapping

The table below is the core matrix the skill should use after classification.

Legend: **PP** Privacy Policy, **CP** Cookie Policy / consent settings, **ToS** Terms / Conditions, **RR** Refund / Return Policy, **SP** Shipping Policy, **ST** Subscription Terms, **AUP** Acceptable Use Policy, **DPA** Data Processing Addendum outline, **ACC** Accessibility Statement, **AI** AI disclosure, **CH** Age / children notice, **MP** Marketplace / seller terms & moderation bundle.

| Business type | Typical outputs | Trigger-sensitive add-ons | Key legal / platform basis |
|---|---|---|---|
| General ecommerce store | PP, CP, ToS, RR, SP, checkout / product / footer checklists | EU withdrawal sections; California opt-out; accessibility; shipping/tax disclosures | citeturn0search0turn2search0turn4search4turn21search4turn24search2turn6search1 |
| Dropshipping store | General ecommerce outputs plus stronger fulfilment, origin, customs, and returns clarity | “Ships from” / cross-border timing / duty-bearing party / return address; platform shipping notes | citeturn4search4turn21search2turn21search4turn11search7 |
| Digital product store | PP, CP if tracking, ToS, RR with digital-content logic | EU / UK digital-content withdrawal waiver language; licence terms | citeturn25search12turn25search10turn25search0 |
| Subscription / membership site | PP, CP, ToS, ST, billing disclosures, cancellation-flow checklist | U.S. recurring-charge controls; California ARL; UK future-regime prep; Apple / Google subscription notes if in-app | citeturn5search0turn4search3turn23view0turn32view2turn16search1 |
| B2C SaaS | PP, CP, ToS, ST if recurring, DPA only if acting as processor, security / subprocessors sections | account deletion, trial disclosures, AI notice, accessibility, California rights | citeturn30search0turn30search1turn11search1turn24search2turn7search1turn6search1 |
| B2B SaaS | PP, CP, ToS, DPA, subprocessors / transfer addendum, AUP | security / admin controls / sales-contact transparency; fewer consumer pages unless self-serve checkout exists | citeturn30search0turn30search1turn30search2 |
| Mobile app landing page | Website PP plus App Store / Google Play notes; if subscriptions, ST; if tracking, CP | app privacy labels, data-safety alignment, account deletion page, support / contact page | citeturn16search0turn16search3turn17search13turn11search1turn17search6 |
| Marketplace / multi-vendor platform | PP, CP, consumer ToS, seller ToS, MP, complaint flow, illegal-content / moderation rules | trader verification, ranking transparency, P2B, DSA / INFORM Consumers Act | citeturn9search4turn10search5turn19search0turn9search5 |
| Affiliate / lead-generation site | PP, CP, ToS, affiliate disclosure, marketing consent language | lead-sharing disclosures; TCPA / SMS escalation; ad pixel and consent logic | citeturn19search5turn20search2turn20search3turn2search0 |
| AI product website | PP, CP, ToS, AI, AUP, DPA if B2B processing, model-input / model-training clauses | transparency, claims substantiation, human review, misuse rules | citeturn7search0turn7search1turn8search2turn8search7turn7search3 |
| Newsletter / email-capture landing page | PP, CP if tracking, ToS or Site Terms light, marketing consent language | double-opt-in preference, CASL / PECR / Spam Act / CAN-SPAM variants | citeturn20search8turn20search3turn1search2turn20search2 |
| International cross-border store | All store outputs plus stronger taxes / duties / country-availability disclosures | currency, VAT/GST, customs, final-price clarity, return destination mismatch checks | citeturn4search4turn21search2turn21search4turn4search1 |

### Page and policy requirements matrix

This is the matrix that should drive **references/page-requirements.md**.

| Trigger | Required or recommended page / artifact | Class | Applies when | Notes for logic |
|---|---|---|---|---|
| Personal data collected | Privacy Policy | Legal requirement | Any covered privacy regime or platform requiring transparency | Always output if any form, analytics, account, checkout, support, or SaaS dashboard exists |
| Non-essential cookies / pixels / analytics | Cookie Policy + banner copy + consent settings | Legal requirement in EU/UK; risk-based elsewhere | Cookies, pixels, SDKs, advertising / retargeting / analytics beyond strict necessity | Banner should not fire non-essential tags pre-consent in EU/UK flows citeturn2search0turn2search2turn3search0turn3search1 |
| Consumer sale of goods | Terms, Refund / Return Policy, Shipping Policy | Legal requirement / risk-based mix | Physical goods sold to consumers | Terms alone are not enough; returns and shipping need separate plain-language pages in most real stores |
| Cross-border goods sale | Customs / duties / delivery-country disclosures | Risk-based recommendation, often consumer-law driven | Store ships internationally or from origin country different from store-facing country | Skill should raise severity if origin country is hidden or return address is absent |
| Digital goods / software licence | Digital product terms / licence clauses | Legal requirement / risk-based mix | Download, software licence, membership assets, templates, courses | Include access method, device limits, refund / waiver rules |
| Auto-renewing plan / free trial | Subscription Terms | Legal requirement / platform requirement | Recurring billing or trial-to-paid | Must cover renewal, frequency, price, cancellation path, billing timing, notices, platform billing if app-based |
| User accounts with personal data | Account deletion / data rights section | Legal requirement / platform requirement | App or service allows account creation | Escalate for Google Play account deletion rule and Apple privacy policy deletion explanation citeturn11search1turn32view3 |
| SaaS acts as processor | DPA outline | Legal requirement | Customer uploads or stores personal data in the service on their own behalf | Output should be outline unless user asks for full DPA |
| UGC / community / marketplace | Community / moderation rules, seller terms, complaint workflow | Legal requirement / risk-based | Users can post, list, or sell | Pull in DSA / P2B / child-safety questions where relevant |
| Child-directed or likely child-accessed | Children’s notice / age gate / parental-consent logic | Legal requirement / legal-review trigger | Product for children or likely accessed by them | Never rely on a generic age-18 footer only citeturn31search0turn31search4turn5search3 |
| AI system or AI marketing claims | AI disclosure notice | Risk-based or legal requirement depending use | AI-generated content, chatbot, automation, model training, decision support | Mark **Legal review required** if high-risk or sensitive domain use |
| Covered accessibility exposure | Accessibility Statement + WCAG remediation checklist | Legal requirement or risk-based | EU-covered digital service, public body, or litigation-sensitive commercial site | Statement alone is not compliance; the checklist is the real control |
| Paid ads / remarketing | Ads-compliance note | Platform requirement | Google Ads / Meta Ads / TikTok Ads etc. | Add destination-policy and customer-data-policy review |
| App distribution | App-store compliance notes | Platform requirement | Apple App Store / Google Play | Generate app-specific privacy / deletion / subscription / sensitive-permissions notes |
| High-risk data | Red flag report + legal-review notice | Risk-based recommendation and escalation | health, biometrics, precise location, finance, employment, children, AI decisioning | The skill should stop being “template-first” and become “issue-spotting first” |

### Output types the skill should support

The requested outputs are all justified, but they should be emitted conditionally rather than always. The skill should support: a website compliance requirements matrix; required pages list; Privacy Policy draft; Cookie Policy draft; cookie banner copy; Terms / ToS draft; Refund & Return Policy draft; Shipping Policy draft; Subscription Terms; AUP; DPA outline; Accessibility Statement; age / children notice; AI disclosure notice; marketing consent language; checkout / product-page / footer checklists; App Store / Google Play compliance notes; final launch checklist; and a Red Flag report. That output model aligns with the duties and platform requirements above and is broad enough to cover all business types in scope. citeturn11search0turn17search6turn18search2turn30search1turn6search1turn7search1

## Skill package specification

### Folder structure

```text
web-compliance-builder/
├── SKILL.md
├── references/
│   ├── jurisdictions.md
│   ├── business-types.md
│   ├── page-requirements.md
│   ├── policy-templates.md
│   ├── checklist-framework.md
│   └── source-register.md
└── scripts/
    ├── compliance_questionnaire.py
    └── checklist_generator.py
```

The `references/` directory should hold stable knowledge assets. The `scripts/` directory should only assemble outputs from the skill’s structured findings; it should not attempt legal interpretation on its own.

### SKILL.md draft

```md
# web-compliance-builder

## Purpose

web-compliance-builder helps users identify, draft, review, and checklist the compliance pages, notices, disclosures, user flows, and launch controls needed for websites, stores, SaaS products, apps, landing pages, and marketplaces.

This skill is designed for:
- ecommerce stores
- dropshipping stores
- digital product stores
- subscription and membership sites
- SaaS websites
- mobile app homepages and landing pages
- marketplaces and multi-vendor platforms
- affiliate and lead-generation sites
- AI product websites
- newsletter and email-capture landing pages
- cross-border stores

## What this skill does

The skill must:
- classify the business model before drafting anything
- determine target regions and likely legal exposure
- identify data collection, cookies, pixels, analytics, advertising, and SDK usage
- identify product and transaction types
- detect high-risk domains and sensitive data
- generate required pages and notices
- generate structured policy drafts
- generate page-level and go-live checklists
- mark unresolved issues that need legal review
- produce a launch gating checklist with pass/fail evidence fields

## What this skill must not do

The skill must not:
- present generic privacy policies or terms without first classifying the business
- treat all outputs as legal requirements
- claim jurisdiction-wide certainty where rules are state-specific or country-specific
- give legal advice
- hide uncertainty
- assume a platform template is legally sufficient
- claim a page is complete without checking the actual facts of the business

## Mandatory workflow

When invoked, follow this order:

1. Identify business type
2. Identify target markets and user regions
3. Identify data collection and tracking
4. Identify transaction model, refunds, subscriptions, shipping, taxes, and payment methods
5. Identify high-risk domains and sensitive data
6. Generate required pages list
7. Generate page-level outlines
8. Generate first-draft text
9. Generate page-level compliance checklist
10. Generate final go-live checklist
11. Mark legal-review issues
12. Produce a blocking gating checklist

## Output labels

Every requirement must be labelled as one of:
- Legal requirement
- Platform requirement
- Best practice
- Risk-based recommendation

## Required disclaimer

Every substantive output must include this disclaimer:

"This output is not legal advice. Compliance requirements vary by jurisdiction, business model, and actual operational practice. High-risk, regulated, sensitive-data, or cross-border businesses should have final materials reviewed by qualified counsel. This skill provides drafting support, issue spotting, and checklisting only."

## Escalation rules

Automatically mark "Legal review required" if the business:
- targets children
- processes health, biometric, financial, employment, or precise location data
- offers AI systems with material user impact
- operates a marketplace or UGC platform
- uses aggressive subscription flows or trial-to-paid architecture
- relies on cross-border fulfilment with unclear seller identity or return location
- combines multiple jurisdictions with conflicting requirements
- plans to rely on consent as the legal basis for complex profiling
- processes customer data as a SaaS processor without a DPA framework
- operates in a regulated vertical

## Evidence-first checklisting

For every checklist item, always include:
- requirement
- why it matters
- applies when
- evidence needed
- pass/fail
- source
- owner
- review frequency
```

### What each reference file should contain

| File | What it should contain |
|---|---|
| `references/jurisdictions.md` | Region-by-region rules summary, trigger logic, terminology differences, privacy / cookie / marketing / consumer-rights / accessibility / AI / children sections, plus “Needs verification” flags where state or country implementation varies |
| `references/business-types.md` | Business-type taxonomy; typical data flows; sales models; high-risk overlays; default required pages; common red flags |
| `references/page-requirements.md` | Page-by-page decision matrix; when each page is required, recommended, or inapplicable; mandatory sections by trigger and region |
| `references/policy-templates.md` | Clause library and modular policy skeletons for PP, CP, ToS, RR, SP, ST, AUP, DPA outline, accessibility, AI, children, marketing consent, marketplace rules |
| `references/checklist-framework.md` | Page-level checklist templates; checkout, product page, footer, app listing, cookie banner, launch, and red-flag schemas |
| `references/source-register.md` | Source inventory with jurisdiction, business type relevance, last verified date, review cadence, risk level, and impacted templates/checklists |

### Seed content outline for reference files

```md
# references/jurisdictions.md

## EU and EEA
- Territorial scope triggers
- Privacy notice triggers
- Cookie consent triggers
- Consumer sales and withdrawal
- Digital content waiver
- Accessibility and EAA
- AI / DSA / marketplace overlays
- Children and special-category data
- Needs verification items

## United Kingdom
- UK GDPR and ICO notice expectations
- PECR cookie / marketing rules
- Distance selling and cancellation
- DMCCA subscription regime status
- Children’s Code
- Accessibility risk notes

## United States baseline
- FTC deception / dark patterns / CAN-SPAM / ROSCA
- California privacy as default state-privacy baseline
- GPC / opt-out architecture
- California ARL
- Children and app-store overlays
- State-law warning

## Canada
- PIPEDA
- CASL
- Competition / drip pricing
- Provincial consumer law warning

## Australia
- Privacy Act coverage and exemptions
- Spam Act
- ACL refunds / guarantees
- Review-frequency note
```

```md
# references/business-types.md

## Ecommerce store
## Dropshipping store
## Digital products
## Subscription and membership
## B2C SaaS
## B2B SaaS
## Mobile app homepage
## Marketplace / multi-vendor
## Affiliate / lead generation
## AI product site
## Newsletter landing page
## Cross-border store

For each:
- definition
- common data collected
- tracking patterns
- transaction patterns
- default pages
- common region overlays
- common red flags
```

```md
# references/page-requirements.md

For each page:
- purpose
- label class options
- trigger logic
- mandatory sections
- region-specific sections
- platform-specific sections
- evidence required
- common failure modes

Pages:
- Privacy Policy
- Cookie Policy
- Cookie Banner
- Terms / ToS
- Refund & Return Policy
- Shipping Policy
- Subscription Terms
- Acceptable Use Policy
- DPA outline
- Accessibility Statement
- Age / Children Notice
- AI Disclosure
- Marketing Consent Language
- Marketplace Seller Terms
- Complaint / moderation process
```

```md
# references/policy-templates.md

Each template should be modular:
- global intro
- data categories module
- tracking and cookies module
- lawful basis / rights module
- sales and shipping module
- subscription / billing module
- app-store / SDK module
- AI module
- children / age module
- marketplace module
- accessibility module
- complaint and contact module
- jurisdiction addenda
```

```md
# references/checklist-framework.md

Checklists:
- homepage / landing page
- footer
- product page
- cart and checkout
- account creation
- consent banner
- email capture form
- subscription sign-up
- app homepage
- app store listing
- seller onboarding
- final launch gating
- red flag report
```

### Source-register seed rows

This seed table is the minimum viable starting content for `references/source-register.md`. In the actual file, every legal or platform rule used in the skill should get its own row.

| Source name | Region | Business types | Why it matters | Last update / check | Review frequency | Change risk | Affects |
|---|---|---|---|---|---|---|---|
| GDPR official text | EU/EEA | all | privacy scope, transparency, rights, processor contracts | Official text; checked 9 Jun 2026 | quarterly | medium | PP, DPA, matrix | citeturn0search0turn30search0 |
| ICO UK GDPR guidance | UK | all | UK privacy notices and accountability | checked 9 Jun 2026 | quarterly | medium | PP, rights, lawyer triggers | citeturn0search1 |
| ePrivacy Directive / EDPB Art. 5(3) / consent | EU/EEA | sites with tracking | cookies, pixels, similar tech | checked 9 Jun 2026 | quarterly | high | CP, banner, consent logic | citeturn2search0turn3search0turn3search1 |
| ICO PECR cookies and email marketing | UK | sites with tracking / email / SMS | cookie and direct-marketing rules | checked 9 Jun 2026 | quarterly | high | CP, banner, marketing language | citeturn2search2turn20search3turn3search3 |
| CCPA statute and CPPA regs | California / U.S. | most consumer-facing sites with U.S. exposure | point-of-collection, rights, selling/sharing, dark patterns | regs effective 1 Jan 2026; checked 9 Jun 2026 | quarterly | high | PP, opt-out, rights pages | citeturn24search0turn24search1 |
| California GPC guidance | California / U.S. | ad-supported sites | global opt-out handling | checked 9 Jun 2026 | quarterly | medium | opt-out page, footer checklist | citeturn24search2 |
| PIPEDA | Canada | all | privacy baseline | checked 9 Jun 2026 | semi-annual | medium | PP, risk notes | citeturn0search3turn0search11 |
| CASL and ISED consent guidance | Canada | newsletter / lead gen / stores | email/SMS consent and unsubscribe | checked 9 Jun 2026 | semi-annual | medium | marketing language | citeturn20search0turn20search8 |
| OAIC small-business guidance | Australia | AU-facing sites | determine Privacy Act coverage | checked 9 Jun 2026 | semi-annual | high | PP, risk notes | citeturn1search0 |
| ACCC refunds guidance | Australia | stores / subscriptions | statutory guarantees and refund limits | checked 9 Jun 2026 | semi-annual | low | RR, checkout copy | citeturn1search1 |
| Apple App Review Guidelines / App privacy | Apple | apps | privacy policy URL, kids, subscriptions, app privacy labels | Apple is a living document; checked 9 Jun 2026 | monthly | high | app notes, PP, ST | citeturn11search0turn16search0turn16search3turn32view3 |
| Google Play User Data / Data safety / account deletion | Google Play | apps | in-app privacy, data safety, deletion | checked 9 Jun 2026 | monthly | high | app notes, PP, deletion | citeturn11search11turn17search13turn11search1turn17search6 |
| Shopify customer privacy tools | Shopify | Shopify stores | cookie banner, privacy page, opt-out page | checked 9 Jun 2026 | quarterly | medium | PP, CP, footer checklist | citeturn11search2turn18search2 |
| DSA official text | EU/EEA | marketplaces, UGC, platforms | trader traceability, dark patterns, platform obligations | checked 9 Jun 2026 | quarterly | high | MP, complaint flows | citeturn9search4turn10search0turn10search5 |
| P2B Regulation | EU/EEA and retained UK relevance warning | marketplaces with business sellers | seller terms, ranking transparency, complaints | checked 9 Jun 2026 | semi-annual | medium | seller ToS, ranking notice | citeturn19search0turn19search13 |
| EU Consumer Rights Directive / UK CCRs | EU/UK | stores, subscriptions, digital products | withdrawal, pre-contract info, digital waiver | checked 9 Jun 2026 | semi-annual | medium | RR, ToS, checkout | citeturn4search4turn25search12turn21search0turn21search4 |
| UK subscription consultation response | UK | subscriptions | future-state implementation warning | Updated 2 Apr 2026 | monthly until commenced | high | ST, risk report | citeturn23view0 |
| EU withdrawal-function directive | EU/EEA | online traders with withdrawal right | upcoming / application from 19 Jun 2026 | official directive; checked 9 Jun 2026 | monthly during rollout | high | withdrawal UI checklist | citeturn28view0turn27view2 |
| EU Accessibility Act / WCAG | EU/EEA and wider | stores, SaaS, apps | accessibility duties and statement framework | checked 9 Jun 2026 | semi-annual | medium | ACC, gating checklist | citeturn6search1turn6search2turn6search9 |
| EU AI Act / Commission AI transparency materials | EU/EEA | AI sites / AI-enabled products | transparency obligations and timelines | checked 9 Jun 2026 | quarterly | high | AI notice, risk report | citeturn7search0turn7search1turn8search0turn8search1 |

## Questionnaire and generation workflows

### Questionnaire draft

The questionnaire should be layered. Every question needs a rationale field so the skill knows what pages and checklist items it affects.

| Layer | Question | Why the skill must ask it | Affects |
|---|---|---|---|
| Must ask | What are you operating: store, SaaS, app, landing page, marketplace, affiliate site, newsletter page, or mixed model? | Determines core page bundle and legal taxonomy | all outputs |
| Must ask | Which countries or regions do you actively target, ship to, sell to, or advertise to? | Territorial scope drives privacy, cookie, consumer, and accessibility logic | requirements matrix, notices, launch checklist |
| Must ask | Do you sell physical goods, digital goods, software access, services, subscriptions, memberships, courses, or in-app purchases? | Consumer-rights and subscription logic changes materially by transaction type | ToS, RR, SP, ST, app notes |
| Must ask | Do you collect any personal data? Which categories: contact, account, payment, device, location, support tickets, uploaded customer data? | Privacy baseline and DPA logic cannot be drafted without this | PP, DPA, rights checks |
| Must ask | Do you use cookies, analytics, pixels, session replay, ad tags, or retargeting? Name tools if known. | Cookie consent and ad-tech disclosures depend on actual tooling | CP, banner, tracking matrix |
| Must ask | Is the site/app account-based? Can users create, delete, or self-serve accounts? | Deletion, retention, access, and app-store requirements | PP, deletion flow, app notes |
| Must ask | Who processes payments: Shopify, Stripe, PayPal, app stores, another PSP? | Payment, refund, and platform-dependency analysis | ToS, RR, ST, platform notes |
| Must ask | Do you have subscriptions, auto-renewal, free trials, or introductory pricing? | Subscription rules and risk intensify quickly here | ST, billing checklist, gating |
| Must ask | Is the product likely to be accessed by children, or directly aimed at them? | Children’s privacy / design can turn the whole output into high-risk mode | CH, parental-consent logic, legal review |
| Conditional | Do you let third parties sell, list, post, review, upload, or message on the platform? | Activates marketplace / UGC / moderation logic | MP, seller ToS, complaint flows |
| Conditional | Do you act as a processor for customer data, or only as controller for your own website data? | Needed for DPA and subprocessors | DPA, security annex, sales-material notes |
| Conditional | Do you use AI to generate content, answer users, score users, moderate content, or support decisions? | AI transparency and legal-review trigger | AI notice, red flag report |
| Conditional | Do you collect health, biometric, employment, financial, or precise location data? | Sensitive-data and regulated-sector trigger | red flag report, legal review |
| Conditional | Are orders fulfilled from a different country than the storefront suggests? | Dropshipping and cross-border delivery risk | SP, checkout disclosures, red flag report |
| Conditional | Are returns sent to a different country or supplier address? | Return policy and deceptive-practice risk | RR, SP, product-page checklist |
| Conditional | Do you send email and SMS marketing, and to which regions? | Consent rules vary sharply | marketing language, suppression-list ops |
| High risk | Are you making health, diagnostic, financial, hiring, or legal-effect claims? | High-risk legal and platform review required | AI / health / employment / finance triggers |
| High risk | Do you share data with ad platforms using enhanced matching, customer lists, or server-side events? | Sensitive advertising-data review | CP, PP, pixel checklist, Meta / Google notes |
| Must chase if unclear | Do you rely on any “template” pages today, and are they accurate to your actual practices? | Many failures come from mismatch, not absence | red flag report |
| Must chase if unclear | Are you B2C, B2B, or mixed? | Consumer law, cancellation rights, and app billing differ | ToS, RR, DPA, app notes |
| Must chase if unclear | Are you intentionally targeting EU / UK users or simply accessible there? | Scope and risk posture differ; if unsure, skill should assume moderate exposure and mark **Needs verification** | requirements matrix, lawyer triggers |

### Questionnaire decision model

The answers should populate a structured object like this:

```json
{
  "business_type": [],
  "target_regions": [],
  "transaction_types": [],
  "platforms": [],
  "data_categories": [],
  "tracking_stack": [],
  "marketing_channels": [],
  "sensitive_data_flags": [],
  "children_flag": false,
  "ugc_flag": false,
  "marketplace_flag": false,
  "processor_flag": false,
  "subscription_flag": false,
  "cross_border_fulfilment_flag": false,
  "app_distribution": [],
  "risk_level": "low|medium|high|blocking"
}
```

That object is the single source of truth for every downstream output.

### Policy generation workflow

The policy workflow should be deterministic.

| Stage | Input | Rule | Output |
|---|---|---|---|
| Business classification | questionnaire object | choose primary and secondary business types | business profile |
| Region mapping | target regions + accessibility + language + explicitly excluded markets | attach legal layers by region | jurisdiction map |
| Data mapping | data categories + tools + processors + ad-tech | determine privacy, cookie, DPA, deletion, transfer modules | data map |
| Transaction mapping | goods / digital / services / subscriptions / shipping / payment rails | determine consumer, refund, shipping, billing modules | commerce map |
| Risk scan | children / sensitive data / AI / marketplace / UGC | add risk notices and lawyer-review markers | risk map |
| Page bundle selection | from business, region, transaction, risk | produce required / recommended / not-applicable page list | required pages list |
| Outline assembly | page bundle + modules | create page-by-page section outlines | content outlines |
| Draft generation | outlines + tone + locale | produce draft text with placeholders only where facts are missing | policy drafts |
| Verification pass | drafts vs questionnaire object | remove generic clauses that are unsupported by facts | compliant draft pack |
| Disclaimer injection | every draft | append non-legal-advice disclaimer | final skill output pack |

The clause library in `policy-templates.md` should be modular. For example, the Privacy Policy template should not be one monolithic block. It should contain separately insertable modules for: controller identity, categories of data, sources of data, purposes, legal bases, cookies and ad tech, sharing / service providers, international transfers, retention, user rights, children, AI, security, complaints, and contact details. GDPR / UK GDPR sites need lawful-basis and rights modules; CCPA/CPRA sites need notice-at-collection, rights, and sale/share modules; app pages need SDK and mobile identifier modules. citeturn0search0turn0search1turn24search0turn11search11turn16search3

### Checklist generation workflow

The checklist workflow should be evidence-led, not prose-led.

| Stage | What it does | Output |
|---|---|---|
| Requirement extraction | convert law / platform / best-practice rules into checklist items | raw requirement list |
| Applicability filter | include only items triggered by facts | scoped checklist |
| Severity scoring | label Blocking / High risk / Medium risk / Best practice | prioritised checklist |
| Evidence binding | require screenshot, URL, config export, platform field, or sample email/SMS copy | evidence-ready checklist |
| Owner assignment | product / legal / engineering / marketing / ops / content | accountable checklist |
| Pass/fail evaluation | allow unknown, pass, fail, partial | review worksheet |
| Lawyer escalation | attach legal-review reason | counsel review queue |
| Gating extraction | lift only blocking items into go-live gate | release gate |

### Final gating checklist schema

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

A rendered checklist row should look like this:

| Severity | Requirement | Why it matters | Applies when | Evidence needed | Status | Source | Owner | Review frequency |
|---|---|---|---|---|---|---|---|---|
| Blocking | Non-essential cookies must not fire before consent in EU/UK flows | Unlawful tracking can invalidate consent and trigger complaints / enforcement | EU/UK visitors + analytics / ads pixels active | CMP config; tag audit; screenshots; test logs | Fail | ePrivacy / ICO / EDPB citeturn2search0turn2search2turn3search0 | Engineering | Quarterly |

## Worked outputs, risk boundaries and maintenance

### Example output for an EU plus U.S. Shopify dropshipping store

**Assumed facts:** Shopify storefront, consumer goods, ships from China to EU and U.S., uses GA4 + Meta Pixel + email capture + Klaviyo, offers discount codes but no recurring subscriptions.

**What the skill should output**

| Output | Result |
|---|---|
| Business classification | `ecommerce_store`, `dropshipping_store`, `international_cross_border_store` |
| Regions | EU/EEA, UK if targeted, U.S. baseline, California flag for privacy opt-out if applicable |
| Required pages | PP, CP, cookie banner, ToS, RR, SP, contact / customer-service page, checkout checklist, product-page checklist, footer checklist |
| Strongly recommended pages | accessibility statement, customs/duties FAQ, “Where we ship from” disclosure |
| Blocking issues likely | banner fires tracking before consent; shipping times unclear; return address hidden; customs / duties responsibility unclear; privacy policy mismatched to pixels used |
| High-risk items | price-promo evidence, hidden mandatory fees, mismatch between “local” branding and overseas fulfilment |
| Legal-review triggers | if California “sale/share” logic applies; if child-directed products; if health / beauty claims are made |

**Required page bundle**

| Page | Why it is needed | Class |
|---|---|---|
| Privacy Policy | personal data, email capture, checkout, analytics, pixels | Legal requirement |
| Cookie Policy + banner | GA4 + Meta Pixel + retargeting | Legal requirement in EU/UK |
| Terms & Conditions | purchase terms, governing law, account / IP / disclaimers | Legal requirement / risk-based |
| Refund & Return Policy | goods returns, exceptions, process, statutory carve-outs | Legal requirement / risk-based |
| Shipping Policy | origin, fulfilment times, carriers, customs / duties, lost parcel handling | Risk-based recommendation with consumer-law support |
| Footer compliance checklist | make pages findable before and during checkout | Best practice / risk control |

**Minimum policy clauses this store should include**

| Document | Clauses the skill should insert |
|---|---|
| Privacy Policy | data categories; Shopify and third-party processors; analytics and ad-tech disclosures; rights section; international transfers; retention; contact |
| Cookie Policy | categories; tool table; consent / withdrawal controls; how to change preferences |
| Returns Policy | return window; condition rules; non-returnables; damaged-item process; statutory rights carve-out; who pays return postage; country of return |
| Shipping Policy | processing time vs transit time; source country; customs / import taxes; failed delivery; tracking; peak-delay disclaimer |
| Terms | merchant identity; order acceptance; price accuracy; shipping limitation; user use rules; liability; governing-law placeholder |

**Gating checklist for this example**

| Severity | Requirement | Applies when | Evidence needed |
|---|---|---|---|
| Blocking | Do not fire Meta Pixel / GA4 before consent for EU/UK traffic | EU / UK visitors + ad / analytics tags | CMP test, network logs |
| Blocking | State shipping origin and estimated fulfilment windows clearly | Dropshipping / cross-border fulfilment | product page, shipping page, checkout copy |
| Blocking | State return address / return country and return process clearly | Goods sale with overseas supplier | returns page, support SOP |
| High risk | State whether duties / VAT / customs are included or borne by buyer | Cross-border shipping | checkout copy, shipping page |
| High risk | Validate discount / strike-through pricing basis | EU pricing promotions | pricing evidence file |
| Medium risk | Add accessibility statement and WCAG remediation plan | EU-facing store / trust optimisation | statement + audit |

The legal basis for this output is the interaction of GDPR transparency, ePrivacy / PECR consent, EU / UK consumer-contract information duties, California opt-out architecture where relevant, and Shopify’s own privacy tooling structure. citeturn0search0turn2search0turn2search2turn4search4turn21search4turn24search2turn11search2turn11search7

### Example output for a B2B SaaS landing page

**Assumed facts:** marketing site for a CRM / workflow SaaS; demo-request form; newsletter signup; analytics; no self-serve purchase on site; product stores customer contact data; targets EU, UK, U.S.

**What the skill should output**

| Output | Result |
|---|---|
| Business classification | `b2b_saas`, optionally `lead_generation_site` |
| Required pages | PP, CP if tracking, ToS / Website Terms, DPA outline, subprocessors / privacy contact section |
| Usually not required at first pass | Refund / Return Policy and Shipping Policy if no self-serve consumer checkout exists |
| Strongly recommended | Security / Trust page, accessibility statement, AI notice if product uses AI, cookie preference centre |
| Blocking issues likely | no DPA framework despite processor role; ad pixels undisclosed; no cookie controls; missing privacy contact; false claims about certifications / security / AI |

**Minimum bundle**

| Page / artifact | Why |
|---|---|
| Privacy Policy | marketing-site data + contact forms + cookies |
| Cookie Policy / banner | analytics / pixels |
| Website Terms | site use and lead-gen controls |
| DPA outline | sales enablement and processor posture |
| Security / trust summary | not always legally required, but essential for B2B deal flow |
| AI disclosure | if AI copilots / automated decision-support / model training are offered |
| Accessibility Statement | recommended for enterprise procurement and EU exposure |

**Core clauses**

| Document | Clauses |
|---|---|
| Privacy Policy | marketing-site data, CRM handling, demo-request data, lawful bases, transfers, rights |
| DPA outline | roles, instructions, security, subprocessors, assistance, deletion / return, audit, transfer mechanism |
| Website Terms | permitted use, no scraping / misuse, no reverse engineering of public demos, disclaimers |
| AI notice | what AI does, limitations, human review, customer control over inputs and outputs |
| Security page | encryption claims, subprocessors, retention, reporting channel, not misleading about guarantees |

This output is driven less by consumer returns law and more by controller / processor separation, data transfers, cookies, and procurement trust expectations. Article 28 processor-contract logic is especially important here. citeturn30search0turn30search1turn30search2turn2search0turn2search2turn7search3

### Example output for a mobile app homepage

**Assumed facts:** app homepage for a fitness and habit app; account creation; analytics SDKs; auto-renewing premium subscription; available on Apple App Store and Google Play; not intended for children.

**What the skill should output**

| Output | Result |
|---|---|
| Business classification | `mobile_app_landing_page`, `subscription_site`, likely `health-adjacent` |
| Required website pages | PP, ST, CP if the homepage itself tracks; app privacy section; support/contact page |
| Required platform notes | Apple privacy-policy URL and in-app link; App Privacy Details alignment; Google Play privacy-policy link in listing and within app if sensitive data; Data safety; account deletion path |
| High-risk triggers | health claims accuracy; subscription/paywall clarity; deletion rights; sensitive permissions |
| Optional but wise | AI notice if using AI coach features; accessibility statement |

**Website and app-store bundle**

| Area | What the skill should generate |
|---|---|
| Public website | Privacy Policy, Subscription Terms, cookie banner copy, homepage footer links |
| Apple note | privacy policy URL, in-app access, app privacy labels, subscription information, health-data caution, kids checks if applicable |
| Google note | privacy policy in listing + in-app where required, data safety mapping, account deletion checklist, prominent disclosure if data use exceeds user expectations |

**Blocking items**

| Severity | Requirement | Evidence |
|---|---|---|
| Blocking | Subscription paywall must clearly explain what the user gets and what renews | paywall screenshots; app copy; pricing tables |
| Blocking | Deletion path must exist if accounts can be created | in-app flow or web deletion page; help article |
| Blocking | Privacy policy and store disclosures must match actual SDK / data practices | SDK inventory; app listing; PP draft |
| High risk | Do not overstate health accuracy or methodology | claim substantiation; medical disclaimer |

Apple specifically requires a privacy-policy link in App Store Connect metadata and within the app, expects deletion / retention explanation in the privacy policy, requires clarity for auto-renewing subscriptions, and applies stricter rules to Kids Category and health-related claims. Google Play requires privacy-policy links in the listing and within the app for sensitive-data or children’s apps, requires Data safety disclosures, requires account deletion when accounts can be created, and requires prominent in-app disclosure where sensitive-data use is outside reasonable user expectation. citeturn32view3turn32view2turn32view0turn16search1turn17search6turn17search13turn11search1turn17search4turn17search11

### Risk boundaries and lawyer-review triggers

The skill should include this escalation table verbatim or near-verbatim.

| Trigger | Why the skill must escalate | Label |
|---|---|---|
| Health, medical, diagnostic, fitness-with-health-claims | sensitive data and sector-specific risk; app platforms scrutinise accuracy claims | Legal review required |
| Biometrics, face / voice / fingerprint handling | sensitive-data and state / country-specific overlays | Legal review required |
| Children or likely child-access | COPPA / Children’s Code / GDPR child-consent issues | Legal review required |
| Financial products, lending, payments, insurance, investments | consumer-finance and distance financial-services complexity | Legal review required |
| Employment / hiring / screening / worker scoring | discrimination, automated decisioning, privacy and labour overlays | Legal review required |
| AI scoring or materially impactful AI | EU AI Act and general consumer-protection risk | Legal review required |
| Marketplace / UGC / community with user posts or sellers | DSA / P2B / moderation / seller verification duties | Legal review required |
| SMS marketing, autodialling, or lead resale | telemarketing consent standards vary and are high-risk | Legal review required |
| Cross-border store with unclear seller identity, origin, duties, or return address | classic refund / misrepresentation dispute pattern | High risk or Blocking depending severity |
| Relying on “just a generator template” not based on actual practices | mismatch risk is often worse than no page | High risk |

### Maintenance and update mechanism

The skill should have a **two-track maintenance model**.

First, maintain the **rule sources** in `references/source-register.md`. Each row should record the source, jurisdiction, applicable business types, affected templates / checklists, last verified date, review cadence, and change risk. Second, maintain the **output modules** in `policy-templates.md` and `checklist-framework.md`. If a source changes, you update the affected modules listed in the source register and re-run scenario tests. This is much safer than editing long templates ad hoc. The need for regular review is especially strong for cookies, California privacy regulations, app-store policies, AI transparency materials, UK subscription implementation, and ad-platform rules. citeturn24search1turn11search0turn12search11turn7search1turn23view0

A workable review cadence is:

| Change risk | Examples | Review cadence |
|---|---|---|
| High | CPPA regulations, Apple / Google Play policies, AI Act guidance, UK subscription implementation, DSA guidance | monthly to quarterly |
| Medium | GDPR / ICO guidance, PIPEDA, OAIC guidance, Google Ads / Meta policy pages | quarterly to semi-annual |
| Low | Core statutes like GDPR text, CAN-SPAM baseline, ROSCA baseline, UK CCRs, ACL guarantees | semi-annual to annual |

### How to package this into a ChatGPT Skill

The packaging path should be straightforward.

| Step | What to do | Deliverable |
|---|---|---|
| Prepare knowledge files | create the folder structure above and populate each reference file with the matrices and clause modules in this report | skill knowledge base |
| Encode operating rules | put the workflow, labels, disclaimer, escalation rules, and output contract into `SKILL.md` | skill instruction layer |
| Implement questionnaire helper | `compliance_questionnaire.py` should return the structured object from the questionnaire | structured intake |
| Implement checklist helper | `checklist_generator.py` should transform the structured intake into page requirements and gating rows | deterministic checklist engine |
| Create scenario tests | test at least: EU Shopify dropshipping, B2B SaaS, mobile app site, newsletter landing page, marketplace | validation pack |
| Add source governance | seed and maintain `source-register.md` with dates and impacted modules | update mechanism |
| Upload and test in builder | verify the skill asks classification questions first and does not jump to generic drafting | deployable skill |
| Add safety assertions | confirm all outputs include the not-legal-advice disclaimer and lawyer-review flags where triggered | final QA |

### Open questions and limitations

This design is strong enough to build the skill, but a few areas should stay explicitly marked:

| Area | Limitation |
|---|---|
| U.S. privacy law | This report uses California plus U.S. federal baseline as the practical default. It does **not** exhaustively codify every current state privacy, telemarketing, or auto-renewal rule. Mark U.S. state expansion as **Jurisdiction-specific**. |
| U.S. subscription law | The safest present approach is to encode ROSCA and California ARL as baseline, and keep broader federal negative-option implementation in a **Needs verification** track because this area has been actively changing. citeturn5search0turn4search3 |
| Canada consumer returns | Canada’s privacy and anti-spam rules are federal, but many refund / cancellation rights are provincial. The skill should warn users rather than fake nationwide certainty. citeturn21search7turn21search19 |
| Accessibility | The European Accessibility Act is highly relevant for EU-facing e-commerce and other covered services, but exact application can still depend on service scope and local implementation. Use **Needs verification** if the service sits near the boundary. citeturn6search1turn6search9 |
| EU withdrawal function | Directive (EU) 2023/2673 applies from 19 June 2026; on 9 June 2026 this sits right at the go-live edge and requires country-by-country verification in the immediate period after application. citeturn28view0turn28view1 |

The report’s final recommendation is simple: build **web-compliance-builder** as a **fact-driven compliance classifier**, a **modular document generator**, and an **evidence-based release gate**, with structured uncertainty labels whenever the law or platform layer is unsettled. That approach best matches both the official legal sources and the current platform environment.