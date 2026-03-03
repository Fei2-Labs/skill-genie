# Execution Contract

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
- do not proceed from a video source until the full transcript has been captured
- acceptable inputs are full on-page transcript text, caption text, or a subtitle file that can be expanded into full text
- title, description, chapters, and summary are supporting context only and cannot replace the transcript
- if the transcript is unavailable, stop and ask for the transcript or subtitle file

Record:
- source type
- source language
- title or working title
- thesis or central question
- key entities, dates, claims, quotes, and unknowns
- material that must survive into the final article
- source metadata fields: title, author, description, body, image list, and page subtype when available

If the route is `Path B`, also record:
- original structure and useful sections
- what must be preserved verbatim or semantically
- what should be rewritten for WeChat readability

If the source worker returns only metadata or a thin description for a URL that should contain article body text, stop and ask for:
- the raw article text
- a markdown export
- or a browser-openable page session that can expose the full body

## Phase 2: Brief and Research Architecture

Create `brief.md` before drafting.

### Strategic Clarification

Before building the brief, verify these five dimensions are resolved.
Ask the user only for dimensions that remain genuinely ambiguous after reading the source packet:

1. **Research goal**: what the article must prove, explain, or enable
2. **Target audience**: reader's current knowledge level and what they need next
3. **Core research points**: the 3-5 claims or angles the article must cover
4. **Language and style**: tone, evidence density, and any constraints
5. **Topic boundaries**: what is explicitly out of scope

If the source packet already answers a dimension clearly, do not re-ask.
Record resolved dimensions in `brief.md` under a `## Clarification Record` section.

### Brief Declaration

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

### Research Brief Structure

Build one central research brief and up to five side briefs for angle expansion.

Each brief must contain:
- `topic`: precise research question
- `purpose`: what finding this answer contributes to the article
- `audience`: who needs this information and why
- `key_points`: 3-5 specific things to investigate
- `framework`: analytical lens or comparison structure to apply
- `expected_depth`: surface scan / working analysis / deep dive

The central brief covers the article's main thesis.
Side briefs cover supporting angles that strengthen or challenge the main thesis.
Do not generate side briefs for tangential decoration.

### Question Lattice

Generate at least 8 questions per layer (32+ total):

- `基础层` (definitions and first principles):
  what the topic is, core concept decomposition, boundary conditions,
  first-principles grounding, key terminology disambiguation.
  Method: treat this layer as if explaining to someone who is smart but new
  to the domain — use the Feynman technique to verify genuine understanding.

- `连接层` (structure and classification):
  internal knowledge structures, category systems, relationships between
  sub-concepts, comparison dimensions, taxonomies, and actor maps.
  Method: map how parts connect before analyzing any single part.

- `应用层` (methods and practice):
  actionable methodologies, decision frameworks, tradeoff matrices,
  workflow steps, best practices, and common failure modes.
  Method: every question should have an answer that someone could act on.

- `前沿层` (real-world application and edge cases):
  case analysis, risk scenarios, emerging variations, internalization
  strategies, future implications, and boundary-pushing applications.
  Method: stress-test the topic against real constraints and edge conditions.

## Phase 3: Research Merge and Evidence Ledger

Do the research pass before writing.

Rules:
- use user-provided material as the anchor
- add missing context only where it sharpens the article
- separate verified fact from inference
- keep track of unresolved claims
- do not move to prose until angle, evidence, and structure are aligned

Create `research.md` with three explicit zones:
- `verified facts`
- `working inferences`
- `open questions`

For each major claim, keep enough traceability to recover:
- source origin
- key quote or datum
- why it matters to the article

If a key claim remains unsupported and changes the main thesis, stop and ask for direction instead of smoothing over the gap.

## Phase 4: Frame-Routed Master Draft

Write `article.md` as the first complete article.

Route the draft by frame:
- `deep-analysis`
  use a narrative or scene-led opening, then move through background, core analysis, case or turn, and synthesis
- `tutorial`
  show the result early, then move through concept, setup, walkthrough, demo, and quick-start takeaway
- `newsletter`
  open with the top line, then short sections with fast transitions

