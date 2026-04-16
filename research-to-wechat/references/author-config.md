# Author Config (EXTEND.md)

The renderer reads an optional `EXTEND.md` file for author-specific preferences that should not be hardcoded in the skill itself.

## Lookup Order

1. **Project-level**: `<project-root>/EXTEND.md`
2. **User-level**: `~/.config/research-to-wechat/EXTEND.md`
3. **Fallback**: `~/.research-to-wechat/EXTEND.md`

The first file found wins. If none exists, CTA is skipped and defaults apply.

## Format

YAML frontmatter only. Example:

```yaml
---
cta:
  enabled: true
  qr_image: "wechatqr.png"
  heading: "👇 扫码加我微信进群"
  body: "群里分享：我的 AI 使用心得 · 最前沿的 AI 工具和玩法 · 帮你跨过信息差"
  footer: "不卖课。就是一群在认真用 AI 搞事情的人，互相交流、少走弯路。"
  blog_url: "https://example.com/blog"
  interactions: "觉得有用？点个赞 👍 点个在看 👀 顺手关注 ⭐ 转发给需要的朋友 🔄"
---
```

## Fields

| Field | Required | Description |
|-------|----------|-------------|
| `cta.enabled` | no | `true` to render CTA. Default `true` when `cta` section exists. |
| `cta.qr_image` | yes | QR code filename. Resolved relative to the article `imgs/` dir, or as an absolute path. Must be uploaded to CDN before render if using `--upload-map`. |
| `cta.heading` | no | Line above the QR code. Default: empty. |
| `cta.body` | no | Description below the QR code. |
| `cta.footer` | no | Secondary text below body. |
| `cta.blog_url` | no | Full URL for "read uncut version" line. Rendered as: `无删减全文请移步 {url}` |
| `cta.interactions` | no | Social engagement prompt (likes, shares, etc.) |

## Renderer Behavior

- When `EXTEND.md` is found and `cta.enabled` is not `false`, the renderer appends a CTA block after the last article section, before `</section></section>`.
- The CTA block inherits the design profile's colors (background, text, accent, surface, radius).
- `qr_image` is looked up in the `--upload-map` if provided, otherwise used as-is.
- If `EXTEND.md` is missing or `cta.enabled: false`, no CTA is rendered. The `ctaId` in the render output still reflects the matched design CTA for reference.
