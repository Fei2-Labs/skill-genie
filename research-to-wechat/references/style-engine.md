# Style Engine

Resolve writing style in this order:
1. explicit user instruction
2. preset mode
3. author mode
4. custom brief

Resolve article structure separately from voice:
1. explicit frame request
2. source-type inference
3. preset default

## Structure Router

### `deep-analysis`

use for: thesis-led essays, industry shifts, business models, policy effects, strategic critique

**Structure: 序言 + 四幕（01/02/03/04），8000-12000 字**

| 部分 | 功能 | 占比 |
|------|------|------|
| 序言（无编号） | 故事开头 + 背景 + 论点引出 | 15% |
| **01** | 铺设背景 / 建立框架 | 25% |
| **02** | 核心论述 / 深入分析 | 25% |
| **03** | 转折 / 案例 / 新视角 | 20% |
| **04** | 升华 / 哲学 / 收束 | 15% |

**Opening rule**: 前 700 字必须是故事或场景，不出论点。读者为故事留下，为论点离开。开头的唯一任务是让读者"读进去"。

Opening patterns:
- 人物传记式："2000年，盖茨把皇座交给了鲍尔默……"
- 流行文化式："在漫威宇宙里，贾维斯是……"
- 电影场景式：从一个具体画面切入
- 个人记忆式：自己的相关经历
- 百年孤独式："多年之后……还会想起……"

Opening to thesis transition: 故事（500-800字）→ 一句话转折（"但就在这个月……"）→ 论点（1-2句）→ 进入正文。

**Sentence rhythm**:
- 长句铺展（40-60字）建立信息量 → 短句收束（15字以内）制造冲击
- 排比句制造气势（三段以上，最后一段要有"升级"）
- 破折号（——）用在关键判断、揭示、转折前制造停顿和戏剧张力
- 书面/分析语言 70% + 口语/网络语言 25% + 圈子术语 5%

**Data density**: 每 200-300 字至少一个数据点。

| 数据策略 | 用法 |
|----------|------|
| 阶梯式 | "450万 → 5000万 → 7亿美元" 制造递进冲击 |
| 对比式 | "从90%降到20%" 强化变化幅度 |
| 锚定式 | "2000万DAU，行业前五" 给参照系 |
| 个人化 | "到手1万，公司实际支付1.8万" 制造共情 |

数据从不孤立出现，必须紧跟解读。大数字用加粗突出。

**Cross-cultural references**: 每篇 5-8 个，混合影视/中国古典/西方历史/商业案例/经济学。每个引用必须承担论证功能，不是装饰。

**Golden sentences**: 每篇 3-5 句截图级金句。

| 类型 | 示例 |
|------|------|
| 对仗式 | "敲门的AI，关门的大厂" |
| 反转式 | "补贴一停，感激清零" |
| 化用式 | "有人辞官归故里，有人星夜赶考场" |
| 定义式 | "一家企业的现状，是所有过去战略选择的总和" |

Position: 序言结尾（定调）、每章结尾（收束）、全文结尾（mic drop）。

**Emotional arc**: 好奇/兴奋（序言）→ 认同/共鸣（01）→ 焦虑/紧张（02）→ 释然/启发（03）→ 升华/回味（04）。

**Chapter hooks**: 每章结尾必须有一句钩子拉向下一章。

**Paragraph rules**: 每段 2-4 句 ≤150 字，关键判断独立成段。章节用 01/02/03/04 编号，序言不编号。加粗用于核心论点、金句、关键数据。「」用于概念术语。

---

### `tutorial`

use for: tools, workflows, installation, operational playbooks, "how to" content

**Structure: 六段式，2000-4000 字**

```
先看结果（成品截图 + 核心数据 + 体验链接）
→ 一、核心概念（一句话定义 + 表格映射）
→ 二、操作步骤（分步 + 代码块 + 配图标记）
→ 三、实战演示（分阶段 + 表格 + 人机协作边界）
→ 四、拿走即用（安装命令 + 使用方式表格）
→ 写在最后（升华 + 自然CTA）
```

**Result-first rule**: 第一部分必须直接展示成品，让读者在 10 秒内判断"这篇值得看"。不解释"这是什么"，直接展示"你会得到什么"。

**Visual rhythm** (教程的视觉密度 > 深度长文):

| 元素 | 频率 |
|------|------|
| 表格 | 每 300-500 字至少一个 |
| 代码块 | 每个操作步骤一个 |
| 配图标记 | 每 500-800 字一处 |
| 分阶段标题 | 实战部分每阶段一个 |

**Operation steps format**: 每步包含一句话目的说明 + 可复制命令 + 配图标记 + 可选踩坑提示。步骤间有因果关系（"完成后你会看到xxx"）。

**Practical demo**: 分阶段叙事，每阶段用表格展示（Agent/任务/产出），明确展示人机协作边界——哪些是 AI 做的，哪些是人做的。

**Language**: 书面/口语比 50/45（比深度长文更口语化），段落 1-3 句 ≤100 字。

---

### `newsletter`

use for: multi-topic roundups, curated briefs, weekly updates
frame: top line -> short sections -> quick takeaways -> next action or links

### `case-study`

use for: launches, campaigns, company moves, product decisions, growth experiments
frame: background -> problem -> options -> action -> result -> lessons

### `commentary`

use for: reactions, critiques, and judgment-heavy essays
frame: thesis -> support -> counterpoint -> judgment

## Preset Catalog

- `deep-analysis`
  use: technology shifts, industry structure, business models, policy effects
  avoid: low-evidence opinion pieces
  frame: question, mechanism map, evidence, tensions, synthesis

- `explainer`
  use: concept unpacking, framework teaching, complex topics for broad readers
  avoid: insider shorthand and unexplained jargon
  frame: definition, why it matters, core parts, example, takeaway

