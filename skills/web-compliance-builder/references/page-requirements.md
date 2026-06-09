# Page Requirements

Page-by-page decision matrix. For each page: **purpose · label class · trigger logic · mandatory sections · region-specific sections · platform-specific sections · evidence required · common failure modes.** Emit a page only when its trigger fires.

## Trigger matrix (drives the required-pages list)

| Trigger | Page / artifact | Class | Applies when |
|---|---|---|---|
| Personal data collected | Privacy Policy | Legal requirement | Any form, analytics, account, checkout, support, or SaaS dashboard exists |
| Non-essential cookies / pixels / analytics | Cookie Policy + banner + consent settings | Legal (EU/UK); risk-based elsewhere | Cookies/pixels/SDKs/retargeting beyond strict necessity |
| Consumer sale of goods | Terms + Refund/Return + Shipping | Legal / risk-based mix | Physical goods sold to consumers |
| Cross-border goods sale | Customs/duties/delivery-country disclosures | Risk-based (consumer-law driven) | Ships internationally or origin ≠ store-facing country |
| Digital goods / software licence | Digital product terms / licence clauses | Legal / risk-based | Download, licence, course, template, membership asset |
| Auto-renewing plan / free trial | Subscription Terms | Legal / platform | Recurring billing or trial-to-paid |
| User accounts with personal data | Account deletion / data-rights section | Legal / platform | Account creation possible |
| SaaS acts as processor | DPA outline | Legal | Customer stores personal data in the service on their own behalf |
| UGC / community / marketplace | Moderation rules, seller terms, complaint workflow | Legal / risk-based | Users can post, list, or sell |
| Child-directed or likely child-accessed | Children's notice / age gate / parental-consent logic | Legal / legal-review trigger | Product for or likely accessed by children |
| AI system or AI marketing claims | AI disclosure notice | Risk-based or legal | AI content, chatbot, automation, training, decision support |
| Covered accessibility exposure | Accessibility Statement + WCAG checklist | Legal or risk-based | EU-covered service, public body, or litigation-sensitive site |
| Paid ads / remarketing | Ads-compliance note | Platform | Google/Meta/TikTok Ads etc. |
| App distribution | App-store compliance notes | Platform | Apple App Store / Google Play |
| High-risk data | Red-flag report + legal-review notice | Risk-based + escalation | Health, biometrics, precise location, finance, employment, children, AI decisioning |

## Page detail

### Privacy Policy — Legal requirement
Mandatory sections: controller identity; categories of data; sources; purposes; legal bases (GDPR/UK); cookies & ad-tech; sharing / service providers; international transfers; retention; user rights; children; AI; security; complaints; contact. Region-specific: lawful-basis + rights modules (EU/UK); notice-at-collection + "sale/share" + sensitive-PI + GPC (California); overseas-disclosure (Australia). Platform: deletion explanation (Apple/Google); SDK & mobile-identifier modules (apps). Evidence: data-map, processor list, tracking inventory. Failure modes: policy lists pixels the site doesn't use, or omits ones it does.

### Cookie Policy + Banner — Legal (EU/UK), risk-based elsewhere
Sections: cookie categories; per-tool table (name, provider, purpose, duration); consent/withdrawal controls; how to change preferences. Banner: reject-equals-accept, symmetrical buttons, no pre-consent firing of non-essential tags. Evidence: CMP config, tag audit, network logs, screenshots. Failure modes: pre-consent tags; "accept" prominent / "reject" buried (dark pattern).

### Terms / ToS — Legal / risk-based
Sections: merchant identity; order acceptance & price accuracy; permitted use; IP; disclaimers; liability; governing law (placeholder); dispute process. Failure modes: consumer-rights waivers that are void (ACL, EU/UK consumer law).

### Refund & Return Policy — Legal / risk-based
Sections: return window; condition rules; non-returnables; damaged-item process; who pays return postage; country of return; statutory-rights carve-out. Region: EU/UK withdrawal vs statutory guarantees (AU). Failure modes: waiving statutory guarantees; physical policy applied to digital goods; hidden overseas return address.

### Shipping Policy — Risk-based with consumer-law support
Sections: processing vs transit time; source country; carriers; customs/import taxes & who bears them; failed delivery; tracking; peak-delay disclaimer. Failure modes: unclear origin/timing for dropshipping; undisclosed duties.

### Subscription Terms — Legal / platform
Sections: what's included; renewal frequency & price; billing timing; cancellation path; pre-renewal notices; trial→paid conversion; platform billing if app-based. Region: ROSCA, California ARL, UK DMCCA (future). Failure modes: buried cancellation; no express informed consent at signup.

### Acceptable Use Policy — risk-based / legal for UGC & AI
Permitted/prohibited use, no scraping/misuse, no reverse engineering, enforcement. Required for marketplaces, UGC, AI products.

### DPA outline — Legal (when processor)
Roles; processing instructions; security; subprocessors; assistance; deletion/return; audit; transfer mechanism (SCC/IDTA). Output an *outline* unless the user asks for a full DPA.

### Accessibility Statement — Legal or risk-based
Conformance target (WCAG 2.2 AA), known limitations, feedback channel, remediation plan. The **WCAG remediation checklist** is the real control — the statement alone is not compliance.

### Age / Children Notice — Legal / legal-review trigger
Children's notice, age gate, parental-consent logic, high-privacy defaults. Country-specific consent age (EU). Never rely on a generic age-18 footer only.

### AI Disclosure — Risk-based or legal
What the AI does; limitations; human review; user control over inputs/outputs; synthetic-media labelling; claims substantiation; training-data/privacy note. Mark **Legal review required** for high-risk/sensitive use.

### Marketing Consent Language — Legal
Per-channel (email/SMS) consent + unsubscribe + sender ID. Variants: CAN-SPAM (opt-out + address), PECR/CASL/Spam Act (consent/soft-opt-in). 

### Marketplace Seller Terms + Complaint/Moderation — Legal / risk-based
Seller onboarding/KYC, trader traceability, ranking transparency, illegal-content & complaint workflow (DSA/P2B/INFORM).
