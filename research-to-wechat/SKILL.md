---
name: research-to-wechat
description: A native research-first pipeline that turns a topic, notes, article, URL, or transcript into a sourced article with an evidence ledger, polished Markdown, inline visuals, cover image, WeChat-ready HTML, browser/API-ready draft assets, and optional multi-platform distribution. Use when the user wants 深度研究、改写成公众号、写作、排版、配图、HTML 转换、公众号草稿生成、多平台分发.
metadata:
  openclaw:
    emoji: "🔬"
    homepage: "https://github.com/Fei2-Labs/skill-genie"
    requires:
      anyBins: ["python3"]
    primaryEnv: "WECHAT_APPID"
  version: "0.5.2"
  category: "content-generation"
  author: "Skill Genie"
  license: "MIT"
---

# Research to WeChat
<!-- // TODO: split SKILL.md into smaller modules/components -->

Use this skill as a native, research-first article system. It does not route execution to external skills.

## Core Rules

- Match the user's language.
- Ask one question at a time.
- Ask only when the answer changes source interpretation, structure frame, style fidelity, or draft delivery behavior.
- Keep Markdown as the canonical article asset until the HTML handoff.
- Save a draft only. Never publish live.
- Separate verified fact, working inference, and open question.
- Every major claim must be traceable to a source.
- Every article must end with a "## 参考链接" or "## References" section listing all sources.
- Apply the full normalization checklist before HTML rendering.
- Every inline image must pass a two-tier evaluation: eliminate defects first, then verify content match.
- the renderer converts `[text](url)` into `text (url)` because WeChat forbids clickable links.
- Never pretend the workflow did interviews, long field research, team debate, or hands-on testing when it did not.
- Prefer visible disclosure of AI assistance and source scope.
- Treat source capture as a runtime boundary: preserve title, author, description, body text, and image list before rewriting.

## Operating Paths

- `Path A: research-first article`
  use for: topic, keyword, question, notes, transcript, subtitle file
  goal: build the article from a research brief and evidence ledger

- `Path B: source-to-WeChat edition`
  use for: article text, markdown file, article URL, WeChat URL
  goal: preserve the useful source core, then rebuild it for WeChat reading and distribution

Default routing:
- procedural or tool-teaching material -> `tutorial`
- thesis, trend, strategy, critique, case material -> `deep-analysis`
- multi-topic roundup -> `newsletter`

## Accepted Inputs

- keyword, topic phrase, or question
- notes, outline, or raw material dump
- article text
- markdown file
- PDF paper, report, or whitepaper
- article URL
- WeChat article URL
- video URL
- full transcript
- subtitle file that can be expanded into a full transcript

PDF policy:
- extract all figures, charts, tables, and diagrams as image assets
- save extracted figures to `imgs/source-fig-*.png`
- record captions and page numbers in `source.md`
- prefer source figures over generated visuals when they support the claim

Video policy:
- a video source is valid only when the workflow can obtain the full spoken transcript
- first attempt transcript recovery from the page, captions, or subtitle assets
- if no full transcript is obtainable, ask for the transcript or subtitle file and wait

## Output

Create one workspace per article:
`research-to-wechat/YYYY-MM-DD-<slug>/`

Required assets:
- `source.md`
- `brief.md`
- `research.md`
- `article.md`
- `article-formatted.md`
- `article.html`
- `manifest.json`
- `imgs/cover.png`
- inline illustration files referenced by the markdown body

Required frontmatter in final markdown:
- `title`
- `author`
- `description`
- `digest`
- `coverImage`
- `styleMode`
- `sourceType`
- `structureFrame`
- `disclosure`

`manifest.json` must capture:
- `pathMode`
- `styleMode`
- `structureFrame`
- `sourceType`
- `confidence`
- `draftStatus`
- output paths

`manifest.json.outputs.wechat` must include:
- `markdown`
- `html`
- `cover_image`
- `title`
- `author`
- `digest`
- `images`

## Script Directory

Determine this SKILL.md directory as `SKILL_DIR`, then use `${SKILL_DIR}/scripts/<name>`.

| Script | Purpose |
|--------|---------|
| `scripts/fetch_wechat_article.py` | WeChat article fetch (mobile UA) |
| `scripts/wechat_delivery.py` | Native WeChat delivery entrypoint (`check`, `design-catalog`, `render`, `upload-images`, `save-draft`) |
| `scripts/install-openclaw.sh` | OpenClaw skill installer |

## Native Capability Contract

This skill executes every stage itself:
- source ingest via bundled fetch script, browser tools, and PDF inspection
- markdown polish via normalization rules in this skill
- inline visual planning and cover direction via native article analysis
- design catalog compile via `python3 "${SKILL_DIR}/scripts/wechat_delivery.py" design-catalog`
- WeChat HTML rendering via `python3 "${SKILL_DIR}/scripts/wechat_delivery.py" render`
- image upload via `python3 "${SKILL_DIR}/scripts/wechat_delivery.py" upload-images`
- draft save via `python3 "${SKILL_DIR}/scripts/wechat_delivery.py" save-draft`
- multi-platform distribution via native browser/API steps when Phase 8 is requested

