<required_reading>
Read references/principles.md before starting.
</required_reading>

<process>
1. Inspect the repository to find all AGENTS.md files and determine which ones apply to the target area.
2. Read the current root AGENTS.md and any inherited or nested instructions that affect it.
3. Classify each line or section into:
   - keep in root
   - move to a topic doc
   - delete
   - ask the user about because it conflicts or depends on a choice
4. If any conflicts exist, pause and ask the user which instruction to keep.
5. Draft the new root AGENTS.md so it stays minimal and points to the topic docs.
6. Create or update the topic docs with the moved guidance, keeping each file narrowly scoped.
7. Verify the result by checking that the root file reads cleanly on its own and that no important guidance was lost.
</process>

<success_criteria>
This workflow is complete when the repo has either:
- a rewritten AGENTS.md structure with the important guidance preserved and the root file minimized, or
- a precise blocker list for the user to resolve before rewriting.
</success_criteria>
