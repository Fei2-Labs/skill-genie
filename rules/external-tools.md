# External tools and skills

- Use Context7 for version-sensitive library, framework, API, or CLI changes unless a CLI tool can retrieve the same docs.
- Resolve the library, fetch the smallest useful snippet, and follow that instead of guessing from memory.
- When the user explicitly names a tool, product, or CLI, check capability first with `which` or `command -v`, then `<tool> --help`.
- If the tool exists, use it directly.
- If the name is ambiguous, ask one minimal disambiguation question before changing files.
- Never invent skill names.
- Use registered skills when a request clearly matches one.