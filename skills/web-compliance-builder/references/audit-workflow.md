# Audit Workflow

AUDIT mode reviews an **existing** site against what its facts require. Build mode asks "what does this site need?"; audit mode asks "what does this site have, and where does it fall short?" Never silently re-draft during an audit — report the gap first.

Enter AUDIT when the user provides existing pages/URLs or asks to 审计 / audit / review / 合规检查 an existing site. Still classify first — you cannot audit without knowing business type, regions, data, transactions, and risk.

## Procedure

1. **Classify** — run the standard classification (business type, regions, data/tracking, transactions, sensitive data). Same intake object as BUILD, plus `mode: "audit"` and `existing_pages`.
2. **Inventory existing pages** — for each page the user supplies (or each URL/page found), record: page type, URL/source, and the actual claims/sections it contains. If a URL can't be fetched, ask the user to paste the text; do not guess content.
3. **Compute the required set** — derive required pages from facts exactly as BUILD step 6 (`page-requirements.md`).
4. **Grade each required item** — assign one status:
   - **Present-OK** — page exists and covers the mandatory sections for the triggered region/platform.
   - **Present-Inadequate** — page exists but misses mandatory sections, is generic/templated, or omits triggered region/platform modules (e.g. PP with no California "sale/share" section while CA exposure exists).
   - **Missing** — required page absent.
   - **Mismatch** — page **contradicts actual practice** (e.g. "we don't use cookies" while GA4+Meta Pixel fire; returns page lists a domestic address while goods ship from and return to overseas). This is the most dangerous — rank Blocking. A wrong page is worse than no page.
5. **Run failure-mode + live-behavior checks** on Present pages — apply the per-page "common failure modes" in `page-requirements.md` and the surface checks in `checklist-framework.md`: pre-consent tag firing, buried/asymmetric reject button, hidden return address/origin, undisclosed duties, missing deletion path, paywall renewal clarity, store-disclosure ↔ SDK mismatch, price-promo prior-price basis.
6. **Produce outputs** — gap report + red-flag report + remediation gating checklist (Blocking gaps first). Mark Needs-verification / Jurisdiction-specific / Legal-review as in BUILD.

## Status decision aid

| Question | If yes |
|---|---|
| Page absent for a triggered requirement? | Missing |
| Page present but contradicts what the site actually does? | Mismatch (Blocking) |
| Page present but missing a mandatory section / region module? | Present-Inadequate |
| Page present and covers all triggered mandatory sections? | Present-OK |
| Page present for something the facts don't require? | Note as "not required" (don't inflate) |

## Gap report format

| Required item | Class | Status | Finding | Fix |
|---|---|---|---|---|
| Privacy Policy | Legal | Present-Inadequate | No California "Do Not Sell or Share" section despite US/CA traffic + Meta Pixel | Add notice-at-collection + sale/share + GPC modules |
| Cookie banner | Legal (EU/UK) | Mismatch | Banner present but GA4 fires before consent | Block non-essential tags until consent; symmetric reject |
| Shipping Policy | Risk-based | Missing | No shipping page; goods ship from overseas | Add origin, transit windows, customs/duties bearer |
| Returns Policy | Legal | Mismatch | Lists a domestic return address; returns actually go to overseas supplier | Correct return address/country + process |

## Severity mapping for remediation gate

- **Mismatch** (page contradicts practice) → Blocking.
- **Missing** legal-requirement page → Blocking.
- **Present-Inadequate** on a legal requirement → High risk (Blocking if it removes a mandatory consumer right or consent control).
- **Missing/Inadequate** platform requirement → Blocking for that channel (app rejection, ad disapproval).
- Best-practice/risk-based gaps → Medium / Best practice.

Lift only Blocking remediation items into the go-live / "is-it-compliant-now" gate.

## After the gap report

Offer to draft or fix the flagged pages (switch to BUILD-style drafting for the specific gaps) only **after** presenting the gap report, or when the user asks. Do not auto-rewrite. Same no-fabrication rule: when a page is inadequate because facts are missing, mark `[需补充 / needs input]`, don't invent.