Requirements:
- one H1 at most
- clean H2 and H3 hierarchy
- evidence-rich paragraphs with clear transitions
- 3 to 6 planned visual insertion points
- temporary visual markers written as `![图片X](TBD)` on isolated lines
- frontmatter must include `digest`, `structureFrame`, and `disclosure`

### Normalization Checklist

Apply these rules to `article.md` before moving to refinement.
The checklist is mandatory for Path B (source rewrite) and recommended for Path A.

**Citation and reference cleanup:**
- remove `[oai_citation:...]` and similar AI-generated citation tags
- remove in-text citation numbers (`[1]`, `[文献2]`, `[source 3]`) and
  trailing reference/bibliography lists unless the user explicitly wants them
- if a citation contains a genuinely useful source name, convert it to an
  inline mention ("according to X" or "X found that")

**Invisible character and syntax repair:**
- strip zero-width spaces, zero-width joiners, and other invisible Unicode
- fix unclosed or malformed bold/italic markers
- fix unclosed or redundant code blocks
- normalize smart quotes, em-dashes, and ellipsis to consistent style

**Math and diagram conversion:**
- convert ALL LaTeX, MathJax, and `$$`-delimited math to plain-text
  descriptions (e.g., "the square root of x" not `\sqrt{x}`)
- convert flowcharts, mind maps, and ASCII diagrams to structured text
  descriptions or ordered lists

**Table standardization:**
- every Markdown table must have a header row, a separator row, and
  consistent column count
- fix ragged or broken table formatting from source extraction

**Structural cleanup:**
- remove scraped UI elements: navigation bars, headers, footers, sidebars,
  cookie notices, "share this" blocks
- remove "read more" links, subscription prompts, and paywall remnants
- ensure exactly one H1 at article start; make it descriptive and
  search-friendly
- verify H2/H3 hierarchy has no skipped levels
- keep to GitHub-Flavored Markdown only

**Content integrity:**
- do not silently delete paragraphs that contain substantive claims
- if a section is removed because it is off-topic, note the removal in
  the evidence ledger
- preserve all data points, statistics, and named sources from the
  original material unless they are demonstrably wrong

**Honesty:**
- do not make false claims about research effort, interviews, or firsthand usage
- place visuals where they improve comprehension, not decoration

Disclosure rules:
- default to a compact disclosure block near the end or in frontmatter-backed metadata
- state AI role, human role if known, and evidence scope
- if the evidence base is thin, state the limitation instead of hiding it

## Phase 5: Refinement and Visual Layer

First hand off to `markdown-polish` and make `article-formatted.md` the canonical article.

### Image Placeholder Strategy

Before generating images, evaluate each `![图片X](TBD)` marker against
these criteria. Remove markers that fail; add markers where needed.

**Placement criteria** — a position earns an image if it meets at least two:
- the surrounding text describes something that benefits from visualization
  (a process, architecture, comparison, data pattern, or physical object)
- the position serves a structural function: summarizing a completed section,
  creating a visual transition, or separating dense argument blocks
- the content is abstract enough that an image would reduce cognitive load
- the position is not within 300 words of another image (avoid clustering)

**Article-type image strategy** — classify each placeholder by its surrounding content:
- entity/product focus: use the entity's proper name or product as the
  search core; show the thing itself or its interface
- abstract/theory focus: translate the abstract concept into a mainstream
  visual metaphor (e.g., "network effects" → interconnected nodes diagram)
- process/tutorial focus: visualize actions, steps, or before/after states
- narrative/storytelling focus: capture atmosphere, setting, or key emotion
- data/analysis focus: match to a specific chart or data visualization type
- hybrid: combine strategies based on which section the image serves

**Image keyword construction** — for each approved placeholder, build:
1. primary keyword: the core visual subject (max 4 words)
2. modifiers: one style modifier + one context modifier
   (e.g., "isometric", "dark background", "minimal", "professional photo")
3. search variants: 2-3 alternative phrasings including at least one English
   variant for broader search or generation coverage

**Global coordination:**
- plan all image keywords together before generating any single image
- ensure visual rhythm: vary between close-up/wide, concrete/abstract,
  photo/illustration across the article
- no two images should depict the same visual concept

