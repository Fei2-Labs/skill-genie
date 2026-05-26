# stalwart-dokploy-resend-relay

Deploy Stalwart Mail Server on a VPS via Dokploy with Resend SMTP relay.

## What it does

`stalwart-dokploy-resend-relay` sets up a production-ready Stalwart mail server on a new VPS managed by Dokploy, routing outbound mail through Resend SMTP relay for environments where direct port 25 egress is blocked.

## When to use

- Setting up a self-hosted email server on a VPS
- Port 25 is blocked by provider/network and you need an SMTP relay
- Using Dokploy for container management

## Key features

- Full Stalwart Mail Server deployment
- Resend SMTP relay configuration (`smtp.resend.com:587`)
- Dokploy container orchestration
- DNS record guidance (MX, SPF, DKIM, DMARC)
- Works on VPS providers that block port 25

---

**Source**: [github.com/Fei2-Labs/skill-genie](https://github.com/Fei2-Labs/skill-genie)
**Author**: [@clarezoe](https://x.com/clarezoe)
