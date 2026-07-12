---
name: landing-launch-check
description: Final pre-launch audit for a multilingual marketing landing page — SEO, AEO/AIO (structured data for AI search), GEO, and EU compliance (GDPR/ePrivacy). Catches the common failures that ship to production when a landing page is built on top of a shared app layer.
license: "MIT"
metadata: {"version":"1.0.0","category":"launch-qa","license":"MIT","tags":["seo","aeo","geo","compliance","gdpr","landing-page","launch","audit","i18n"],"hermes":{"tags":["seo","aeo","geo","compliance","gdpr","landing-page","launch","audit","i18n"]}}
---

# Landing Page Final Launch Check

A focused, evidence-based audit that runs **after** the landing page is built and deployed, **before** declaring it launch-ready. Designed for marketing landing pages that extend a shared app layer (e.g. a Nuxt app-base with i18n, auth, and compliance components inherited by B2C/B2B apps).

## When to use

- A new landing page has been deployed and needs a final sign-off
- A landing page was built on top of a shared app layer and may have inherited wrong defaults
- The site targets multiple locales (e.g. Swedish + English) and needs per-locale SEO
- The site targets EU users and needs GDPR/ePrivacy compliance
- Before submitting to Google Search Console and AI search engines

## What this skill checks

Four dimensions, each with concrete pass/fail criteria:

1. **Technical SEO** — meta tags, canonical, hreflang, sitemap, robots.txt
2. **AEO/AIO/GEO** — structured data (JSON-LD) for AI search engines and rich results
3. **i18n correctness** — per-locale meta, lang attribute, og:locale
4. **EU compliance** — cookie consent, privacy policy, terms, GDPR Art. 13 elements

## Prerequisites

- The landing page is deployed and accessible via its public URL
- `curl` available for HTTP inspection
- Python 3 for parsing HTML
- (Optional) Playwright + a Chrome instance with CDP for Google Search Console submission
- (Optional) `gh` CLI for creating follow-up issues

## Audit procedure

### Phase 1: Crawl the live pages

Fetch the HTML for every locale variant and the robots.txt:

```bash
curl -s https://example.com/ -o /tmp/landing-sv.html
curl -s https://example.com/en -o /tmp/landing-en.html
curl -s https://example.com/robots.txt -o /tmp/robots.txt
curl -s -o /dev/null -w "%{http_code}" https://example.com/sitemap.xml
```

### Phase 2: Technical SEO audit

For each locale variant, extract and check:

```python
import re
html = open('/tmp/landing-sv.html').read()
checks = {
    'title': re.findall(r'<title>([^<]*)</title>', html),
    'lang': re.findall(r'<html[^>]*lang="([^"]*)"', html),
    'description': re.findall(r'name="description" content="([^"]{0,80})', html)[:1],
    'canonical': re.findall(r'rel="canonical" href="([^"]*)"', html),
    'hreflang': re.findall(r'hreflang="([^"]*)"', html),
    'og:locale': re.findall(r'og:locale" content="([^"]*)"', html),
    'og:image': re.findall(r'og:image" content="([^"]{0,90})', html),
    'og:url': re.findall(r'og:url" content="([^"]*)"', html),
    'twitter:card': re.findall(r'twitter:card" content="([^"]*)"', html),
    'json-ld': len(re.findall(r'application/ld\+json', html)),
    'robots_meta': re.findall(r'<meta name="robots" content="([^"]*)"', html),
}
```

**Pass criteria (per locale):**

| Check | Requirement | Common failure |
|-------|-------------|----------------|
| title | Present, localized, < 60 chars | Hardcoded English on all locales |
| lang | Matches locale (`sv-SE`, `en-GB`) | Inherited `lang="sv"` on EN page |
| description | Present, localized, 150-160 chars | Hardcoded fallback from nuxt.config |
| canonical | Self-referencing, per-locale URL | Missing entirely |
| hreflang | `x-default` + all locale variants | Missing (no `i18n.baseUrl` set) |
| og:locale | Matches locale (`sv_SE`, `en_GB`) | Missing |
| og:image | Points to production domain, not staging | Staging/dev domain leaked into prod |
| og:url | Per-locale URL | Single hardcoded URL |
| twitter:card | `summary_large_image` | Missing |
| json-ld | At least 1 block | Zero structured data |

**robots.txt checks:**

```
User-Agent: *
Allow: /
Disallow: /login          # inherited auth pages shouldn't be indexed
Disallow: /register
Disallow: /en/login
Sitemap: https://example.com/sitemap.xml
```

**Sitemap checks:**
- `/sitemap.xml` returns 200
- Contains all public URLs
- Has `xhtml:link rel="alternate"` with hreflang for locale variants

