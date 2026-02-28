# ai-csuite

Script-backed AI C-Suite skill for structured strategic decisions.

<p align="center">
  <a href="#english">English</a> | <a href="#中文">中文</a>
</p>

---

<a name="english"></a>

## What this skill does

- Builds a stage-aware executive roster for SaaS teams.
- Runs a multi-round debate with role-based positions.
- Produces a structured `CEO BRIEF` and `CEO DECISION`.
- Validates output shape and scans the skill for publish-time safety checks.

## Included files

- `SKILL.md`: prompt workflow and operating rules.
- `config/company.yaml`: required company context template.
- `scripts/prepare_session.py`: validates context and builds session packet.
- `scripts/run_debate.py`: generates debate output markdown.
- `scripts/validate_output.py`: checks mandatory output markers.
- `scripts/security_scan.py`: static checks for risky patterns/imports.
- `.github/workflows/ci.yml`: GitHub Actions smoke checks.

## Requirements

- Python 3.11+ (stdlib only).
- No third-party Python dependencies.

## Quick start

1. Enter the skill directory:

```bash
cd ai-csuite
```

2. Fill company context:

```bash
cp config/company.yaml config/company.local.yaml
```

Edit `config/company.local.yaml` with your real values.

3. Run security scan:

```bash
python3 scripts/security_scan.py .
```

4. Prepare the session:

```bash
python3 scripts/prepare_session.py \
  --topic "Should we change pricing for SMB annual plans?" \
  --company-file config/company.local.yaml
```

5. Run the debate:

```bash
python3 scripts/run_debate.py \
  --topic "Should we change pricing for SMB annual plans?" \
  --company-file config/company.local.yaml \
  --output logs/latest-decision.md
```

6. Validate generated output:

```bash
python3 scripts/validate_output.py --file logs/latest-decision.md
```

If validation prints `PASS`, the decision file is complete.

## Company config schema

`config/company.yaml` must contain:

- `company_name`
- `product`
- `stage` (`solo | pre-seed | seed | series-a`)
- `arr_or_mrr`
- `runway_months`
- `team_size`
- `constraints` (YAML list)

## Stage behavior

- `solo`: 2 rounds, lean executive panel.
- `pre-seed`: 2 rounds, includes customer voice in debate.
- `seed`: 3 rounds, adds growth debate depth.
- `series-a`: 3 rounds, full C-suite coverage.

`CV` and `CFO` always provide a pre-round data brief, even when not both in debate roster.

## Output contract

Generated markdown includes:

- `DATA BRIEF (Pre-Round)`
- Round sections for active agents
- `CEO BRIEF`
- `CEO DECISION`
- Decision metadata (`CONFIDENCE`, `REVERSIBILITY`, next steps)

## VirusTotal-safe publishing checklist

Before tagging or releasing:

```bash
python3 scripts/security_scan.py .
python3 scripts/prepare_session.py --topic "sanity check" --company-file config/company.yaml
python3 scripts/run_debate.py --topic "sanity check" --company-file config/company.yaml --output logs/sanity.md
python3 scripts/validate_output.py --file logs/sanity.md
```

Expected:

- `security_scan.py` returns `PASS`
- `validate_output.py` returns `PASS`
- No obfuscated payloads, no non-stdlib imports, no hidden outbound calls

## GitHub publishing flow

From repository root:

```bash
git add ai-csuite
git commit -m "Publish ai-csuite skill with runtime scripts and docs"
git push origin main
```

---

<a name="中文"></a>

## 简介

脚本支持的 AI C-Suite 技能，用于结构化战略决策。

## 功能

- 为 SaaS 团队构建阶段感知的高管团队
- 运行多轮辩论，基于角色的立场
- 生成结构化的 `CEO BRIEF` 和 `CEO DECISION`
- 验证输出形状并扫描技能进行发布时安全检查

## 包含文件

- `SKILL.md`：提示工作流和操作规则
- `config/company.yaml`：必需的公司上下文模板
- `scripts/prepare_session.py`：验证上下文并构建会话包
- `scripts/run_debate.py`：生成辩论输出 markdown
- `scripts/validate_output.py`：检查必需输出标记
- `scripts/security_scan.py`：静态检查风险模式/导入

## 要求

- Python 3.11+（仅标准库）
- 无第三方 Python 依赖

## 快速开始

1. 进入技能目录：

```bash
cd ai-csuite
```

2. 填写公司上下文：

```bash
cp config/company.yaml config/company.local.yaml
```

编辑 `config/company.local.yaml` 填入真实值。

3. 运行安全扫描：

```bash
python3 scripts/security_scan.py .
```

4. 准备会话：

```bash
python3 scripts/prepare_session.py \
  --topic "我们是否应该更改 SMB 年度计划的定价？" \
  --company-file config/company.local.yaml
```

5. 运行辩论：

```bash
python3 scripts/run_debate.py \
  --topic "我们是否应该更改 SMB 年度计划的定价？" \
  --company-file config/company.local.yaml \
  --output logs/latest-decision.md
```

6. 验证生成的输出：

```bash
python3 scripts/validate_output.py --file logs/latest-decision.md
```

如果验证打印 `PASS`，决策文件已完成。

## 公司配置模式

`config/company.yaml` 必须包含：

- `company_name`
- `product`
- `stage`（`solo | pre-seed | seed | series-a`）
- `arr_or_mrr`
- `runway_months`
- `team_size`
- `constraints`（YAML 列表）

## 阶段行为

- `solo`：2 轮，精简高管小组
- `pre-seed`：2 轮，包含客户声音在辩论中
- `seed`：3 轮，增加增长辩论深度
- `series-a`：3 轮，完整 C-suite 覆盖

## 输出契约

生成的 markdown 包括：

- `DATA BRIEF (Pre-Round)`
- 活跃代理的轮次部分
- `CEO BRIEF`
- `CEO DECISION`
- 决策元数据（`CONFIDENCE`、`REVERSIBILITY`、后续步骤）

