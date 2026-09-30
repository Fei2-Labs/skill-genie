---
name: "wechat-compliance-check"
description: "用确定性词库扫描与 Jev 语境、变体判定检查微信公众号文章。保证范围是对当前词库零命中，不承诺通过微信审核。"
license: "MIT"
metadata: {"openclaw":{"homepage":"https://github.com/nicekate/wechat-compliance-check"},"version":"1.1.0","tags":["wechat","compliance","content-safety","chinese-writing"],"hermes":{"tags":["wechat","compliance","content-safety","chinese-writing"]}}
---

# 微信公众号内容合规检查

本技能以代码驱动扫描，不把词库对照交给模型自行完成。它能保证文章
对**当前随技能发布的词库**没有确定性命中，并让 Jev 处理标为
`[CONTEXT]` 的语境和整篇文章的规避表达检查。它**不承诺通过微信审核**：
微信规则不公开且会变化，本技能也不检查图片文字或超出词库范围的平台检测类别。

## 命令

从本文件所在目录确定 `SKILL_DIR`，执行：

```bash
python3 "${SKILL_DIR}/scripts/compliance_scan.py" article.md --json
python3 "${SKILL_DIR}/scripts/compliance_scan.py" article.md --json --no-jev
python3 "${SKILL_DIR}/scripts/compliance_scan.py" --validate-wordlist
```

可用选项：`--wordlist PATH` 指定词库，`--log-dir PATH` 指定原始请求/响应
交换记录目录。默认词库是 `references/sensitive-words.md`。

## 退出码和报告

| 退出码 | 含义 | 交付行为 |
|---:|---|---|
| 0 | `clean`：确定性零命中、语境安全、整文变体通过 | 可继续流程 |
| 1 | `violations`：确定性命中、敏感语境或变体阈值失败 | 必须改写并重新扫描 |
| 2 | `blocked`：缺凭据、Jev 不可用/非法/低置信度、预算超限或需要 Jev | 不得放行 |
| 3 | 词库解析错误 | 不得放行 |

即使 `[ALWAYS]` 命中，扫描器也会列出全部确定性命中；缺少
`TYPESAFE_API_KEY` 不会阻止这些本地命中被报告，但任何需要 Jev 的步骤都
返回 `blocked`。`--no-jev` 仅是离线诊断模式；存在 `[CONTEXT]` 命中时它
绝不能返回 `clean`，也不能替代整文 Jev 检查。

JSON 报告包含 `deterministic_hits`、`context_hits`、`variant_scan`、
`policy_version`、词库和文章哈希、`gaps`。每条命中包含行号、原文片段、
类别、等级、标记、建议替换和段落。请求与响应原样落盘到日志目录，但
报告和错误消息不回显凭据、原始 provider body 或异常文本。

## 词库契约

词库只解析类别标题下 fenced block 内的条目。条目格式严格为：

```text
词 → 替换 | 🔴/🟡/⚠️ | [ALWAYS|CONTEXT|REGEX] 备注
```

坏行、未知等级、重复词、非法正则或未闭合 fenced block 都会以退出码 3
失败，绝不静默跳过。ASCII 匹配不区分大小写；CJK 保持精确匹配；全角
ASCII 会折叠为半角。条目可能带有更新器写入的来源、日期、Jev 分数和运行
ID 元数据。词库现有条目及其可能重叠的子串和宽泛类别标签是源数据，扫描器
逐条报告，不擅自去重或重新解释。

## 判定边界

- `[ALWAYS]` 和 `[REGEX]` 命中直接违规，不交给模型覆盖。
- 每个 `[CONTEXT]` 命中都附带段落和词库备注交 Jev；敏感概率至少 0.50
  时违规。
- 整篇文章只发起一次 Jev 变体检查，识别谐音、拆字、拼音缩写、隐晦指代
  和词库外高风险表述。变体期望分数至少 2.0，或 3–4 级概率至少 0.20
  时违规。
- Jev Score 是 0–4 级的概率加权期望，通常为小数；响应分布必须完整、有限、
  和为 1，并与分数在 provider 四舍五入容差内一致。
- 无凭据、超时、429/529 重试耗尽、401/422、非法 JSON、坏响应或低置信度
  均 `blocked`。文章超预算时报告未覆盖范围，绝不静默截断。

## 自动更新

月度调研 procedure 在 [references/monthly-update.md](references/monthly-update.md)，
政策阈值在 [references/policy.md](references/policy.md)。更新器只接受带来源
URL、日期和**已验证 Jev 分布**的新增条目；不能凭调用者自己填写的
`evidence_score` 绕过验证。它只创建 `auto/wordlist-YYYY-MM` 分支上的增量，
不自动合并 `main` 或发布 ClawHub。
