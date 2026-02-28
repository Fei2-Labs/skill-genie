# close-loop

High-signal end-of-session memory and shipping workflow for users, LLMs, and autonomous bots.

<p align="center">
  <a href="#english">English</a> | <a href="#中文">中文</a> | <a href="#日本語">日本語</a>
</p>

---

<a name="english"></a>

## Purpose

`close-loop` turns session wrap-up into a deterministic operating procedure:

1. close repo/task state cleanly,
2. produce reliable memory updates,
3. apply low-risk self-improvements,
4. queue publishable artifacts.

It is designed for low human overhead and supports autonomous mode selection.

## Who should use this

- User: says `wrap up`, `close session`, `end session`, or `/wrap-up`.
- LLM agent: executes the 4 phases and emits both human + JSON artifacts.
- `openclaw` bot: runs the adaptive strategy path (`openclaw` canonical mode; `adaptive` alias).

## Entry points

- Main workflow: `SKILL.md`
- Policy and mode logic: `components/01-design-principles.md`
- Ship actions: `components/02-phase-1-ship-state.md`
- Memory engine: `components/03-phase-2-memory.md`
- Output contract: `components/04-phase-3-4-and-output.md`
- Output template: `assets/templates/wrap-report-template.md`
- Framework references: `references/memory-frameworks.md`

## Quick run

1. Trigger with `wrap up` or equivalent phrase.
2. Apply action gates and auto-select strategy mode.
3. Run phases in strict order:
   - Phase 1: Ship State
   - Phase 2: Consolidate Memory
   - Phase 3: Review and Apply Improvements
   - Phase 4: Publish Queue
4. Emit two outputs:
   - Artifact A: human-readable report
   - Artifact B: machine-readable JSON

## Strategy modes

Supported mode inputs:

- `safe`
- `balanced`
- `openclaw`
- `adaptive` (alias; normalized to `openclaw`)

Canonical output mode values:

- `safe`, `balanced`, `openclaw`

Mode intent:

- `safe`: deterministic and conservative; static checks only.
- `balanced`: quality/speed compromise; bounded dynamic checks.
- `openclaw`: adaptive archive exploration with bounded autonomous retries.

## Auto-selection behavior

`close-loop` compares all strategies before choosing:

1. run static replay for `safe`, `balanced`, `openclaw`,
2. compute score: `strategyScore = utilityGain - riskPenalty - costPenalty`,
3. select highest non-violating strategy,
4. keep alternatives in output.

Tie-break rule:

- if margin is < 5%, prefer lower-risk strategy.

Human interaction policy:

- no manual mode question by default,
- ask only when irreversible external actions are policy-ambiguous.

## Memory persistence and retrieval

Memory model:

- working (ephemeral),
- episodic,
- semantic,
- procedural.

Write pipeline:

1. extract candidates,
2. verify provenance/dedupe/contradictions,
3. run static checks,
4. apply score/confidence/TTL/sensitivity gates,
5. write only accepted records.

Persistence targets:

- Native IDE memory store if available.
- If native memory is unavailable, persist session memory under:
  - `docs/memory/<YYYY-MM-DD_HHMM>-session.md`
- Project rule/config memory may also update:
  - `CLAUDE.md`
  - `.claude/rules/*`
  - `CLAUDE.local.md` (private/local context)

How the model reaches memory in future runs:

- by reading persisted files and/or host-provided native memory injection.
- `close-loop` itself is policy; persistence layer determines storage backend.

## Safety model

- Action gates for `commit`, `push`, `deploy`, `publish`.
- Prompt-injection and poisoning resistance in memory candidate filtering.
- Contradictions are not overwritten; conflicting records become `needs-review`.
- `openclaw` uses bounded reflection retries and cost/token budgets.

## Required output contract

Artifact A (human report sections):

1. Ship State
2. Mode Decision
3. Memory Writes
4. Findings (applied)
5. No action needed
6. Publish queue
7. Blocked items

Artifact B (JSON) includes:

- selected strategy input + canonical strategy
- candidate mode comparison
- memory evaluation and archive update
- safety block
- KPIs (noise, reuse, correction, precision, token overhead, cost per useful write, decision confidence)

Use:

- `assets/templates/wrap-report-template.md`

## Recommended bot behavior (`openclaw`)

For long or shifting tasks:

1. normalize `adaptive` to `openclaw`,
2. run static baseline first,
3. run dynamic checks only after static pass,
4. promote archive candidate only if utility and efficiency both improve,
5. fallback to `balanced` or `safe` on repeated failures.

## Troubleshooting

