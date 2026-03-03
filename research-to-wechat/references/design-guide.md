# Article Design Guide

> Used by Phase 6 (refinement) to select a visual design template from `design.pen` via Pencil MCP.
> Requires the Pencil MCP server to be configured in the user's Claude Code environment.

---

## Prerequisite: Pencil MCP

The design templates live in `design.pen` at the skill root directory. Reading and applying these designs requires the **Pencil MCP server** to be running.

If Pencil MCP is not available, skip design selection and proceed with HTML rendering only (md2wechat handles its own styling via themes).

## Available Designs

`design.pen` contains 10 article layout styles, each with Light and Dark variants (20 screens total), plus 6 CTA (call-to-action) templates.

### Article Layouts

| # | Name | ID (Light) | ID (Dark) | Visual Character |
|---|------|-----------|----------|-----------------|
| 01 | 极简 (Minimal) | `HQLZX` | `4Znb9` | Clean white, simple typography, hero image, well-spaced sections |
| 02 | 编辑 (Editorial) | `P7h4J` | `ktRJG` | Header bar, strong typography, news/media editorial feel |
| 03 | 杂志 (Magazine) | `GJ40s` | `fVmOU` | Luxury magazine aesthetic, serif fonts, high-end visual |
| 04 | 科技 (Tech) | `QPb0Z` | `EBxCi` | Blue/dark tones, code blocks, tech UI elements, data-oriented |
| 05 | 生活 (Lifestyle) | `Tc2E9` | `wiCwu` | Warm, personal, colorful cards, lifestyle content |
| 06 | 典雅 (Elegant) | `zlQmy` | `RK3dM` | Traditional Chinese aesthetic, warm yellows, serif fonts |
| 07 | 粗犷 (Bold) | `eLE4I` | `AKs17` | Strong contrasts, bold typography, industrial/design focus |
| 08 | 活泼 (Lively) | `ZwGhE` | `X6VqH` | Playful purple/orange, rounded elements, creative/fun |
| 09 | 商务 (Business) | `e7KIB` | `49JrE` | Dark blue gradient hero, data points, corporate/strategy |
| 10 | 艺术 (Art) | `rdHk7` | `stjEM` | Dark hero, art-focused, pink accents, creative/artistic |

### CTA Templates

| Name | ID | Visual Character |
|------|-----|-----------------|
| CTA - Light Minimal | `YCqgA` | Clean white, minimal accents |
| CTA - Dark Minimal | `U5FfV` | Dark background, minimal accents |
| CTA - Light Gradient | `vj1H4` | Soft gradient background, purple accents |
| CTA - Dark Gradient | `Z7dEq` | Deep purple gradient, glowing accents |
| CTA - Warm Editorial | `wyyNI` | Warm cream tones, serif typography, gold accents |
| CTA - Tech Neon | `5hruL` | Black background, green terminal aesthetic |

## Auto-Selection Rules

When the user does not specify a design, select based on article content and structure frame.

### By Topic

| Article Topic | Primary Design | Fallback |
|---------------|---------------|----------|
| AI / programming / dev tools / tech products | 04 科技 | 01 极简 |
| Business / strategy / management / finance | 09 商务 | 02 编辑 |
| Lifestyle / emotion / personal growth / wellness | 05 生活 | 01 极简 |
| Design / creativity / branding / visual | 07 粗犷 | 10 艺术 |
| Culture / history / humanities / philosophy | 06 典雅 | 03 杂志 |
| News / commentary / opinion / critique | 02 编辑 | 01 极简 |
| Fun / youth / creative / community | 08 活泼 | 05 生活 |
| Art / music / film / creative industry | 10 艺术 | 03 杂志 |
| General / uncategorized | 01 极简 | 02 编辑 |

### By Structure Frame

| Structure Frame | Suggested Designs |
|----------------|-------------------|
| `deep-analysis` | 09 商务, 02 编辑, 04 科技 (match to topic) |
| `tutorial` | 04 科技, 01 极简 |
| `newsletter` | 02 编辑, 01 极简 |
| `case-study` | 09 商务, 06 典雅 |
| `commentary` | 02 编辑, 07 粗犷 |
| `narrative` | 05 生活, 03 杂志, 06 典雅 |
| `trend-report` | 04 科技, 09 商务 |
| `founder-letter` | 01 极简, 06 典雅 |

### CTA Selection

| Article Design | Matching CTA |
|---------------|-------------|
| 04 科技 | Tech Neon |
| 06 典雅, 03 杂志 | Warm Editorial |
| 09 商务 | Dark Minimal |
| 08 活泼, 10 艺术 | Light/Dark Gradient |
| Default | Light Minimal |

### Light vs Dark

Default to **Light** mode. Use **Dark** mode when:
- the user explicitly requests dark mode
- the article topic is strongly associated with dark aesthetics (cybersecurity, night/space, underground culture)
- the hero image works better on a dark background

## Design Application Workflow

1. **Read article metadata**: extract `structureFrame`, topic keywords from title and brief
2. **Select design**: apply the auto-selection rules above
3. **Open design.pen** via Pencil MCP: `open_document` with the design.pen path
4. **Read the selected design template**: `batch_get` with the design node ID
5. **Adapt the template**: use `batch_design` to populate the template with actual article content (title, author, sections, images, CTA)
6. **Screenshot and verify**: `get_screenshot` to validate the final layout
7. **Export**: the populated design serves as a visual reference or can be exported for use

## Pencil MCP Operations Reference

```
# Open the design file
open_document("/path/to/research-to-wechat/design.pen")

# Read a design template structure
batch_get(nodeIds: ["HQLZX"], readDepth: 3)

# Copy a template and populate it
batch_design:
  screen=C("HQLZX", document, {name: "My Article", positionDirection: "right", positionPadding: 100})

# Take a screenshot to verify
get_screenshot(nodeId: "screen-id")
```