### Image Generation

Generate inline images for the marked positions through `inline-visuals`.
Replace every temporary marker with a real relative asset path.

### Cover Generation

Generate the cover through `cover-art`:
- primary cover: 900 x 383 px (2.35:1 aspect), export at 2x (1800 x 766)
- secondary thumbnail: 200 x 200 px square cropped from center of primary
- place at `imgs/cover.png` (primary) and `imgs/cover-thumb.png` (secondary)
- make sure frontmatter points `coverImage` to `imgs/cover.png`
- make sure the disclosure block and evidence-sensitive wording survive polishing
- workers may use HTML export templates internally (html2canvas → PNG download),
  but the final workspace must keep resolved PNG paths for cover and inline assets

### Image Evaluation

After generating or selecting each image, verify against two tiers:

**Tier A — elimination** (reject immediately if any apply):
- visible watermark, logo overlay, or stock-photo ID
- commercial sales text or promotional banner baked into the image
- resolution too low to read on mobile (< 600px wide)
- content inappropriate, off-topic, or culturally mismatched

**Tier B — quality match** (evaluate remaining candidates):
- core match: does the image depict the primary keyword subject?
  (highest priority — reject if the answer is no)
- language consistency: if the image contains text, does it match
  the article language or is the text minimal enough to be neutral?
- style consistency: does the image feel like it belongs in the same
  article as the other images?
- information value: does the image add understanding beyond the text,
  or is it pure decoration?

If an image fails Tier B core match, regenerate with adjusted keywords
before accepting a decorative fallback.

### Article Design Selection

After images are finalized, apply a visual design template from `design.pen` via `article-design`.
This step requires the **Pencil MCP server** to be available. If Pencil MCP is not configured, skip
this step and proceed to HTML rendering (md2wechat handles its own styling).

**Auto-selection**: when the user does not specify a design, select one based on article topic and
structure frame using the rules in [design-guide.md](design-guide.md):

| Article Topic | Design |
|---------------|--------|
| AI / programming / tech | 04 科技 |
| Business / strategy / finance | 09 商务 |
| Lifestyle / personal growth | 05 生活 |
| Culture / history / humanities | 06 典雅 |
| News / commentary / opinion | 02 编辑 |
| Design / creativity / branding | 07 粗犷 |
| Fun / youth / community | 08 活泼 |
| Art / music / film | 10 艺术 |
| General / uncategorized | 01 极简 |

**User override**: if the user names a design style (e.g., "用科技排版", "杂志风格", "Dark 模式"),
use their choice instead of auto-selection.

**Workflow**:
1. determine `SKILL_DIR` (the directory containing SKILL.md)
2. open `${SKILL_DIR}/design.pen` via Pencil MCP `open_document`
3. read the selected template via `batch_get` with the design node ID and `readDepth: 3`
4. copy the template via `batch_design` Copy operation
5. populate with actual article content (title, author, sections, images, CTA)
6. verify via `get_screenshot`

Default to Light mode. Use Dark mode when the user requests it or the content strongly
suggests it (cybersecurity, space, underground culture themes).

## Phase 6: WeChat Delivery and Manifest

### HTML Rendering

Render `article-formatted.md` into `article.html` through `wechat-render`.

**Converter selection** (in priority order):

1. **md2wechat skill** (Go binary, ai mode) — if the skill is installed:
   ```bash
   # Preview only (no image upload)
   bash skills/md2wechat/scripts/run.sh convert [article-path] --mode ai --theme [theme] --preview -o [output-path]

   # With image upload to WeChat CDN
   bash skills/md2wechat/scripts/run.sh convert [article-path] --mode ai --theme [theme] --upload -o [output-path]
   ```
   Uses Claude to generate WeChat-compatible HTML with inline CSS. No external API calls.

   Built-in themes:
   - `autumn-warm` (秋日暖光): warm orange accent, best for emotional stories and lifestyle essays
   - `spring-fresh` (春日清新): spring green, best for travel and nature content
   - `ocean-calm` (深海静谧): deep ocean blue, best for technical articles and business analysis
   - `custom`: user-defined prompt for complete customization

   Default: `--mode ai --theme autumn-warm`.
   For long-form deep-analysis: consider `ocean-calm`.
   For tutorial: consider `spring-fresh` or `autumn-warm`.

   Install: `curl -fsSL https://raw.githubusercontent.com/geekjourneyx/md2wechat-skill/main/scripts/install.sh | bash`
   Config: `bash skills/md2wechat/scripts/run.sh config init` (sets up `~/.config/md2wechat/config.yaml`)
   Requires: `WECHAT_APPID` and `WECHAT_SECRET` env vars for draft upload; `IMAGE_API_KEY` for AI image generation.

