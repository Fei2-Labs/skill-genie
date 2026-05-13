# WordPress VPS Install Handoff

## Current goal

Turn this skill into a fresh-VPS WordPress installer that defaults to Docker + Dokploy.

## Locked-in scope

- Docker-only installation path
- Dokploy is the default Docker tool
- Dokploy installation is part of the skill
- No local LAMP/LEMP installation branch
- No separate live-site repair flow in this skill

## What is already done

- Renamed the skill folder to `wordpress-vps-install`
- Updated `SKILL.md` to describe the new VPS install workflow
- Updated `README.md` to match the new name
- Added the skill to the repo index README
- Added `TODO.md`
- Added `prd.md`

## Key decisions already made

- If the user chooses Docker, Dokploy is the default
- If the user does not specify another Docker tool, use Dokploy
- Domain routing and container orchestration are handled by Dokploy
- The skill should guide an agent through the install in one pass

## Current file list

- `SKILL.md`
- `README.md`
- `TODO.md`
- `prd.md`

## Suggested next step

Rewrite `SKILL.md` into the final executable flow:
1. confirm VPS/domain inputs
2. install Dokploy if missing
3. deploy WordPress + DB stack in Dokploy
4. configure routing
5. bootstrap WordPress
6. verify the public site returns 200

## Follow-up notes

- Keep the skill narrow and deterministic
- If later needed, split live-site repair into a separate skill
- Treat `TODO.md` as the lightweight backlog for future tweaks
