# Execution Contract
<!-- // TODO: split execution-contract.md into smaller modules/components -->

## Route Selection

Choose the route before writing:

- `Path A: research-first article`
  use when the user gives a topic, question, notes, transcript, or subtitle file
- `Path B: source-to-WeChat edition`
  use when the user gives article text, markdown, article URL, or WeChat URL

Then choose the structure frame:
- `tutorial` for tools, workflows, and how-to material
- `deep-analysis` for trends, critiques, strategic questions, and thesis-led essays
- `newsletter` only for multi-topic roundup requests

## Phase 1: Source Packet

Convert the raw input into one workable source package in `source.md`.

Blocking rule for video sources:
- do not proceed until the full transcript has been captured
- acceptable inputs are full transcript text, caption text, or a subtitle file
- title, description, chapters, and summary are supporting context only

Blocking rule for PDF sources:
- extract all figures, charts, tables, and diagrams as image assets
- save them as `imgs/source-fig-01.png`, `imgs/source-fig-02.png`, and so on
- record figure label, page number, caption, file path, and supported claim in `source.md`

For WeChat article URLs:
- use `python3 "${SKILL_DIR}/scripts/fetch_wechat_article.py" "<URL>" --json`
- preserve title, author, description, content, and image list before rewriting

For generic URLs:
- use browser tools to capture the same fields
- if the page exposes only metadata and not body text, stop and ask for a readable source

Record:
- source type
- source language
- title or working title
- thesis or central question
- key entities, dates, claims, quotes, and unknowns
- material that must survive into the final article

If the route is `Path B`, also record:
- original structure and useful sections
- what must be preserved verbatim or semantically
- what should be rewritten for WeChat readability

## Phase 2: Brief and Research Architecture

Create `brief.md` before drafting.

Resolve these dimensions before building the brief:
1. research goal
2. target audience
3. core research points
4. language and style
5. topic boundaries

Record resolved dimensions in `brief.md` under `## Clarification Record`.

`brief.md` must declare:
- route choice and why
- target reader
- output language
- target article length
- target digest angle
- structure frame
- must-cover points
- disagreement or uncertainty checks
- source material that cannot be dropped

Build one central research brief and up to five side briefs.

Generate at least 32 questions across four layers:
- `基础层`: definitions and first principles
- `连接层`: structure, taxonomy, actor maps, and comparison dimensions
- `应用层`: methods, workflows, decision frameworks, and failure modes
- `前沿层`: cases, risks, edge conditions, and future implications

## Phase 3: Research Merge and Evidence Ledger

Do the research pass before writing.

Rules:
- use user-provided material as the anchor
- add missing context only where it sharpens the article
- separate verified fact from inference
- keep track of unresolved claims
- do not move to prose until angle, evidence, and structure are aligned

Create `research.md` with:
- `verified facts`
- `working inferences`
- `open questions`

Every claim that goes beyond common knowledge must be traceable to a source.

If a key claim remains unsupported and changes the main thesis, stop and ask for direction instead of smoothing over the gap.

## Phase 4: Frame-Routed Master Draft

Write `article.md` as the first complete article.

Route the draft by frame:
- `deep-analysis`: narrative or scene-led opening, then background, core analysis, case or turn, and synthesis
- `tutorial`: show the result early, then concept, setup, walkthrough, demo, and quick-start takeaway
- `newsletter`: top line first, then short sections with fast transitions

Requirements:
- one H1 at most
- clean H2 and H3 hierarchy
- evidence-rich paragraphs with clear transitions
- 3 to 6 planned visual insertion points
- temporary visual markers written as `![图片X](TBD)` on isolated lines
- frontmatter must include `digest`, `structureFrame`, and `disclosure`

Source attribution rules:
- when the source is a forum post or community discussion, treat it as **topic inspiration only** — write an independent article on the topic, do not narrate the forum event ("某论坛出现了一个帖子")
- never include forum usernames, post numbers, or reply counts in the article body
- absorb community viewpoints into the author's own analysis ("换个角度看", "一个普遍的体感是") instead of quoting anonymous users ("有人说", "一个人的原话是")
- the source URL belongs in the references section only, not in the narrative
- no numbered markdown lists — WeChat wraps them in `<ol>` causing double numbering; use inline text ("第一步...第二步...") or continuous short paragraphs instead
- article must end with `## 参考链接` or `## References`