If the user has no preference, use `autumn-warm`.

Product: `article.html` in the workspace directory. Browser-open the preview to verify
cover, digest, author, and image paths match the markdown source.

### Draft Upload

Before draft delivery, run an environment check for whichever path is available:
- API draft path (md2wechat): `bash skills/md2wechat/scripts/run.sh config validate`
  (checks WECHAT_APPID, WECHAT_SECRET, and API connectivity)
- browser draft path: Chrome availability, profile/session status, and editor reachability

If md2wechat is installed and configured, the convert + draft can be a single command:
```bash
bash skills/md2wechat/scripts/run.sh convert [article-path] --mode ai --theme [theme] --upload --draft --cover [cover-path]
```

Draft handoff rules:
- title, summary, author, and cover must be resolved before browser upload
- if login is needed, pause for login and resume
- before first use, suggest the environment check offered by the resolved draft worker
- report success with output paths and draft status

Draft fallback ladder:
- `L0 api-draft`
  use when direct draft API is available
- `L1 automated-browser`
  use when the worker can upload content and images end-to-end
- `L2 assisted-browser`
  use when login, selectors, or confirmation need the user
- `L3 manual-handoff`
  use when automation fails; provide exact paths and copy fields

Before finishing, write `manifest.json` with:
- route choice
- source type
- style mode
- structure frame
- confidence summary
- draft status
- output file paths

Required manifest shape (wechat field is always required; other platforms are optional):
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
    },
    "xiaohongshu": { "html": "...", "copy": { "title": "...", "body": "...", "tags": [] } },
    "jike": { "copy": { "body": "...", "circles": [] } },
    "xiaoyuzhou": { "audio": "...", "script": "...", "copy": { "title": "...", "description": "..." } },
    "moments": { "copy": { "body": "..." } }
  }
}
```

If rendering or draft upload fails, keep the highest-quality completed artifact set and report the exact stopping point.

## Phase 7: Multi-Platform Distribution (Optional)

This phase only executes when the user explicitly requests it (e.g., "多平台分发", "转小红书", "转即刻", "写朋友圈文案", "做播客脚本"). If the user does not request it, Phase 6 is the final phase.

### Trigger and Scope

When the user triggers multi-platform distribution:
1. check which platforms the user wants (all, or specific ones)
2. generate platform-specific content for each requested platform
3. extend `manifest.json` with the new platform output entries
4. optionally trigger distribution via `multi-platform-distribute`

### Platform Content Generation

For each platform, generate content following the rules in
[platform-copy.md](platform-copy.md):

- **小红书 (xiaohongshu)**: article → 8-10 card carousel HTML + publishing copy
  (title 15-20 chars, body 150-250 chars, 8-12 tags)
- **即刻 (jike)**: article → conversation-style post (200-400 chars, circle tags)
- **小宇宙 (xiaoyuzhou)**: article → podcast script (1500-2000 chars) + optional TTS audio
- **朋友圈 (moments)**: article → 3-5 line personal status copy

### Distribution Execution

If the user says "发布" or "一键发布", execute the distribution flow:

Execution order (sequential, avoid Chrome port conflicts):
1. 公众号 (wechat) — Phase 6 already handled this
2. 小红书 (xhs) — Chrome CDP
3. 即刻 (jike) — Chrome CDP
4. 小宇宙 (xiaoyuzhou) — Chrome CDP

Same four-level fallback ladder as Phase 6:
- `L0 api-draft` → `L1 automated-browser` → `L2 assisted-browser` → `L3 manual-handoff`

Report each platform's status (success/failed/skipped) with links where available.
