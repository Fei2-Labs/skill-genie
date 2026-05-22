# skill-genie

[![Last commit](https://img.shields.io/github/last-commit/clarezoe/skill-genie)](https://github.com/clarezoe/skill-genie/commits/main)
[![Stars](https://img.shields.io/github/stars/clarezoe/skill-genie)](https://github.com/clarezoe/skill-genie/stargazers)
[![Issues](https://img.shields.io/github/issues/clarezoe/skill-genie)](https://github.com/clarezoe/skill-genie/issues)

<p align="center">
  <a href="#english">English</a> | <a href="#中文">中文</a> | <a href="#日本語">日本語</a>
</p>

---

<a name="english"></a>

A curated collection of reusable skills and workflows that turn everyday tasks into fast, repeatable actions.

## Why this exists

Most personal automation fails because the best methods live in scattered notes. This repo turns those methods into clear, reusable skills that are easy to find, run, and improve.

## What's inside

- Skill folders with their own `SKILL.md` and supporting assets.
- References and scripts that keep each skill practical and maintainable.

## Featured skills

- [`omnidebug-autopilot`](./omnidebug-autopilot): Autonomous root-cause debugging workflow with deterministic browser reproduction, artifact capture, and fix verification scripts.
- [`close-loop`](./close-loop): End-of-session ship-and-memory workflow with autonomous strategy selection (`safe`, `balanced`, `openclaw`/`adaptive`), ALMA-inspired evaluation, and machine-readable JSON output.
- [`ai-csuite`](./ai-csuite): Script-backed AI executive debate workflow that generates stage-aware strategic recommendations, CEO briefs, and decision artifacts.
- [`foxcode-openclaw`](./foxcode-openclaw): Configure Foxcode AI models in OpenClaw with interactive setup, status monitoring, and validation tools. Supports 5 endpoints and 3 Claude models.
- [`handoff`](./handoff): Create a compact handoff with tracked lifecycle metadata, `CURRENT` pointer routing, and `INDEX.md` summaries for low-cost continuation.
- [`handoff-receiver`](./handoff-receiver): Resume work from a prior handoff by validating repo state, reconciling context, and continuing the next actionable step safely.
- [`session-handoff`](./session-handoff): Summarize the current session into a precise handoff file with tracked states, `CURRENT` pointer routing, and `INDEX.md` metadata for low-token continuation.
- [`research-to-wechat`](./research-to-wechat): End-to-end article orchestration that turns topics, URLs, and transcripts into researched Markdown, visual assets, WeChat-ready HTML, and a saved draft.
- [`wechat-compliance-check`](./wechat-compliance-check): Scan WeChat articles for 100+ sensitive words across 8 categories (VPN tools, political, reverse-engineering, grey market, etc.) and auto-rewrite violations before publishing.
- [`aegis-protocol`](./aegis-protocol): High-confidence code security review workflow for changed code, using modern threat-informed methodologies with strict false-positive filtering.
- [`psychology-master`](./psychology-master): Psychology expertise for human mind optimization, learning science, habits, motivation, and behavioral change.
- [`refactor-agents-md`](./refactor-agents-md): Refactor AGENTS.md files into a minimal root file plus topic-specific follow-up docs using progressive disclosure.
- [`npm-publish`](./npm-publish): Publish NPM packages with authentication and release flow support for a clean registry upload.
- [`wordpress-vps-install`](./wordpress-vps-install): Fresh-VPS WordPress bootstrap workflow for container setup, DB wiring, WP-CLI install, and public-site verification.
- [`stalwart-dokploy-resend-relay`](./stalwart-dokploy-resend-relay): Deploy Stalwart Mail Server on Dokploy with a Resend relay default for environments where outbound SMTP port 25 is blocked.

## skillgenie CLI

Install and manage skills across Claude Code and OpenClaw from this repo.

```bash
# List available skills
./skillgenie list

# Show install status per runtime
./skillgenie status

# Install one skill (auto-detects runtimes)
./skillgenie install research-to-wechat

# Install to a specific runtime
./skillgenie install research-to-wechat --claude      # Claude Code only
./skillgenie install research-to-wechat --openclaw    # OpenClaw only
./skillgenie install research-to-wechat --global      # both

# Install all skills
./skillgenie install --all --global

# Preview without executing
./skillgenie install --all --dry-run

# Update (re-install) a skill
./skillgenie update close-loop
```

Backends: Claude Code uses `openskills` (must be installed); OpenClaw uses direct file copy.

## Skill layout

Each skill folder should contain:

- `SKILL.md` for the main execution workflow
- `README.md` for quick orientation
- `CHANGELOG.md` for skill-specific release history when needed
- `LICENSE` when the skill is intended to be published independently
- `references/` for source docs and deeper notes
- `docs/` for skill-specific publishing or usage documentation
- `assets/` for templates and reusable artifacts
- `scripts/` only when automation clearly reduces manual work

## How to use

1. Browse a skill folder that matches your task.
2. Read the skill `README.md` for scope and files.
3. Open `SKILL.md` and follow the workflow.
4. Use included references, scripts, and templates when needed.

## Add a new skill

- Keep it focused on a single job.
- Document the happy path and edge cases in `SKILL.md`.
- Include scripts or assets when they remove manual work.

## Principles

- Small, composable skills over monoliths.
- Clear steps over clever tricks.
- Practical defaults with room to customize.

---

<a name="中文"></a>

## 简介

一个精心策划的可复用技能和工作流集合，将日常任务转化为快速、可重复的操作。

## 为什么存在

大多数个人自动化失败是因为最好的方法散落在各种笔记中。这个仓库将这些方法转化为清晰、可复用的技能，易于查找、运行和改进。

## 内容

- 技能文件夹，包含各自的 `SKILL.md` 和支持资源
- 参考文档和脚本，保持每个技能实用且可维护

## 精选技能

- [`omnidebug-autopilot`](./omnidebug-autopilot): 自主根因调试工作流，包含确定性浏览器复现、工件捕获和修复验证脚本
- [`close-loop`](./close-loop): 会话结束时的交付和记忆工作流，包含自主策略选择
- [`ai-csuite`](./ai-csuite): 脚本支持的 AI 高管辩论工作流
- [`foxcode-openclaw`](./foxcode-openclaw): 在 OpenClaw 中配置 Foxcode AI 模型，支持交互式设置、状态监控和验证工具
- [`handoff`](./handoff): 生成轻量 handoff，并维护状态元数据、`CURRENT` 指针与 `INDEX.md` 摘要，便于低成本续接
- [`handoff-receiver`](./handoff-receiver): 通过验证仓库状态、对齐上下文并继续下一步，安全接手上一轮 handoff
- [`session-handoff`](./session-handoff): 将当前会话整理为精确的 handoff 文件，并维护状态、`CURRENT` 指针与 `INDEX.md`，便于低 token 成本续接
- [`research-to-wechat`](./research-to-wechat): 面向公众号内容生产的端到端文章编排 skill，可把选题、链接和字幕转成深度研究文章、配图、HTML 与草稿箱结果
- [`wechat-compliance-check`](./wechat-compliance-check): 扫描公众号文章中 8 大类 100+ 敏感词（翻墙工具、政治敏感、逆向破解、灰产等），自动改写为安全表述
- [`aegis-protocol`](./aegis-protocol): 高置信度代码安全审查工作流，基于现代威胁建模方法论，严格过滤误报
- [`psychology-master`](./psychology-master): 心理学能力，用于人类思维优化、学习科学、习惯、动机与行为改变
- [`refactor-agents-md`](./refactor-agents-md): 将 AGENTS.md 精简为最小根文件，并按主题拆分到后续文档
- [`npm-publish`](./npm-publish): 支持认证与发布流程的 NPM 包发布 skill
- [`linuxdo-application`](./linuxdo-application): 通过自适应问卷和规则感知生成，为 Linux.do 注册撰写高通过率、去 AI 化的中文申请小作文
- [`wordpress-vps-install`](./wordpress-vps-install): 面向新 VPS 的 WordPress 初始化工作流，包含容器配置、数据库连接、WP-CLI 安装与线上验证
- [`stalwart-dokploy-resend-relay`](./stalwart-dokploy-resend-relay): 在 Dokploy 上部署 Stalwart 邮件服务器，并默认通过 Resend 中继处理受限的 25 端口外发

## 技能结构

每个技能文件夹应包含：

- `SKILL.md` - 主要执行工作流
- `README.md` - 快速入门
- `CHANGELOG.md` - 需要时记录该 skill 自己的发布历史
- `LICENSE` - 当该 skill 需要独立发布时使用
- `references/` - 源文档和深入笔记
- `docs/` - 该 skill 自己的发布或使用文档
- `assets/` - 模板和可复用工件
- `scripts/` - 仅当自动化明显减少手动工作时

## 使用方法

1. 浏览匹配你任务的技能文件夹
2. 阅读技能 `README.md` 了解范围和文件
3. 打开 `SKILL.md` 并按照工作流操作
4. 需要时使用包含的参考、脚本和模板

## 添加新技能

- 专注于单一任务
- 在 `SKILL.md` 中记录正常路径和边缘情况
- 当脚本能减少手动工作时包含它们

## 原则

- 小而可组合的技能优于单体
- 清晰的步骤优于巧妙的技巧
- 实用的默认值，留有定制空间

---

<a name="日本語"></a>

## 概要

日常タスクを迅速かつ反復可能なアクションに変える、再利用可能なスキルとワークフローのキュレーションコレクション。

## なぜ存在するか

ほとんどの個人自動化は、最良の方法が散在するメモにあるため失敗します。このリポジトリは、それらの方法を見つけやすく、実行しやすく、改善しやすい明確で再利用可能なスキルに変えます。

## 内容

- 独自の `SKILL.md` とサポートアセットを持つスキルフォルダ
- 各スキルを実用的で保守しやすくするリファレンスとスクリプト

## 注目のスキル

- [`omnidebug-autopilot`](./omnidebug-autopilot): 決定論的ブラウザ再現、アーティファクトキャプチャ、修正検証スクリプトを備えた自律的ルート原因デバッグワークフロー
- [`close-loop`](./close-loop): 自律戦略選択を備えたセッション終了時のシップ＆メモリワークフロー
- [`ai-csuite`](./ai-csuite): ステージ対応の戦略的推奨、CEOブリーフ、決定アーティファクトを生成するスクリプト支援AI経営陣討論ワークフロー
- [`foxcode-openclaw`](./foxcode-openclaw): インタラクティブセットアップ、ステータス監視、検証ツールを備えたOpenClawでのFoxcode AIモデル設定
- [`handoff`](./handoff): 状態メタデータ、`CURRENT` ポインタ、`INDEX.md` 要約を維持しながら軽量 handoff を作成
- [`handoff-receiver`](./handoff-receiver): 過去の handoff を検証しながら安全に引き継ぎ、次の実行ステップへ進めるワークフロー
- [`session-handoff`](./session-handoff): 現在のセッションを精密な handoff に要約し、状態・`CURRENT`・`INDEX.md` を維持して低コストに再開できるようにする
- [`research-to-wechat`](./research-to-wechat): トピック、URL、字幕から調査済みMarkdown、ビジュアル、WeChat向けHTML、下書き保存までをつなぐ記事オーケストレーションスキル
- [`wechat-compliance-check`](./wechat-compliance-check): WeChat記事の8カテゴリ100+センシティブワードをスキャンし、公開前に自動書き換え
- [`aegis-protocol`](./aegis-protocol): 変更コードの高信頼性セキュリティレビューワークフロー、脅威モデリングベースの手法で誤検知を厳格にフィルタリング
- [`psychology-master`](./psychology-master): 人間の思考最適化、学習科学、習慣、動機づけ、行動変容のための心理学スキル
- [`refactor-agents-md`](./refactor-agents-md): AGENTS.md を最小限のルートファイルとトピック別ドキュメントに再編するスキル
- [`npm-publish`](./npm-publish): 認証と公開フローを支援する NPM パッケージ公開スキル
- [`linuxdo-application`](./linuxdo-application): アダプティブ調査とルール認識テキスト生成により、Linux.do登録用の高合格率・脱AI中国語申請文を作成
- [`wordpress-vps-install`](./wordpress-vps-install): 新規 VPS 向け WordPress 初期セットアップ、DB 接続、WP-CLI インストール、公開確認のワークフロー
- [`stalwart-dokploy-resend-relay`](./stalwart-dokploy-resend-relay): Dokploy 上で Stalwart を配備し、制限された 25 番ポートの送信は Resend リレーを既定にするワークフロー

## スキル構成

各スキルフォルダには以下が含まれます：

- `SKILL.md` - メイン実行ワークフロー
- `README.md` - クイックオリエンテーション
- `CHANGELOG.md` - 必要に応じたスキル単位の更新履歴
- `LICENSE` - スキルを個別公開する場合のライセンス
- `references/` - ソースドキュメントと詳細なメモ
- `docs/` - そのスキル専用の公開・利用ドキュメント
- `assets/` - テンプレートと再利用可能なアーティファクト
- `scripts/` - 自動化が手動作業を明確に削減する場合のみ

## 使い方

1. タスクに合ったスキルフォルダを閲覧
2. スキル `README.md` を読んでスコープとファイルを理解
3. `SKILL.md` を開いてワークフローに従う
4. 必要に応じて含まれるリファレンス、スクリプト、テンプレートを使用

## 新しいスキルを追加

- 単一のジョブに集中
- `SKILL.md` でハッピーパスとエッジケースを文書化
- スクリプトまたはアセットが手動作業を削減する場合に含める

## 原則

- モノリスよりも小さく構成可能なスキル
- 巧妙なトリックよりも明確なステップ
- カスタマイズの余地を持つ実用的なデフォルト