Apply the normalization checklist before refinement:
- remove citation artifacts
- remove invisible characters
- convert LaTeX and diagrams to plain-language descriptions
- standardize tables
- remove scraped UI remnants
- preserve statistics, named sources, and substantive paragraphs unless they are demonstrably wrong

## Phase 5: Refinement and Visual Layer

Make `article-formatted.md` the canonical article.

Before generating visuals:
- keep placeholders only when they improve comprehension or structure
- prefer extracted source figures when they directly support the surrounding claim
- keep at least 300 words between major visuals unless the article structure truly needs more density

For each approved image position, build:
1. primary keyword
2. one style modifier and one context modifier
3. 2 to 3 alternative search or generation variants

Cover generation requirements:
- primary cover: `imgs/cover.png`, 900x383 px, exported at 2x
- square thumbnail: `imgs/cover-thumb.png`, 200x200 px
- frontmatter `coverImage` must point to `imgs/cover.png`

Image evaluation:
- Tier A reject rules: watermark, baked-in sales text, low resolution, off-topic subject, cultural mismatch
- Tier B match rules: core subject, language consistency, style consistency, and information value

## Phase 6: Article Design

If Pencil MCP is available:
- open `${SKILL_DIR}/design.pen`
- choose a template via [design-guide.md](design-guide.md)
- populate title, author, sections, images, and CTA
- verify via screenshot

If Pencil MCP is unavailable:
- stay in the native HTML renderer
- choose light or dark mode directly from user instruction, `styleMode`, or article topic

## Phase 7: Native WeChat Delivery

### Project AGENTS Compliance (mandatory before any delivery step)

Before rendering or uploading, read the project's `AGENTS.md` (or the file it points to, e.g. `../AGENTS-wechat.md`) and verify the article against every applicable rule. Walk through each section of the project AGENTS file and confirm compliance:

1. Read the project AGENTS file in full
2. For each rule section (Writing Style, HTML Hard Rules, Typography, Image Rules, CTA Rule, Article End Structure, etc.), check the current article/HTML against it
3. Log any violations found
4. Fix all violations before proceeding to render

This step catches project-specific rules that the skill's own checklist may not cover (e.g. project-specific banned words, CTA templates, font requirements, dark mode defaults, typography constraints like no nested lists).

Before delivery, run:
```bash
python3 "${SKILL_DIR}/scripts/wechat_delivery.py" check
```

### Render

Render `article-formatted.md` into `article.html`:
```bash
python3 "${SKILL_DIR}/scripts/wechat_delivery.py" render article-formatted.md -o article.html
```

Optional flags:
- `--design [design-id-or-name]`
- `--color-mode light|dark`
- `--upload-map [json-path]`

