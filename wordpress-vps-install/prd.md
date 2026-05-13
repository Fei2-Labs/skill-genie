# wordpress-vps-install

## Goal

Create a skill for a fresh VPS that can install WordPress end-to-end with Docker, using Dokploy as the default Docker path. The skill should provision Dokploy if needed, deploy the WordPress stack, configure the public domain, run the WordPress bootstrap, and verify the site is live.

## Requirements

- Target a brand-new VPS, not an already-running WordPress site.
- Use Docker as the only installation path in this skill.
- Default the Docker path to Dokploy.
- Include Dokploy installation steps as part of the skill.
- Use Dokploy for container orchestration and domain routing.
- Bootstrap WordPress on the live volume with WP-CLI or equivalent one-shot install logic.
- Verify the public domain returns `200` and shows the WordPress homepage.
- Keep the flow reproducible and guided so an agent can complete it in one run.

## Acceptance Criteria

- [ ] The skill clearly documents that local/non-Docker installation is out of scope.
- [ ] The skill defaults to Dokploy when no other Docker tool is specified.
- [ ] The skill includes Dokploy installation or bootstrap steps for a fresh VPS.
- [ ] The skill includes WordPress stack deployment, domain routing, and install steps.
- [ ] The skill includes a final verification step for `200` response and homepage content.
- [ ] The skill can be followed on a clean VPS without relying on prior WordPress setup.

## Definition of Done

- Skill workflow is clear and linear.
- The default Docker path is unambiguous.
- Dokploy installation is included and not treated as a separate prerequisite.
- Verification steps are explicit and testable.
- TODO items are either completed or tracked separately.

## Technical Approach

Use a single Docker-only path centered on Dokploy. The skill should start with host and domain confirmation, then install Dokploy if absent, then create or deploy the WordPress stack, configure routing in Dokploy, run the WordPress bootstrap against the live volume, and verify the public URL.

This approach keeps the skill focused on new VPS bootstrap and avoids splitting the workflow into separate local and Docker branches.

## Decision (ADR-lite)

**Context**: The initial concept included both local and Docker installation paths, but the user narrowed the scope to fresh VPS deployment with Docker and Dokploy as the default.

**Decision**: Make Docker the only supported installation path in this skill, default to Dokploy, and include Dokploy installation in the workflow.

**Consequences**: The skill becomes simpler and more reliable for fresh VPS bootstrapping, but it no longer covers local LAMP/LEMP-style installs or alternate Docker orchestration tools.

## Out of Scope

- Local installation without Docker
- LAMP/LEMP or other system-package-based WordPress installs
- Alternate Docker orchestrators as first-class paths
- Migration or repair of an already-live WordPress instance

## Technical Notes

- Current skill folder: `wordpress-vps-install`
- Existing files: `SKILL.md`, `README.md`, `TODO.md`
- Repo index already includes the skill
- This PRD reflects the narrowed scope: fresh VPS, Docker-only, Dokploy default
- If future support for other Docker tools is needed, it should become a separate follow-up or a second workflow
