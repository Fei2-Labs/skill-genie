# init-rules

Interactively generate personalized agent rules.

## What it does

`init-rules` asks about your tech stack, work style, and preferences through a short interview, then writes customized rule files for the skill-genie `rules/` directory.

## When to use

- First time setting up skill-genie
- User says "init rules", "set up my rules", "configure agent rules"

## How it works

1. Asks questions one at a time (work style, tech stack, deployment, language preferences)
2. Skips questions the user marks as irrelevant
3. Generates rule files: `router.md`, `session-sync.md`, `workflow-tools.md`, `stack-and-deployment.md`, `external-tools.md`

## Prerequisites

Requires [Skill Genie](https://github.com/Fei2-Labs/skill-genie) to be installed first.

---

**Source**: [github.com/Fei2-Labs/skill-genie](https://github.com/Fei2-Labs/skill-genie)
**Author**: [@clarezoe](https://x.com/clarezoe)
