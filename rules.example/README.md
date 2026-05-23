# Rules

Your personalized agent rules go here. Two ways to set them up:

## Option 1: Let your agent generate them (recommended)

Tell your agent:
```
skillgenie read init-rules
```
It will ask you a few questions and generate your rules automatically.

## Option 2: Manual

Copy the starter files and edit them yourself:
```bash
cp rules.example/router.md rules/
cp rules.example/session-sync.md rules/
cp rules.example/workflow-tools.md rules/
cp rules.example/stack-and-deployment.md rules/
cp rules.example/external-tools.md rules/
```

## Files

| File | Purpose |
|------|---------|
| `router.md` | Top-level universal rules |
| `session-sync.md` | Session start, git sync |
| `workflow-tools.md` | Tool preferences, debugging |
| `stack-and-deployment.md` | Tech stack, deployment |
| `external-tools.md` | Skills and external tools |

After editing, run `./setup.sh` to apply.