- `tutorial`
  use: tools, workflows, operations, playbooks
  avoid: abstract discussion with no actionable path
  frame: result, concept, setup, steps, demo, checklist

- `case-study`
  use: launches, campaigns, company stories, growth moves, failures
  avoid: evidence fragments without chronology
  frame: background, problem, options, action, result, lessons

- `commentary`
  use: reactions, critiques, strategic judgments, trend takes
  avoid: fence-sitting and unsupported rhetoric
  frame: thesis, support, counterpoint, judgment

- `narrative`
  use: 人物、品牌、经历、历史转折
  avoid: report-style dumping
  frame: opening scene, conflict, development, insight, return

- `trend-report`
  use: market scans, sector outlooks, platform change, AI tracking
  avoid: presenting weak signals as settled facts
  frame: current state, fresh signals, scenarios, implications

- `founder-letter`
  use: strategic updates, principle statements, roadmap framing, culture writing
  avoid: generic PR polish
  frame: why now, what changed, decisions, principles, next move

- `newsletter`
  use: weekly roundups, curated briefs, multi-topic updates
  avoid: overlong transitions and one-thread essays
  frame: top line, short sections, quick takeaways, links or actions

## Author Mode

When the user names a writer, build an author card from 1 to 3 representative pieces.

Extract and store:
- `voice`
- `reader_distance`
- `paragraph_cadence`
- `opening_pattern`
- `argument_pattern`
- `evidence_habit`
- `signature_devices`
- `taboos`
- `safe_boundary`

Apply the author card with these rules:
- keep the cadence, lens, and evidence preference
- soften highly distinctive metaphors and sentence signatures
- inject the user's topic, reader, and required depth
- verify the result feels inspired, not impersonated
- never inherit false intimacy, invented reporting access, or signature claims that the current evidence cannot support

## Custom Brief

If the style is user-defined, ask for:
- target reader
- tone
- structural preference
- evidence density
- banned expressions

Compress the answer into a short internal brief before drafting.

## Article Normalization

These rules apply regardless of style mode. They run after drafting and before
the refinement handoff. The authoritative detailed version lives in
[execution-contract.md](execution-contract.md) Phase 4; this is the compact
reference.

### Source Artifact Removal
- strip AI-generated citation tags (`[oai_citation:...]`, `[source:...]`)
- strip numbered in-text citations and trailing reference lists
- convert useful citation content to inline attribution
- strip scraped UI: navigation, footers, cookie banners, "share" blocks

### Format Repair
- fix unclosed bold/italic/code markers
- normalize smart quotes, dashes, and ellipsis
- strip invisible Unicode (zero-width spaces, joiners, BOM)
- standardize Markdown tables: header + separator + consistent columns
- fix unclosed or redundant code blocks

### Content Conversion
- convert LaTeX/MathJax/`$$`-delimited math to plain-text descriptions
- convert flowcharts, mind maps, and ASCII diagrams to ordered lists or
  structured descriptions
- ensure exactly one H1, search-friendly, at article start
- verify heading hierarchy (no skipped levels)

### Integrity Rule
- never silently remove substantive paragraphs
- preserve all data points and named sources from original material
- log any structural removal in the evidence ledger

## Writing Checklists

### deep-analysis checklist (出稿前自检)

- [ ] 标题是否制造了认知冲突？
- [ ] 开头 700 字是否全是故事/场景？
- [ ] 全文是否在 8000-12000 字之间？
- [ ] 是否有 01/02/03/04 四幕结构？
- [ ] 每 200-300 字是否有一个数据点？
- [ ] 是否有 5+ 个跨文化引用？
- [ ] 是否有一个贯穿全文的核心隐喻？
- [ ] 情感弧线是否有起伏？
- [ ] 是否有 3-5 句截图级金句？
- [ ] 每章结尾是否有钩子拉向下一章？
- [ ] 结尾是否有升华（不是总结）？
- [ ] 段落是否都在 150 字以内？

### tutorial checklist (出稿前自检)

- [ ] 第一部分是否是"先看结果"？（成品 + 数据 + 链接）
- [ ] 读者能否在 10 秒内判断"这篇值得看"？
- [ ] 核心概念是否用一句话说清楚了？
- [ ] 每个操作步骤是否有可复制的命令？
- [ ] 是否有完整的实战案例走完全流程？
- [ ] 是否有"拿走即用"的快速安装命令？
- [ ] 人机协作的边界是否清晰？
- [ ] 表格数量是否够多？（至少 3-4 个）
- [ ] 配图标记是否够多？（至少 4-6 处）
- [ ] 字数是否在 2000-4000 字之间？
- [ ] 结尾是否有自然的 CTA？

## Writing Prohibitions

Regardless of frame or style mode:

**Language prohibitions:**
- 不说"笔者""本文将介绍""今天给大家分享"
- 不用"震惊""竟然""难以置信"等营销号词
- 不堆砌专业术语
- 不用感叹号表达情绪（用句子本身制造冲击）
- 不过度使用 emoji（全文最多 0-2 个）
- 不写"总结一下"之类的段落

**Content prohibitions:**
- 不以论点开头（故事/场景/结果先行）
- 不写空洞的感慨和鸡汤
- 论点不能没有故事/案例支撑
- 数据不能没有解读
- 类比不能只是装饰（必须承担论证功能）
- 不硬 CTA（不说"点赞关注转发"）
- 不自夸（"这可能是最全面的分析"）
- 不写万金油式的建议（"要拥抱变化""要持续学习"）

## Honesty Guardrails

Regardless of style:
- do not claim interviews, field tests, or long research timelines unless the source packet proves them
- keep human and AI contribution statements truthful
- if evidence is partial, prefer a scoped claim over theatrical certainty
