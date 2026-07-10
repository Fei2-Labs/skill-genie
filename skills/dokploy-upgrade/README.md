# dokploy-upgrade

Upgrade Dokploy on a VPS running Docker Swarm.

## What it does

`dokploy-upgrade` upgrades a Dokploy PaaS instance running in Docker Swarm via the official `install.sh` update path, with pre-flight health checks, breaking-change review, host-mode port conflict handling, and post-upgrade verification.

## When to use

- Upgrading Dokploy to the latest or a specific version
- Managing a fleet of VPS hosts running Dokploy
- Needing a repeatable, verified upgrade procedure for Docker Swarm deployments

## Key features

- Current version detection via `docker service inspect`
- Latest version check against GitHub releases
- Breaking-change review for minor/major version jumps
- Pre-flight health check (all Swarm services must be healthy)
- Official `install.sh` update path (supports pinning a specific version)
- Handling of the `host-mode port already in use` Swarm update behavior
- Post-upgrade verification (image, container health, UI HTTP 200, all services)
- Rollback procedure via version pinning
- Host documentation update step
