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

## Skill layout

Each skill folder should contain:

- `SKILL.md` for the main execution workflow
- `README.md` for quick orientation
- `references/` for source docs and deeper notes
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

## 技能结构

每个技能文件夹应包含：

- `SKILL.md` - 主要执行工作流
- `README.md` - 快速入门
- `references/` - 源文档和深入笔记
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

## スキル構成

各スキルフォルダには以下が含まれます：

- `SKILL.md` - メイン実行ワークフロー
- `README.md` - クイックオリエンテーション
- `references/` - ソースドキュメントと詳細なメモ
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
