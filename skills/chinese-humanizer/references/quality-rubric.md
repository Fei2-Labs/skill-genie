# 质量评估与自检 / Quality Rubric & Self-Audit

Score internally 1–5 per dimension. **Do not show the score unless the user asks.** Separate 可读 (readable) from 可信 (credible) — a smooth rewrite that drifted the facts fails.

## 10 dimensions

| 维度 | 评估问题 |
| --- | --- |
| 准确性 accuracy | 是否保留原意，是否引入新事实（必须为零，除非用户提供） |
| 具体性 specificity | 是否减少空话，增加可验证细节（对象/动作/约束），而不是只换词 |
| 体裁一致性 genre fit | 是否符合平台和用途，像该体裁本来该有的中文 |
| 作者声音一致性 voice fit | 有样文时是否像用户本人，而不是统一 AI 编辑腔 |
| 证据密度 evidence density | 判断前有没有事实、案例、数据、边界支撑 |
| 节奏自然度 rhythm | 句长、段落、转折是否按信息密度自然变化 |
| 可发布程度 publishability | 贴出去会不会像模板话，能否直接使用 |
| 克制度 restraint | 是否删掉过度升维、过度情绪、过度解释 |
| 边界感 boundary | 是否标出不确定、限制和风险 |
| 非伪装性 integrity | 是否避免错别字、假口语、假经历、检测规避框架 |

## Self-audit checklist (run before final output)

- [ ] 有没有编造任何事实、数据、来源、经历、机构、日期？
- [ ] 有没有改动用户原本的核心主张？
- [ ] 体裁是否仍然正确，没有跑偏？
- [ ] 正式文本有没有被改得太口语？
- [ ] 还有没有残留的空泛套话？
- [ ] 每个主要判断是否都有证据、来源、具体场景或清晰边界？
- [ ] 结尾是否说了有用的话，而不是上价值？
- [ ] 句长是否过于均匀？
- [ ] 有没有把真实作者的怪癖/犹豫/复杂感一起抹平？
- [ ] 修改说明有没有压过正文？

If any critical item fails (fabrication, genre drift, over-casualization), **revise once** before responding. Fabrication is a hard fail — never ship it.

## Detector-score policy

Detector score (Turnitin / GPTZero / etc.) is at most an external **risk signal**, never the quality target. Research is explicit: detectors are probabilistic,误判低分段，被改写文本本就难判，短/公式化/非英文文本更不稳。Optimizing the score pulls the product toward "逃检优化" and away from "真实性编辑". Optimize for 可发布质量, not score.
