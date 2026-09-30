# wechat-compliance-check

微信公众号文章的确定性敏感词扫描与 Jev 语境检查。

## 保证边界

扫描器保证的是：对当前发布的 `references/sensitive-words.md`，
`[ALWAYS]`/`[REGEX]` 零命中；每个 `[CONTEXT]` 命中都经过 Jev 安全语境
判定；并且整篇文章的规避表达检查通过。它**不保证通过微信审核**。
微信审核规则不公开并会变化，本技能不覆盖图片文字，也不替代平台审核。
词库中的重叠词和宽泛分类标签作为源数据保留，扫描器逐条报告。

## 使用

```bash
python3 scripts/compliance_scan.py article.md --json
python3 scripts/compliance_scan.py article.md --json --no-jev
python3 scripts/compliance_scan.py --validate-wordlist
```

退出码：`0` clean，`1` violations，`2` blocked，`3` 词库解析错误。
缺少 `TYPESAFE_API_KEY`、Jev 响应非法、低置信度或文本超预算都会
`blocked`，不会放行。`--no-jev` 只用于离线诊断，存在上下文命中时不会
返回 clean，也不能绕过整文检查。

原始 Jev 请求和响应按运行记录到日志目录；输出不会打印凭据、原始 provider
body 或异常文本。默认日志目录为文章旁的 `.wechat-compliance-logs/`，也可用
`--log-dir` 或 `COMPLIANCE_LOG_DIR` 指定。

## 月度更新

候选条目由月度 procedure 调研并取得来源 URL、日期和已验证 Jev 分布后，
通过 `scripts/update_wordlist.py` 以只增不删方式写入。更新器拒绝删除或修改
现有条目、无来源、低于证据阈值、未经验证的 `evidence_score` 和新增
`[REGEX]`。月度任务只推送专用 `auto/wordlist-YYYY-MM` 分支；合并和
ClawHub 发布仍需人工操作。详见 `references/monthly-update.md`。
