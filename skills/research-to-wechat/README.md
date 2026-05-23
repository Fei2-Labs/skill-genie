# Research to WeChat
<!-- // TODO: split README.md into smaller modules/components -->

Turn a topic, notes, article, URL, or transcript into a research-backed WeChat article with an evidence ledger, routed structure, polished Markdown, inline visuals, cover art, native HTML output, a saved draft, and optional multi-platform distribution.

## Install

**OpenClaw / ClawHub:**
```bash
clawhub install research-to-wechat
```

**Manual:**
```bash
curl -fsSL https://raw.githubusercontent.com/Fei2-Labs/skill-genie/main/research-to-wechat/scripts/install-openclaw.sh | bash
```

**Optional runtime integrations:**
- Pencil MCP server for article design templates from `design.pen`
- Official WeChat credentials for draft delivery: `WECHAT_APPID`, `WECHAT_SECRET`
- Optional draft update target: `WECHAT_DRAFT_MEDIA_ID`

## Design Runtime

`render` now reads `design.pen` directly and compiles it into an agent-readable
design catalog before HTML generation. The renderer uses the selected profile's
background, typography, accent, surface, border, and hero treatment instead of
only switching between fixed light and dark palettes.

Inspect the compiled catalog:

```bash
python3 scripts/wechat_delivery.py design-catalog \
  --output references/design-catalog.json
```

Render with design-driven HTML:

```bash
python3 scripts/wechat_delivery.py render article-formatted.md \
  -o article.html \
  --design-pen design.pen \
  --color-mode dark
```

## What this skill is

`research-to-wechat` is a native, research-first article system for WeChat production.
It no longer routes execution to external skills. Research, normalization, visual planning, HTML rendering, image upload, and draft save are all described and executed inside this skill.

The main contract stays stable from source packet to draft:
`source.md -> brief.md -> research.md -> article.md -> article-formatted.md -> article.html -> manifest.json`

## Who this is for

- Writers who start from a topic and want a complete “research to draft” workflow
- Operators who need a repeatable WeChat article pipeline with traceable evidence
- Creators who publish to WeChat Official Accounts and optionally cross-post to other platforms
- Agents that need one consistent output contract across different source types

## What it produces

For every run, the skill creates one workspace:
`research-to-wechat/YYYY-MM-DD-<slug>/`

Expected files:
- `source.md`
- `brief.md`
- `research.md`
- `article.md`
- `article-formatted.md`
- `article.html`
- `manifest.json`
- `imgs/cover.png`
- inline image files referenced by the article body

The final Markdown must include these frontmatter keys:
- `title`
- `author`
- `description`
- `digest`
- `coverImage`
- `styleMode`
- `sourceType`
- `structureFrame`
- `disclosure`

`manifest.json.outputs.wechat` keeps the same public contract:
- `markdown`
- `html`
- `cover_image`
- `title`
- `author`
- `digest`
- `images`

## Two operating paths

### Path A: research-first article
Use this when the user starts from:
- a topic
- a question
- notes or outline fragments
- a transcript
- a subtitle file

### Path B: source-to-WeChat edition
Use this when the user starts from:
- article text
- markdown
- article URL
- WeChat URL

In Path B, the workflow preserves the useful source core first, then rebuilds it for WeChat readability, visuals, digest, and draft delivery.

## Supported inputs

- keyword, topic phrase, or question
- notes or raw material dump
- raw article text
- markdown file
- PDF paper, report, or whitepaper
- article URL
- WeChat article URL
- video URL
- full transcript
- subtitle file that can be expanded into a full transcript

Special handling:
- WeChat article URLs are fetched with `scripts/fetch_wechat_article.py`
- PDF sources must preserve figures, charts, tables, and diagrams as reusable assets
- video workflows block until the full transcript is available

## Core workflow

