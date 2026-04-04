# WeChat HTML Compatibility Reference

Practical constraints and official API details for publishing to WeChat Official Accounts.
Aligned with the official server-side draft and media interfaces.

## Scope Split

The official WeChat H5 dark mode guide applies to standalone pages rendered by
the WeChat in-app browser. It recommends:
Reference: https://developers.weixin.qq.com/doc/subscription/guide/h5/darkmode.html

- declaring `color-scheme` via `<meta name="color-scheme" content="light dark">`
  or `:root { color-scheme: light dark; }`
- using `@media (prefers-color-scheme: dark)` to switch colors
- managing larger palettes with CSS variables
- swapping images with `<picture><source media="(prefers-color-scheme: dark)">`
- using `matchMedia('(prefers-color-scheme: dark)')` when JavaScript must react
  to theme changes

This skill usually produces Official Account article body HTML, not a generic
standalone H5 page. For article body HTML written into the WeChat editor:

- do not rely on `<style>` blocks, media queries, or `matchMedia()` surviving
  the editor round-trip
- treat dark mode as a precomputed visual variant with inline styles
- use explicit backgrounds on the outer wrapper and key inner containers
- prefer a single dark-safe image asset in final article HTML unless the
  renderer has verified that `<picture>/<source>` survives save + publish

Renderer note:

- the bundled `wechat_delivery.py render` command emits inline styles directly
- the native renderer must still be verified against the rules below
- any browser-assisted fallback must preserve the same HTML contract

## HTML Compatibility Rules

These rules are mandatory for any HTML that will be pasted or written into the
WeChat editor. Violations cause silent style loss or layout breakage.

### 1. All CSS must be inline

The WeChat editor strips `<style>` tags on save. The left-side editor preview
may look correct (the `<style>` block is still in the DOM), but the right-side
phone preview and the published article will lose all styles.

- Every CSS rule must be written as a `style=""` attribute on the element.
- Emit inline styles directly during rendering.
- Verify that no `<style>` block remains in the output.

### 2. Use `<section>` instead of `<div>`

The WeChat editor has inconsistent support for `<div>`. Replace all `<div>`
tags with `<section>` in the final HTML.

### 3. No flexbox or grid

WeChat does not support CSS `display: flex` or `display: grid`.
Use `<table>` for any multi-column layout (price comparisons, stats rows,
side-by-side cards, API parameter tables, etc.).

### 4. Dark theme requires explicit background on outermost wrapper

The WeChat article container has a white background. If dark-themed content
does not set its own `background`, white bleeds through.

- Wrap the entire content in `<section style="background:#0F172A; padding:0; margin:0;">`.
- Also set `background` on inner containers (content-wrap, card containers)
  to prevent white gaps at any nesting level.
- For standalone preview H5 files, also declare `color-scheme` and
  `prefers-color-scheme` handling if system-following dark mode is desired.
- For final editor HTML, resolve the chosen dark palette before upload rather
  than depending on runtime theme switching.

## Inline Image Upload API

### Endpoint

```
POST /cgi-bin/media/uploadimg?access_token={ACCESS_TOKEN}
Content-Type: multipart/form-data
```

The form field name **must** be `media`.

### Success response

```json
{
  "errcode": 0,
  "url": "http://mmecoa.qpic.cn/sz_mmecoa_png/..."
}
```

The returned `url` is the CDN address for use in `<img src="">`.

### Common mistakes

| Mistake | Result |
|---------|--------|
| Wrong endpoint | Upload fails |
| Wrong field name | Upload fails |
| **field name = `media`** | **success** |

## Cover Material Upload API

### Endpoint

```
POST /cgi-bin/material/add_material?access_token={ACCESS_TOKEN}&type=image
Content-Type: multipart/form-data
```

This endpoint returns a permanent `media_id` for the cover and an image URL.
Use the returned `media_id` as `thumb_media_id` in the draft request.

## Draft Save APIs

Use the official draft box APIs. Create and update are separate endpoints.

### Create draft

### Endpoint

```
POST /cgi-bin/draft/add?access_token={ACCESS_TOKEN}
Content-Type: application/json
```

### Required parameters

```
articles[0].title = Article title
articles[0].content = HTML body (inline styles only)
articles[0].thumb_media_id = Permanent media ID from cover upload
articles[0].digest = Summary
articles[0].author = Author
articles[0].content_source_url = Original URL (optional)
```

### Update draft endpoint

```
POST /cgi-bin/draft/update?access_token={ACCESS_TOKEN}
Content-Type: application/json
```

Additional required fields:

```
media_id = Existing draft media ID
index = 0
articles = Single article object
```

### Common mistakes

| Mistake | Result |
|---------|--------|
| External image URLs in article content | WeChat filters them |
| Missing `thumb_media_id` | Draft add/update fails |
| Sending form-encoded payloads to draft APIs | API rejects the request |
| Using editor-only fields like `AppMsgId` | Wrong API family |

## CDP Image Upload Workflow

When a browser fallback is needed for inspection or assisted recovery:

1. Read the image file as base64.
2. Inject the base64 string into `window.__img` via `Runtime.evaluate`.
   For large files, split into chunks of ≤ 500 KB each.
3. Use the browser session only for inspection or recovery, not as the primary delivery path.

**Why not fetch from a local HTTP server?**
Even with `Page.setBypassCSP(true)`, CORS still blocks cross-origin fetch.
CSP and CORS are two independent mechanisms — bypassing one does not affect
the other. Injecting base64 data directly via CDP avoids both.

## Error Quick Reference

| Symptom | Cause | Fix |
|---------|-------|-----|
| Editor left panel has dark theme, phone preview is white | `<style>` tags stripped | Emit inline styles only |
| Dark theme but white gaps between sections | Outermost wrapper has no `background` | Add `<section style="background:...">` wrapper |
| Standalone preview follows system dark mode, published article does not | Editor HTML is not a full H5 runtime | Precompute the dark palette and inline it before upload |
| Article body images disappear after save | External image URLs were used | Upload body images via `/cgi-bin/media/uploadimg` first |
| Cover image missing | No permanent cover media ID | Upload cover via `/cgi-bin/material/add_material` |
| Draft update fails | Missing `media_id` or wrong payload shape | Use `/cgi-bin/draft/update` with `media_id`, `index`, and `articles` |
| Fetch local image gets `Failed to fetch` | CORS blocking | Don't fetch localhost; inject base64 via CDP |
| CSP bypass but fetch still fails | CSP ≠ CORS | Use CDP base64 injection |

## Dependencies

WeChat disallows clickable hyperlinks in editor HTML, so the renderer turns `[text](url)` into plain `text (url)` and relies on explicit URLs in the reference section.

For official API delivery:

- `WECHAT_APPID`
- `WECHAT_SECRET`
- the bundled native renderer and delivery scripts