### Phase 3: AEO/AIO/GEO audit (structured data)

AI search engines (Google AI Overviews, Perplexity, ChatGPT Search, Bing Copilot) rely on structured data to cite sources. Check for JSON-LD presence and validity:

```python
import json, re
html = open('/tmp/landing-sv.html').read()
m = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
if m:
    data = json.loads(m.group(1))
    types = [g['@type'] for g in data.get('@graph', [data])]
    print('JSON-LD types:', types)
```

**Recommended JSON-LD types for a landing page:**

| Type | Purpose | Required fields |
|------|---------|-----------------|
| `Organization` | Brand entity for AI/Knowledge Graph | name, url, logo |
| `WebSite` | Site entity with language | name, url, inLanguage, publisher |
| `FAQPage` | Q&A pairs for rich results + AI citation | mainEntity[].name, acceptedAnswer.text |
| `SportsEvent` | (if applicable) Event listings | name, startDate, location, competitor |

**Validation:**
- JSON must be valid (parse without error)
- Test at https://search.google.com/test/rich-results
- Test at https://validator.schema.org/

**Key AEO insight:** The FAQ content must be **localized per locale** — an EN page serving SV FAQ text confuses AI engines. Use i18n keys in the JSON-LD generator, not hardcoded strings.

### Phase 4: i18n correctness audit

The most common landing page bug: a shared app layer hardcodes one locale's meta in `nuxt.config.ts` or `definePageMeta()`, and every locale variant serves the same meta.

**Check each locale variant independently:**

```bash
# SV page should have sv-SE lang, sv_SE og:locale, Swedish title
curl -s https://example.com/ | grep -oP '(?<=lang=")[^"]*|(?<=og:locale" content=")[^"]*|(?<=<title>)[^<]*'

# EN page should have en-GB lang, en_GB og:locale, English title
curl -s https://example.com/en | grep -oP '(?<=lang=")[^"]*|(?<=og:locale" content=")[^"]*|(?<=<title>)[^<]*'
```

**Common failures when extending a shared app layer:**

1. `app.head.htmlAttrs.lang` hardcoded in `nuxt.config.ts` → all locales get same lang
2. `definePageMeta({ title: '...' })` hardcoded → all locales get same title
3. `useSeoMeta({ description: '...' })` hardcoded → all locales get same description
4. `og:image` URL points to staging domain → leaked from default config
5. No `i18n.baseUrl` → `useLocaleHead()` can't generate canonical/hreflang

**Fix pattern (Nuxt + @nuxtjs/i18n):**

```ts
// In the page component, NOT in nuxt.config.ts
const { t, locale } = useI18n()
const i18nHead = useLocaleHead({ seo: true, lang: true })

useHead({
  htmlAttrs: computed(() => i18nHead.value.htmlAttrs ?? {}),
  link: computed(() => i18nHead.value.link ?? []),
  meta: computed(() => i18nHead.value.meta ?? []),
})

useSeoMeta({
  title: () => t('landing.meta.title'),
  description: () => t('landing.meta.description'),
  ogLocale: () => locale.value === 'sv' ? 'sv_SE' : 'en_GB',
  // ... all meta from i18n keys, not hardcoded
})
```

```ts
// nuxt.config.ts — set baseUrl so useLocaleHead can generate canonical/hreflang
i18n: {
  baseUrl: 'https://example.com',
}
```

### Phase 5: EU compliance audit

**Business classification (do this first):**
- Is it B2C or B2B?
- Does it process personal data? (cookies, analytics, forms, auth)
- Does it target EU/EEA users? (GDPR + ePrivacy apply)
- Does it have third-party trackers? (GA, Meta Pixel, Hotjar, etc.)

**Required pages check:**

```bash
for p in privacy terms cookie-settings; do
  echo -n "/$p: "; curl -s -o /dev/null -w "%{http_code}" https://example.com/$p
done
```

**Cookie consent banner check:**

1. Banner appears on first visit (no prior consent cookie)
2. "Accept All" and "Essential Only" buttons are **equally prominent** (no dark pattern)
3. Consent is recorded with a timestamp
4. Consent can be withdrawn via `/cookie-settings`
5. **Pre-consent tag firing**: no third-party trackers load before consent is given

**Privacy policy GDPR Art. 13 elements:**

Scan the privacy policy text for these required elements:

| Element | Swedish keyword | Status |
|---------|-----------------|--------|
| Data controller identity | personuppgiftsansvarig | |
| Legal basis | rättslig grund | |
| Retention period | lagringstid | |
| Data subject rights | rättigheter | |
| Supervisory authority (IMY for SE) | IMY | |
| Third-party processors | tredje part / underbehandlare | |
| Data transfer outside EU/EEA | överföring | |
| Contact for data protection | e-post / kontakt | |

