# refactor-agents-md

Refactor bloated AGENTS.md / CLAUDE.md into clean, topic-specific docs.

## What it does

`refactor-agents-md` takes a monolithic agent guidance file that has grown into a "ball of mud" and splits it into a minimal root file plus topic-specific follow-up documents using progressive disclosure.

## When to use

- Your AGENTS.md or CLAUDE.md has grown too large with contradictions and stale instructions
- User asks to clean up, split, or review agent guidance files

## How it works

1. Analyze the existing file for sections, contradictions, and bloat
2. Extract topic-specific content into separate focused documents
3. Create a minimal root file that routes to topic docs on demand
4. Remove contradictions and stale instructions

## Key features

- Progressive disclosure: agents only load what they need
- Detects contradictions and redundancy
- Preserves important rules while removing noise
- Works with any agent config format (AGENTS.md, CLAUDE.md, etc.)

---

**Source**: [github.com/Fei2-Labs/skill-genie](https://github.com/Fei2-Labs/skill-genie)
**Author**: [@clarezoe](https://x.com/clarezoe)
