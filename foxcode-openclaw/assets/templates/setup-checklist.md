# Foxcode OpenClaw Setup Checklist

> Print this checklist and check off items as you complete them.

**Setup Goal:** Configure Foxcode AI models in OpenClaw  
**Estimated Time:** 10-15 minutes  
**Skill Level:** Beginner-friendly

---

## Pre-Setup Preparation

Before you begin, ensure you have:

- [ ] A Foxcode account (register at [foxcode.rjj.cc](https://foxcode.rjj.cc/auth/register))
- [ ] OpenClaw installed on your system
- [ ] Basic familiarity with editing text files
- [ ] About 15 minutes of uninterrupted time

---

## Phase 1: Get API Token (3 min)

### Step 1: Log in to Foxcode

- [ ] Visit [foxcode.rjj.cc/auth/login](https://foxcode.rjj.cc/auth/login)
- [ ] Enter your credentials
- [ ] Successfully logged in

### Step 2: Generate API Token

- [ ] Navigate to [API Keys page](https://foxcode.rjj.cc/api-keys)
- [ ] Click "Create New Key" (or similar button)
- [ ] Enter a descriptive name (e.g., "My OpenClaw Setup")
- [ ] Generate the token
- [ ] **Copy token immediately** (it may not be shown again!)
- [ ] Store token temporarily in a secure text file

**Token Format Check:** Does your token look like `sk-foxcode-xxxxxxxx...`?
- [ ] Yes, format looks correct

---

## Phase 2: Choose Endpoint (2 min)

### Understanding Your Options

Review the endpoints and select one:

| Endpoint | Best For | Reliability | Cost |
|----------|----------|-------------|------|
| Official | Beginners, reliability | ★★★★★ | $$$ |
| Super | Cost savings | ★★★★☆ | $$ |
| Ultra | Maximum savings | ★★★☆☆ | $ |
| AWS | Speed priority | ★★★★★ | $$$ |
| AWS Thinking | Complex tasks | ★★★★★ | $$$ |

### Decision

- [ ] Checked current endpoint status: `python3 scripts/check_status.py`
- [ ] Selected endpoint: ___________________
- [ ] Base URL: ___________________

**For Beginners:** We recommend starting with the **Official** endpoint (`https://code.newcli.com/claude`).

---

## Phase 3: Configure OpenClaw (5 min)

### Step 1: Locate Config File

- [ ] Found config file location:
  - macOS/Linux: `~/.config/openclaw/config.json`
  - Or searched with: `find ~ -name "config.json" -path "*/openclaw/*"`
- [ ] Opened config file in text editor

### Step 2: Set Base Configuration

Add or update these fields:

```json
{
  "base_url": "YOUR_ENDPOINT_URL",
  "api_key": "YOUR_API_TOKEN"
}
```

- [ ] Set `base_url` to selected endpoint
- [ ] Set `api_key` to your token
- [ ] Saved the file

### Step 3: Choose Primary Model

**Options:**
- `claude-opus-4-5-20251101` - Most capable (complex tasks)
- `claude-sonnet-4-5-20251101` - Balanced (recommended for daily use) ✓
- `claude-haiku-4-5-20251101` - Fast and cheap (quick tasks)

- [ ] Selected primary model: ___________________
- [ ] Added to config: `"model": "SELECTED_MODEL"`
- [ ] Saved the file

**Beginner Recommendation:** Use `claude-sonnet-4-5-20251101` for the best balance.

### Step 4: Configure Fallback Models

- [ ] Decided on fallback strategy:
  - [ ] Conservative (Sonnet → Haiku → Opus)
  - [ ] Speed-First (Haiku → Sonnet)
  - [ ] Capability-First (Opus → Sonnet)
  - [ ] No fallbacks (simple setup)

If using fallbacks, add to config:
```json
"fallback_models": [
  "claude-haiku-4-5-20251101",
  "claude-opus-4-5-20251101"
]
```

- [ ] Added fallback models to config (if applicable)

---

## Phase 4: Validate & Test (3 min)

### Validation

- [ ] Ran validator: `python3 scripts/validate_config.py`
- [ ] All checks passed
- [ ] If errors, reviewed and fixed them

### Common Validation Fixes

If you see these errors:

**"Invalid JSON"**
- [ ] Checked for missing commas, brackets, or quotes
- [ ] Validated with: `python3 -m json.tool config.json`

**"API token invalid"**
- [ ] Re-copied token from Foxcode dashboard
- [ ] Removed any extra spaces

**"Cannot reach endpoint"**
- [ ] Checked internet connection
- [ ] Verified URL spelling
- [ ] Tried different endpoint

### Testing

- [ ] Restarted OpenClaw (if it was running)
- [ ] Started OpenClaw
- [ ] Ran a test prompt: "Hello, can you confirm my Foxcode setup is working?"
- [ ] Received a valid response

---

## Post-Setup

### Documentation

- [ ] Bookmarked status page: https://status.rjj.cc/status/foxcode
- [ ] Saved API token in password manager (if not using env var)
- [ ] Noted which endpoint I'm using

### Quick Reference Commands

Save these for later:

```bash
# Check endpoint status
python3 scripts/check_status.py

# Validate config
python3 scripts/validate_config.py

# Reconfigure (interactive)
python3 scripts/configure_foxcode.py
```

---

## Troubleshooting Notes

If you encounter issues, document them here:

**Issue:** ___________________
**Solution:** ___________________

**Issue:** ___________________
**Solution:** ___________________

---

## Completion

- [ ] Configuration working
- [ ] Test prompt successful
- [ ] All set! 🎉

**Date Completed:** _______________

---

## Optional: Advanced Configuration

Once basic setup is working, consider:

- [ ] Setting environment variable for API token (more secure)
- [ ] Adjusting `timeout` for your network (default: 60 seconds)
- [ ] Tuning `max_tokens` for your use case
- [ ] Experimenting with different endpoints
- [ ] Setting up multiple profiles for different tasks

---

## Resources

- **Status Page:** https://status.rjj.cc/status/foxcode
- **API Keys:** https://foxcode.rjj.cc/api-keys
- **Setup Guide:** See `README.md` in this skill
- **Endpoint Details:** See `references/foxcode-endpoints.md`
- **Config Reference:** See `references/openclaw-config.md`

---

**Questions or Issues?**

Run the interactive setup wizard:
```bash
python3 scripts/configure_foxcode.py
```
