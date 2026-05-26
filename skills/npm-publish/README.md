# npm-publish

Publish an NPM package to the registry with full auth handling.

## What it does

`npm-publish` handles the entire npm publish flow including browser-based login, 2FA/security key (WebAuthn) support, and pre-publish validation.

## When to use

- User says "publish to npm", "npm publish", "deploy to npm"
- Ready to release a new version of an npm package

## Prerequisites

- Node.js 22+ and npm installed
- `package.json` with correct name, version, and `prepublishOnly` script
- Password manager CLI (optional, for retrieving credentials)

## Key features

- Handles browser-based npm login flow
- Supports 2FA and security key authentication
- Pre-publish validation checks
- Version verification before publish

---

**Source**: [github.com/Fei2-Labs/skill-genie](https://github.com/Fei2-Labs/skill-genie)
**Author**: [@clarezoe](https://x.com/clarezoe)
