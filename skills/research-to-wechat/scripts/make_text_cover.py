#!/usr/bin/env python3
"""Render a dark, text-only WeChat cover whose square center crop keeps every line.

Reference design: wechat/2026-09-26-gsd-advanced/imgs/cover.png (2026-09-29).
The cover is 2048x872 (2.35:1). WeChat's square thumbnail is the center
872x872 crop (x 588..1460), so every text line, the kicker pill and the accent
bar are kept inside a 760px-wide band around the center. Fonts shrink only when
a line would leave that band; shorten the words first.

Usage:
    python3 make_text_cover.py --out imgs/cover.png \
        --kicker "AI 编程助手 · 实操教程" \
        --title "总改错代码？" \
        --subtitle "先立规则，再查数据" \
        --footer "从第一步到多仓库，不跳步骤" \
        --square-preview imgs/cover-square-preview.png
"""

from __future__ import annotations

import argparse

from PIL import Image, ImageDraw, ImageFont

W, H = 2048, 872
SAFE_WIDTH = 760  # widest allowed element; square crop is 872px wide
REGULAR = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

COLORS = {
    "background": "#081120",
    "grid": "#122239",
    "card": "#111d30",
    "border": "#35516c",
    "pill": "#182e49",
    "kicker": "#a4bed9",
    "title": "#f6f8ff",
    "accent": "#a581ff",
    "footer": "#b4d4ec",
}


def fitted_font(draw: ImageDraw.ImageDraw, text: str, path: str, size: int, limit: int) -> ImageFont.FreeTypeFont:
    font = ImageFont.truetype(path, size)
    while size > 24 and text_width(draw, text, font) > limit:
        size -= 2
        font = ImageFont.truetype(path, size)
    return font


def text_width(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont) -> int:
    box = draw.textbbox((0, 0), text, font=font)
    return box[2] - box[0]


def draw_centered(draw: ImageDraw.ImageDraw, text: str, y: int, font: ImageFont.FreeTypeFont, color: str) -> None:
    draw.text(((W - text_width(draw, text, font)) / 2, y), text, font=font, fill=color)


def render(kicker: str, title: str, subtitle: str, footer: str) -> Image.Image:
    image = Image.new("RGB", (W, H), COLORS["background"])
    draw = ImageDraw.Draw(image)
    for x in range(0, W, 52):
        draw.line((x, 0, x, H), fill=COLORS["grid"], width=1)
    for y in range(0, H, 52):
        draw.line((0, y, W, y), fill=COLORS["grid"], width=1)
    draw.rounded_rectangle((278, 86, 1770, 785), radius=32, fill=COLORS["card"], outline=COLORS["border"], width=3)

    kicker_font = fitted_font(draw, kicker, REGULAR, 39, SAFE_WIDTH - 80)
    pill_half = min(SAFE_WIDTH, text_width(draw, kicker, kicker_font) + 160) // 2
    draw.rounded_rectangle((W // 2 - pill_half, 120, W // 2 + pill_half, 189), radius=18, fill=COLORS["pill"], outline=COLORS["border"], width=2)
    draw_centered(draw, kicker, 128, kicker_font, COLORS["kicker"])

    draw_centered(draw, title, 264, fitted_font(draw, title, BOLD, 105, SAFE_WIDTH), COLORS["title"])
    draw_centered(draw, subtitle, 422, fitted_font(draw, subtitle, BOLD, 70, SAFE_WIDTH), COLORS["title"])
    draw.rounded_rectangle((W // 2 - SAFE_WIDTH // 2, 557, W // 2 + SAFE_WIDTH // 2, 568), radius=5, fill=COLORS["accent"])
    draw_centered(draw, footer, 619, fitted_font(draw, footer, REGULAR, 47, SAFE_WIDTH), COLORS["footer"])
    return image


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", required=True)
    parser.add_argument("--kicker", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--subtitle", required=True)
    parser.add_argument("--footer", required=True)
    parser.add_argument("--square-preview", help="optional path for the center 1:1 crop, for visual review")
    args = parser.parse_args()

    image = render(args.kicker, args.title, args.subtitle, args.footer)
    image.save(args.out, optimize=True)
    if args.square_preview:
        left = (W - H) // 2
        image.crop((left, 0, left + H, H)).save(args.square_preview, optimize=True)
    print(f"cover: {args.out} {image.size}")


if __name__ == "__main__":
    main()
