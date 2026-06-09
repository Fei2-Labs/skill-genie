# Midjourney Prompt Guide

This reference condenses the user's `Midjourney Prompt Engineering Deep Dive.pdf` and the current official Midjourney docs checked on June 9, 2026.

## Core Model Behavior

- Midjourney gives the earliest prompt tokens the strongest influence. Put the subject, visual objective, and must-have constraint first.
- The 30 to 80 token range usually balances control and coherence. Longer prompts can work for complex layouts, but late details are easier to ignore.
- Modern Midjourney prefers grammatical, descriptive prose. Avoid old keyword-stuffing prompt style.
- Standard punctuation helps readability, but parameters must be clean command syntax at the end.
- Use underscores to bind critical compound descriptors: `matte_polycarbonate_housing`, `North_European_overcast_daylight`.

## Parameter Syntax

Place parameters at the end:

```text
[prompt text] --ar 1:1 --raw --stylize 30 --chaos 0 --v 7
```

Do not use commas in parameter syntax. Do not put prompt text after parameters.

Common parameters:

- `--ar W:H`: aspect ratio. Use integers, not decimals.
- `--raw`: reduce Midjourney's default aesthetic styling.
- `--stylize` or `--s`: default styling strength. Lower values give more literal control.
- `--chaos` or `--c`: variation across initial grid. Use `0` for predictable iteration.
- `--weird` or `--w`: eccentricity. Avoid for clean design unless the user asks for strangeness.
- `--stop`: stop generation early for softer and less defined output.
- `--iw`: image prompt weight, from 0 to 3, default 1.
- `--sref URL`: style reference. Transfers palette, medium, lighting, and visual feel.
- `--sw N`: style reference weight, from 0 to 1000, default 100.
- `--oref URL`: Omni Reference for V7 object, character, vehicle, or asset consistency.
- `--ow N`: Omni Reference weight, from 1 to 1000, default 100. Keep below 400 for predictable results.
- `--no`: excludes concepts. Similar to a negative weight.
- `--v N`: model version.
- `--hd`: V8.1 native 2K HD generation.

## Version Notes

- Official docs checked June 9, 2026 list V7 as the current default Midjourney version.
- V8.1 was released April 30, 2026. It is faster and supports HD images with `--hd`.
- V8.1 is useful for clean high-resolution images when V7-only features are not needed.
- V7 supports Omni Reference and strong reference-controlled workflows.
- Official docs list Multi-Prompting support in older model versions and show compatibility differences by version. Verify official docs before making a time-sensitive compatibility claim.

## Weighting

Use `::` to split concepts and weight them. The double colon has no space on the left and one space on the right when more prompt text follows.

```text
minimalist desktop radio receiver::2 soft diffuse overcast light::1 clutter::-0.5 --raw --v 7
```

Rules:

- Unspecified weight defaults to 1.
- Negative weights suppress concepts.
- The sum of all weights must be greater than zero.
- Use weights when a secondary concept dominates the image.

## Minimalist And Honest UI Strategy

Midjourney often adds visual complexity because training data rewards detailed, dramatic images. Counter that with literal design constraints.

Use:

- `vast negative space`
- `centered composition`
- `orthographic view`
- `top-down knolling layout`
- `90-degree aerial view`
- `flat lay presentation`
- `axonometric drawing`
- `axially symmetric`
- `perfect circular geometry`
- `monoline art`
- `deep depth of field`
- `zero-contrast soft shadows`
- `soft diffuse North-European daylight`
- `subdued ambient studio lighting`

Avoid:

- `beautiful`
- `high quality`
- `premium`
- `epic lighting`
- `photorealistic`
- `hyperrealistic`
- `superdetailed`
- `4K`, `8K`, `16K`

Replace abstract praise with physical description:

- `matte light grey polycarbonate chassis`
- `brushed anodized aluminum`
- `sandblasted silver steel`
- `raw unfinished concrete`
- `translucent violet-tinted plastic`
- `flush-fitting seams`
- `radial precision dial`
- `perfectly debossed alignment markings`
- `Helvetica typography`
- `Akzidenz-Grotesk typography`

## Negative Blocks

For flat, restrained, logo, or UI-like output:

```text
--no depth, 3d, shading, gradient, texture, shadow, noise, clutter, volumetric, realistic, hyperdetailed
```

For logos:

```text
--no text, letters, words, signature, watermark, background, shadow, gradient, depth, 3d, shading, photorealistic, noise
```

For photography where some shadow is desirable, do not ban all shadows. Use a softer phrase:

```text
zero-contrast soft shadows
```

## Blueprint Patterns

Minimal product/object poster:

```text
design specification sheet for a restrained desktop radio receiver, matte light grey polycarbonate chassis, perfectly circular dial, Akzidenz-Grotesk typography labeling, flat top-down knolling layout, centered on a solid matte white surface, soft diffuse overcast light, zero-contrast shadows, architectural orthographic composition --raw --ar 707:500 --stylize 30 --chaos 0 --no depth, 3d, shading, gradient, texture, shadow, noise, clutter, volumetric, realistic, hyperdetailed --v 7
```

Graphic symbol or logo:

```text
abstract geometric hexagon frame symbol, monoline line art, single color, flat design, clean vector emblem, black on solid white background --raw --ar 1:1 --stylize 20 --chaos 0 --no text, letters, words, signature, watermark, background, shadow, gradient, depth, 3d, shading, photorealistic, noise --v 7
```

Architectural concept space:

```text
architectural wide shot of a minimalist Scandinavian concrete pavilion interior, floor-to-ceiling windows, soft morning light through glass, expansive smooth raw concrete walls, a single low-profile wooden bench, vast empty negative space, quiet contemplative atmosphere, 24mm wide angle lens --raw --ar 141:100 --stylize 120 --chaos 0 --hd --v 8.1
```

Editorial fine art:

```text
abstract composition of paper structures, delicate overlapping matte white sheets, geometric sharp folds, linear arrangement, subtle cast shadows, monochromatic grayscale palette, soft diffused North-European daylight, studio fine art photography, macro lens view, deep depth of field --raw --ar 100:141 --stylize 150 --chaos 0 --no color, vibrant, saturation, background noise, grain --v 7
```

Functionalist control panel:

```text
design blueprint graphic of flat circular control dials on a modular matrix, sandblasted silver aluminum panel, flush-fitting toggle switches, clean Helvetica typography, orthographic projection view, perfectly balanced grid layout, neutral grey and silver color scheme --raw --ar 141:100 --stylize 40 --chaos 0 --v 8.1
```
