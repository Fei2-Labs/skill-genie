# 作者声音校准 / Voice Calibration

When the user provides a writing sample (2–3 paragraphs ideal), extract a voice profile and match it. Without a sample, do **not** invent a persona — use restrained, natural, genre-fit Chinese.

## Privacy rule

Use the sample only for the current task. Do not summarize it into a reusable identity profile. Do not carry it across unrelated requests.

## Extract these features

| 特征 | 怎么看 |
| --- | --- |
| 句长偏好 | 偏短句还是长句？长短交错的幅度？ |
| 用词层级 | 偏书面还是偏口语？术语密度？ |
| 第一人称 | 用"我/我们"吗？频率多高？ |
| 标点习惯 | 爱用破折号、括号、省略号还是句号到底？ |
| 转场方式 | 显式连接词，还是语义跳接？ |
| 判断强度 | 敢下结论，还是偏保守？ |
| 余味偏好 | 喜欢收束利落，还是留开放结尾？ |
| 边角习惯 | 有没有可信的小怪癖、口头判断、特定比喻？ |

## Apply

- Match sentence rhythm and register first; tells second.
- **Preserve signs of human writing** — real authors have odd-but-credible details, unresolved contradictions, mild hedges. These are worth more than any "像人词". Do not flatten them.
- Do not over-clean. A perfectly smooth rewrite that erases the author's quirks reads more AI, not less.
- Do not add 第一人称 or 口语 markers (说实话/老实讲/真的/挺/蛮) unless the sample shows them.

## No-sample default

- 体裁内自然化：clarity + specificity + genre register.
- 不主动加个人经历、不主动加强情绪。
- Default to a restrained voice; let the facts and scenes carry the "human" feel.
