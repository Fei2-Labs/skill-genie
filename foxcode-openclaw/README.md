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
├── references/
│   ├── foxcode-endpoints.md    # Endpoint details
│   └── openclaw-config.md      # Config reference
└── assets/templates/
    └── setup-checklist.md      # Printable checklist
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

### 端点选择

| 端点 | 适用场景 |
|------|----------|
| 官方 | 稳定性优先 |
| Super | 节省成本 |
| Ultra | 最大优惠 |
| AWS | 速度优先 |
| AWS 思考 | 复杂任务 |

### 配置示例

```json
{
  "models": {
    "providers": {
      "foxcode": {
        "baseUrl": "https://code.newcli.com/claude",
        "apiKey": "你的令牌",
        "api": "anthropic-messages",
        "models": [{ "id": "claude-sonnet-4-5-20251101", "name": "Claude Sonnet", "contextWindow": 200000, "maxTokens": 4096 }]
      }
    }
  }
}
```

### 常用命令

```bash
python3 scripts/check_status.py      # 检查状态
python3 scripts/validate_config.py   # 验证配置
python3 scripts/configure_foxcode.py # 重新配置
```
