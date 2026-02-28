# Foxcode OpenClaw Setup Guide

> A beginner-friendly guide to configuring Foxcode AI models in OpenClaw.
> **Time to complete:** ~10 minutes | **Difficulty:** Easy

---

## Before You Start (2 minutes)

### What You Need

| Item | How to Get It |
|------|---------------|
| **Foxcode API Token** | [Register here](https://foxcode.rjj.cc/auth/register?aff=FH6PK) → [API Keys page](https://foxcode.rjj.cc/api-keys) |
| **OpenClaw installed** | Should already be set up on your system |
| **Config file location** | Usually `~/.openclaw/openclaw.json` |

### Quick Confidence Check

- [ ] I know where to paste my API token
- [ ] I understand there are different endpoints (speed vs cost options)
- [ ] I can edit a JSON file

> **Tip:** If any box is unchecked, that's fine! This guide will walk you through everything step by step.

---

## Phase 1: Get Your API Token (3 minutes)

### Step 1.1: Register or Log In

1. [Register here](https://foxcode.rjj.cc/auth/register?aff=FH6PK) to create an account
2. Or log in if you already have an account
3. Navigate to [API Keys](https://foxcode.rjj.cc/api-keys)

### Step 1.2: Generate a Token

1. Click "Create New Key" or similar button
2. Give it a name (e.g., "OpenClaw-Setup")
3. **Copy the token immediately** (it may not be shown again)

> **Security Note:** Treat this token like a password. Don't share it or commit it to git.

### Step 1.3: Save Token Securely

For now, paste it into a temporary text file or secure note:

```
FOXCODE_API_TOKEN=your_token_here
```

---

## Phase 2: Choose Your Endpoint (2 minutes)

Foxcode offers 5 different endpoints. Each has different trade-offs:

### Endpoint Comparison

| Endpoint | URL | Best For | Response | Cost |
|----------|-----|----------|----------|------|
| **Official** | `https://code.newcli.com/claude` | Reliability | Standard | Standard |
| **Super** | `https://code.newcli.com/claude/super` | Cost saving | Good | Discounted |
| **Ultra** | `https://code.newcli.com/claude/ultra` | Maximum savings | Slower | Lowest |
| **AWS** | `https://code.newcli.com/claude/aws` | Speed | Fastest | Standard |
| **AWS (Thinking)** | `https://code.newcli.com/claude/droid` | Complex tasks | Variable | Standard |

### Decision Guide

```
Just getting started?  →  Official (reliable, predictable)
Want to save money?    →  Super or Ultra
Need fast responses?   →  AWS
Doing complex coding?  →  AWS (Thinking)
```

### Check Current Status

Before choosing, verify endpoint health:

```bash
python3 scripts/check_status.py
```

> **Recommendation for beginners:** Start with the **Official** endpoint. It's the most reliable while you're learning.

---

## Phase 3: Configure OpenClaw (3 minutes)

### Step 3.1: Open Your Config File

Find and open your OpenClaw config file:

```bash
# Default location
open ~/.openclaw/openclaw.json

# Or find it
find ~ -name "openclaw.json" 2>/dev/null
```

### Step 3.2: Set the Base URL

Add or update these fields in your config:

```json
{
  "models": {
    "providers": {
      "foxcode": {
        "baseUrl": "https://code.newcli.com/claude",
        "apiKey": "YOUR_API_TOKEN_HERE"
      }
    }
  }
}
```

Replace the URL with your chosen endpoint from Phase 2.

### Step 3.3: Set Your Primary Model

Add the model configuration:

```json
{
  "models": {
    "providers": {
      "foxcode": {
        "baseUrl": "https://code.newcli.com/claude",
        "apiKey": "YOUR_API_TOKEN_HERE",
        "models": [
          {
            "id": "claude-sonnet-4-5-20251101",
            "name": "Claude Sonnet",
            "contextWindow": 200000,
            "maxTokens": 4096
          }
        ]
      }
    }
  }
}
```

**Available Models:**

| Model | Use Case |
|-------|----------|
| `claude-opus-4-5-20251101` | Most capable, best for complex tasks |
| `claude-sonnet-4-5-20251101` | Balanced - good for daily use (Recommended) |
| `claude-haiku-4-5-20251101` | Fast and cheap, good for quick tasks |

> **Beginner recommendation:** Start with `claude-sonnet-4-5-20251101`. It hits the sweet spot of capability and speed.

---

## Phase 4: Configure Fallback Models (2 minutes)

Fallback models provide backup if your primary is unavailable.

### Step 4.1: Add Fallback Configuration

Update your config with multiple models:

```json
{
  "models": {
    "providers": {
      "foxcode": {
        "baseUrl": "https://code.newcli.com/claude",
        "apiKey": "YOUR_API_TOKEN_HERE",
        "models": [
          {
            "id": "claude-sonnet-4-5-20251101",
            "name": "Claude Sonnet",
            "contextWindow": 200000,
            "maxTokens": 4096
          },
          {
            "id": "claude-haiku-4-5-20251101",
            "name": "Claude Haiku",
            "contextWindow": 200000,
            "maxTokens": 4096
          }
        ]
      }
    }
  }
}
```

### Fallback Strategies

| Strategy | Config | When to Use |
|----------|--------|-------------|
| **Conservative** | Sonnet → Haiku → Opus | Maximum reliability |
| **Speed-First** | Haiku → Sonnet | Prioritize fast responses |
| **Capability-First** | Opus → Sonnet | Prioritize best results |

> **For beginners:** Use the Conservative strategy shown above.

---

## Phase 5: Validate and Test (2 minutes)

### Step 5.1: Run Validation

```bash
python3 scripts/validate_config.py
```

Expected output:
```
✓ Config file syntax valid
✓ API token format valid
✓ Base URL reachable
✓ Primary model available
✓ Fallback models configured
All checks passed!
```

### Step 5.2: Test in OpenClaw

Start OpenClaw and run a simple test:

```bash
openclaw
```

Then ask:
```
Hello! Can you confirm my Foxcode configuration is working?
```

You should get a response confirming the model is active.

---

## Troubleshooting

### "API token invalid"

1. Re-copy token from [API Keys page](https://foxcode.rjj.cc/api-keys)
2. Check for extra spaces before/after
3. Verify token hasn't expired

### "Cannot reach endpoint"

```bash
# Check if endpoint is up
python3 scripts/check_status.py

# Try alternative endpoint
```

### "Model not found"

1. Verify model name spelling
2. Check if model is available on your endpoint tier
3. Try: `python3 scripts/check_status.py --models`

### Config file issues

```bash
# Validate JSON syntax
python3 -m json.tool ~/.openclaw/openclaw.json

# Re-run setup wizard
python3 scripts/configure_foxcode.py
```

---

## Next Steps

Now that you're set up:

1. **Bookmark the status page:** https://status.rjj.cc/status/foxcode
2. **Check status regularly:** `python3 scripts/check_status.py`
3. **Optimize over time:** Try different endpoints to find your preference

### Quick Commands Reference

| Task | Command |
|------|---------|
| Check status | `python3 scripts/check_status.py` |
| Reconfigure | `python3 scripts/configure_foxcode.py` |
| Validate setup | `python3 scripts/validate_config.py` |

---

## Appendix: Full Config Example

```json
{
  "models": {
    "providers": {
      "foxcode": {
        "baseUrl": "https://code.newcli.com/claude",
        "apiKey": "sk-foxcode-xxxxxxxxxxxxxxxx",
        "api": "anthropic-messages",
        "models": [
          {
            "id": "claude-sonnet-4-5-20251101",
            "name": "Claude Sonnet",
            "contextWindow": 200000,
            "maxTokens": 4096
          },
          {
            "id": "claude-haiku-4-5-20251101",
            "name": "Claude Haiku",
            "contextWindow": 200000,
            "maxTokens": 4096
          },
          {
            "id": "claude-opus-4-5-20251101",
            "name": "Claude Opus",
            "contextWindow": 200000,
            "maxTokens": 4096
          }
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": "foxcode/claude-sonnet-4-5-20251101"
    }
  }
}
```

---

**You're all set!** 🎉

If you encounter any issues, re-run `python3 scripts/configure_foxcode.py` for interactive help.

---

## 中文版指南 (Chinese Version)

### 快速开始

```bash
# 运行交互式设置
python3 scripts/configure_foxcode.py
```

### 你需要准备

| 项目 | 获取方式 |
|------|----------|
| **Foxcode API Token** | [点击这里注册](https://foxcode.rjj.cc/auth/register?aff=FH6PK) → [API Keys 页面](https://foxcode.rjj.cc/api-keys) |
| **OpenClaw 已安装** | 系统应已安装 |
| **配置文件位置** | 通常是 `~/.openclaw/openclaw.json` |

### Foxcode 端点选择

| 端点 | 网址 | 适用场景 | 速度 | 价格 |
|------|------|----------|------|------|
| **官方** | `https://code.newcli.com/claude` | 稳定性优先 | 标准 | 标准 |
| **Super** | `https://code.newcli.com/claude/super` | 节省成本 | 良好 | 优惠 |
| **Ultra** | `https://code.newcli.com/claude/ultra` | 最大优惠 | 较慢 | 最低 |
| **AWS** | `https://code.newcli.com/claude/aws` | 速度优先 | 最快 | 标准 |
| **AWS思考** | `https://code.newcli.com/claude/droid` | 复杂任务 | 可变 | 标准 |

### 基本配置示例

```json
{
  "models": {
    "providers": {
      "foxcode": {
        "baseUrl": "https://code.newcli.com/claude",
        "apiKey": "你的API令牌",
        "api": "anthropic-messages",
        "models": [
          {
            "id": "claude-sonnet-4-5-20251101",
            "name": "Claude Sonnet",
            "contextWindow": 200000,
            "maxTokens": 4096
          }
        ]
      }
    }
  }
}
```

### 常用命令

```bash
# 检查端点状态
python3 scripts/check_status.py

# 验证配置
python3 scripts/validate_config.py

# 重新配置
python3 scripts/configure_foxcode.py
```

### 需要帮助？

- **状态页面**: https://status.rjj.cc/status/foxcode
- **Foxcode 支持**: https://foxcode.rjj.cc
