# Linux.do Application Writer

Craft high-pass-rate, de-AI'd Chinese applications (小作文) for Linux.do registration through an adaptive survey and rule-aware text generation.

## Install

**OpenClaw / ClawHub:**
```bash
clawhub install linuxdo-application
```

**Manual:**
```bash
git clone https://github.com/Fei2-Labs/skill-genie.git
cp -r skill-genie/linuxdo-application ~/.openclaw/skills/linuxdo-application
```

## Usage

Trigger the skill with any of these phrases:
- "write linux.do application"
- "linux.do 小作文"
- "linux.do 注册申请"
- "help me apply to linux.do"

The agent will:
1. Conduct an adaptive Chinese-language survey (5-8 questions, one at a time)
2. Generate a draft application covering all 4 required info blocks
3. Run a risk check and de-AI polish pass before outputting plain text

## Compatibility

| Agent | Compatible |
|-------|-----------|
| OpenClaw | Yes |
| Hermes | Yes |
| Claude Code | Yes |
| Other SKILL.md agents | Yes |

No scripts or external dependencies — pure SKILL.md workflow.

## File Structure

```
linuxdo-application/
├── SKILL.md                          # Main workflow
├── README.md                         # This file
└── references/
    ├── linuxdo-rules.md              # Official rules + community signals
    └── de-ai-checklist.md            # 12 AI markers to detect and fix
```

## License

MIT
