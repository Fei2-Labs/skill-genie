<principles>
<rule name="root_scope">
Treat the root AGENTS.md as a universal contract, not a knowledge dump. Keep only instructions that should apply to every task in the repository.
</rule>

<rule name="universal_content">
Good root content is usually limited to:
- a one-sentence project description
- package manager or workspace expectations if non-default
- non-standard build, test, or typecheck commands
- repository-wide safety constraints that matter for every task
</rule>

<rule name="split_triggers">
Move content out of the root file when it is specific to one domain, one workflow, or one tool. If only some tasks need it, it belongs elsewhere.
</rule>

<rule name="contradiction_handling">
When instructions conflict, preserve neither by default. Identify the exact conflict, explain the consequence of each option, and ask the user to choose.
</rule>

<rule name="bloat_signals">
Treat these as deletion candidates unless there is a strong reason to keep them:
- obvious advice the agent already knows
- duplicated instructions with slightly different wording
- vague slogans that do not change behavior
- stale references to paths, commands, or project state
</rule>

<rule name="file_organization">
Prefer a small root file with direct links to topic-specific docs. Name follow-up files by purpose, such as testing, formatting, release, or platform-specific guidance.
</rule>

<rule name="output_goal">
A good refactor leaves the root file shorter, clearer, and easier to scan, while the total guidance stays available in focused follow-up docs.
</rule>
</principles>
