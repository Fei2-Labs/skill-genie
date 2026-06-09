# Policy Templates

Modular clause library. **Never emit a monolithic block.** Assemble only the modules the intake object triggers, then fill placeholders `[[like_this]]` only where a real fact is missing. Strip any module not supported by the facts during the verification pass.

Every assembled document ends with the required non-legal-advice disclaimer (see SKILL.md).

## Module index

Insertable modules (reused across documents):

- `intro` — document title, business identity, effective date, scope.
- `data_categories` — what personal data is collected (contact, account, payment, device, location, support, uploaded customer data).
- `data_sources` — direct, automatic, third-party.
- `purposes` — why each category is processed.
- `legal_bases` — GDPR/UK lawful bases per purpose (consent, contract, legitimate interests, legal obligation). EU/UK only.
- `cookies_adtech` — tracking technologies, tools table, consent/withdrawal.
- `sharing_providers` — processors / service providers / recipients.
- `intl_transfers` — transfer mechanisms (SCC/IDTA), destinations.
- `retention` — retention periods / criteria.
- `user_rights` — access, deletion, correction, portability, objection; how to exercise. EU/UK rights vs California rights vs APP access differ — pick by region.
- `notice_at_collection` — California point-of-collection + "Do Not Sell or Share" + sensitive-PI + GPC.
- `overseas_disclosure` — Australia APP overseas-disclosure section.
- `children` — age threshold, parental consent, high-privacy defaults.
- `ai` — what AI does, limitations, human review, input/output control, synthetic-media labelling.
- `security` — safeguards (no overstated guarantees), breach contact.
- `sdk_mobile` — app SDKs, mobile identifiers, app-store deletion explanation.
- `complaints_contact` — DPO/privacy contact, supervisory-authority/regulator complaint route.
- `jurisdiction_addenda` — region-specific riders appended after the core body.

## Document skeletons (module order)

**Privacy Policy:** `intro` → `data_categories` → `data_sources` → `purposes` → `legal_bases`(EU/UK) → `cookies_adtech` → `sharing_providers` → `intl_transfers` → `retention` → `user_rights` (+`notice_at_collection` if CA, +`overseas_disclosure` if AU) → `children`(if triggered) → `ai`(if triggered) → `sdk_mobile`(if app) → `security` → `complaints_contact` → `jurisdiction_addenda` → disclaimer.

**Cookie Policy:** `intro` → cookie categories → tools table (name · provider · purpose · category · duration) → consent/withdrawal controls → how to change preferences → disclaimer.

**Cookie Banner copy:** layered notice + symmetrical Accept / Reject / Preferences; no pre-consent non-essential firing; short purpose line + link to Cookie Policy.

**Terms / ToS:** `intro`/merchant identity → order acceptance & price accuracy → permitted use → IP → consumer-rights preservation note → disclaimers → liability cap → governing law `[[jurisdiction]]` → dispute process → disclaimer.

**Refund & Return Policy:** scope → return window → condition rules → non-returnables → damaged/defective process → who pays return postage → `[[return_address_country]]` → statutory-rights carve-out → digital-content waiver (if digital) → disclaimer.

**Shipping Policy:** processing vs transit time → `[[source_country]]` → carriers → customs/import taxes & bearer → failed delivery → tracking → peak-delay disclaimer → disclaimer.

**Subscription Terms:** what's included → renewal frequency & `[[price]]` → billing timing → cancellation path → pre-renewal notices → trial→paid conversion terms → platform-billing note (if app) → ROSCA/ARL/region rider → disclaimer.

**AUP:** permitted use → prohibited use (scraping, misuse, reverse engineering, illegal content) → enforcement/suspension → reporting channel → disclaimer.

**DPA outline:** roles (controller/processor) → processing details/instructions → security measures → subprocessors annex → assistance (rights, DPIA, breach) → deletion/return on termination → audit → transfer mechanism `[[SCC/IDTA]]` → disclaimer.

**Accessibility Statement:** conformance target (WCAG 2.2 AA) → known limitations → feedback/contact → remediation plan & dates → disclaimer.

**Children Notice:** who it's for → age threshold `[[country_age]]` → data practices → parental consent mechanism → high-privacy defaults → contact → disclaimer.

**AI Disclosure:** what the AI does → limitations & error modes → human-review availability → user control over inputs/outputs → synthetic-media labelling → claims substantiation note → training-data/privacy note → disclaimer.

**Marketing Consent language:** per-channel consent statement → sender identification → physical postal address (CAN-SPAM) → unsubscribe mechanism → region variant (opt-in vs opt-out) → suppression-list note.

**Marketplace Seller Terms:** eligibility/KYC → trader traceability fields → listing rules → ranking-transparency note → prohibited goods → complaint/takedown workflow → liability allocation → disclaimer.

## Region clause selection rules

- EU/UK site → include `legal_bases`, EU/UK `user_rights`, `intl_transfers`.
- California exposure → include `notice_at_collection` + GPC handling.
- Australia → include `overseas_disclosure`.
- App distribution → include `sdk_mobile` + store deletion explanation.
- Processor role → produce DPA outline; reference it from Privacy Policy.
- No fact to support a clause → omit it (verification pass removes unsupported generic clauses).
