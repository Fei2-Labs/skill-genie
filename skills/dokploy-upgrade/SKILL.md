---
name: "dokploy-upgrade"
description: "Upgrade Dokploy on a VPS running Docker Swarm. Covers version check, breaking-change review, pre-flight health checks, the official install.sh update path, host-mode port conflict handling, and post-upgrade verification. Use when the user asks to upgrade/update Dokploy on any fleet host."
license: "MIT"
metadata: {"version":"1.0.0","category":"infrastructure","license":"MIT","tags":["infrastructure","dokploy","docker-swarm","devops","upgrade"],"hermes":{"tags":["infrastructure","dokploy","docker-swarm","devops","upgrade"]}}
---

# Dokploy Upgrade

Upgrade a Dokploy PaaS instance running in Docker Swarm on a VPS.

## Triggers

- "upgrade dokploy"
- "update dokploy"
- "dokploy version upgrade"
- "升级 dokploy"

## Required Inputs

- SSH alias for the target host (e.g. `shuttleup`, `otamatone`)
- Optional: specific target version (defaults to latest release)

## Procedure

### 1. Determine current version

```bash
ssh <host> "docker service inspect dokploy --format '{{.Spec.TaskTemplate.ContainerSpec.Image}}'"
```

Extract the tag (e.g. `v0.28.8`).

### 2. Check latest version

```bash
# Web search: "dokploy latest version release github"
# Or fetch the GitHub releases page:
# https://github.com/Dokploy/dokploy/releases
```

Compare current vs latest. If already latest, stop and report.

### 3. Review breaking changes

If it's a minor/major version jump (e.g. 0.28 → 0.29), fetch the release notes
for the target version and the intermediate minor versions. Look for:
- Database migrations
- Breaking config changes
- Required manual steps

Report any concerns to the user before proceeding.

### 4. Pre-flight health check

```bash
ssh <host> "docker service ls --format '{{.Name}}\t{{.Replicas}}\t{{.Image}}'"
```

All services must show `1/1` (or expected replica count). Do not proceed if
any service is unhealthy.

Also check node availability:

```bash
ssh <host> "docker node ls --format '{{.Hostname}}\t{{.Status}}\t{{.Availability}}'"
```

### 5. Run the upgrade

**To latest:**

```bash
ssh <host> "curl -sSL https://dokploy.com/install.sh | sh -s update"
```

**To a specific version:**

```bash
ssh <host> "export DOKPLOY_VERSION=v0.29.11 && curl -sSL https://dokploy.com/install.sh | sh -s update"
```

The script pulls the new image and runs `docker service update --image ...`.

### 6. Handle "host-mode port already in use"

Dokploy publishes port 3000 in **host mode**. During `docker service update`,
Swarm must stop the old container before starting the new one. The update
output will show repeated:

```
overall progress: 0 out of 1 tasks
1/1: no suitable node (host-mode port already in use on 1 node)
```

**This is normal.** The old container eventually releases the port and the new
one starts. Wait for the command to complete — do not interrupt.

If it genuinely stalls (more than ~2 minutes of the same message), check:

```bash
ssh <host> "docker service inspect dokploy --format '{{.UpdateStatus.State}} {{.UpdateStatus.Message}}'"
```

- `updating` → still in progress, keep waiting
- `completed` → done
- `paused` / `rollback` → problem, investigate

### 7. Post-upgrade verification

```bash
# Image updated
ssh <host> "docker service inspect dokploy --format '{{.Spec.TaskTemplate.ContainerSpec.Image}}'"

# Service healthy
ssh <host> "docker service ls --format '{{.Name}}\t{{.Replicas}}\t{{.Image}}' | grep dokploy"

# Container running and healthy
ssh <host> "docker ps --format '{{.Names}}\t{{.Image}}\t{{.Status}}' | grep dokploy"

# Update status
ssh <host> "docker service inspect dokploy --format '{{.UpdateStatus.State}} {{.UpdateStatus.Message}}'"

# UI reachable (Dokploy runs on :3000)
ssh <host> "curl -sS -o /dev/null -w '%{http_code}' http://localhost:3000"

# All other services still healthy
ssh <host> "docker service ls --format '{{.Name}}\t{{.Replicas}}\t{{.Image}}'"
```

Expected: image tag matches target version, container `Up (healthy)`, update
status `completed`, UI returns `200`, all services `1/1`.

### 8. Update host documentation

After a successful upgrade, update the host's markdown file in `hosts/`:

```markdown
_Last verified <YYYY-MM-DD>. Dokploy upgraded <old> → <new>._
```

Commit the change.

## Rollback

If the upgrade fails and Dokploy is broken:

```bash
ssh <host> "export DOKPLOY_VERSION=<old-version> && curl -sSL https://dokploy.com/install.sh | sh -s update"
```

This re-pulls the old image and rolls the service back.

## Notes

- The `install.sh` script is the official upgrade path for both manual and
  automated Dokploy installations.
- Dokploy data lives in Docker volumes (`dokploy-postgres`, `dokploy-redis`)
  and survives image updates. No backup step is strictly required for minor
  upgrades, but a `docker volume` snapshot is prudent for major jumps.
- Traefik (`dokploy-traefik`) and the database containers
  (`dokploy-postgres`, `dokploy-redis`) are **not** updated by this process —
  only the `dokploy` service itself.
- The upgrade causes a brief downtime (~10-30s) while the old container stops
  and the new one starts.
