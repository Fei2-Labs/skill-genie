# Foxcode OpenClaw Integration

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Compatible-green.svg)](https://openclaw.ai)

> A beginner-friendly skill to configure Foxcode AI models in OpenClaw with interactive setup, status monitoring, and validation tools.

## Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/foxcode-openclaw.git
cd foxcode-openclaw

# Run interactive setup
python3 scripts/configure_foxcode.py
```

## What is Foxcode?

[Foxcode](https://foxcode.rjj.cc) is a Chinese AI service providing access to Claude Code models through multiple endpoints optimized for different use cases:

| Endpoint | Best For | Characteristics |
|----------|----------|-----------------|
| **Official** | Reliability | Highest uptime, standard pricing |
| **Super** | Cost Efficiency | 20-30% savings, good for daily use |
| **Ultra** | Maximum Savings | 40-50% discount, best for batch jobs |
| **AWS** | Speed | Fastest response times |
| **AWS Thinking** | Complex Tasks | Extended reasoning capability |

## Features

- **Interactive Setup Wizard** - Step-by-step configuration for beginners
- **Status Monitoring** - Real-time endpoint health checks
- **Configuration Validation** - Verify your setup before using
- **Multiple Endpoints** - Support for all 5 Foxcode tiers
- **Primary & Fallback Models** - Configure backup models for reliability
- **Security First** - API key input hidden, file permissions restricted
- **Environment Variables** - Support for secure token management

## Requirements

- Python 3.8+
- OpenClaw installed and configured
- Foxcode API token ([Get one here](https://foxcode.rjj.cc/api-keys))

## Installation

### Method 1: Direct Usage

```bash
# Download the scripts
curl -O https://raw.githubusercontent.com/yourusername/foxcode-openclaw/main/scripts/configure_foxcode.py

# Run the wizard
python3 configure_foxcode.py
```

### Method 2: Clone Repository

```bash
git clone https://github.com/yourusername/foxcode-openclaw.git
cd foxcode-openclaw

# Optional: Install as skill
openskills install foxcode-openclaw/
```

## Usage

### Interactive Configuration

```bash
python3 scripts/configure_foxcode.py
```

This wizard will:
1. Ask for your Foxcode API token (input hidden)
2. Show available endpoints with current status
3. Explain trade-offs (speed vs cost vs features)
4. Let you select primary and fallback models
5. Test the connection
6. Save the configuration

### Check Endpoint Status

```bash
# Check all endpoints
python3 scripts/check_status.py

# Check specific endpoint
python3 scripts/check_status.py --endpoint ultra

# JSON output for automation
python3 scripts/check_status.py --format json
```

### Validate Configuration

```bash
# Validate current config
python3 scripts/validate_config.py

# Validate specific file
python3 scripts/validate_config.py --config ~/.openclaw/openclaw.json
```

## Configuration

### OpenClaw Config File Location

- **macOS/Linux**: `~/.openclaw/openclaw.json`
- **Windows**: `%APPDATA%\openclaw\openclaw.json`

### Minimal Configuration

Add to your `~/.openclaw/openclaw.json`:

```json
{
  "models": {
    "providers": {
      "foxcode": {
        "baseUrl": "https://code.newcli.com/claude",
        "apiKey": "sk-foxcode-your-token-here",
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

### With Fallback Models

```json
{
  "models": {
    "providers": {
      "foxcode": {
        "baseUrl": "https://code.newcli.com/claude",
        "apiKey": "sk-foxcode-your-token-here",
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

### Using Environment Variables

For better security, use environment variables:

```json
{
  "models": {
    "providers": {
      "foxcode": {
        "baseUrl": "https://code.newcli.com/claude",
        "apiKey": "${FOXCODE_API_TOKEN}",
        "api": "anthropic-messages"
      }
    }
  }
}
```

Set the environment variable:

```bash
# macOS/Linux
export FOXCODE_API_TOKEN="sk-foxcode-your-token"

# Add to ~/.zshrc or ~/.bashrc for persistence
echo 'export FOXCODE_API_TOKEN="sk-foxcode-your-token"' >> ~/.zshrc
```

## Model Selection Guide

| Model | Capability | Speed | Cost | Best For |
|-------|-----------|-------|------|----------|
| `claude-opus-4-5-20251101` | Highest | Slower | Highest | Complex reasoning, coding |
| `claude-sonnet-4-5-20251101` | High | Fast | Medium | Daily use, general tasks |
| `claude-haiku-4-5-20251101` | Good | Fastest | Lowest | Quick tasks, high volume |

## Documentation

- **[Setup Guide](README_DETAILED.md)** - Detailed step-by-step instructions
- **[Endpoint Reference](references/foxcode-endpoints.md)** - All 5 endpoints documented
- **[Configuration Reference](references/openclaw-config.md)** - Complete config options
- **[Setup Checklist](assets/templates/setup-checklist.md)** - Printable checklist

## Troubleshooting

### Common Issues

**"API token invalid"**
- Double-check token from https://foxcode.rjj.cc/api-keys
- Ensure no extra spaces when copying
- Verify token hasn't expired

**"Cannot reach endpoint"**
- Check status: `python3 scripts/check_status.py`
- Verify your network connection
- Try alternative endpoint

**"Model not found"**
- Verify model ID spelling
- Check if model is available on your endpoint tier

See [Troubleshooting Guide](README_DETAILED.md#troubleshooting) for more.

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Security

- API tokens are never logged or stored in plain text
- Configuration files are created with 600 permissions (owner-only access)
- Environment variables recommended for production use
- See [SECURITY.md](SECURITY.md) for vulnerability reporting

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

## Acknowledgments

- [Foxcode](https://foxcode.rjj.cc) for providing the AI service
- [OpenClaw](https://openclaw.ai) for the AI agent platform
- [psychology-master](references/psychology-credits.md) skill for learning science principles

## Support

- **Status Page**: https://status.rjj.cc/status/foxcode
- **Foxcode Support**: https://foxcode.rjj.cc
- **Issues**: [GitHub Issues](https://github.com/yourusername/foxcode-openclaw/issues)

---

**Disclaimer**: This is an unofficial integration. Foxcode and OpenClaw are trademarks of their respective owners.
