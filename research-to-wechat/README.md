# Research to WeChat

Turn a topic, notes, article, URL, or transcript into a research-backed WeChat article with an evidence ledger, routed structure, polished Markdown, inline visuals, cover art, HTML output, a saved browser draft, and optional multi-platform distribution (小红书、即刻、播客、朋友圈).

## Install

**OpenClaw / ClawHub:**
```bash
clawhub install research-to-wechat
```

**Manual:**
```bash
curl -fsSL https://raw.githubusercontent.com/Fei2-Labs/skill-genie/main/research-to-wechat/scripts/install-openclaw.sh | bash
```

**Optional dependencies:**
- `md2wechat` skill — for HTML rendering (`clawhub install md2wechat` or [install guide](https://github.com/geekjourneyx/md2wechat-skill))
- Pencil MCP server — for article design templates from `design.pen`
- `WECHAT_APPID` / `WECHAT_SECRET` — for draft upload (not needed for research and writing)

## What this skill is

`research-to-wechat` is a research-first control-plane skill for WeChat article production.
It keeps one stable article contract from source packet to WeChat draft, while routing each stage to the right worker.
The key difference from a simple formatter is that this skill treats research assets, evidence limits, and structure choice as first-class outputs.

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

`manifest.json.outputs.wechat`: `markdown`, `html`, `cover_image`, `title`, `author`, `digest`, `images`

Optional multi-platform outputs (when Phase 8 is triggered):
`manifest.json.outputs.xiaohongshu`, `.jike`, `.xiaoyuzhou`, `.moments`

## Two operating paths

### Path A: research-first article
Use this when the user starts from:
- a topic
- a question
- notes or outline fragments
- a transcript
- a subtitle file
The workflow builds:
`source packet -> brief -> research architecture (32+ questions) -> evidence ledger -> article -> WeChat draft`

### Path B: source-to-WeChat edition
Use this when the user starts from:
- article text
- markdown
- article URL
- WeChat URL
The workflow first preserves the useful source core, then rebuilds it for WeChat readability, visuals, digest, and draft delivery.

## Supported inputs

- keyword, topic phrase, or question
- notes or raw material dump
- raw article text
- markdown file
- article URL
- WeChat article URL (fetched via bundled `scripts/fetch_wechat_article.py`)
- video URL
- full transcript
- subtitle file that can be expanded into a full transcript

Video handling rules:
- a video workflow does not start writing until the full transcript is available
- first try to recover transcript text from the page, captions, or subtitle assets
- title, description, chapters, and summary are supporting context only
- if the page has no full transcript, ask for the transcript or subtitle file and wait

## Core workflow

1. Route the request into `Path A` or `Path B`
2. Reduce the source into `source.md`
3. Create `brief.md` with strategic clarification, reader, thesis, frame, digest angle, and must-keep material
4. Build the research architecture: structured question lattice (32+ questions across 4 cognitive layers) and evidence ledger in `research.md`
5. Draft the canonical article with the selected writing framework and apply the normalization checklist
6. Polish the Markdown, add inline visuals (with two-tier quality evaluation), generate cover art, and select article design from `design.pen`
7. Render WeChat-compatible HTML via `md2wechat` skill (ai mode, no external API) and save a draft
8. *(optional)* Generate and distribute multi-platform content (小红书、即刻、小宇宙、朋友圈)

Phase 8 only runs when the user explicitly requests it.

Delivery ladder: `L0 api-draft` -> `L1 automated-browser` -> `L2 assisted-browser` -> `L3 manual-handoff`

## Writing frameworks

The skill uses detailed writing frameworks per structure frame:

- **deep-analysis**: 四幕式框架 (序言 + 01/02/03/04), 8000-12000 字. Story-first opening, sentence rhythm (long-short alternation), data density (one data point per 200-300 words), 5-8 cross-cultural references, 3-5 golden sentences, emotional arc, chapter hooks.
- **tutorial**: 六段式框架 (先看结果→概念→操作→实战→拿走即用→升华), 2000-4000 字. Result-first rule, visual rhythm (tables every 300-500 words, code blocks per step), operation step format with copyable commands.

Each frame has a self-check list and writing prohibitions. See `references/style-engine.md`.

## Research and honesty contract

This skill follows a strict provenance rule:
- separate verified fact, working inference, and open question
- keep enough source traceability to recover major claims
- prefer visible disclosure of AI assistance and source scope
- never fabricate interviews, long research timelines, or firsthand testing
- apply the full normalization checklist: no citation artifacts, no LaTeX, no broken tables, no scraped UI remnants

If the evidence base is thin, the article should narrow its claims instead of sounding more certain.

## Style system

The skill resolves style in this order:
1. explicit user instruction
2. preset mode
3. author mode
4. custom brief

Structure is routed separately:
1. explicit frame request
2. source-type inference
3. preset default

Core frames:
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

Author mode builds a compact author card from representative pieces and emulates cadence, framing, and evidence habits without copying distinctive phrasing.

Custom mode asks for:
- target reader
- tone
- structure preference
- evidence density
- banned expressions

## HTML rendering

The skill converts Markdown to WeChat-compatible HTML via the **md2wechat skill** — Go binary using ai mode (Claude-powered, no external API). Themes: `autumn-warm`, `spring-fresh`, `ocean-calm`, `custom`.

## Article design (requires Pencil MCP)

The skill includes `design.pen` with 10 article layout styles (each in Light/Dark) and 6 CTA templates. When the **Pencil MCP server** is configured, the skill auto-selects a design based on article topic:

| Topic | Design |
|-------|--------|
| AI / tech / programming | 04 科技 |
| Business / strategy | 09 商务 |
| Lifestyle / personal growth | 05 生活 |
| Culture / history | 06 典雅 |
| News / commentary | 02 编辑 |
| Design / creativity | 07 粗犷 |
| Fun / youth | 08 活泼 |
| Art / music / film | 10 艺术 |
| General | 01 极简 |

Users can override by naming a style (e.g., "用杂志排版", "科技风格 Dark 模式").

**Setup**: Add the Pencil MCP server to your Claude Code configuration. If Pencil MCP is not available, design selection is skipped and md2wechat handles styling via its own themes. See `references/design-guide.md` for full details.

## Example requests

- “围绕 AI Agent 安全，写一篇深度分析文章，最后生成公众号草稿”
- “围绕 AI Agent 安全，做 Path A 深度研究，文章里保留证据边界，再生成公众号草稿”
- “把这篇文章链接做成公众号版本，用 newsletter 风格”
- “把这篇公众号链接改写成更适合微信阅读的版本，保留原始论点，但补齐研究背景”
- “根据这个视频字幕写成 founder-letter 风格文章，并配图”
- “模仿某位作者的节奏来写，但不要像在冒充本人”
- “写完公众号后，帮我转小红书和即刻”
- “这篇文章用商务风格排版”
- “用科技风格 Dark 模式排版这篇 AI 文章”

## 中文说明

这是一个”研究资产优先”的公众号文章 skill。
你给它选题、问题、笔记、文章链接、公众号链接或视频转录，它会把流程收敛成统一产物：
`source.md -> brief.md -> research.md -> article.md -> article.html -> 草稿箱`

可选多平台分发：小红书轮播图、即刻文案、小宇宙播客脚本、朋友圈文案。

它适合：
- 从零开始写深度文章的人
- 要把外部素材改造成公众号版本的人
- 需要证据可追溯写作流程的自动化工作流
- 需要一稿多平台分发的创作者

它的核心不是绑死某个下游实现，而是维持统一的文章契约：
- Markdown 始终是主资产
- 研究资产和证据边界先于排版
- 结构框架按素材类型路由，而不是一把梭
- 写作有详细方法论：深度长文四幕式（8000-12000字）、教程六段式（2000-4000字）
- 每篇文章经过规范化清单和写作自检
- 配图和封面服务于理解，不只是装饰
- 排版设计根据文章选题自动选择（需要 Pencil MCP；10 种风格 + 明暗模式）
- HTML 转换用 md2wechat（ai 模式，不调外部 API）
- 诚实标注 AI 参与和证据范围
- 最终只保存草稿，不直接发布

## Acknowledgements

- [content-pipeline](https://github.com/OrangeViolin/content-pipeline) by OrangeViolin — writing frameworks (deep-analysis 四幕式, tutorial 六段式), multi-platform distribution specs, and fetch_wechat_article.py
- [md2wechat-skill](https://github.com/geekjourneyx/md2wechat-skill) by geekjourneyx — Markdown-to-WeChat HTML converter with ai mode themes and draft API integration
- [翔宇工作流](https://xiangyugongzuoliu.com/35-n8n-ai-auto-writing-system-workflow/) — research architecture (structured question lattice, strategic clarification) and article normalization checklist inspired by the n8n AI auto-writing workflow
