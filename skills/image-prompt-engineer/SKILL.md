---
name: "image-prompt-engineer"
description: "Generate production-ready image prompts for Midjourney and other image models. Use when the user asks to create, refine, translate, critique, or produce variants of image-generation prompts, AI art prompts, Midjourney /imagine prompts, product shots, logos, interiors, editorial images, style prompts, negative prompts, or prompt packs. Default to Midjourney when the user does not specify an image model, and remind the user once."
license: "MIT"
metadata: {"version":"1.0.2","category":"creative-tools","tags":["image-prompts","midjourney","prompt-engineering","generative-ai"],"license":"MIT","hermes":{"tags":["image-prompts","midjourney","prompt-engineering","generative-ai"]}}
---

# Image Prompt Engineer

## Overview

Generate precise image prompts that a user can paste directly into an image model. Default to Midjourney when the user does not name a model, and briefly state that default before the prompt.

Use English for the final prompt text unless the user explicitly requests another prompt language. Match explanations, labels, and notes to the user's language.

## Workflow

1. Identify the target model.
   - No model specified: use Midjourney and say once: `Defaulting to Midjourney.`
   - Model specified: adapt to that model and omit Midjourney-only parameters.
2. Infer missing creative details from the user's goal. Ask only when the missing detail changes the fundamental output, such as product identity, brand constraints, or prohibited content.
3. Produce prompt-ready output, not a tutorial. Include short rationale only when it helps the user choose between variants.
4. For Midjourney, place all parameters at the absolute end of the prompt, separated by spaces, with no punctuation inside parameter syntax.

## Midjourney Prompt Shape

Use this order for most Midjourney prompts:

```text
[primary subject and visual objective], [composition and camera/view], [materials and physical properties], [environment or background], [lighting], [style constraints], [technical constraints] --parameters
```

Front-load the most important concept in the first 10 to 30 tokens. Keep standard prompts around 30 to 80 tokens. Use 80 to 150 tokens only for highly specific layouts, product constraints, or complex spatial relationships.

Prefer natural, grammatical descriptive prose over comma-stuffed keyword lists. Use underscores to bind words that must stay together as one concept, such as `matte_polycarbonate_housing`.

## Midjourney Defaults

Default to the current Midjourney default model for general prompts unless the user asks for a version-specific feature. As of the June 2026 Midjourney docs, the default model is V7, while V8.1 is available for faster generation and HD images.

Use these defaults for controlled, production-oriented prompts:

- General controlled prompt: `--raw --stylize 50 --chaos 0`
- Minimal, flat, logo, or UI-like output: `--raw --stylize 20 --chaos 0`
- High-detail interior or environmental image: `--raw --stylize 100` to `--stylize 150`
- V8.1 HD output: append `--v 8.1 --hd` when native 2K output matters more than V7-only features.
- V7 feature workflows: append `--v 7` when using Omni Reference, or when a requested workflow depends on features absent from V8.1.

Use `--raw`, not `--style raw`, because current Midjourney docs name the parameter Raw as `--raw`.

## Version And Feature Choices

- Use V7 by default for most Midjourney prompt generation.
- Use V8.1 for fast clean renders, native HD, image prompts, style references, and prompt adherence without V7-only references.
- Use V7 for Omni Reference: `--oref URL --ow 100`.
- Use V6.1 or another supported version only when the user specifically needs a feature that the current docs limit to that version.
- Check official Midjourney docs before asserting latest compatibility or default version in a time-sensitive answer.

## Quality Rules

- Replace subjective terms with physical and visual specifics.
  - Avoid: `beautiful`, `high quality`, `epic lighting`, `photorealistic`, `hyperrealistic`, `8K`.
  - Prefer: material, finish, geometry, lens, lighting physics, color palette, surface texture, and background treatment.
- For minimalist, Scandinavian, or "Honest UI" aesthetics, describe physical restraint instead of using only the word `minimalist`.
  - Use terms like `vast negative space`, `centered composition`, `orthographic view`, `soft diffuse North-European daylight`, `matte injection-molded polycarbonate`, `brushed anodized aluminum`, `Helvetica typography`, `Akzidenz-Grotesk typography`.
- For logos and flat graphics, ban text artifacts and depth effects.
- For product design, prioritize material honesty, scale, seam lines, tactile controls, and real lighting.
- For architecture, use camera and space terms such as `24mm wide angle lens`, `floor-to-ceiling windows`, `raw concrete`, `single low-profile wooden bench`, `expansive negative space`.

## Negative Controls

Use `--no` for Midjourney exclusions when compatible with the target version:

```text
--no text, letters, words, signature, watermark, clutter, noise, shadow, gradient, depth, 3d, overprocessed
```

Do not put compound phrases in `--no` when each word would be harmful independently. Midjourney may read words in the negative block separately.

For weighted prompts, keep the total concept weight greater than zero:

```text
minimalist mechanical dial::2 soft shadow::0.5 clutter::-0.5 --raw --v 7
```

## Output Formats

For a single prompt request, return:

```markdown
Defaulting to Midjourney.

Prompt:
[paste-ready prompt]
```

For variants, return compact numbered prompts with meaningful variant names:

```markdown
Defaulting to Midjourney.

1. Product Poster
[prompt]

2. Editorial Still Life
[prompt]
```

For prompt refinement, return the improved prompt first, then a short `Changed:` line naming the most important fixes.

## Reference

Read `references/midjourney-prompt-guide.md` when the request needs Midjourney parameter details, version tradeoffs, prompt weighting, image/style references, negative prompt strategy, or minimalist product/logo/interior blueprints.
