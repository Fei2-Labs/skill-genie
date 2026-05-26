# shared-memory

Portable project memory that any AI agent can find.

## What it does

`shared-memory` defines an on-disk convention for storing project knowledge that works across all AI coding agents (Claude Code, Cursor, Codex, OpenClaw, Aider, etc.). It includes a shared layer in the project repo and a private layer for personal notes.

## When to use

- Saving project knowledge that should survive across tools
- User says "save to shared memory", "remember this for all agents"
- When you suspect another agent's memory might be relevant

## How it works

1. Reads existing shared memory from the project's `.memory/` directory
2. Writes new knowledge using a structured format with metadata
3. Private notes go to a gitignored layer
4. Any agent can discover and read the shared layer

## Key features

- Cross-agent compatible: works with any tool that can read files
- Structured format with timestamps and categories
- Private layer for personal/sensitive notes (gitignored)
- Search and retrieval across all stored knowledge

---

**Source**: [github.com/Fei2-Labs/skill-genie](https://github.com/Fei2-Labs/skill-genie)
**Author**: [@clarezoe](https://x.com/clarezoe)
