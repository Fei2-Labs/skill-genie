---
name: research-to-wechat
description: A research-first content pipeline that turns a topic, notes, article, URL, or transcript into a sourced article with an evidence ledger, routed structure, polished Markdown, inline visuals, cover image, WeChat-ready HTML, browser-saved draft, and optional multi-platform distribution (小红书、即刻、播客、朋友圈). Use when the user wants 深度研究、改写成公众号、写作、排版、配图、HTML 转换、公众号草稿生成、多平台分发.
metadata:
  openclaw:
    emoji: "🔬"
    homepage: "https://github.com/Fei2-Labs/skill-genie"
    requires:
      anyBins: ["python3"]
    primaryEnv: "WECHAT_APPID"
  version: "0.4.2"
  category: "content-generation"
  author: "Skill Genie"
  license: "MIT"
---

# Research to WeChat

Use this skill as a research-first control plane. Do not duplicate downstream skill wording.

## Core Rules

- Match the user's language.
- Ask one question at a time.
- Ask only when the answer changes source interpretation, structural frame, style fidelity, or draft publishing behavior.
- Keep Markdown as the canonical article asset until the HTML handoff.
- Save a draft only. Never publish live.
- Separate verified fact, working inference, and open question.
- Every major claim must be traceable to a source. Collect source URLs during research.
- Every article must end with a "## 参考链接" or "## References" section listing all sources.
- Apply the full normalization checklist to every article before refinement. Source artifacts, broken formatting, and LaTeX fragments must not survive into the final draft.
- Every inline image must pass a two-tier evaluation: first eliminate disqualifying defects, then verify content match to the surrounding text.
- Never pretend the workflow did interviews, long field research, team debate, or hands-on testing when it did not.
- Prefer visible disclosure of AI assistance and source scope. Refuse human-only framing that would misrepresent the process.
- Treat source capture as a runtime boundary: preserve title, author, description, body text, and image list before rewriting.

## Operating Paths

Route the request into one of two paths:

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

## Capability Aliases

Resolve capabilities through internal aliases, not vendor-style names:
- `source-ingest`
- `markdown-polish`
- `inline-visuals`
- `cover-art`
- `article-design`
- `wechat-render`
- `wechat-draft`
- `multi-platform-distribute` (loaded only when Phase 7 is triggered)

Use the current alias map in [capability-map.md](references/capability-map.md).

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
- when the source is a PDF paper or report, extract all figures, charts, tables, and diagrams as image assets
- save extracted figures to `imgs/source-fig-*.png` with captions and page numbers recorded in `source.md`
- source figures carry higher credibility than AI-generated images and must be preferred in the final article

Video policy:
- a video source is valid only when the workflow can obtain the full spoken transcript
- first attempt transcript recovery from the page, captions, or subtitle assets
- if the page exposes only metadata, description, or chapter markers, do not start article generation
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

Required records outside the article:
- `brief.md`
  must capture: target reader, thesis, must-cover points, frame choice, and what cannot be dropped
- `research.md`
  must capture: verified facts, working inferences, open questions, and source notes
- `manifest.json`
  must capture: `pathMode`, `styleMode`, `structureFrame`, `sourceType`, `confidence`, `draftStatus`, and output paths
  `manifest.json.outputs.wechat` must include: `markdown`, `html`, `cover_image`, `title`, `author`, `digest`, and `images`
  optional platform fields (`xiaohongshu`, `jike`, `xiaoyuzhou`, `moments`) are added when Phase 8 runs

## Script Directory

Determine this SKILL.md directory as `SKILL_DIR`, then use `${SKILL_DIR}/scripts/<name>`.

| Script | Purpose |
|--------|---------|
| `scripts/fetch_wechat_article.py` | WeChat article fetch (Python, simulates WeChat mobile UA) |
| `scripts/install-openclaw.sh` | OpenClaw skill installer (copies to `~/.openclaw/skills/`) |

## Provenance Contract

The workflow must keep a compact evidence ledger throughout the run:
- what came from the user
- what came from fetched source material
- what was added as supporting context
- what remains uncertain

Default article disclosure should state:
- what AI did
- what the human provided or reviewed, if known
- what the evidence base was
- what confidence limit remains, if the source packet is thin

## Delivery Ladder

Resolve WeChat draft delivery in this order:
1. API draft when credentials and converter tooling are ready
2. automated browser draft when the worker can drive the editor safely
3. assisted browser draft when login or selectors need user help
4. manual handoff with exact file paths when automation fails

## Style Resolution

Resolve style in this order:
1. explicit user instruction
2. preset mode
3. author mode
4. custom brief

Use the full style system in [style-engine.md](references/style-engine.md).

## Execution

Run the article through these phases:
1. intake and route selection
2. source packet, brief, and strategic clarification
3. research architecture with structured question lattice (32+ questions across 4 cognitive layers)
4. research merge and evidence ledger
5. frame-routed master draft with full normalization checklist and writing framework self-check
6. refinement, image strategy, visual evaluation, and design selection
7. WeChat HTML rendering, draft upload, and manifest
8. (optional) multi-platform content generation and distribution

Phase 8 only executes when the user explicitly requests it (e.g., "多平台分发", "转小红书", "转即刻", "写朋友圈文案", "做播客脚本").

Use the execution contract in [execution-contract.md](references/execution-contract.md).
Use the design guide in [design-guide.md](references/design-guide.md) for article design selection.
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
- every image placeholder was evaluated against placement criteria before generation, and every generated image passed the two-tier quality check
- markdown and HTML agree on title, summary, cover, and image paths
- `manifest.json` agrees with the actual output set and draft state
- the article does not overclaim research effort or authorship
- the workflow can stop safely at the highest-quality completed artifact if a later handoff fails
- if Phase 8 was triggered, platform copies follow [platform-copy.md](references/platform-copy.md) specs and manifest includes their output entries
