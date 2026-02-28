# Foxcode OpenClaw

Configure Foxcode AI models in OpenClaw with interactive setup and validation.

<p align="center">
  <a href="#english">English</a> | <a href="#中文">中文</a> | <a href="#日本語">日本語</a>
</p>

---

<a name="english"></a>

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

The wizard saves to two files:

**1. `~/.openclaw/openclaw.json`** (models and endpoints):
```json
{
  "models": {
    "providers": {
      "foxcode": {
        "baseUrl": "https://code.newcli.com/claude",
        "api": "anthropic-messages",
        "models": [
          { "id": "claude-sonnet-4-5-20251101", "name": "Claude Sonnet", "contextWindow": 200000, "maxTokens": 4096 },
          { "id": "claude-opus-4-5-20251101", "name": "Claude Opus", "contextWindow": 200000, "maxTokens": 4096 },
          { "id": "claude-haiku-4-5-20251101", "name": "Claude Haiku", "contextWindow": 200000, "maxTokens": 4096 }
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

**2. `~/.openclaw/agents/main/agent/auth-profiles.json`** (API key):
```json
{
  "profiles": {
    "foxcode:default": {
      "type": "api_key",
      "provider": "foxcode",
      "key": "sk-ant-your-token-here"
    }
  }
}
```

**Note:** OpenClaw stores API keys in `auth-profiles.json`, NOT in `openclaw.json`.

## Commands

| Task | Command |
|------|---------|
| Check status | `python3 scripts/check_status.py` |
| Configure | `python3 scripts/configure_foxcode.py` |
| Validate | `python3 scripts/validate_config.py` |

## Files

```
foxcode-openclaw/
├── SKILL.md
├── README.md
├── scripts/
│   ├── configure_foxcode.py
│   ├── validate_config.py
│   └── check_status.py
└── references/
    ├── foxcode-endpoints.md
    └── openclaw-config.md
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

<a name="中文"></a>

## 快速开始

```bash
python3 scripts/configure_foxcode.py
```

## 准备工作

