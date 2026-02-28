# OmniDebug Autopilot

Autonomous root-cause debugging skill for modern codebases.

<p align="center">
  <a href="#english">English</a> | <a href="#中文">中文</a>
</p>

---

<a name="english"></a>

`omnidebug-autopilot` gives an AI agent a strict, repeatable debug workflow:

1. reproduce the issue deterministically
2. isolate the true root cause
3. apply the smallest valid fix
4. verify with hard quality gates

It includes a browser-first module for deterministic UI bug reproduction, artifact capture, and fix verification.

## Why This Skill

Debugging often fails because teams patch symptoms, skip reproducibility, or accept false-green checks.

This skill enforces:
- deterministic reproduction before edits
- evidence-backed root-cause statements
- minimum blast-radius fixes
- verification loops until green
- no-interruption default execution for autonomous agents

## Core Capabilities

- Stack-aware debugging across Node.js, Python, Go, Rust, Java/Kotlin, Ruby, PHP, .NET, Swift
- Root-cause-first analysis chain
- Browser debugging artifact pipeline
- Verification gates for test, lint, typecheck, build, and smoke checks
- Ordered auto-fix heuristics by risk/likelihood

## Main Workflow

### Phase 1: Triage
- Capture exact failure text and command
- Inspect logs/network before code changes
- Identify likely regression window

### Phase 2: Reproduction
- Create a deterministic repro command
- Remove noise (parallelism, retries, random data)
- Confirm reproducibility (minimum 2 runs)

### Phase 3: Evidence Collection
- Gather logs, stack traces, failing requests
- Capture env/runtime differences
- For browser bugs, capture trace/screenshot/network metadata

### Phase 4: Root Cause Analysis
Build one falsifiable cause statement using:
- symptom
- immediate fault location
- underlying mechanism
- trigger condition
- missing safeguard

### Phase 5: Fix Strategy
- Apply smallest valid root-cause fix
- Preserve public behavior unless bug requires correction
- Reject bypass hacks as final fix

### Phase 6: Verification
- Run targeted checks first
- Run full project gates
- If any gate fails, return to Phase 4

## Browser Debugging Module

### Included Scripts
- `scripts/repro_browser_issue.py`
- `scripts/capture_browser_artifacts.py`
- `scripts/verify_browser_fix.py`

### Standard Browser Flow

```bash
# 1) Reproduce browser failure (expect fail)
python scripts/repro_browser_issue.py \
  --project-root . \
  --repro-cmd "pnpm exec playwright test tests/bug.spec.ts --project=chromium --workers=1 --retries=0" \
  --expect fail \
  --runs 2

# 2) Capture artifacts
python scripts/capture_browser_artifacts.py \
  --project-root . \
  --output-dir .debug/browser-artifacts

# 3) Verify fix (expect pass)
python scripts/verify_browser_fix.py \
  --project-root . \
  --verify-cmd "pnpm exec playwright test tests/bug.spec.ts --project=chromium --workers=1 --retries=0" \
  --runs 2 \
  --signature-file .debug/browser-repro/repro_report.json
```

Supported ecosystems:
- Playwright
- Cypress
- Selenium
- WebdriverIO

## Script Reference

### `repro_browser_issue.py`
- Re-runs repro command and checks deterministic signature
- Outputs: run logs + `repro_report.json`
- Exit codes: `0` success, `10` reproducibility failure

### `capture_browser_artifacts.py`
- Collects screenshots, traces, HAR/video/log artifacts into one bundle
- Outputs: artifact tree + `manifest.json`
- Exit codes: `0` success, `10` empty capture (unless `--allow-empty`)

### `verify_browser_fix.py`
- Re-runs verification command and checks old failure signature is absent
- Outputs: run logs + `verify_report.json`
- Exit codes: `0` success, `11` verification failure

## References

- `references/browser-repro-playbook.md`
- `references/browser-artifact-checklist.md`

## Folder Structure

```text
omnidebug-autopilot/
├─ SKILL.md
├─ README.md
├─ references/
│  ├─ browser-repro-playbook.md
│  └─ browser-artifact-checklist.md
└─ scripts/
   ├─ repro_browser_issue.py
   ├─ capture_browser_artifacts.py
   └─ verify_browser_fix.py
```

## Guardrails

- Never claim success without passing verification
- Never skip tests to force green state
- Never hardcode secrets/endpoints
- Never ship temporary bypasses as final fixes
- Keep fixes minimal and architecture-compatible

## License

MIT

---

<a name="中文"></a>

## 简介

自主根因调试技能，适用于现代代码库。

`omnidebug-autopilot` 为 AI 代理提供严格、可重复的调试工作流：

1. 确定性复现问题
2. 隔离真正根因
3. 应用最小有效修复
4. 通过严格质量门验证

## 为什么需要此技能

调试经常失败，因为团队修补症状、跳过可复现性或接受假绿色检查。

此技能强制执行：
- 编辑前确定性复现
- 基于证据的根因陈述
- 最小影响范围修复
- 循环验证直到通过
- 自主代理无中断默认执行

## 核心能力

- 跨 Node.js、Python、Go、Rust、Java/Kotlin、Ruby、PHP、.NET、Swift 的堆栈感知调试
- 根因优先分析链
- 浏览器调试工件管道
- 测试、lint、类型检查、构建和冒烟检查的验证门
- 按风险/可能性排序的自动修复启发式

## 主要工作流

### 阶段 1：分类
- 捕获确切失败文本和命令
- 在代码更改前检查日志/网络
- 识别可能的回归窗口

### 阶段 2：复现
- 创建确定性复现命令
- 移除噪音（并行、重试、随机数据）
- 确认可复现性（最少 2 次运行）

### 阶段 3：证据收集
- 收集日志、堆栈跟踪、失败请求
- 捕获环境/运行时差异
- 对于浏览器 bug，捕获跟踪/截图/网络元数据

### 阶段 4：根因分析
使用以下内容构建一个可证伪的原因陈述：
- 症状
- 直接故障位置
- 底层机制
- 触发条件
- 缺失的保护措施

### 阶段 5：修复策略
- 应用最小有效的根因修复
- 保留公共行为，除非 bug 需要纠正
- 拒绝绕过 hack 作为最终修复

### 阶段 6：验证
- 先运行针对性检查
- 运行完整项目门
- 如果任何门失败，返回阶段 4

## 脚本参考

### `repro_browser_issue.py`
- 重新运行复现命令并检查确定性签名
- 输出：运行日志 + `repro_report.json`
- 退出码：`0` 成功，`10` 可复现性失败

### `capture_browser_artifacts.py`
- 将截图、跟踪、HAR/视频/日志工件收集到一个包中
- 输出：工件树 + `manifest.json`
- 退出码：`0` 成功，`10` 空捕获（除非 `--allow-empty`）

### `verify_browser_fix.py`
- 重新运行验证命令并检查旧失败签名不存在
- 输出：运行日志 + `verify_report.json`
- 退出码：`0` 成功，`11` 验证失败

## 防护措施

- 永远不在未通过验证的情况下声称成功
- 永远不跳过测试以强制绿色状态
- 永远不硬编码密钥/端点
- 永远不将临时绕过作为最终修复发布
- 保持修复最小且架构兼容
