---
name: "init-rules"
description: "Interactively generate personalized agent rules. Asks about tech stack, work style, and preferences, then writes customized rule files. Use when user says \"init rules\", \"set up my rules\", or \"configure agent rules\"."
license: "MIT"
requires: "Fei2-Labs/skill-genie"
metadata: {"version":"1.0.2","tags":["agent-rules","configuration","onboarding","workflow"],"hermes":{"tags":["agent-rules","configuration","onboarding","workflow"]}}
---

# Init Rules

> **Requires [Skill Genie](https://github.com/Fei2-Labs/skill-genie)**. This skill generates rule files for the skill-genie `rules/` directory. Install skill-genie first, then run this skill.

Generate personalized agent rule files through a short interview.

## Process

Ask the user these questions ONE AT A TIME. After each answer, move to the next. Skip questions the user says aren't relevant.

### 1. Work style
- "How should I behave? (e.g., execute without asking, ask before acting, explain reasoning, be concise)"

### 2. Tech stack
- "What's your default tech stack? (e.g., Nuxt + Appwrite, Next.js + Supabase, Rails, Swift/macOS, none)"

### 3. Package manager
- "Package manager preference? (pnpm, npm, yarn, bun, or N/A)"

### 4. Deployment
- "How do you deploy? (e.g., Vercel, Dokploy, Docker, AWS, manual, none)"

### 5. Git workflow
- "Git rules? (e.g., never push without asking, auto-push OK, use PRs, conventional commits)"

### 6. Code quality
- "Any hard code rules? (e.g., no `any`, max file length, test required, specific linter)"

### 7. Skills integration
- "Should I auto-load skills when a task matches? (yes/no)"

### 8. Session behavior
- "Anything special at session start? (e.g., check upstream, read AGENTS.md, run status)"

## Output

Before writing, if `rules/` already contains `.md` files:
1. Read all existing rule files fully — understand the user's current preferences and intent
2. Back them up: `mv rules/ rules.bak.$(date +%Y%m%d%H%M)/ && mkdir rules/`
3. When generating new rules, compare the user's new answers against their existing rules:
   - **No conflict**: Keep the existing rule as-is in the new output
   - **Conflict detected**: Explain the conflict to the user, suggest which version is better and why, then ask which to use
   - **New rule with no existing equivalent**: Add it
4. The goal is to produce rules that reflect the user's FULL intent — both what they said in this interview AND what they previously established

After collecting answers, generate these files in the skill-genie `rules/` directory:

- `rules/router.md` — Universal top-level rules
- `rules/session-sync.md` — Session start behavior
- `rules/workflow-tools.md` — Tool and workflow preferences
- `rules/stack-and-deployment.md` — Tech stack and deployment (skip if "none")
- `rules/external-tools.md` — Skills and external tool usage

Then run `setup.sh` to apply them.

## Rules format

Each file should be concise Markdown, under 30 lines. Use bullet points. No fluff. Example:

```markdown
# Workflow and tools

- Prefer CLI over MCP when both can do the job.
- Batch independent operations.
- Verify feature doesn't already exist before creating it.
```

## Important

- Do NOT include project-specific details — those belong in project AGENTS.md
- Keep rules universal (apply to any project the user works on)
- If user says "same as example", copy from `rules.example/`
