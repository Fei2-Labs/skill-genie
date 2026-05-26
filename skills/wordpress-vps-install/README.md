# WordPress VPS Install

Fresh-VPS bootstrap workflow for installing WordPress, wiring the live container stack, and verifying the public site.

## Use when

- provisioning a new VPS for WordPress
- setting up the database, volume, and proxy route
- running WP-CLI install on the live volume
- validating the site returns `200` after install

## Main file

- [`SKILL.md`](./SKILL.md)

## What it does

- inspects the running stack and env values
- checks the WordPress volume and DB wiring
- runs installation against the live files
- verifies the public URL after deployment
---

**Source**: [github.com/Fei2-Labs/skill-genie](https://github.com/Fei2-Labs/skill-genie)
**Author**: [@clarezoe](https://x.com/clarezoe)

