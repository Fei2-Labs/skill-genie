---
name: "wordpress-vps-install"
description: "Bootstrap a fresh VPS with WordPress installed and verified end-to-end; use when you need to provision the stack, align volumes and environment variables, run WP-CLI installation, and confirm the public site is live."
license: "MIT"
metadata: {"version":"1.3.2","category":"wordpress-install","license":"MIT","tags":["wordpress","vps","deployment","dokploy"],"hermes":{"tags":["wordpress","vps","deployment","dokploy"]}}
---

# WordPress VPS Install

Use this skill when setting up a brand-new VPS so WordPress installs successfully and the public site comes online cleanly.

## Scope

This skill covers:
- fresh VPS provisioning for a WordPress site
- Docker Compose or container-based WordPress + MySQL setup
- proxy/routing labels for the public domain
- `.env` bootstrap values for WordPress and database setup
- WP-CLI installation on the live volume
- durable WP-CLI availability across container redeploys
- theme and plugin activation after install
- public verification after deployment
- repository hygiene so dev-meta folders are not synced to GitHub/VPS deploy

## Repo sync hygiene (mandatory)

Before first deploy in a new WordPress VPS repo, ensure non-runtime folders are not synced:

- `.claude/`
- `.cursor/`
- `.trellis/`
- `docs/` (unless user explicitly wants docs versioned)

Commands:

```bash
# add ignore rules
printf "\n.claude/\n.cursor/\n.trellis/\ndocs/\n" >> .gitignore

# stop tracking already-committed folders without deleting local files
git rm -r --cached .claude .cursor .trellis docs
```

Rule:
- Keep runtime WordPress artifacts only (theme/plugin/config/deploy-relevant files) in deploy sync.

## Dokploy-only operations (mandatory)

All services must be created and managed through Dokploy only.

Hard rules:
- Deploy and update services only through Dokploy CLI or Dokploy API.
- Do not deploy app services by ad-hoc SSH `docker compose up` outside Dokploy CLI/API project management.
- Do not keep long-lived manually created stacks that are not visible in Dokploy UI.
- If an emergency SSH change is made, it must be migrated into Dokploy immediately and the manual stack removed.
- Always verify the resulting service is visible and manageable in Dokploy UI before considering the task complete.

## Quick start

```text
1. Confirm the public domain and target VPS
2. Inspect the container stack and compose files
3. Verify the WordPress volume, DB env, and proxy labels
4. Fix the smallest missing piece
5. Run WP-CLI install against the live volume
6. Verify the domain returns 200 and the homepage loads
```

## Triggers

- "set up WordPress on a new VPS"
- "install WordPress on this server"
- "bootstrap a fresh WordPress instance"
- "new machine WordPress install"
- "make the VPS serve the homepage"
- "WordPress install succeeded locally but not on the domain"

## Installation workflow

### 0. Non-negotiable safety protocol (run first)

Before any `docker compose up/down` or compose edits on VPS:

```bash
# 0.1 identify the exact Dokploy project and compose path
docker inspect <wordpress-container> --format '{{ index .Config.Labels "com.docker.compose.project" }} {{ index .Config.Labels "com.docker.compose.project.config_files" }}'

# 0.2 mandatory backup (compose + env) with timestamp
TS="$(date +%Y%m%d-%H%M%S)"
cp /etc/dokploy/compose/<project>/code/docker-compose.yml /etc/dokploy/compose/<project>/code/docker-compose.yml.bak.$TS
cp /etc/dokploy/compose/<project>/code/.env /etc/dokploy/compose/<project>/code/.env.bak.$TS

# 0.3 validate with explicit project name and env file
cd /etc/dokploy/compose/<project>/code
docker compose -p <project> --env-file .env config >/tmp/<project>.resolved.yml
```

Hard rules:
- Never run `docker compose` without `-p <project>` on Dokploy hosts.
- Never run compose commands from the wrong directory.
- Never create ad-hoc project names (for example accidental `code-*` stacks).
- Never use guessed DB/env values; use values from the active Dokploy `.env`.
- If health degrades after change, restore backup immediately:

```bash
cp docker-compose.yml.bak.<timestamp> docker-compose.yml
cp .env.bak.<timestamp> .env
docker compose -p <project> --env-file .env up -d
```

### 1. Confirm the target

Collect the minimal target info:
- public domain
- VPS host or SSH alias
- WordPress title
- admin username
- admin email
- whether the site should be installed from scratch or attached to an existing volume

### 2. Inspect the live stack

Check the running services, network, and mounts.

```bash
docker ps --format "{{.ID}} {{.Image}} {{.Names}} {{.Status}}"
docker inspect <wordpress-container>
docker inspect <db-container>
```

Verify:
- WordPress container is up
- database container is healthy
- both containers share the expected network
- WordPress files live on a persistent volume
- any theme/plugin bind mounts point at the right paths

### 3. Verify environment variables

The install job must use the real live env values, not placeholders.

```bash
docker inspect -f '{{range .Config.Env}}{{println .}}{{end}}' <wordpress-container> | grep -E 'WORDPRESS_|MYSQL_'
```

