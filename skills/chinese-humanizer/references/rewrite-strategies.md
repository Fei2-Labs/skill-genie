# 改写策略 / Rewrite Strategies

Operations, not word swaps. AI 味 is not a single-word problem — it is "词承担了本该由事实承担的工作". The fix is to redistribute the work back to facts, scenes, subjects, and rhythm.

## Core operations

1. **删 (delete)** — throat-clearing, redundant connectors, empty evaluations, generic upbeat endings. If a sentence only restates the previous one in new words, merge or cut.
2. **降维 (de-escalate)** — narrow oversized claims. "改变行业" → "先影响客服和内容生产". Keep the judgment, shrink the scope to what the evidence supports.
3. **具体化 (concretize)** — replace abstract nouns with action chains. "提升协同效率" → "谁少发了几次消息、谁少切了几个系统、哪一步不再手工对账". Detail can be a role, a time, an action, a constraint — not necessarily a number.
4. **重组 (restructure)** — break 三段式 / 总分总 into a real problem chain: 为什么用 → 能解决什么 → 难点在哪 → 判断条件是什么. Vary sentence and paragraph length by information density, not randomly.
5. **换语体 (re-register)** — match the genre's register. Keep necessary formality in technical/legal/academic/business text. Do not convert formal text to chat.
6. **标注需补 (mark gaps)** — when the draft is too empty to fix without facts, output a 保守可用版 plus `[需补充：具体数据/案例/来源]`. Never invent to fill.

## Five proven methods (with failure contrast)

### 方法 1：宏大判断 → 可验证事实
- ❌ 失败（只换口语）："说实话这平台挺好用，能帮企业少走弯路。"
- ✅ 成功："这款协作平台主要解决三件事：任务分散在聊天软件里、审批进度没人跟、会议纪要没人整理。AI 目前只放在两个环节：自动生成纪要，提醒负责人补齐下一步。它不是数字化转型引擎，更像一个减少漏事的工作台。"

### 方法 2：伪权威 → 明确来源，无来源标风险
- 原文："多位行业专家认为，生成式 AI 将成为未来企业竞争的关键变量。"
- ✅ 有来源版：`麦肯锡 2023 年报告估算，生成式 AI 每年可能带来 2.6–4.4 万亿美元经济价值。`
- ✅ 无来源版：`至少在客服、代码生成和内容生产这几个环节，生成式 AI 已经开始改变企业成本结构。`
- ❌ 失败："很多人都觉得 AI 以后会非常重要。"（仍空，且没收窄）

### 方法 3：保留体裁，不乱加人味（技术文档）
- 原文："本功能旨在为用户提供更加便捷、高效和智能化的配置体验。"
- ❌ 失败："这个功能说白了就是让你别被配置折磨，点几下就搞定。"
- ✅ 成功："这个功能用于批量创建配置项。用户上传 CSV 后，系统校验字段、显示错误行，确认后一次性写入配置中心。"
- 关键：技术文档的人味是清楚、准确、可操作，不是口语。

### 方法 4：作者位置替代安全中立腔（知乎）
- 原文："是否转行产品经理，需要从个人兴趣、能力结构、行业趋势等多维度综合判断。"
- ❌ 失败："我觉得转不转产品经理这事吧，还是看你自己。"
- ✅ 成功："我不建议只因为'门槛低'就转。这个岗位最消耗人的不是画原型，而是每天处理不完整的信息：老板一句方向、研发一句排期、销售一个临时需求。你如果讨厌反复沟通，转过去大概率更痛苦。"

### 方法 5：改结构，而不是只改句子
- 原文："随着 AI 快速发展，越来越多企业关注 AI 客服。一方面提升效率，另一方面降低成本，因此前景广阔。"
- ✅ 成功："客服团队最先愿意用 AI，不是因为它'先进'，而是夜间、节假日、高峰期的问题太重复。订单状态、退款进度、发票抬头，这些不该一直占人工坐席。真正难的是边界：什么时候转人工、怎么记录上下文、出错谁负责。能不能省钱，最后取决于这些细节。"

## 八种失败方法（不要做）

1. 简单同义词替换（重要意义→重大价值）——表皮动了，结构没动。
2. 强行口语化——把正式体裁改轻浮。
3. 故意加错别字——只降专业性，不增真实感。
4. 加假个人感（我觉得/说实话/老实讲/让我震惊的是）——最容易露馅。
5. 过度缩短句子——连续短句变"制造金句"（dramatic fragmentation）。
6. 为绕检测改事实表述——伤准确性，最危险。
7. 把正式文本改成社媒口吻——体裁错位。
8. 用检测器分数代替编辑质量——把产品带进逃检优化。