1. Route the request into `Path A` or `Path B`
2. Reduce the source into `source.md`
3. Create `brief.md` with reader, thesis, frame, digest angle, and must-keep material
4. Build the research architecture and evidence ledger in `research.md`
5. Draft the canonical article and apply the normalization checklist
6. Polish the Markdown, plan visuals, generate cover art, and optionally apply `design.pen`
7. Render native WeChat-compatible HTML, upload images when needed, save a draft, and write `manifest.json`
8. *(optional)* Generate and distribute multi-platform content

Phase 8 runs only when the user explicitly requests it.

Delivery ladder:
- `L0 official-http`
- `L1 assisted-browser`
- `L2 manual-handoff`

## Native delivery commands

Check delivery readiness:
```bash
python3 scripts/wechat_delivery.py check
```

Render `article-formatted.md` to WeChat HTML:
```bash
python3 scripts/wechat_delivery.py render article-formatted.md -o article.html
```

Upload local images to WeChat CDN:
```bash
python3 scripts/wechat_delivery.py upload-images imgs/cover.png imgs/inline-01.png --appid "$WECHAT_APPID" --secret "$WECHAT_SECRET" --output upload-map.json
```

Save a draft:
```bash
python3 scripts/wechat_delivery.py save-draft --html article.html --markdown article-formatted.md --appid "$WECHAT_APPID" --secret "$WECHAT_SECRET"
```

Update an existing draft:
```bash
python3 scripts/wechat_delivery.py save-draft --html article.html --markdown article-formatted.md --appid "$WECHAT_APPID" --secret "$WECHAT_SECRET" --media-id "$WECHAT_DRAFT_MEDIA_ID"
```

Native delivery guarantees:
- inline styles only
- no `<div>`
- no flexbox or grid
- explicit dark backgrounds when `dark` mode is used
- title, author, digest, cover, and image paths stay aligned with Markdown
- inline article images use official `media/uploadimg`
- cover images are uploaded as permanent media before `draft/add` or `draft/update`
- WeChat content cannot contain clickable hyperlinks; `render` writes `[text](url)` as `text (url)` and leaves reference URLs plain text.

## Writing frameworks

The skill routes by structure frame:
- `deep-analysis` for thesis-led essays and strategic topics
- `tutorial` for tools and workflows
- `newsletter` for multi-topic roundups
- `case-study` and `commentary` when the material clearly asks for them

Preset modes:
- `deep-analysis`
- `explainer`
- `tutorial`
- `case-study`
- `commentary`
- `narrative`
- `trend-report`
- `founder-letter`
- `newsletter`

Style rendering is determined by:
- explicit user instruction
- `styleMode`
- `structureFrame`
- optional design selection from `design.pen`
- light or dark output mode

## Article design

The skill includes `design.pen` with 10 article layout styles and 6 CTA templates.
When Pencil MCP is configured, the skill can:
- open the design file
- auto-select a layout by article topic and frame
- populate the template with article content
- verify the result by screenshot

If Pencil MCP is unavailable, the skill stays in the native renderer and chooses light or dark mode directly.

## Example requests

- “围绕 AI Agent 安全，写一篇深度分析文章，最后生成公众号草稿”
- “把这篇文章链接做成公众号版本，用 newsletter 风格”
- “把这篇公众号链接改写成更适合微信阅读的版本，保留原始论点，但补齐研究背景”
- “根据这个视频字幕写成 founder-letter 风格文章，并配图”
- “写完公众号后，帮我转小红书和即刻”
- “这篇文章用商务风格排版”
- “用科技风格 Dark 模式排版这篇 AI 文章”

## 中文说明

这是一个原生执行的公众号文章 skill。
你给它选题、问题、笔记、文章链接、公众号链接或视频转录，它会把流程收敛成统一产物：
`source.md -> brief.md -> research.md -> article.md -> article-formatted.md -> article.html -> manifest.json`

核心变化：
- 不再依赖外部 skill 做 HTML 转换或草稿保存
- Markdown 仍然是主资产
- 研究资产和证据边界先于排版
- 结构框架按素材类型路由
- 配图和封面服务于理解，不只是装饰
- 原生 WeChat 交付脚本负责 HTML 渲染、图片上传和草稿保存
- 最终只保存草稿，不直接发布