```python
import re, html as H
h = open('/tmp/priv.html').read()
text = H.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', re.sub(r'<script.*?</script>', '', h, flags=re.DOTALL))))
kws = ['personuppgiftsansvarig', 'rättslig grund', 'lagringstid', 'rättigheter', 'IMY', 'tredje', 'överföring', 'e-post']
for k in kws:
    print(f'{k}: {k.lower() in text.lower()}')
```

**Risk classification:**

- **Low risk**: No third-party trackers, first-party cookies only, no forms → compliance is mostly about having the pages present
- **Medium risk**: Analytics with consent gating, auth/login collecting email + name
- **High risk**: Third-party trackers, payment processing, cross-border data transfer, children's data → legal review required

### Phase 6: Submit to Google Search Console (optional, via CDP)

If the user wants to submit the sitemap to Google Search Console using their already-logged-in Chrome:

1. Ensure Chrome is running with `--remote-debugging-port=9222`
2. Connect via Playwright `connectOverCDP`
3. Navigate to the Sitemaps page
4. Fill the sitemap input with the **full URL** (e.g. `https://example.com/sitemap.xml`, not just `sitemap.xml`)
5. Click the Submit button (Material Design `div.U26fgk.O0WRkf`, not a native `<button>`)
6. Verify the sitemap appears in the list with status "Success"

```js
import { chromium } from 'playwright'
const browser = await chromium.connectOverCDP('http://127.0.0.1:9222')
const ctx = browser.contexts()[0]
const page = await ctx.newPage()
await page.goto('https://search.google.com/search-console/sitemaps?resource_id=sc-domain:example.com', { waitUntil: 'networkidle' })
await page.waitForTimeout(3000)
await page.locator('input[aria-label="Enter sitemap URL"]').fill('https://example.com/sitemap.xml')
await page.locator('div.U26fgb.O0WRkf').filter({ hasText: 'Submit' }).first().click()
await page.waitForTimeout(5000)
// Verify: look for "Success" in the sitemap table row
```

**Gotcha:** For `sc-domain:` properties, the sitemap URL must be the full HTTPS URL, not a relative path. Relative paths like `sitemap.xml` will return "Invalid sitemap address".

### Phase 7: Generate report

Output a structured report with:

1. **Summary table** — dimension × status (Pass/Fail/Warning)
2. **Findings** — each issue with severity, evidence, and fix
3. **Remediation checklist** — actionable items, ordered by severity
4. **Compliance disclaimer** — "This audit is not legal advice. High-risk businesses should have final materials reviewed by qualified counsel."

## Severity levels

| Level | Meaning | Action |
|-------|---------|--------|
| 🔴 Critical | Breaks indexing, leaks wrong locale, or violates GDPR | Fix before launch |
| 🟠 High | Misses SEO/AEO opportunity or compliance gap | Fix before launch |
| 🟡 Medium | Suboptimal but not breaking | Fix after launch |
| 🟢 Low | Cosmetic or future improvement | Backlog |

## Common failure patterns (from real audits)

1. **SV page serves EN meta** — `nuxt.config.ts` hardcodes English title/description; the SV page (default locale) serves English to Google.se
2. **EN page has `lang="sv"`** — `app.head.htmlAttrs.lang` hardcoded in shared config; `useLocaleHead()` not used
3. **No canonical URLs** — `i18n.baseUrl` not set; `useLocaleHead()` can't generate them
4. **No hreflang alternates** — same cause as above; Google can't associate locale variants
5. **og:image points to staging** — default config leaked from dev environment
6. **Zero structured data** — no JSON-LD at all; AI search engines have no structured signal
7. **Inherited auth pages indexable** — `/login`, `/register` from shared app layer not disallowed in robots.txt
8. **No sitemap.xml** — static sitemap not created; Google has to discover URLs by crawling
9. **Privacy policy missing GDPR Art. 13 elements** — controller identity, legal basis, retention period, IMY complaints right not mentioned
10. **Sitemap submitted as relative path** — Google Search Console rejects `sitemap.xml`; needs full `https://example.com/sitemap.xml`

## Tools used

- `curl` — fetch live HTML and check HTTP status
- `python3` with `re` — parse HTML meta tags and JSON-LD
- `playwright` (optional) — submit sitemap to Google Search Console via CDP
- `gh` CLI (optional) — create follow-up issues for remediation items

## Disclaimer

This audit provides technical SEO checking, structured data validation, and compliance issue-spotting only. It is not legal advice. High-risk, regulated, or cross-border businesses should have final compliance materials reviewed by qualified counsel.
