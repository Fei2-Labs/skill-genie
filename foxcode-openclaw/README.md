# Foxcode OpenClaw

Configure Foxcode AI models in OpenClaw with interactive setup and validation.

## Quick Start

```bash
python3 scripts/configure_foxcode.py
```

## Requirements

| Item | Get it |
|------|--------|
| Foxcode API Token | [Register](https://foxcode.rjj.cc/auth/register?aff=FH6PK) → [API Keys](https://foxcode.rjj.cc/api-keys) |
| OpenClaw | Already installed |
| Config file | `~/.openclaw/openclaw.json` |

## Endpoints

| Name | URL | Best For |
|------|-----|----------|
| Official | `https://code.newcli.com/claude` | Reliability |
| Super | `https://code.newcli.com/claude/super` | Cost savings |
| Ultra | `https://code.newcli.com/claude/ultra` | Max savings |
| AWS | `https://code.newcli.com/claude/aws` | Speed |
| AWS Thinking | `https://code.newcli.com/claude/droid` | Complex tasks |

## Models

| Model | Use Case |
|-------|----------|
| `claude-opus-4-5-20251101` | Complex tasks |
| `claude-sonnet-4-5-20251101` | Daily use (recommended) |
| `claude-haiku-4-5-20251101` | Quick tasks |

## Config Example

```json
{
  "models": {
    "providers": {
      "foxcode": {
        "baseUrl": "https://code.newcli.com/claude",
        "apiKey": "YOUR_TOKEN",
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
  },
  "agents": {
    "defaults": {
      "model": "foxcode/claude-sonnet-4-5-20251101"
    }
  }
}
```

## Commands

| Task | Command |
|------|---------|
| Check status | `python3 scripts/check_status.py` |
| Configure | `python3 scripts/configure_foxcode.py` |
| Validate | `python3 scripts/validate_config.py` |

## Files

```
foxcode-openclaw/
├── SKILL.md                    # Skill workflow
├── README.md                   # This file
├── scripts/
│   ├── configure_foxcode.py    # Interactive setup
│   ├── validate_config.py      # Config validation
│   └── check_status.py         # Endpoint health check
└── references/
    ├── foxcode-endpoints.md    # Endpoint details
    └── openclaw-config.md      # Config reference
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Invalid token | Re-copy from [API Keys](https://foxcode.rjj.cc/api-keys) |
| Endpoint unreachable | Run `check_status.py`, try different endpoint |
| JSON syntax error | Run `python3 -m json.tool ~/.openclaw/openclaw.json` |

## Links

- Status: https://status.rjj.cc/status/foxcode
- API Keys: https://foxcode.rjj.cc/api-keys

---

## 中文版

### 快速开始

```bash
python3 scripts/configure_foxcode.py
```

### 准备工作

| 项目 | 获取方式 |
|------|----------|
| Foxcode API 令牌 | [点击注册](https://foxcode.rjj.cc/auth/register?aff=FH6PK) → [API Keys 页面](https://foxcode.rjj.cc/api-keys) |
| OpenClaw | 已安装 |
| 配置文件 | `~/.openclaw/openclaw.json` |

### 端点选择

| 端点 | 网址 | 适用场景 |
|------|------|----------|
| 官方 | `https://code.newcli.com/claude` | 稳定性优先 |
| Super | `https://code.newcli.com/claude/super` | 节省成本 |
| Ultra | `https://code.newcli.com/claude/ultra` | 最大优惠 |
| AWS | `https://code.newcli.com/claude/aws` | 速度优先 |
| AWS 思考 | `https://code.newcli.com/claude/droid` | 复杂任务 |

### 模型选择

| 模型 | 适用场景 |
|------|----------|
| `claude-opus-4-5-20251101` | 复杂任务 |
| `claude-sonnet-4-5-20251101` | 日常使用（推荐） |
| `claude-haiku-4-5-20251101` | 快速任务 |

### 配置示例

```json
{
  "models": {
    "providers": {
      "foxcode": {
        "baseUrl": "https://code.newcli.com/claude",
        "apiKey": "你的令牌",
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
  },
  "agents": {
    "defaults": {
      "model": "foxcode/claude-sonnet-4-5-20251101"
    }
  }
}
```

### 常用命令

| 任务 | 命令 |
|------|------|
| 检查状态 | `python3 scripts/check_status.py` |
| 配置 | `python3 scripts/configure_foxcode.py` |
| 验证 | `python3 scripts/validate_config.py` |

### 故障排除

| 问题 | 解决方案 |
|------|----------|
| 令牌无效 | 从 [API Keys](https://foxcode.rjj.cc/api-keys) 重新复制 |
| 端点无法访问 | 运行 `check_status.py`，尝试其他端点 |
| JSON 语法错误 | 运行 `python3 -m json.tool ~/.openclaw/openclaw.json` |

### 链接

- 状态页面: https://status.rjj.cc/status/foxcode
- API Keys: https://foxcode.rjj.cc/api-keys
