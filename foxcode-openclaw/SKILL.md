---
name: foxcode-openclaw
description: Configure and manage Foxcode AI models in OpenClaw. Guides users through API setup, endpoint selection, primary/fallback model configuration, and status monitoring. Optimized for beginners with psychology-backed teaching approach.
license: MIT
metadata:
  version: 1.1.0
  category: ai-configuration
  author: Skill Genie
---

# Foxcode OpenClaw Setup

Configure Foxcode's Claude Code models in OpenClaw with an interactive, beginner-friendly workflow.

## Quick Start

```
1. Run: python3 scripts/configure_foxcode.py
2. Provide your Foxcode API token
3. Select endpoint(s) - comma-separated or "all"
4. Choose default endpoint and primary model
5. Test connection
6. Run: source ~/.zshrc (or restart terminal)
```

**Note:** The wizard automatically sets `FOXCODE_API_TOKEN` in your shell profile and uses `${FOXCODE_API_TOKEN}` in the config for security.

## Triggers

- "set up foxcode in openclaw"
- "configure foxcode models"
- "setup openclaw with foxcode"
- "check foxcode status"
- "change my openclaw model"
- "/foxcode-setup"

## Capabilities

### 1. Interactive Configuration (`configure_foxcode.py`)

Guided setup wizard that:
- Validates API token format
- Allows selecting multiple endpoints (comma-separated or "all")
- Explains endpoint differences (speed vs cost vs features)
- Sets default endpoint and primary model
- Adds all 3 models to each selected endpoint
- Uses environment variable reference for security
- Automatically sets `FOXCODE_API_TOKEN` in shell profile
- Tests connection before finishing

**Usage:**
```bash
python3 scripts/configure_foxcode.py
```

### 2. Status Monitoring (`check_status.py`)

Check health and availability of all Foxcode endpoints:
- Endpoint response times
- Current status (up/down)
- Recent incident history
- Recommended alternative if issues detected

**Usage:**
```bash
# Check all endpoints
python3 scripts/check_status.py

# Check specific endpoint
python3 scripts/check_status.py --endpoint ultra

# JSON output for automation
python3 scripts/check_status.py --format json
```

### 3. Configuration Validation (`validate_config.py`)

Verify your setup is correct:
- API token validity
- Base URL accessibility
- Model availability
- Configuration file syntax

**Usage:**
```bash
# Validate current config
python3 scripts/validate_config.py

# Validate specific file
python3 scripts/validate_config.py --config ~/.config/openclaw/config.json
```

## Workflow

### Phase 1: Preparation (2 minutes)

**Before you start:**
- Have your Foxcode API token ready (get one at https://foxcode.rjj.cc/api-keys)
- Know where your OpenClaw config file is located
- Optional: Check current status to pick the best endpoint

**Quick check:**
```bash
python3 scripts/check_status.py
```

### Phase 2: Interactive Setup (5 minutes)

Run the configuration wizard:
```bash
python3 scripts/configure_foxcode.py
```

The wizard will:
1. Ask for your API token (input is hidden for security)
2. Show available endpoints with current status
3. Let you select multiple endpoints (comma-separated or "all")
4. Ask which endpoint should be default
5. Let you select primary model
6. Test the connection
7. Save the configuration (uses `${FOXCODE_API_TOKEN}` env var)
8. Set `FOXCODE_API_TOKEN` in your shell profile

### Phase 3: Verification (2 minutes)

Apply the environment variable:
```bash
source ~/.zshrc  # or restart terminal
```

Validate everything is working:
```bash
python3 scripts/validate_config.py
```

Run a test prompt in OpenClaw to confirm.

### Phase 4: Monitoring (ongoing)

Check status anytime:
```bash
python3 scripts/check_status.py
```

## Endpoint Reference

| Endpoint | URL | Best For | Characteristics |
|----------|-----|----------|-----------------|
| **Official** | `https://code.newcli.com/claude` | Reliability | Standard pricing, full features |
| **Super** | `https://code.newcli.com/claude/super` | Cost efficiency | Discounted rate, good for most tasks |
| **Ultra** | `https://code.newcli.com/claude/ultra` | Maximum savings | Lowest cost, may have rate limits |
| **AWS** | `https://code.newcli.com/claude/aws` | Speed | AWS infrastructure, fast response |
| **AWS (Thinking)** | `https://code.newcli.com/claude/droid` | Complex tasks | Extended thinking capability |

**Status Page:** https://status.rjj.cc/status/foxcode

## Model Selection Guide

### Primary Model Selection

| Model | Strengths | Best For |
|-------|-----------|----------|
| `claude-opus-4-5-20251101` | Most capable | Complex reasoning, coding, analysis |
| `claude-sonnet-4-5-20251101` | Balanced | General tasks, daily use |
| `claude-haiku-4-5-20251101` | Fast, cheap | Quick tasks, high volume |

### Fallback Strategy

Configure 1-2 fallback models for reliability:

**Recommended setups:**
- **Conservative**: Opus → Sonnet → Haiku
- **Balanced**: Sonnet → Haiku
- **Cost-optimized**: Haiku (primary) → Sonnet (for complex tasks)

## Troubleshooting

### Common Issues

**"Missing env var FOXCODE_API_TOKEN"**
- Run: `source ~/.zshrc` (or restart terminal)
- Verify: `echo $FOXCODE_API_TOKEN`
- If empty, add manually to `~/.zshrc`: `export FOXCODE_API_TOKEN="your-token"`

**"API token invalid"**
- Double-check token from https://foxcode.rjj.cc/api-keys
- Ensure no extra spaces when copying
- Regenerate token if needed

**"Endpoint unreachable"**
- Check status: `python3 scripts/check_status.py`
- Try alternative endpoint
- Check your network connection

**"Model not available"**
- Verify model name spelling
- Check if model is available on your endpoint tier
- Try fallback model

### Getting Help

1. Check status page: https://status.rjj.cc/status/foxcode
2. Review detailed guides in `references/`
3. Re-run `configure_foxcode.py` to reconfigure

## File Structure

```
foxcode-openclaw/
├── SKILL.md                    # This file
├── README.md                   # Detailed setup guide
├── references/
│   ├── foxcode-endpoints.md    # Endpoint details
│   └── openclaw-config.md      # Configuration reference
├── scripts/
│   ├── configure_foxcode.py    # Interactive setup wizard
│   ├── check_status.py         # Status monitoring
│   └── validate_config.py      # Config validation
└── assets/
    └── templates/
        └── setup-checklist.md  # Printable checklist
```

## References

- **Endpoint Details**: `references/foxcode-endpoints.md`
- **OpenClaw Config**: `references/openclaw-config.md`
- **Setup Checklist**: `assets/templates/setup-checklist.md`

## Related Skills

| Skill | Use When |
|-------|----------|
| psychology-master | Need to adapt teaching for different learner profiles |
| ui-ux-pro-max | Need to create additional visual guides |

## Changelog

### v1.1.0 (Current)
- Multi-endpoint selection (comma-separated or "all")
- All 3 models added to each selected endpoint
- Environment variable reference for API key security
- Auto-set `FOXCODE_API_TOKEN` in shell profile
- Separate provider for each endpoint (foxcode, foxcode-super, etc.)

### v1.0.0
- Initial release
- Interactive configuration wizard
- Status monitoring script
- Validation script
- Psychology-optimized README guide
