# Business Types

Business-type taxonomy → typical data flows, transaction patterns, default required pages, common region overlays, common red flags. Classify primary + secondary type from the questionnaire before drafting.

Legend: **PP** Privacy Policy · **CP** Cookie Policy/consent · **ToS** Terms · **RR** Refund/Return · **SP** Shipping · **ST** Subscription Terms · **AUP** Acceptable Use · **DPA** Data Processing Addendum outline · **ACC** Accessibility Statement · **AI** AI disclosure · **CH** Children/age notice · **MP** Marketplace/seller bundle.

## Core mapping

| Business type | Typical outputs | Trigger-sensitive add-ons |
|---|---|---|
| General ecommerce store | PP, CP, ToS, RR, SP, checkout/product/footer checklists | EU withdrawal sections; California opt-out; accessibility; shipping/tax disclosures |
| Dropshipping store | ecommerce outputs + stronger fulfilment/origin/customs/returns clarity | "ships from" / cross-border timing / duty-bearing party / return address; platform shipping notes |
| Digital product store | PP, CP if tracking, ToS, RR with digital-content logic | EU/UK digital-content withdrawal waiver; licence terms |
| Subscription / membership | PP, CP, ToS, ST, billing disclosures, cancellation-flow checklist | US recurring-charge controls (ROSCA); California ARL; UK future-regime prep; Apple/Google subscription notes if in-app |
| B2C SaaS | PP, CP, ToS, ST if recurring, DPA if processor, security/subprocessors | account deletion, trial disclosures, AI notice, accessibility, California rights |
| B2B SaaS | PP, CP, ToS, DPA, subprocessors/transfer addendum, AUP | security/admin controls, sales-contact transparency; fewer consumer pages unless self-serve checkout exists |
| Mobile app landing page | website PP + App Store/Play notes; ST if subscriptions; CP if tracking | app privacy labels, data-safety alignment, account-deletion page, support/contact |
| Marketplace / multi-vendor | PP, CP, consumer ToS, seller ToS, MP, complaint flow, moderation rules | trader verification, ranking transparency, P2B, DSA/INFORM Consumers Act |
| Affiliate / lead-gen | PP, CP, ToS, affiliate disclosure, marketing-consent language | lead-sharing disclosures; TCPA/SMS escalation; ad-pixel consent logic |
| AI product website | PP, CP, ToS, AI, AUP, DPA if B2B processing, model-input/training clauses | transparency, claims substantiation, human review, misuse rules |
| Newsletter / email-capture page | PP, CP if tracking, light Site Terms, marketing-consent language | double-opt-in; CASL/PECR/Spam Act/CAN-SPAM variants |
| International cross-border store | all store outputs + stronger taxes/duties/country-availability disclosures | currency, VAT/GST, customs, final-price clarity, return-destination mismatch checks |

## Per-type detail

For each type the skill reasons over: **definition · common data collected · tracking patterns · transaction patterns · default pages · common region overlays · common red flags.**

### Ecommerce store
Sells physical goods to consumers. Data: contact, account, payment (via PSP), order history, support. Tracking: GA4, ad pixels, retargeting. Transactions: one-off purchases, discounts. Default: PP, CP, ToS, RR, SP. Overlays: EU withdrawal, California opt-out, EAA. Red flags: terms-only with no separate returns/shipping pages; pixels undisclosed; promo pricing without prior-price evidence.

### Dropshipping store
Ecommerce where goods ship from a third party, often overseas. Adds: origin disclosure, realistic transit times, duty-bearing party, return address/country. Red flags: "local" branding masking overseas fulfilment; hidden return address; unclear customs responsibility — classic refund/misrepresentation pattern → often **Blocking**.

### Digital products
Downloads, software licences, courses, templates, memberships. Data: account, payment, usage. Transactions: instant digital delivery. Default: PP, CP if tracking, ToS, RR with digital-content logic. Overlay: EU/UK digital-content withdrawal **waiver** (consumer waives the cooling-off right to get instant access). Red flags: applying a physical-goods returns policy to digital goods.

### Subscription / membership
Recurring billing, trials, intro pricing. Default adds ST + cancellation-flow checklist. Overlays: ROSCA (US), California ARL, UK DMCCA (future), Apple/Google billing if in-app. Red flags: unclear renewal terms, hard-to-find cancellation, trial-to-paid without express informed consent → **High risk / Legal review**.

### B2C SaaS
Self-serve software to consumers. Data: account, usage, billing, possibly uploaded content. Default: PP, CP, ToS, ST if recurring, DPA only if acting as processor. Add: account deletion, trial disclosures, AI notice, accessibility, California rights.

### B2B SaaS
Software to businesses; often no on-site consumer checkout. Default: PP, CP, ToS, DPA, subprocessors/transfer addendum, AUP. Driven by controller/processor separation and procurement trust, not consumer-returns law. Security/Trust page essential for deal flow. Red flags: processor role with no DPA framework; false security/certification/AI claims.

### Mobile app landing page
Marketing site for an iOS/Android app. Website needs PP (+ ST if subscriptions, CP if the page itself tracks). Platform notes dominate: Apple privacy-policy URL + in-app link + App Privacy Details + subscription clarity + Kids/health scrutiny; Google Play privacy link in listing & in-app for sensitive/children's apps + Data safety + account-deletion path + prominent disclosure when data use exceeds expectations.

### Marketplace / multi-vendor
Third parties sell/list/post. Default: PP, CP, consumer ToS, seller ToS, MP bundle, complaint flow, moderation rules. Overlays: DSA (trader traceability, ranking transparency, dark-pattern limits), P2B, US INFORM Consumers Act (high-volume seller verification). Almost always → **Legal review required**.

### Affiliate / lead-generation
Captures and may resell leads; affiliate revenue. Default: PP, CP, ToS, affiliate disclosure, marketing-consent language. Red flags: lead resale without disclosed sharing; SMS/autodialling → TCPA escalation.

### AI product website
Offers AI generation, chat, scoring, moderation, or decision support. Default: PP, CP, ToS, AI disclosure, AUP, DPA if B2B processing, model-input/training clauses. Mark **Legal review required** for high-risk or sensitive-domain use.

### Newsletter / email-capture page
Single-purpose signup. Default: PP, CP if tracking, light Site Terms, marketing-consent language. Consent model varies sharply by region (CASL/PECR opt-in vs CAN-SPAM opt-out). Prefer double-opt-in for mixed audiences.

### Cross-border store
Sells/ships across regions. All store outputs + currency, VAT/GST, customs/duties, country availability, final-price clarity, return-destination mismatch checks. Red flags: hidden origin, undisclosed import charges, return address in a different country.