Check:
- `WORDPRESS_DB_HOST`
- `WORDPRESS_DB_NAME`
- `WORDPRESS_DB_USER`
- `WORDPRESS_DB_PASSWORD`
- `WORDPRESS_URL`
- `WORDPRESS_TITLE`
- `WORDPRESS_ADMIN_USER`
- `WORDPRESS_ADMIN_PASSWORD`
- `WORDPRESS_ADMIN_EMAIL`

### 4. Confirm the volume alignment

The WP-CLI container must operate on the same `/var/www/html` data as the live WordPress container.

Good patterns:
- `--volumes-from <wordpress-container>`
- the exact same named volume mounted at `/var/www/html`

Bad patterns:
- a fresh anonymous volume
- running `wp` in a container that cannot see the live site files

### 5. Install WordPress on the live volume

Use the live WordPress files and the real DB credentials.

```bash
docker run --rm \
  --network <wordpress-network> \
  --volumes-from <wordpress-container> \
  --entrypoint sh \
  -e WORDPRESS_DB_HOST=<db-host> \
  -e WORDPRESS_DB_NAME=<db-name> \
  -e WORDPRESS_DB_USER=<db-user> \
  -e WORDPRESS_DB_PASSWORD=<db-password> \
  -e WORDPRESS_URL=https://example.com \
  -e WORDPRESS_TITLE="Site Name" \
  -e WORDPRESS_ADMIN_USER=admin \
  -e WORDPRESS_ADMIN_PASSWORD='change-me' \
  -e WORDPRESS_ADMIN_EMAIL=admin@example.com \
  wordpress:cli-php8.2 -lc '
    if ! wp core is-installed --path=/var/www/html --allow-root; then
      wp core install --path=/var/www/html --allow-root \
        --url="$WORDPRESS_URL" \
        --title="$WORDPRESS_TITLE" \
        --admin_user="$WORDPRESS_ADMIN_USER" \
        --admin_password="$WORDPRESS_ADMIN_PASSWORD" \
        --admin_email="$WORDPRESS_ADMIN_EMAIL" \
        --skip-email;
    fi;
    wp theme activate <theme-slug> --path=/var/www/html --allow-root || true;
    wp plugin activate <plugin-slug> --path=/var/www/html --allow-root || true;
  '
```

### 5.1 Ensure CLI tools are durable (host + container)

If `wp` or `rg` is missing, install baseline tools on the VPS host:

```bash
apt-get update -y
apt-get install -y ripgrep curl less php-cli php-curl php-mbstring php-xml
curl -fsSL https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar -o /usr/local/bin/wp
chmod +x /usr/local/bin/wp
wp --info
rg --version
```

Important:
- Host-level installs can help ad-hoc diagnostics, but they do not make WP-CLI available inside a recreated WordPress app container.
- Installing `wp` interactively inside a running container is usually ephemeral and may disappear after redeploy.

Preferred durable approach:
- Keep a dedicated `wpcli` service in `docker-compose.yml` using `wordpress:cli-*`.
- Mount the same live WordPress volume (`/var/www/html`) and same project bind mount (`./wp-content`) as the app container.
- Keep the service running (for example with `restart: unless-stopped` and a long-running sleep loop), so `docker exec <wpcli-container> wp ...` is always available.
- Do not rely on one-time `profiles: ["setup"]` if ongoing CLI access is required.
- Use `command: ["sleep", "infinity"]` (preferred) instead of shell loop strings to avoid quoting/parsing errors.

Example durable service shape:

```yaml
wpcli:
  image: wordpress:cli-php8.2
  restart: unless-stopped
  depends_on:
    db:
      condition: service_healthy
    wordpress:
      condition: service_started
  volumes:
    - wordpress_data:/var/www/html
    - ./wp-content:/var/www/html/wp-content
  command: ["sleep", "infinity"]
```

### 6. Handle common blockers

#### Wrong DB host

If the install fails with database connection errors:
- inspect the live container env again
- use the actual DB host name from the network

#### TLS/SSL DB error

If `wp db check` fails with a certificate error:
- skip the precheck
- use the direct install command if the database is otherwise reachable

#### Router mismatch

If the domain still returns 404 after containers are healthy:
- inspect proxy labels
- point the public host rule at the real WordPress service

#### Wrong volume

If install succeeds but the site still shows install or old content:
- rerun using the live WordPress volume

#### WP-CLI works on host but not in container

If host `wp` works but app/container commands fail:
- verify which container actually contains `/var/www/html` with `wp-config.php`
- prefer a dedicated `wpcli` service over patching the web container
- execute commands with:

```bash
docker exec <wpcli-container> sh -lc 'cd /var/www/html && wp --allow-root <command>'
```

### 7. Verify the result

```bash
curl -k -I https://example.com/
curl -k https://example.com/ | head
```

Expect:
- `200` response on the public URL
- homepage HTML instead of install redirect
- theme and plugin output present

## Safety rules

- Do not delete existing volumes unless the user explicitly asks for a reset.
- Do not trust placeholder `.env` values on the VPS.
- Do not assume the first WP-CLI container used the correct live volume.
- Prefer the smallest repair that gets the public site working.

## Exit criteria

The install is complete when:
- the public URL returns `200`
- the homepage renders
- `wp core is-installed` succeeds on the live volume
- theme/plugin activation is done or intentionally skipped
- the site is reachable without an install redirect
