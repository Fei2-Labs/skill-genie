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
| Cover / 头图 | `imgs/cover.png` | 1800×766 | 2.35:1 | Article header + wide feed card. **This is the cover you upload.** |
| Square crop | `imgs/cover-thumb.png` | 800×800 | 1:1 | Fallback only, where a square is explicitly required. Normally the human crops the square from the cover in the editor. |

Generate both in the draft's `build_images.py`. The 2.35:1 cover is the one that
becomes `thumb_media_id`.

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
