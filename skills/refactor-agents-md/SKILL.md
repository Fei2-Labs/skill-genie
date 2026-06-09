---
name: "refactor-agents-md"
description: "Refactors AGENTS.md files into a minimal root file plus topic-specific follow-up docs using progressive disclosure. Use when cleaning up, splitting, or reviewing AGENTS.md / CLAUDE.md guidance — or when the file has grown into a \"ball of mud\" with contradictions, bloat, and stale instructions."
license: "MIT-0"
metadata: {"openclaw":{"emoji":"🧹","homepage":"https://github.com/Fei2-Labs/skill-genie"},"category":"developer-tools","author":"Skill Genie","tags":["agents-md","claude-md","refactoring","progressive-disclosure","ai-config"],"version":"1.0.2","license":"MIT-0","hermes":{"tags":["agents-md","claude-md","refactoring","progressive-disclosure","ai-config"]}}
---

<objective>
Refactor AGENTS.md files so the root file stays small, stable, and broadly useful while detailed guidance moves into focused follow-up docs. The skill helps identify contradictions, separate essentials from bloat, and produce a clearer instruction hierarchy that is easier for agents to follow.
</objective>

<quick_start>
1. Identify whether the user wants a review, a rewrite proposal, or an in-repo refactor.
2. Read the current AGENTS.md content and classify each instruction as root-essential, topic-specific, conflicting, redundant, vague, or stale.
3. Keep only universal instructions in the root file, move the rest into topic docs, and surface any contradictions before editing.
</quick_start>

<essential_principles>
<principle name="keep-root-minimal">
The root AGENTS.md should contain only what applies to every task: a one-line project description, package manager expectations if non-default, non-standard build or typecheck commands, and truly universal constraints.
</principle>

<principle name="resolve-conflicts-first">
If two instructions disagree, do not silently merge them. Surface the conflict, explain the tradeoff briefly, and ask the user which version to keep before rewriting.
</principle>

<principle name="group-by-purpose">
Move remaining guidance into separate files grouped by topic or behavior, not by author, chronology, or file location.
</principle>

<principle name="delete-bloat">
Flag redundant, vague, self-evident, or outdated instructions for deletion instead of preserving them in a new location.
</principle>

<principle name="prefer_progressive_disclosure">
Keep the root file as a router into narrower guidance. Detail belongs in follow-up docs that are only read when relevant.
</principle>
</essential_principles>

<intake>
Ask the user which mode they want:
1. Review only
2. Propose a rewrite
3. Apply the refactor in the repo

If the user already gave enough context, skip extra questions and go straight to the matching workflow.
</intake>

<routing>
<mode name="review-only">workflows/audit-agents-md.md</mode>
<mode name="propose-rewrite">workflows/audit-agents-md.md</mode>
<mode name="apply-refactor">workflows/refactor-agents-md.md</mode>
</routing>

<reference_index>
All shared guidance lives in references/:

**Principles and heuristics:** references/principles.md
</reference_index>

<workflows_index>
<workflow name="audit-agents-md.md">Review an AGENTS.md file, classify instructions, and propose a minimal split.</workflow>
<workflow name="refactor-agents-md.md">Inspect the repo and rewrite AGENTS.md files in place.</workflow>
</workflows_index>

<success_criteria>
The skill is complete when it can consistently:
- identify contradictions before rewriting
- keep root AGENTS.md content minimal
- split topic-specific guidance into separate docs
- flag redundant, vague, and stale instructions for deletion
- produce a clear proposed file structure or apply it in the repo
</success_criteria>
