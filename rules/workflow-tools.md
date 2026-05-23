# Workflow and tools

- Prefer CLI tools over MCP when both can accomplish the same task.
- Batch independent operations instead of running them sequentially.
- Check existing context before rereading files already in context.
- Use debugging output first when logs or network traces can explain the issue.
- Verify whether the feature already exists before editing it.
- Keep the requested scope small and stop once the change is correct.
- Do not use scripts to work around a problem when the task can be solved directly.
- Keep verification focused on correctness and runtime/build errors.