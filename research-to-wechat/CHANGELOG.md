# Changelog

All notable changes to `research-to-wechat` will be documented in this file.

## 0.4.0 - 2026-03-04

### Added

- **Writing frameworks**: deep-analysis 四幕式框架 (序言+01/02/03/04, 8000-12000字) with sentence rhythm, data density, cross-cultural references, golden sentences, emotional arc, and chapter hooks
- **Writing frameworks**: tutorial 六段式框架 (先看结果→概念→操作→实战→拿走即用→升华, 2000-4000字) with result-first rule, visual rhythm specs, and operation step format
- **Writing checklists**: per-frame self-check lists (deep-analysis: 12 items, tutorial: 11 items)
- **Writing prohibitions**: language and content prohibitions merged from both frameworks
- **HTML converter**: md2wechat skill (Go binary, ai mode with Claude-powered HTML generation, no external API)
- **Article design templates**: `design.pen` with 10 layout styles (极简/编辑/杂志/科技/生活/典雅/粗犷/活泼/商务/艺术), each with Light/Dark variants, plus 6 CTA templates
- **Design auto-selection**: automatic design matching based on article topic and structure frame (requires Pencil MCP)
- **Design guide**: new `references/design-guide.md` with selection rules, node ID table, CTA matching, and Pencil MCP workflow
- **Cover spec**: 900x383px primary at 2x, 200x200px center-cropped thumbnail, HTML template → PNG download workflow
- **Phase 7 multi-platform distribution** (optional): xiaohongshu carousel, jike post, xiaoyuzhou podcast script, wechat moments copy
- **Platform copy specs**: new `references/platform-copy.md` with per-platform writing rules
- **WeChat article fetch script**: `scripts/fetch_wechat_article.py` (Python, mobile WeChat UA, 30s timeout)
- **multi-platform-distribute capability alias**: Chrome CDP sequential execution, independent profiles, L0-L3 fallback
- **OpenClaw compatibility**: metadata block in SKILL.md frontmatter (emoji, homepage, requires, primaryEnv, version, category)
- **OpenClaw install script**: `scripts/install-openclaw.sh` for `~/.openclaw/skills/` installation

### Updated

- style-engine.md: Structure Router deep-analysis and tutorial entries expanded from one-line summaries to full writing methodology
- execution-contract.md: Phase 5 cover generation detailed with dimensions and HTML template workflow
- execution-contract.md: Phase 5 now includes article design selection step with auto-selection table and Pencil MCP workflow
- execution-contract.md: Phase 6 HTML rendering updated with converter selection order and fallback logic
- execution-contract.md: manifest.json format expanded to support optional multi-platform output fields
- capability-map.md: source-ingest now includes bundled fetch_wechat_article.py as primary WeChat fetch tool
- capability-map.md: wechat-render now references md2wechat Go skill
- capability-map.md: wechat-draft updated with md2wechat's built-in `--draft` API support
- capability-map.md: cover-art now specifies 900x383px dimensions and 2x export
- capability-map.md: new article-design alias with Pencil MCP prerequisite and auto-selection rules
- SKILL.md: 8-phase pipeline (Phase 8 optional), article-design alias, design-guide reference, updated done conditions
- README.md: article design section with topic-to-design table, Pencil MCP setup instructions, OpenClaw install section, Chinese section updated
- docs/EXAMPLES.md: design selection examples, updated output checklist
- docs/GITHUB_RELEASE.md: design-guide.md and design.pen in required files, design review question added

## 0.3.0 - 2026-03-03

### Added

- Strategic clarification protocol: five-dimension check (goal, audience, core points, style, boundaries) before research begins
- Structured question lattice: 32+ questions across 4 cognitive layers with Feynman technique and first-principles grounding
- Structured research brief format: each brief requires topic, purpose, audience, key_points, framework, and expected_depth
- Full article normalization checklist (12+ rules): citation cleanup, invisible character repair, math-to-text conversion, table standardization, heading hierarchy, content integrity
- Image placeholder strategy: placement criteria, 6 article-type image classifications (entity, abstract, process, narrative, data, hybrid), keyword construction discipline
- Two-tier image evaluation: Tier A elimination (watermarks, low quality, off-topic) and Tier B content matching (subject match, style consistency, information value)
- Article Normalization compact reference section in style-engine.md

### Updated

- Phase 2 research architecture expanded with strategic clarification, structured brief format, and detailed question lattice
- Phase 4 normalization rules replaced with detailed 12+ rule checklist (was 5 vague bullet points)
- Phase 5 visual layer expanded with image placeholder strategy, keyword construction, global coordination, and two-tier evaluation
- SKILL.md core rules: added normalization enforcement and image evaluation requirements
- SKILL.md phase descriptions: signal research depth, normalization, and visual evaluation
- SKILL.md done conditions: added normalization and image quality verification checks
- inline-visuals capability alias: keyword-based generation, two-tier evaluation, regeneration support
- markdown-polish capability alias: normalization checklist application requirement

## 0.2.0 - 2026-03-03

### Added

- Research-first route model with `Path A` topic-first writing and `Path B` source-to-WeChat rewriting
- Required workspace records: `brief.md`, `research.md`, and `manifest.json`
- Evidence-ledger contract separating verified facts, working inferences, and open questions
- WeChat delivery ladder covering API draft, automated browser, assisted browser, and manual handoff
- Required `manifest.json.outputs.wechat` field contract for downstream draft workers

### Updated

- Source ingestion rules now preserve title, author, description, body, and image metadata before rewriting
- Tutorial and deep-analysis structure rules now align with the upstream content-pipeline writing frameworks
- Example prompts now reflect route selection, thin-source blocking, disclosure requirements, and manifest output

## 0.1.1 - 2026-03-03

### Fixed

- Replaced machine-specific absolute Dropbox paths in `SKILL.md` reference links with portable relative paths
- Improved cross-machine portability for ClawHub installs

### Updated

- Video ingestion now requires the full transcript before article generation can begin
- Metadata, description, chapters, or summary are now treated as supporting context only for video sources

## 0.1.0 - 2026-03-03

### Added

- Initial `research-to-wechat` skill for topic-to-draft WeChat article orchestration
- Neutral capability alias layer in `references/capability-map.md`
- Style system in `references/style-engine.md`
- Phase-based execution contract in `references/execution-contract.md`
- Skill-level README for GitHub presentation and onboarding
- Skill-level GitHub release checklist and example prompt set
- Skill-level MIT license

### Updated

- Root repository `README.md` now lists `research-to-wechat` in English, Chinese, and Japanese
