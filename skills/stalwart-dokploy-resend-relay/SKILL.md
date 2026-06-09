---
name: "stalwart-dokploy-resend-relay"
description: "Set up Stalwart Mail Server on a new VPS via Dokploy, with default outbound delivery through Resend SMTP relay for environments where direct SMTP port 25 egress is blocked."
license: "MIT"
metadata: {"version":"1.1.2","category":"email-infrastructure","license":"MIT","tags":["email-infrastructure","stalwart","dokploy","resend"],"hermes":{"tags":["email-infrastructure","stalwart","dokploy","resend"]}}
---

# Stalwart on Dokploy (Resend Relay Default)

Use this skill to deploy a production-ready Stalwart server on a new VPS managed by Dokploy.

Default assumption:
- outbound SMTP port `25` is blocked by provider/network
- outbound mail must go through `smtp.resend.com:587`

## Scope

This skill covers:
- preflight validation (MX, Dokploy, Stalwart)
- Stalwart deployment on Dokploy
- domain + DNS records for mailbox hosting
- TLS certificate setup for mail/web endpoints
- mailbox and admin provisioning
- relay route to Resend SMTP
- verification for IMAP/SMTP and queue behavior

## Triggers

- "set up stalwart on new vps"
- "install mail server on dokploy"
- "stalwart with resend relay"
- "smtp 25 blocked setup"
- "host support@ mailbox on vps"

## Required Inputs

- Domain: e.g. `example.com`
- Mail host: e.g. `mail.example.com`
- VPS SSH access
- Dokploy access
- Resend API key

## Mandatory Preflight (Run First)

Before any configuration changes, run all checks below.

### 1. DNS/MX check

```bash
dig +short MX <domain>
dig +short A mail.<domain>
```

Pass criteria:
- MX includes `mail.<domain>` with valid priority
- `mail.<domain>` resolves to VPS public IP

If fail:
- stop and prompt user to fix DNS first
- optionally offer to provide exact records to add

### 2. Dokploy existence check

On VPS:

```bash
docker ps --format '{{.Names}} {{.Image}}' | grep -i dokploy
```

Pass criteria:
- Dokploy services are running

If fail:
- prompt user: install Dokploy now?
- if user approves auto-install, install and verify Dokploy before continuing

### 3. Stalwart existence check

On VPS:

```bash
docker ps --format '{{.Names}} {{.Image}}' | grep -i stalwart
```

Pass criteria:
- existing Stalwart service/container found

If fail:
- prompt user: install Stalwart automatically via Dokploy now?
- if approved, deploy Stalwart and continue

## Decision Flow (Required)

Use this exact branching logic:

1. If MX is incorrect:
- do not proceed with mailbox validation
- provide DNS fix instructions
- wait for user confirmation and re-check

2. If Dokploy missing:
- ask user whether to install automatically
- if yes, install Dokploy and verify
- if no, stop with clear manual prerequisites

3. If Stalwart missing:
- ask user whether to install automatically in Dokploy
- if yes, deploy Stalwart and verify
- if no, stop with required manual steps

Only continue to next phases when all three preflight checks pass.

## DNS Baseline

Add/verify these records:

1. Mail host A:
- `mail` `A` -> `<VPS_PUBLIC_IP>`

2. Inbound MX:
- `@` `MX` priority `10` -> `mail.<domain>`

3. SPF for domain:
- `@` `TXT` -> `v=spf1 mx include:amazonses.com -all`

4. DMARC starter:
- `_dmarc` `TXT` -> `v=DMARC1; p=none;`

Notes:
- Keep existing Resend send-domain records (`send.<domain>` MX/SPF/DKIM) if used.
- Root-domain MX for mailbox hosting and `send.<domain>` MX for sending workflows can coexist.

## Deploy Stalwart in Dokploy

- Use Stalwart image (`stalwartlabs/stalwart:latest-alpine`)
- Expose/route ports: `25`, `465`, `587`, `993`, `8080`, `443`
- Persist volumes for `/etc/stalwart`, `/var/lib/stalwart`, `/opt/stalwart-mail`

If bootstrap keeps resetting after restart, fix volume ownership:

```bash
sudo chown -R 2000:2000 /var/lib/docker/volumes/<stalwart-volume>/_data
```

## Stalwart Bootstrap

- Complete bootstrap once (default domain, hostname, internal directory)
- Confirm admin account is persistent after restart

Target settings:
- default hostname: `mail.<domain>`
- default domain: `<domain>`

## TLS Certificate (must not be self-signed)

Use Let’s Encrypt for `mail.<domain>`:

