# Workflow and tools

Preferences for how the agent works: CLI vs MCP, batching, debugging approach, verification.

## ClawdHub publishing

When a skill under `skills/` is modified and committed, publish it to ClawdHub:

```bash
clawdhub publish ./skills/<skill-name> --slug <skill-name> --version <new-version> --changelog "<summary of changes>"
```

Rules:
- Bump the version beyond what is currently on ClawdHub (`clawdhub list` to check).
- Update the `version` field in the skill's SKILL.md frontmatter to match.
- The `--changelog` must be a concise summary of what changed.
- Always include `--tags` with comma-separated tags describing the skill's function (e.g. `session-memory,workflow,handoff`). Derive tags from the skill's category and purpose.
- Do not publish if the skill has uncommitted changes — commit first.
- If `clawdhub` is not in PATH, skip and inform the user.

<!-- Generate with: skillgenie read init-rules -->
