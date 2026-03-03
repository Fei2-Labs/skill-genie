# Capability Map

Use this file to resolve neutral capability aliases to installed skills without hardcoding vendor-style identifiers.

## Resolution Table

- `source-ingest`
  look for: a skill that can fetch a URL and recover the full source text needed for writing
  use for: article URLs, video URLs, login-gated pages, delayed-render pages
  note: for video URLs, prefer a worker that can recover the complete transcript or caption text, not just metadata
  note: for article rewrites, prefer a worker that preserves headline, author, dates, and other source metadata
  note: ideal output fields are `title`, `author`, `description`, `content`, `images`, and source subtype
  note: for WeChat articles, use the bundled fetch script first:
        `python3 "${SKILL_DIR}/scripts/fetch_wechat_article.py" "<URL>" --json`
        (uses mobile WeChat user-agent to bypass anti-scraping; 30-second timeout)
        If the script fails, fall back to a skill-based worker or ask the user to paste the article text.
  note: prefer a worker that supports a wait mode for manual login or delayed loading

- `markdown-polish`
  look for: a skill that cleans markdown, repairs typography, and improves frontmatter and readability
  use for: canonical article cleanup before visuals and HTML rendering
  note: it must preserve disclosure, digest, and structure-sensitive headings
  note: it must apply the normalization checklist: citation tag removal, invisible character cleanup, math-to-text conversion, table standardization, and heading hierarchy validation

- `inline-visuals`
  look for: a skill that analyzes article structure and generates or selects visuals for body sections
  use for: informational or narrative images placed inside the article body
  note: the control plane provides image keywords and placement criteria; the worker generates or searches based on those keywords
  note: each image must pass a two-tier evaluation before acceptance: (A) no watermarks, no baked-in text, no low resolution, no off-topic content; (B) core subject match to the surrounding article text, style consistency with other article images, and information value beyond decoration
  note: prefer a worker that supports keyword-based generation or search, not just random illustration
  note: the worker should support regeneration when an image fails the quality check

- `cover-art`
  look for: a skill that generates an article cover image from text content
  use for: producing `imgs/cover.png` (900x383px primary) and `imgs/cover-thumb.png` (200x200px)
  note: browser-downloadable HTML templates are acceptable internally (html2canvas → PNG download),
        but the final artifact must be resolved PNG paths in the workspace
  note: export at 2x resolution (1800x766 for primary)

- `article-design`
  look for: Pencil MCP server with access to `design.pen` at the skill root directory
  use for: applying a visual layout template to the article based on topic and structure frame
  prerequisite: Pencil MCP server must be configured in the user's Claude Code environment
  resolution:
    1. if Pencil MCP is available: open `design.pen`, auto-select a design based on article topic
       and structure frame using the rules in [design-guide.md](design-guide.md), copy the template,
       populate with article content, and verify via screenshot.
    2. if Pencil MCP is not available: skip design selection and proceed with HTML rendering only.
       md2wechat handles its own styling via themes.
  note: `design.pen` contains 10 article layout styles (Light/Dark each) and 6 CTA templates
  note: auto-selection maps article topics to designs: AI/tech → 04 科技, business → 09 商务,
        lifestyle → 05 生活, culture → 06 典雅, editorial → 02 编辑, general → 01 极简
  note: user can override auto-selection by naming a design (e.g., "用科技风格", "用杂志排版")
  note: see [design-guide.md](design-guide.md) for the full selection table and Pencil MCP operations

- `wechat-render`
  look for: a tool or skill that converts markdown into WeChat-compatible HTML
  use for: rendering the canonical markdown article into `article.html`
  resolution order:
    1. `md2wechat` skill (Go binary, ai mode) — check if the skill is installed (`bash skills/md2wechat/scripts/run.sh` exists).
       `bash skills/md2wechat/scripts/run.sh convert [path] --mode ai --theme [theme] --preview -o [output]`
       With image upload: add `--upload` flag.
       Uses Claude to generate WeChat-compatible HTML with inline CSS — no external API calls.
       Built-in ai themes: `autumn-warm` (emotional/lifestyle), `spring-fresh` (nature/travel),
       `ocean-calm` (technical/business), `custom` (user-defined prompt).
       Default: `--mode ai --theme autumn-warm`.
       Install: `curl -fsSL https://raw.githubusercontent.com/geekjourneyx/md2wechat-skill/main/scripts/install.sh | bash`
       Repo: https://github.com/geekjourneyx/md2wechat-skill
  note: prefer a worker that keeps cover, digest, author, and inline image paths aligned with markdown
  note: prefer a worker that can replace local content images with upload-ready URLs when needed
  note: md2wechat also supports `--upload` to push images to WeChat CDN and `--draft` to create drafts directly

- `wechat-draft`
  look for: a skill that creates a WeChat Official Account draft
  use for: draft creation via API or browser
  resolution order:
    1. `md2wechat` skill — if installed and WeChat credentials are configured (`WECHAT_APPID`, `WECHAT_SECRET`):
       `bash skills/md2wechat/scripts/run.sh convert [path] --mode ai --theme [theme] --upload --draft --cover [cover-path]`
       This converts, uploads images, and creates the draft in one command.
    2. browser-based draft worker — fallback when API credentials are unavailable.
  note: prefer API draft (L0) over browser automation
  note: prefer draft saving rather than live publishing
  note: the worker should expose draft status clearly so `manifest.json` can record it

- `multi-platform-distribute`
  look for: a skill or script that publishes content to multiple platforms via Chrome CDP or API
  use for: distributing generated platform copies to 小红书, 即刻, 小宇宙, etc.
  note: only loaded when the user explicitly requests multi-platform distribution (Phase 7)
  note: reads from `manifest.json` outputs to determine what to publish where
  note: execution order: wechat → xhs → jike → xiaoyuzhou (sequential, avoid Chrome port conflicts)
  note: follows the same L0-L3 fallback ladder as wechat-draft
  note: each platform uses an independent Chrome profile to avoid session conflicts

## Loading Rule

- Do not load every implementation at once.
- Run `openskills list` when resolution is needed.
- Select the worker whose description best matches the alias requirement.
- Keep this skill as the control plane and the resolved skill as the worker.
