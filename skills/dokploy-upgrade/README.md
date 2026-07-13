# dokploy-upgrade

Upgrade Dokploy on a VPS running Docker Swarm.

## What it does

`dokploy-upgrade` upgrades a Dokploy PaaS instance running in Docker Swarm via the official `install.sh` update path, with release-note review, resource and Swarm pre-flight checks, host-mode port conflict handling, and verified convergence.

## When to use

- Upgrading Dokploy to the latest or a specific version
- Managing a fleet of VPS hosts running Dokploy
- Needing a repeatable, verified upgrade procedure for Docker Swarm deployments

## Key features

- Current version detection via `docker service inspect`
- Latest version check against GitHub releases
- Release-note review for every version crossed
- Pre-flight health and resource checks (disk, memory, swap, and Swarm convergence)
- Official `install.sh` update path with a pinned target version and HTTP-failure-safe download
- Handling of the `host-mode port already in use` Swarm update behavior
- Post-upgrade polling for the exact image, a running Swarm task, UI HTTP 200, and all services converged
- Rollback procedure via version pinning and the same verification gate
- Host documentation update step
