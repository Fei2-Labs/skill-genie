# WeChat HTML Compatibility Reference

Practical constraints and API details for publishing to WeChat Official Accounts.
Sourced from production debugging sessions.

## HTML Compatibility Rules

These rules are mandatory for any HTML that will be pasted or written into the
WeChat editor. Violations cause silent style loss or layout breakage.

### 1. All CSS must be inline

The WeChat editor strips `<style>` tags on save. The left-side editor preview
may look correct (the `<style>` block is still in the DOM), but the right-side
phone preview and the published article will lose all styles.

- Every CSS rule must be written as a `style=""` attribute on the element.
- Use `premailer` (Python) or an equivalent CSS inliner as a post-processing
  step before writing HTML to the editor.
- After inlining, verify that no `<style>` block remains in the output.

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

## Image Upload API

### Endpoint

```
POST /cgi-bin/uploadimg2cdn?token={TOKEN}&lang=zh_CN&f=json&ajax=1
Content-Type: multipart/form-data
```

The form field name **must** be `upfile`. Other names (`file`, `imgfile`,
`media`) return `errcode: -1`.

### Success response

```json
{
  "base_resp": {"err_msg": "ok", "ret": 0},
  "errcode": 0,
  "url": "http://mmecoa.qpic.cn/sz_mmecoa_png/..."
}
```

The returned `url` is the CDN address for use in `<img src="">`.

### Common mistakes

| Mistake | Result |
|---------|--------|
| `POST /cgi-bin/filepage?action=upload_material` | `200009 not found` |
| field name = `file` / `imgfile` / `media` | `errcode: -1` |
| **field name = `upfile`** | **success** |

## Draft Save API (operate_appmsg)

### Endpoint

```
POST /cgi-bin/operate_appmsg?sub=update&t=ajax-response&type=77&lang=zh_CN&token={TOKEN}
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
```

### Required parameters

```
AppMsgId = {appmsgid}      ← capital A required
count = 1
data_seq = 0
operate_from = Chrome
isnew = 0
article_type = news
title0 = Article title
content0 = HTML body (inline styles only)
digest0 = Summary
author0 = Author
need_open_comment0 = 1
only_fans_can_comment0 = 0
auto_gen_digest0 = 0
```

### Common mistakes

| Mistake | Result |
|---------|--------|
| `appmsgid` (lowercase a) | `200009 not found` |
| `action=save&sub=update` in query | `200009 not found` |
| **`AppMsgId` (capital A) in body** | **success** |

## CDP Image Upload Workflow

When uploading images via Chrome DevTools Protocol (browser-based draft path):

1. Read the image file as base64.
2. Inject the base64 string into `window.__img` via `Runtime.evaluate`.
   For large files, split into chunks of ≤ 500 KB each.
3. In the page context: `atob()` → `Uint8Array` → `Blob` → `FormData`.
4. `fetch('/cgi-bin/uploadimg2cdn?token=...', { method: 'POST', body: fd })`.
5. Collect the returned CDN URL.

**Why not fetch from a local HTTP server?**
Even with `Page.setBypassCSP(true)`, CORS still blocks cross-origin fetch.
CSP and CORS are two independent mechanisms — bypassing one does not affect
the other. Injecting base64 data directly via CDP avoids both.

## Error Quick Reference

| Symptom | Cause | Fix |
|---------|-------|-----|
| Editor left panel has dark theme, phone preview is white | `<style>` tags stripped | Inline all CSS with premailer |
| Dark theme but white gaps between sections | Outermost wrapper has no `background` | Add `<section style="background:...">` wrapper |
| Image upload returns `200009 not found` | Wrong endpoint | Use `/cgi-bin/uploadimg2cdn` |
| Image upload returns `errcode: -1` | Wrong field name | Use `upfile` |
| `operate_appmsg` returns `200009` | Parameter case wrong | Use `AppMsgId` (capital A) |
| Fetch local image gets `Failed to fetch` | CORS blocking | Don't fetch localhost; inject base64 via CDP |
| CSP bypass but fetch still fails | CSP ≠ CORS | Use CDP base64 injection |

## Dependencies

For browser-based draft workflows that need CSS inlining:

- `premailer` (Python): CSS → inline style conversion
- `websockets` (Python): CDP communication

Install: `pip3 install premailer websockets`