```bash
sudo certbot certonly --standalone -d mail.<domain> --non-interactive --agree-tos -m support@<domain>
```

Then import the cert into Stalwart certificate store and set as `defaultCertificateId`.

If the UI create form rejects the PEM with `No certificates found in PEM`, create the certificate through the JMAP `x:Certificate/set` endpoint instead, using the leaf certificate PEM and private key, then set `x:SystemSettings.defaultCertificateId` to the created certificate object ID and restart Stalwart so 465/993 pick up the new cert.

Verify:

```bash
openssl s_client -connect mail.<domain>:465 -servername mail.<domain> < /dev/null 2>/dev/null | openssl x509 -noout -subject -issuer -dates
openssl s_client -connect mail.<domain>:993 -servername mail.<domain> < /dev/null 2>/dev/null | openssl x509 -noout -subject -issuer -dates
```

Expected:
- CN includes `mail.<domain>`
- issuer is Let’s Encrypt (not self-signed)

## Create Mailboxes

Create at least:
- admin mailbox (e.g. `admin@<domain>`)
- support mailbox (e.g. `support@<domain>`)

Verify auth from server side:

```bash
# IMAP auth test
openssl s_client -quiet -crlf -connect 127.0.0.1:<mapped-993> <<<'a1 LOGIN support@<domain> <password>'

# SMTP auth test
# AUTH PLAIN with base64(\0user\0pass)
```

## Critical Default: Outbound Relay via Resend

When port 25 egress is blocked, do not use direct MX delivery route for outbound.

Configure in Stalwart:

1. Create route `relay` (`@type: Relay`):
- address: `smtp.resend.com`
- port: `587`
- implicitTls: `false`
- authUsername: `resend`
- authSecret: `<RESEND_API_KEY>`

2. Update `x:MtaOutboundStrategy` route expression:
- keep local delivery rule for local domains
- set default route `else` to `'relay'`

Resulting behavior:
- local recipient domains -> local route
- external recipients -> Resend relay route

## Web Admin Routing (Dokploy)

Map host to Stalwart web service (`container port 8080`):
- Host: `mail.<domain>`
- Path: `/`
- Internal Path: `/`
- HTTPS: enabled
- Redeploy after domain change

Admin UI URL:
- `https://mail.<domain>/admin/`

## Verification Checklist

1. DNS:
```bash
dig +short MX <domain>
dig +short A mail.<domain>
```

2. Ports:
```bash
nc -zv mail.<domain> 993
nc -zv mail.<domain> 465
nc -zv mail.<domain> 25
```

3. IMAP/SMTP login works for `support@<domain>`.

4. Queue health:
- `x:QueuedMessage/get` should not accumulate permanent `TemporaryFailure` entries.
- If messages stay `Scheduled` too long, inspect route/worker status and restart service.

5. End-to-end test:
- send external test mail from Thunderbird and verify delivery
- send inbound test to `support@<domain>` and verify receipt

## Thunderbird Client Settings

Use manual settings (autodiscovery may fail):

- IMAP: `mail.<domain>` / `993` / `SSL/TLS` / `Normal password`
- SMTP: `mail.<domain>` / `465` / `SSL/TLS` / `Normal password`
- username: full email address

If direct outbound delivery remains blocked and Stalwart queue is not healthy, temporary fallback:
- SMTP server in client: `smtp.resend.com`
- port: `465` (SSL/TLS) or `587` (STARTTLS)
- username: `resend`
- password: Resend API key

## Common Failure Modes

1. Bootstrap not persisting
- Cause: wrong volume permissions
- Fix: `chown` volumes to stalwart user (`2000:2000`)

2. TLS cert mismatch/self-signed
- Cause: default cert still active
- Fix: import LE cert and set default certificate in `x:SystemSettings`
- If the UI errors with `No certificates found in PEM`, use JMAP `x:Certificate/set` with the leaf PEM + private key, then restart Stalwart

3. External send fails, queue error `Network unreachable (os error 101)`
- Cause: blocked outbound 25
- Fix: force outbound route to Resend relay

4. Inbound mail not arriving
- Cause: MX or port 25 path wrong/firewall
- Fix: validate DNS MX + open/route tcp 25 end-to-end

## Exit Criteria

Complete when:
- preflight checks all pass (MX, Dokploy, Stalwart)
- `https://mail.<domain>/admin/` opens
- valid LE cert is presented on 465/993/443
- `support@<domain>` can authenticate over IMAP/SMTP
- inbound mail to `support@<domain>` is received
- outbound to external recipients is delivered via relay without queue stall