The output HTML must satisfy:
- inline CSS only
- no `<div>`
- no flexbox or grid
- explicit dark background on the outer wrapper and key inner containers
- title, author, digest, cover, and inline images aligned with markdown/frontmatter
- reference links section: every `<section>` and `<p>` must have `text-align:left` (WeChat's justify stretches character spacing on short lines)
- no numbered markdown lists (`1.` `2.` etc.) — WeChat wraps them in `<ol>` causing double numbering; use inline text ("第一步...第二步...") instead

### Upload Images

When local images need CDN URLs, upload them with:
```bash
python3 "${SKILL_DIR}/scripts/wechat_delivery.py" upload-images imgs/inline-01.png imgs/inline-02.png --appid "$WECHAT_APPID" --secret "$WECHAT_SECRET" --output upload-map.json
```

Rules:
- endpoint: `/cgi-bin/media/uploadimg`
- multipart field name: `media`
- authentication: official `access_token` from `stable_token`
- returned mapping replaces local paths in the render step
- **upload-map must include ALL images referenced in the HTML**: inline images, cover image (`imgs/cover.png`), and QR code (`wechatqr.png`). Missing any image results in broken local paths in the final HTML.

### Pre-Draft Checklist

Every item must pass before calling `save-draft`. Run checks via terminal, not by memory.

**Content quality:**
```bash
# 1. Banned words (project AGENTS list — paste full BANNED var from project AGENTS)
grep -nE "$BANNED" article-formatted.md || echo "✅ 禁用词通过"

# 2. AI sentence patterns — negation forms (MUST catch ALL variants, not just pairs)
grep -n '不是\|不只\|不再\|而非\|而是' article-formatted.md && echo "❌ 否定句式命中 — 逐条检查，改写为正面陈述" || echo "✅ 否定句式通过"
# Every hit must be reviewed. Acceptable only in direct quotes or factual negation (e.g. "不需要 API").
# Unacceptable: "不是 A，而是 B" / "不是 A 造成的" / headings with 不是 / "而非" / "不再是"
# Rewrite method: say B directly, delete A.

# 3. Dash count (body ≤5)
grep -c '——' article-formatted.md

# 4. Exclamation marks (must be 0)
grep -c '！' article-formatted.md

# 5. WeChat compliance (sensitive words)
# Run wechat-compliance-check skill scan; ALWAYS hits must be fixed, CONTEXT hits need human judgment
```

**HTML integrity:**
```bash
# 6. No class attributes
grep -c 'class=' article.html | xargs -I{} test {} -eq 0 && echo "✅ no class" || echo "❌ class= found"

# 7. No <style> tags
grep -c '<style' article.html | xargs -I{} test {} -eq 0 && echo "✅ no style" || echo "❌ <style> found"

# 8. No <a href> links
grep -c '<a href' article.html | xargs -I{} test {} -eq 0 && echo "✅ no links" || echo "❌ <a href> found"

# 9. Outer section has background
python3 -c "import re;h=open('article.html').read();m=re.search(r'<section[^>]*>',h);print('✅ background' if m and 'background' in m.group() else '❌ outer section missing background')"
```

**Assets:**
```bash
# 10. Cover image exists and is correct size
python3 -c "from PIL import Image;i=Image.open('imgs/cover.png');print(f'✅ cover {i.size}' if i.size==(900,383) else f'❌ cover wrong size: {i.size}')"

# 11. All inline images exist
ls -la imgs/inline-*.png

# 12. Upload map exists and all CDN URLs are populated
python3 -c "import json;m=json.load(open('upload-map.json'));assert all(v.startswith('http') for v in m.values());print(f'✅ {len(m)} images mapped')"

# 13. HTML references CDN URLs, not local paths
grep -c 'imgs/' article.html | xargs -I{} test {} -eq 0 && echo "✅ no local paths" || echo "❌ local image paths remain"

# 14. Upload map includes cover + QR (not just inline images)
python3 -c "import json;m=json.load(open('upload-map.json'));missing=[k for k in ['imgs/cover.png','wechatqr.png'] if k not in m];print('❌ missing: '+str(missing)) if missing else print('✅ cover+QR in map')"

# 15. No bare wechatqr.png in HTML
grep -c '"wechatqr.png"' article.html | xargs -I{} test {} -eq 0 && echo "✅ QR is CDN" || echo "❌ bare wechatqr.png"
```

**WeChat rendering:**
```bash
# 16. Reference links section has text-align:left (prevents justify spacing)
python3 -c "
import re
h=open('article.html').read()
idx=h.find('参考链接')
if idx<0: print('⚠️ no references section')
else:
    after=h[idx:idx+2000]
    p_tags=re.findall(r'<p style=\"([^\"]+)\"',after)
    bad=[i for i,s in enumerate(p_tags) if 'text-align:left' not in s and 'text-align:center' not in s]
    print('❌ refs missing text-align:left on p tags: '+str(bad)) if bad else print('✅ refs left-aligned')
"

# 17. No numbered lists (WeChat renders double numbering)
grep -c '^[0-9]\.' article-formatted.md | xargs -I{} test {} -eq 0 && echo "✅ no numbered lists" || echo "❌ numbered lists found — convert to inline text"

# 18. No forum usernames or specific post references (unless explicitly requested)
grep -cE '@[a-zA-Z]|linux\.do 上 [a-zA-Z]' article-formatted.md | xargs -I{} test {} -eq 0 && echo "✅ no usernames" || echo "❌ forum usernames found"
```

**Draft parameters:**
```bash
# 19. Frontmatter has required fields
python3 -c "
import re
md=open('article-formatted.md').read()
for f in ['title','author','digest','coverImage']:
    assert f in md, f'❌ missing {f}'
print('✅ frontmatter complete')
"

# 20. Cover image will be passed explicitly
# save-draft MUST include --cover-image imgs/cover.png
```

Any failure → fix and re-check before proceeding to save-draft.

**Project AGENTS compliance:**
```bash
# 21. Read project AGENTS file and verify every rule section
# Walk through each section of the project AGENTS.md (or file it references):
#   - File Conventions: directory naming, image location
#   - Default Strategy: dark/light mode, cover generation
#   - Layout & Theme: 375px mobile, CTA matching
#   - Article End Structure: 参考链接 → CTA order
#   - CTA Rule: template text, QR image, blog URL, interactions
#   - HTML Hard Rules: inline style, no class, section nesting, dark bg
#   - Image Rules: upload endpoint, img sizing, QR width
#   - Typography: no title in body, font family, no nested lists, refs text-align:left
#   - Writing Style: hook opening, meta info, transitions, analysis not translation
#   - AI 句式禁令: negation pairs, dash limit, exclamation marks
#   - Workflow step 3: banned words grep, AI pattern grep, compliance check
# Any violation → fix before save-draft.
```

Any failure → fix and re-check before proceeding to save-draft.

### Save Draft

Create or update the draft with:
```bash
python3 "${SKILL_DIR}/scripts/wechat_delivery.py" save-draft --html article.html --markdown article-formatted.md --cover-image imgs/cover.png --appid "$WECHAT_APPID" --secret "$WECHAT_SECRET"
```

To update an existing draft instead of creating a new one:
```bash
python3 "${SKILL_DIR}/scripts/wechat_delivery.py" save-draft --html article.html --markdown article-formatted.md --cover-image imgs/cover.png --appid "$WECHAT_APPID" --secret "$WECHAT_SECRET" --media-id "$WECHAT_DRAFT_MEDIA_ID"
```

`--cover-image` is mandatory. Omitting it results in a draft without a cover.

**Draft replacement rule**: When re-creating a draft (e.g. to fix a missing cover), delete the old draft first via `/cgi-bin/draft/delete` before creating a new one. Never leave duplicate drafts. The `/cgi-bin/draft/update` API does **not** update `thumb_media_id`, so cover fixes always require delete + create.

Rules:
- obtain `access_token` from `https://api.weixin.qq.com/cgi-bin/stable_token`
- upload the cover image with `/cgi-bin/material/add_material`
- create drafts with `/cgi-bin/draft/add`
- update drafts with `/cgi-bin/draft/update` and `media_id`
- default cover upload type is `image`; switch to `thumb` only when the account requires thumbnail-specific constraints
- use `thumb_media_id` from the permanent cover upload
- report `draftStatus` clearly for the manifest

### Delivery Ladder

- `L0 official-http`
  use when `WECHAT_APPID` and `WECHAT_SECRET` are available
- `L1 assisted-browser`
  use only when account setup or draft inspection needs the user
- `L2 manual-handoff`
  stop with exact file paths, required draft fields, and current API error when official delivery fails

Before finishing, write `manifest.json` with:
- route choice
- source type
- style mode
- structure frame
- confidence summary
- draft status
- output file paths

Required manifest shape:
```json
{
  "outputs": {
    "wechat": {
      "markdown": "/abs/path/article-formatted.md",
      "html": "/abs/path/article.html",
      "cover_image": "/abs/path/imgs/cover.png",
      "title": "Article title",
      "author": "Author name",
      "digest": "120-char digest",
      "images": ["/abs/path/imgs/inline-01.png"]
    }
  }
}
```

If rendering or draft upload fails, keep the highest-quality completed artifact set and report the exact stopping point.

## Phase 8: Multi-Platform Distribution

This phase runs only when the user explicitly requests it.

Rules:
- derive platform copy from the canonical article
- follow [platform-copy.md](platform-copy.md)
- execute platforms sequentially to avoid platform state conflicts
- record every generated platform asset in `manifest.json`
