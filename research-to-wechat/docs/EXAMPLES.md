# Example Prompts

Use these examples to show how the skill should be invoked from different starting points.

## Path A topic-first

```text
围绕”AI Agent 在中小企业里的真实落地成本”走 Path A 写一篇 deep-analysis 文章。
先做 source.md、brief.md、research.md，明确区分 verified facts、working inferences、open questions。
需要 3 张正文配图、1 个封面，最后输出 article-formatted.md、article.html、manifest.json，并保存到公众号草稿箱。
```

## Path B article URL

```text
把这篇文章链接按 Path B 整理成公众号版本。
保留原文核心观点和来源信息，但改成更适合微信阅读的 explainer 结构。
先保住 title、author、description、content、images 再重写，最后保存草稿，不要正式发布。
```

## WeChat URL with thin-source guard

```text
把这个公众号链接改写成公众号文章。
如果你只能抓到标题或摘要，没有拿到正文，请只问我一个问题来要原文或可访问页面，不要硬写。
最后给我 manifest.json 里的 wechat 输出字段。
```

## Video URL

```text
根据这个视频链接做一篇 trend-report 风格文章。
先提取完整 transcript；如果页面拿不到完整 transcript，请只问我一个问题来要 transcript 或字幕文件。
没有完整 transcript 就不要开始写作。最后输出 Markdown、HTML 和公众号草稿。
```

## Transcript-first

```text
下面是播客逐字稿，请整理成 newsletter 风格文章。
要求高信息密度、易扫描、5 个以内小节、2 张正文配图。
在 disclosure 里明确说明是基于 transcript 的 AI 整理稿。
```

## Author-style request

```text
模仿我提供的三篇样文的节奏和视角来写这篇文章，但不要复制明显句式。
选题是”独立开发者为什么越来越需要内容系统而不是单篇爆文”。
如果原样文里有明显的虚构采访感或过强个人签名句式，不要继承。
```

## Custom brief

```text
目标读者是做知识付费的个人品牌。
语气要克制、锋利、不要鸡汤。
结构希望是”问题 - 误区 - 机制 - 解法 - 结论”。
证据密度高，禁用”时代红利””认知升级”这类表达。
```

## Conversion-only orientation

```text
我已经有一篇完整 Markdown。
请不要重写核心观点，只做结构优化、配图、封面、HTML 转换和公众号草稿保存。
manifest.json 里请把 outputs.wechat.markdown/html/cover_image/title/author/digest/images 写完整。
```

## Delivery ladder request

```text
这篇内容只需要保存到公众号草稿箱，不要正式发布。
如果 API draft 可用就走 API；不行就退到浏览器自动化；再不行就停在 assisted 或 manual handoff。
如果登录公众号网页是必需步骤，就暂停等我登录后继续。
```

## Multi-platform distribution

```text
公众号草稿保存后，帮我转小红书和即刻。
小红书要轮播图 + 文案，即刻写成同行聊天的口吻。
朋友圈也帮我写一条，3-5 行就够了。
```

## HTML theme selection

```text
这篇文章用 md2wechat 的 ocean-calm 主题转 HTML，适合技术分析类内容。
转完后预览确认封面、摘要、配图路径都对得上 Markdown 源文件。
```

## Article design selection (requires Pencil MCP)

```text
这篇 AI 文章用科技风格排版，Dark 模式。
如果 Pencil MCP 没配置就跳过排版，直接用 md2wechat 的主题转 HTML。
```

```text
这篇文化类文章用典雅风格排版，Light 模式。排版完成后截图给我确认。
```

```text
帮我自动选排版风格，根据文章内容来。
```

## What good output leaves behind

The result should leave behind:

- one article workspace directory
- one `source.md`
- one `brief.md` with strategic clarification record
- one `research.md` with verified facts / working inferences / open questions
- one canonical formatted markdown file (normalization checklist applied)
- one HTML file ready for WeChat (rendered via md2wechat ai mode)
- one cover image (900x383px at 2x)
- resolved inline image paths (each passing two-tier evaluation)
- one `manifest.json` with `outputs.wechat.*`
- one saved draft or a clearly reported fallback level
- *(if Phase 8 triggered)* platform copies and manifest entries for requested platforms

## What to avoid

- starting prose before the source packet and angle are stable
- starting design polish before the article angle is stable
- rewriting from thin metadata when full body text is required
- copying a named writer too literally
- blurring verified fact and inference
- decorative images that do not improve understanding
- skipping the normalization checklist or writing framework self-check
- using external API mode for HTML conversion when ai mode is available
- direct live publishing when the request says draft only
