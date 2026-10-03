# Cover Design Guide

> Rules for the article cover image, its dimensions, the WeChat two-image reality,
> crop-safe text layout, and how to change a cover without touching the body.
> Learned the hard way 2026-09-25 while iterating a live draft's cover.

---

## The one fact that governs everything

**A WeChat draft has exactly ONE cover field: `thumb_media_id`.** The `articles`
schema accepts only `article_type`, `title`, `author`, `digest`, `content`,
`content_source_url`, `thumb_media_id`, `need_open_comment`,
`only_fans_can_comment`, `image_info`, `cover_info`, `product_info`.

What the editor shows as **两张图** — a wide 头图 at the top of the article and a
small square 缩略图 in some feed/list/share slots — are **two crops of the same
cover material**, not two separately-settable images. You upload one cover; the
editor lets you drag a 1:1 crop box over it for the square slot. **The API cannot
set an independent square thumbnail.** Do not try to solve "the square thumbnail
looks wrong" with an API call — that is an editor crop the human drags.

## Cover material: dimensions

| Asset | File | Size | Ratio | Used for |
|-------|------|------|-------|----------|
| Cover / 头图 | `imgs/cover.png` | 2048×872 (Kompany episodes: 1800×766) | 2.35:1 | Article header + wide feed card. **This is the cover you upload.** |
| Square preview | `imgs/cover-square-preview.png` | 872×872 | 1:1 | Check only: the center crop WeChat will use as the square thumbnail. Never upload. |
| Square crop | `imgs/cover-thumb.png` | 800×800 | 1:1 | Fallback only, where a square is explicitly required. |

The 2.35:1 cover is the one that becomes `thumb_media_id`. For non-Kompany
articles, render it with `scripts/make_text_cover.py` (see the default layout
section below).

## Upload the WIDE cover, `--cover-type image` — never the square

Set the cover to the wide `cover.png` with `--cover-type image`. **Do NOT** upload
the square `cover-thumb.png` as `--cover-type thumb` for the draft cover:

- WeChat center-crops whatever cover you give it to the feed card's wide aspect.
- A square image fed in that way loses its top and bottom bands — the last line
  of text gets chopped off, and the result reads as oversized and clipped.
- The wide 2.35:1 cover keeps its single line of text inside the visible band, so
  it survives the crop.

This was the 2026-09-25 mistake: the cover was set from the square thumb, the feed
card cropped it, and the bottom hook line disappeared. Sibling episode 01 used the
wide cover with `--cover-type image` and displayed correctly. Match that.

## Text layout rules (author-written cover, dark theme)

The cover title/hook is author-written and NOT bound by the "don't touch the body"
rule. Design it like the reference episodes:

1. **Wide cover (2.35:1):** one accent bar, kicker `Kompany AI 日记 · NN`, a two-line
   hook (white line + orange payoff line, ~84px bold), one supporting line, and an
   optional bottom metric strip (3 columns) inside a `surface`-colored band. Keep
   the hook to one line each — a wide canvas has horizontal room, so do not stack
   many lines.
2. **Square crop (1:1), when you make one at all:** keep it AIRY. Short lines
   (≤4–5 chars each), ~72–76px bold, generous top margin and line spacing, and keep
   all key text inside the vertical center band so any horizontal crop still shows
   the whole hook. A long line at a big font on a small square reads as crowded and
   "too big" — shorten the words, do not just shrink the font a little.
3. Dark theme only for this collection. Always pair a background with its text
   color; never leave a surface half-styled.

## Default for non-Kompany articles: centered text card (founder-approved 2026-10-02)

Reference: `wechat/2026-09-26-gsd-advanced/imgs/cover.png`. The founder liked it
because the automatic square thumbnail showed the whole title, centered, with no
manual crop. Use this layout by default. Render it with the bundled script, which
keeps the exact geometry and colors:

```bash
python3 "${SKILL_DIR}/scripts/make_text_cover.py" --out imgs/cover.png \
  --kicker "<主题 · 文章类型>" --title "<痛点问句，≤6 字>" \
  --subtitle "<解决办法，≤9 字>" --footer "<读者收获，≤13 字>" \
  --square-preview imgs/cover-square-preview.png
```

The output stays a wide 2048×872 (2.35:1) cover. Do not make a square cover.
Upload only `imgs/cover.png`. `cover-square-preview.png` is only for checking what
the automatic square thumbnail will show; never upload it.

Why it works: after publishing, WeChat creates the square thumbnail itself by
cropping the center 872×872 (x 588–1460) of the 2048×872 cover. Every element is horizontally centered and no wider than 760px, so
the square crop keeps all of it. Vertically everything sits inside the full height.

Layout, top to bottom (y values on the 2048×872 canvas):

1. Background `#081120` with a 52px grid in `#122239`, 1px lines.
2. Card: rounded rectangle (278,86)–(1770,785), radius 32, fill `#111d30`, 3px border `#35516c`.
3. Kicker pill at y 120–189, radius 18, fill `#182e49`, 2px border `#35516c`; text at y 128, Noto Sans CJK Regular 39px, `#a4bed9`. Format: `<主题> · <文章类型>`, e.g. `AI 编程助手 · 实操教程`.
4. Title at y 264: Noto Sans CJK Bold 105px, `#f6f8ff`. The reader's pain as a short question, e.g. `总改错代码？`.
5. Subtitle at y 422: Bold 70px, `#f6f8ff`. The fix, e.g. `先立规则，再查数据`.
6. Accent bar at y 557–568, radius 5, `#a581ff` (violet), 760px wide, centered.
7. Footer at y 619: Regular 47px, `#b4d4ec`. What the reader gets, e.g. `从第一步到多仓库，不跳步骤`.

Rules:
- Four text lines only. No icons, no people, no logos, no AI-generated imagery.
- Text comes from the article's pain-first title; never an internal codename or a term a new reader doesn't know.
- Shorten words before letting the script shrink a font. If it shrinks, the line is too long.
- Always open `cover-square-preview.png` and check every line is whole before uploading.

The Kompany AI 日记 collection keeps its own layout (rule 1 above).

## Changing ONLY the cover of an existing draft

Use the `update-cover` subcommand — **not** `save-draft`. `save-draft` rewrites the
whole article from local html/markdown, which risks body drift and needs a
re-render just to swap a picture. `update-cover` reads the live body back via
`draft/get` and re-pushes only `thumb_media_id`, so the body cannot move:

```bash
python3 "${SKILL_DIR}/scripts/wechat_delivery.py" update-cover \
  --media-id "$MEDIA_ID" --cover-image imgs/cover.png --cover-type image
```

It self-verifies with a `draft/get` readback (title/body preserved) after writing.

## Ordering with the manual settings (hard constraint)

Every cover write is still a `draft/update`, and a `draft/update` **wipes**
原创 / 赞赏 / 合集 (editor-only fields the API cannot restore). So:

- Do ALL cover iteration BEFORE the human sets 原创/赞赏/合集 in the editor.
- Once those three are set, do NOT run `update-cover`/`save-draft` again, or they
  are cleared and must be re-done by hand.
- If the cover truly must change after they were set, the order is:
  `update-cover` → read back → re-set all three in the editor → 保存为草稿.