| 项目 | 获取方式 |
|------|----------|
| Foxcode API 令牌 | [点击注册](https://foxcode.rjj.cc/auth/register?aff=FH6PK) → [API Keys 页面](https://foxcode.rjj.cc/api-keys) |
| OpenClaw | 已安装 |
| 配置文件 | `~/.openclaw/openclaw.json` |

## 端点选择

| 端点 | 网址 | 适用场景 |
|------|------|----------|
| 官方 | `https://code.newcli.com/claude` | 稳定性优先 |
| Super | `https://code.newcli.com/claude/super` | 节省成本 |
| Ultra | `https://code.newcli.com/claude/ultra` | 最大优惠 |
| AWS | `https://code.newcli.com/claude/aws` | 速度优先 |
| AWS 思考 | `https://code.newcli.com/claude/droid` | 复杂任务 |

## 模型选择

| 模型 | 适用场景 |
|------|----------|
| `claude-opus-4-5-20251101` | 复杂任务 |
| `claude-sonnet-4-5-20251101` | 日常使用（推荐） |
| `claude-haiku-4-5-20251101` | 快速任务 |

## 配置示例

向导保存到两个文件：

**1. `~/.openclaw/openclaw.json`**（模型和端点）：
```json
{
  "models": {
    "providers": {
      "foxcode": {
        "baseUrl": "https://code.newcli.com/claude",
        "api": "anthropic-messages",
        "models": [
          { "id": "claude-sonnet-4-5-20251101", "name": "Claude Sonnet", "contextWindow": 200000, "maxTokens": 4096 },
          { "id": "claude-opus-4-5-20251101", "name": "Claude Opus", "contextWindow": 200000, "maxTokens": 4096 },
          { "id": "claude-haiku-4-5-20251101", "name": "Claude Haiku", "contextWindow": 200000, "maxTokens": 4096 }
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

**2. `~/.openclaw/agents/main/agent/auth-profiles.json`**（API 密钥）：
```json
{
  "profiles": {
    "foxcode:default": {
      "type": "api_key",
      "provider": "foxcode",
      "key": "sk-ant-your-token-here"
    }
  }
}
```

**注意：** OpenClaw 将 API 密钥存储在 `auth-profiles.json` 中，而不是 `openclaw.json`。

## 常用命令

| 任务 | 命令 |
|------|------|
| 检查状态 | `python3 scripts/check_status.py` |
| 配置 | `python3 scripts/configure_foxcode.py` |
| 验证 | `python3 scripts/validate_config.py` |

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| 令牌无效 | 从 [API Keys](https://foxcode.rjj.cc/api-keys) 重新复制 |
| 端点无法访问 | 运行 `check_status.py`，尝试其他端点 |
| JSON 语法错误 | 运行 `python3 -m json.tool ~/.openclaw/openclaw.json` |

## 链接

- 状态页面: https://status.rjj.cc/status/foxcode
- API Keys: https://foxcode.rjj.cc/api-keys

---

<a name="日本語"></a>

## クイックスタート

```bash
python3 scripts/configure_foxcode.py
```

## 要件

| 項目 | 入手方法 |
|------|----------|
| Foxcode API トークン | [登録](https://foxcode.rjj.cc/auth/register?aff=FH6PK) → [API Keys](https://foxcode.rjj.cc/api-keys) |
| OpenClaw | インストール済み |
| 設定ファイル | `~/.openclaw/openclaw.json` |

## エンドポイント

| 名前 | URL | 用途 |
|------|-----|------|
| Official | `https://code.newcli.com/claude` | 信頼性 |
| Super | `https://code.newcli.com/claude/super` | コスト削減 |
| Ultra | `https://code.newcli.com/claude/ultra` | 最大節約 |
| AWS | `https://code.newcli.com/claude/aws` | 速度 |
| AWS Thinking | `https://code.newcli.com/claude/droid` | 複雑なタスク |

## モデル

| モデル | 用途 |
|-------|------|
| `claude-opus-4-5-20251101` | 複雑なタスク |
| `claude-sonnet-4-5-20251101` | 日常使用（推奨） |
| `claude-haiku-4-5-20251101` | クイックタスク |

## 設定例

ウィザードは2つのファイルに保存します：

**1. `~/.openclaw/openclaw.json`**（モデルとエンドポイント）：
```json
{
  "models": {
    "providers": {
      "foxcode": {
        "baseUrl": "https://code.newcli.com/claude",
        "api": "anthropic-messages",
        "models": [
          { "id": "claude-sonnet-4-5-20251101", "name": "Claude Sonnet", "contextWindow": 200000, "maxTokens": 4096 },
          { "id": "claude-opus-4-5-20251101", "name": "Claude Opus", "contextWindow": 200000, "maxTokens": 4096 },
          { "id": "claude-haiku-4-5-20251101", "name": "Claude Haiku", "contextWindow": 200000, "maxTokens": 4096 }
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

**2. `~/.openclaw/agents/main/agent/auth-profiles.json`**（APIキー）：
```json
{
  "profiles": {
    "foxcode:default": {
      "type": "api_key",
      "provider": "foxcode",
      "key": "sk-ant-your-token-here"
    }
  }
}
```

**注意：** OpenClawはAPIキーを `auth-profiles.json` に保存し、`openclaw.json` には保存しません。

## コマンド

| タスク | コマンド |
|------|---------|
| ステータス確認 | `python3 scripts/check_status.py` |
| 設定 | `python3 scripts/configure_foxcode.py` |
| 検証 | `python3 scripts/validate_config.py` |

## トラブルシューティング

| 問題 | 解決策 |
|------|--------|
| 無効なトークン | [API Keys](https://foxcode.rjj.cc/api-keys) から再コピー |
| エンドポイントに到達できない | `check_status.py` を実行、別のエンドポイントを試す |
| JSON 構文エラー | `python3 -m json.tool ~/.openclaw/openclaw.json` を実行 |

## リンク

- ステータス: https://status.rjj.cc/status/foxcode
- API Keys: https://foxcode.rjj.cc/api-keys
