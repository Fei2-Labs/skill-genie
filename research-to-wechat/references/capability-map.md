# Internal Capability Contract

Use this file to keep `research-to-wechat` native. Do not resolve external skills from here.

## Native Stages

- `source-ingest`
  use for: article URLs, video URLs, login-gated pages, delayed-render pages, PDF papers
  execution:
  - for WeChat URLs, run `python3 "${SKILL_DIR}/scripts/fetch_wechat_article.py" "<URL>" --json`
  - for generic URLs, use the browser tools to capture title, author, description, body, and image list
  - for PDF papers and reports, extract all figures, charts, tables, and diagrams into `imgs/source-fig-*.png`
  - for video URLs, obtain the full transcript before writing
  requirement: preserve title, author, description, body text, image list, and source subtype when available

- `markdown-polish`
  use for: canonical article cleanup before visuals and HTML rendering
  execution:
  - remove citation artifacts, broken formatting, invisible characters, and LaTeX fragments
  - preserve disclosure, digest, and structure-sensitive headings
  - standardize tables and heading hierarchy

- `inline-visuals`
  use for: informational or narrative images inside the article body
  execution:
  - decide placement from the surrounding text
  - prefer source figures extracted from PDFs when they support the claim
  - build primary keyword, modifiers, and search variants per image
  - reject images with watermarks, baked-in sales text, low resolution, or off-topic subjects

- `cover-art`
  use for: `imgs/cover.png` and `imgs/cover-thumb.png`
  execution:
  - generate a primary cover at 900x383 px
  - export at 2x resolution
  - produce a centered square thumbnail at 200x200 px
  - keep frontmatter `coverImage` aligned with `imgs/cover.png`

- `article-design`
  use for: applying a visual layout template from `design.pen`
  prerequisite: Pencil MCP server is configured
  execution:
  - open `design.pen`
  - select a design from [design-guide.md](design-guide.md)
  - populate the chosen template with title, author, sections, images, and CTA
  - verify via screenshot before using it as the visual source of truth
  fallback: if Pencil MCP is unavailable, keep the article in the native HTML renderer and choose light or dark mode directly

- `wechat-render`
  use for: rendering `article-formatted.md` into `article.html`
  execution:
  - run `python3 "${SKILL_DIR}/scripts/wechat_delivery.py" render [article-path] -o [output-path]`
  - optionally pass `--design [design-id-or-name]`
  - optionally pass `--color-mode light|dark`
  - optionally pass `--upload-map [json-path]` when local image paths were replaced by CDN URLs
  requirements:
  - inline styles only
  - no `<div>`
  - no flexbox or grid
  - explicit background for dark mode
  - cover, digest, author, and image paths must match the markdown source

- `wechat-draft`
  use for: image upload and draft save
  execution:
  - upload images with `python3 "${SKILL_DIR}/scripts/wechat_delivery.py" upload-images [images...]`
  - save the draft with `python3 "${SKILL_DIR}/scripts/wechat_delivery.py" save-draft --html [article.html] --markdown [article-formatted.md]`
  requirements:
  - obtain `access_token` from `WECHAT_APPID` and `WECHAT_SECRET`
  - inline image upload must use `/cgi-bin/media/uploadimg` with multipart field `media`
  - cover image upload must use `/cgi-bin/material/add_material`
  - draft save must use `/cgi-bin/draft/add` or `/cgi-bin/draft/update`
  - updating an existing draft uses `media_id`, not editor session fields
  - expose draft status clearly so `manifest.json` can record it

- `multi-platform-distribute`
  use for: optional Phase 8 delivery to 小红书、即刻、小宇宙、朋友圈
  execution:
  - derive platform copy from the canonical article and `platform-copy.md`
  - execute platforms sequentially to avoid platform state conflicts
  - keep platform outputs in `manifest.json`

## Loading Rule

- Keep `research-to-wechat` as the only skill in the loop.
- Use bundled scripts first.
- Use browser, PDF, image, and Pencil tools directly when the stage needs them.
- Do not run skill discovery commands from this skill's runtime flow.