- No memory updates appear:
  - check provenance/score/TTL/sensitivity gates; rejected writes should show in report.
- Mode seems too conservative:
  - inspect `modeSelection` penalties and `decisionConfidence`.
- Memory cost too high:
  - inspect `retrievedTokenSize`, `endToEndMemoryCost`, and `costPerUsefulWrite`.
- Conflicting memory persists:
  - review `needs-review` records and evidence links before promotion.

---

<a name="中文"></a>

## 简介

高信号会话结束记忆和交付工作流，适用于用户、LLM 和自主机器人。

## 目的

`close-loop` 将会话收尾转化为确定性操作流程：

1. 干净地关闭仓库/任务状态
2. 生成可靠的记忆更新
3. 应用低风险自我改进
4. 排队可发布工件

## 适用人群

- 用户：说 `wrap up`、`close session`、`end session` 或 `/wrap-up`
- LLM 代理：执行 4 个阶段并输出人类 + JSON 工件
- `openclaw` 机器人：运行自适应策略路径

## 策略模式

支持的模式输入：

- `safe` - 确定性和保守；仅静态检查
- `balanced` - 质量/速度折衷；有界动态检查
- `openclaw` - 自适应归档探索，有界自主重试
- `adaptive`（别名；规范化为 `openclaw`）

## 记忆持久化和检索

记忆模型：
- 工作记忆（短暂）
- 情景记忆
- 语义记忆
- 程序记忆

持久化目标：
- 原生 IDE 记忆存储（如果可用）
- 如果原生记忆不可用，持久化到：`docs/memory/<YYYY-MM-DD_HHMM>-session.md`

## 安全模型

- `commit`、`push`、`deploy`、`publish` 的操作门
- 记忆候选过滤中的提示注入和投毒抵抗
- 矛盾不被覆盖；冲突记录变为 `needs-review`
- `openclaw` 使用有界反射重试和成本/令牌预算

## 故障排除

- 没有记忆更新出现：检查来源/分数/TTL/敏感性门；拒绝的写入应在报告中显示
- 模式似乎太保守：检查 `modeSelection` 惩罚和 `decisionConfidence`
- 记忆成本太高：检查 `retrievedTokenSize`、`endToEndMemoryCost` 和 `costPerUsefulWrite`
- 冲突记忆持续：在提升前审查 `needs-review` 记录和证据链接

---

<a name="日本語"></a>

## 概要

ユーザー、LLM、自律ボット向けの高信号セッション終了メモリおよび出荷ワークフロー。

## 目的

`close-loop` はセッションのまとめを決定論的オペレーティング手順に変えます：

1. リポ/タスク状態をクリーンにクローズ
2. 信頼性の高いメモリ更新を生成
3. 低リスクの自己改善を適用
4. 公開可能なアーティファクトをキュー

## 対象ユーザー

- ユーザー：`wrap up`、`close session`、`end session`、または `/wrap-up` と言う
- LLM エージェント：4 つのフェーズを実行し、人間 + JSON アーティファクトを出力
- `openclaw` ボット：適応戦略パスを実行

## 戦略モード

サポートされるモード入力：

- `safe` - 決定論的で保守的；静的チェックのみ
- `balanced` - 品質/速度の妥協；制限付き動的チェック
- `openclaw` - 制限付き自律リトライでの適応アーカイブ探索
- `adaptive`（エイリアス；`openclaw` に正規化）

## メモリ永続化と取得

メモリモデル：
- ワーキング（一時）
- エピソード
- セマンティック
- 手続き

永続化ターゲット：
- ネイティブ IDE メモリストア（利用可能な場合）
- ネイティブメモリが利用できない場合、`docs/memory/<YYYY-MM-DD_HHMM>-session.md` に永続化

## セーフティモデル

- `commit`、`push`、`deploy`、`publish` のアクションゲート
- メモリ候補フィルタリングにおけるプロンプトインジェクションおよびポイズニング耐性
- 矛盾は上書きされない；競合レコードは `needs-review` になる
- `openclaw` は制限付きリフレクションリトライとコスト/トークン予算を使用

## トラブルシューティング

- メモリ更新が表示されない：出典/スコア/TTL/感度ゲートをチェック；拒否された書き込みはレポートに表示されるはず
- モードが保守的すぎる：`modeSelection` ペナルティと `decisionConfidence` を検査
- メモリコストが高すぎる：`retrievedTokenSize`、`endToEndMemoryCost`、`costPerUsefulWrite` を検査
- 競合メモリが持続：`needs-review` レコードと証拠リンクを昇格前にレビュー