Use the internal contract in [capability-map.md](references/capability-map.md).

## Delivery Ladder

Resolve WeChat draft delivery in this order:
1. `L0 official-http`: `WECHAT_APPID` and `WECHAT_SECRET` are ready, so bundled scripts call the official media and draft APIs directly
2. `L1 assisted-browser`: only use a browser when the account setup or draft inspection needs human help
3. `L2 manual-handoff`: stop with exact file paths and required API fields when official delivery cannot proceed


## Author Config (EXTEND.md)

The renderer reads an optional `EXTEND.md` for author-specific CTA content and preferences. This keeps the skill generic — CTA text, QR codes, and blog URLs belong to the author, not the skill.

Lookup order: project dir → `~/.config/research-to-wechat/` → `~/.research-to-wechat/`

See [author-config.md](references/author-config.md) for the full format and field reference.

When `EXTEND.md` is present with a `cta` section, the renderer appends a styled CTA block after the article body. When absent, no CTA is rendered.

## Style Resolution

Resolve style in this order:
1. explicit user instruction
2. preset mode
3. author mode
4. custom brief

Use the full style system in [style-engine.md](references/style-engine.md).

Visual rendering is decided by:
- `styleMode`
- `structureFrame`
- `light` or `dark` output mode

## Execution

Run the article through these phases:
1. intake and route selection
2. source packet, brief, and strategic clarification
3. research architecture with structured question lattice
4. research merge and evidence ledger
5. frame-routed master draft with normalization checklist, writing self-check, and **machine-verified Chinese de-AI scan** (Phase 5 must not proceed without running these):
   ```bash
   # negation-contrast patterns (must be 0 hits)
   grep -n '不是.*而是\|不仅.*而且\|不只.*更\|不再.*而是\|已经不是' article-formatted.md
   # em-dash count (≤5 in body)
   grep -c '——' article-formatted.md
   # exclamation marks (must be 0)
   grep -c '！' article-formatted.md
   ```
6. **微信敏感词合规检查**（⛔ 必须通过才能继续）：用 `wechat-compliance-check` 扫描 `article-formatted.md`，有命中则改写后重新扫描，直到零违规。
7. refinement, visual strategy, and image evaluation
8. native WeChat HTML rendering via `wechat_delivery.py render`, image upload, draft save, and manifest.

   **Image upload rules:**
   - If `imgs/cdn-urls.json` already exists from a previous upload, **skip re-uploading unchanged images**. Only upload new or modified files (compare filename + file size/mtime).
   - `wechatqr.png` (CTA QR code) must reuse the existing CDN URL from project-level `images/wechatqr.png` or a previous `cdn-urls.json`. Never re-upload the same QR code per article.
   - After upload, always merge new CDN URLs into the existing `cdn-urls.json` (not overwrite).

   **Draft save rules:**
   - If `manifest.json` already contains a `media_id`, pass `--media-id` to `save-draft` to **update the existing draft**. Never create a duplicate.
   - If a duplicate draft was accidentally created, delete it via API (`draft/delete`) immediately and keep only the original `media_id`.
   - `manifest.json` is the single source of truth for `media_id`.

   **Before draft save, run HTML compliance check** (must all pass):
   ```bash
   grep -c 'class=' article.html          # must be 0
   grep -c '<style' article.html          # must be 0
   grep -c '<a href' article.html         # must be 0
   # outermost <section> must have background
   python3 -c "import re;h=open('article.html').read();m=re.search(r'<section[^>]*>',h);print('OK' if m and 'background' in m.group() else 'FAIL')"
   ```
9. optional multi-platform content generation and distribution

Phase 9 only executes when the user explicitly requests it.

Use the execution contract in [execution-contract.md](references/execution-contract.md).
Use the platform copy specs in [platform-copy.md](references/platform-copy.md) for Phase 8.

## Done Condition

The skill is complete only when all of these hold:
- the article reads as researched before it reads as polished
- the route choice and structure frame fit the source instead of forcing one house style
- the chosen style is visible without collapsing into imitation
- the writing framework self-check for the chosen frame has been applied
- the evidence ledger clearly separates fact from interpretation
- every visual adds narrative or explanatory value
- the normalization checklist has been applied: no citation artifacts, no LaTeX, no broken tables, no scraped UI remnants
- every image placeholder was evaluated against placement criteria before generation
- every generated or selected image passed the two-tier quality check
- markdown and HTML agree on title, summary, cover, and image paths
- HTML contains zero `class=` attributes, zero `<style>` tags, zero `<a href>` links, and outermost `<section>` has explicit `background`
- `manifest.json` agrees with the actual output set and draft state
- the article does not overclaim research effort or authorship
- `wechat-compliance-check` returned zero violations on the final markdown
- the workflow can stop safely at the highest-quality completed artifact if a later handoff fails
- if Phase 8 was triggered, platform copies follow [platform-copy.md](references/platform-copy.md) and manifest includes their output entries
