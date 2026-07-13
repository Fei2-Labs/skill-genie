---
name: "dokploy-upgrade"
description: "Upgrade Dokploy on a VPS running Docker Swarm. Covers version check, breaking-change review, pre-flight health checks, the official install.sh update path, host-mode port conflict handling, and post-upgrade verification. Use when the user asks to upgrade/update Dokploy on any fleet host."
license: "MIT"
metadata: {"version":"1.1.0","category":"infrastructure","license":"MIT","tags":["infrastructure","dokploy","docker-swarm","devops","upgrade"],"hermes":{"tags":["infrastructure","dokploy","docker-swarm","devops","upgrade"]}}
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
- Optional: specific target version. Resolve and pin a release tag before updating;
  do not use the mutable `latest` image tag for a production upgrade.

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

Fetch the release notes for every release between the installed and target
versions, including patch releases. Look for:
- Database migrations
- Breaking config changes
- Required manual steps

Report any concerns to the user before proceeding.

### 4. Pre-flight health check

```bash
ssh <host> "docker service ls --format '{{.Name}}\t{{.Replicas}}\t{{.Image}}'"
```

Every service's running replica count must equal its desired replica count.
Do not assume `1/1`: applications can intentionally use more replicas. Stop
if this command prints a service:

```bash
ssh <host> "docker service ls --format '{{.Name}} {{.Replicas}}' | awk '{split(\$2, replicas, \"/\"); if (replicas[1] != replicas[2]) print}'"
```

Also check node availability:

```bash
ssh <host> "docker node ls --format '{{.Hostname}}\t{{.Status}}\t{{.Availability}}'"
```

Check that the control-plane replacement has adequate local headroom:

```bash
ssh <host> "df -h /; free -h; swapon --show"
```

Record the current Dokploy image tag before continuing. It is the rollback
target.

### 5. Run the upgrade

**To latest (only when an exact release tag is not required):**

```bash
ssh <host> "curl --fail --silent --show-error --location https://dokploy.com/install.sh | sh -s update"
```

**To a specific version:**

```bash
ssh <host> "export DOKPLOY_VERSION=<target-version> && curl --fail --silent --show-error --location https://dokploy.com/install.sh | sh -s update"
```

Use the specific-version form for production. The script pulls the new image
and runs `docker service update --image ...`.
It can return before the replacement task is fully running, so it is not the
completion signal.

### 6. Handle "host-mode port already in use"

Dokploy publishes port 3000 in **host mode**. During `docker service update`,
Swarm must stop the old container before starting the new one. The update
output will show repeated:

```
overall progress: 0 out of 1 tasks
1/1: no suitable node (host-mode port already in use on 1 node)
```

**This is normal.** The old container eventually releases the port and the new
one starts. Wait for the command to complete, then poll for task convergence —
do not treat the command return as proof of a healthy upgrade.

If it genuinely stalls (more than ~2 minutes of the same message), check:

```bash
ssh <host> "docker service inspect dokploy --format '{{.UpdateStatus.State}} {{.UpdateStatus.Message}}'"
```

- `updating` → still in progress, keep waiting
- `completed` → done
- `paused` / `rollback` → problem, investigate

### 7. Post-upgrade verification

```bash
# Wait up to two minutes for the exact image and a running Dokploy task.
ssh <host> '
  set -e
  for attempt in $(seq 1 24); do
    image=$(docker service inspect dokploy --format "{{.Spec.TaskTemplate.ContainerSpec.Image}}")
    replicas=$(docker service ls --format "{{.Name}} {{.Replicas}}" | sed -n "s/^dokploy //p")
    state=$(docker service ps dokploy --no-trunc --format "{{.CurrentState}}" | head -1)
    if [ "$image" = "dokploy/dokploy:<target-version>" ] && [ "$replicas" = "1/1" ] && printf "%s" "$state" | grep -q "^Running"; then
      exit 0
    fi
    sleep 5
  done
  echo "Dokploy did not converge within two minutes" >&2
  exit 1
'

# Verify the panel and every Swarm service.
ssh <host> "curl --fail --silent --show-error --max-time 10 --output /dev/null http://127.0.0.1:3000/"
ssh <host> "docker service ls --format '{{.Name}} {{.Replicas}}' | awk '{split(\$2, replicas, \"/\"); if (replicas[1] != replicas[2]) print}'"
```

Expected: the exact image tag is running, the Dokploy task is `Running`, the
panel returns HTTP `200`, and the final service-convergence command prints
nothing. Do not require Docker's `healthy` state: Dokploy may not define a
container healthcheck.

### 8. Update host documentation

After a successful upgrade, update the host's markdown file in `hosts/`:

```markdown
_Last verified <YYYY-MM-DD>. Dokploy upgraded <old> → <new>._
```

Commit the change.

## Rollback

If the upgrade fails and Dokploy is broken:

```bash
ssh <host> "export DOKPLOY_VERSION=<old-version> && curl --fail --silent --show-error --location https://dokploy.com/install.sh | sh -s update"
```

Use the same `--fail --silent --show-error --location` curl options as the
upgrade. Then rerun the full post-upgrade convergence and HTTP checks with
`<old-version>` as the target. This re-pulls the old image and rolls the
service back only after the old control plane has been verified.

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
