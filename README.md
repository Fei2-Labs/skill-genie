# skill-genie

[![Last commit](https://img.shields.io/github/last-commit/clarezoe/skill-genie)](https://github.com/clarezoe/skill-genie/commits/main)
[![Stars](https://img.shields.io/github/stars/clarezoe/skill-genie)](https://github.com/clarezoe/skill-genie/stargazers)
[![Issues](https://img.shields.io/github/issues/clarezoe/skill-genie)](https://github.com/clarezoe/skill-genie/issues)

A curated collection of reusable skills and workflows that turn everyday tasks into fast, repeatable actions.

## Why this exists

Most personal automation fails because the best methods live in scattered notes. This repo turns those methods into clear, reusable skills that are easy to find, run, and improve.

## What's inside

- Skill folders with their own `SKILL.md` and supporting assets.
- References and scripts that keep each skill practical and maintainable.

## Featured skills

- [`omnidebug-autopilot`](./omnidebug-autopilot): Autonomous root-cause debugging workflow with deterministic browser reproduction, artifact capture, and fix verification scripts.
- [`close-loop`](./close-loop): End-of-session ship-and-memory workflow with typed memory consolidation, safety gates, and publish queue handling.

## Skill layout

Each skill folder should contain:

- `SKILL.md` for the main execution workflow
- `README.md` for quick orientation
- `references/` for source docs and deeper notes
- `assets/` for templates and reusable artifacts
- `scripts/` only when automation clearly reduces manual work

## How to use

1. Browse a skill folder that matches your task.
2. Read the skill `README.md` for scope and files.
3. Open `SKILL.md` and follow the workflow.
4. Use included references, scripts, and templates when needed.

## Add a new skill

- Keep it focused on a single job.
- Document the happy path and edge cases in `SKILL.md`.
- Include scripts or assets when they remove manual work.

## Principles

- Small, composable skills over monoliths.
- Clear steps over clever tricks.
- Practical defaults with room to customize.
