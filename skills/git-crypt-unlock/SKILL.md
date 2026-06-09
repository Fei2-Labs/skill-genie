---
name: "git-crypt-unlock"
description: "Auto-unlock git-crypt encrypted files in the current repo. Fetches the GPG private key and passphrase from Bitwarden via rbw, imports the key, presets the passphrase into gpg-agent, and runs git-crypt unlock — fully non-interactive after the rbw master-password prompt. Use when encrypted files (GITCRYPT binary blobs) appear in a repo, after a fresh clone of a git-crypt repo, or on a new machine."
license: "MIT"
metadata: {"version":"1.0.0","triggers":["unlock git-crypt","git-crypt unlock","解锁仓库","解锁加密文档","解密 AGENTS.md","decrypt internal docs","unlock encrypted docs"],"tags":["git-crypt","gpg","bitwarden","rbw","encryption","developer-tools"]}
---

# git-crypt Unlock

Unlock git-crypt encrypted files in the current repository, bootstrapping the GPG key from Bitwarden (rbw) if this machine doesn't have it yet.

## Personal configuration (this user)

| Setting | Value |
|---|---|
| GPG key id | `25FFD2B10C7545B6` (uid `clarezoe`, sign ed25519 + encrypt cv25519 subkey) |
| Bitwarden item (rbw) | `gpg-git-crypt` |
| — armored private key | item **notes** (`rbw get gpg-git-crypt --field notes`) |
| — key passphrase | item field `passphrase` (`rbw get gpg-git-crypt --field passphrase`) |
| gpg-preset-passphrase | `/opt/homebrew/opt/gnupg/libexec/gpg-preset-passphrase` |

## Flow

Run steps in order; skip any step whose check already passes. Never echo the passphrase or private key into output/logs; pipe directly between commands.

### 1. Preconditions

```bash
which git-crypt gpg rbw || brew install git-crypt gnupg rbw
git rev-parse --show-toplevel                  # must be inside a git repo
ls "$(git rev-parse --show-toplevel)/.git-crypt" 2>/dev/null || echo "repo not git-crypt managed — nothing to unlock"
```

### 2. Already unlocked? (idempotency)

```bash
cd "$(git rev-parse --show-toplevel)"
git-crypt status -e 2>/dev/null | head
# Pick one encrypted file; if its working-tree copy does NOT start with \0GITCRYPT, it is already decrypted → DONE.
f=$(git-crypt status -e 2>/dev/null | awk '{print $2}' | head -1)
[ -n "$f" ] && head -c 9 "$f" | grep -q GITCRYPT && echo LOCKED || echo "already unlocked — done"
```

### 3. GPG key present?

```bash
gpg --list-secret-keys 25FFD2B10C7545B6 >/dev/null 2>&1 && echo "key present" || echo "key missing → step 4"
```

### 4. Import key from Bitwarden (only if missing)

`rbw unlock` pops a pinentry for the **Bitwarden master password — the user types it** (the one interactive moment; everything after is automatic).

```bash
rbw unlock
rbw get gpg-git-crypt --field notes | gpg --import   # pipe; never write key to a file
```

If `rbw get` errors: list candidates with `rbw list | grep -i gpg` and tell the user the expected item name (`gpg-git-crypt`, key in notes, passphrase in field `passphrase`); do not guess at other vault items.

### 5. Preset passphrase into gpg-agent (makes unlock non-interactive)

```bash
grep -q allow-preset-passphrase ~/.gnupg/gpg-agent.conf 2>/dev/null || { echo allow-preset-passphrase >> ~/.gnupg/gpg-agent.conf; gpgconf --kill gpg-agent; }
# Preset for every keygrip of the key (sign + encrypt subkey):
for grip in $(gpg --list-secret-keys --with-keygrip 25FFD2B10C7545B6 | awk '/Keygrip/{print $3}'); do
  rbw get gpg-git-crypt --field passphrase | /opt/homebrew/opt/gnupg/libexec/gpg-preset-passphrase --preset "$grip"
done
```

### 6. Unlock + verify

```bash
cd "$(git rev-parse --show-toplevel)" && git-crypt unlock
# Verify: the file from step 2 must now be readable plaintext
head -c 9 "$f" | grep -q GITCRYPT && echo "STILL LOCKED — investigate" || echo "unlocked ✓"
```

### 7. Report

State: repo path, which steps actually ran (key imported? passphrase preset?), and the verify result. Remind: decrypted files are plaintext in the working tree — do not copy them outside the repo.

## Failure notes

- `rbw unlock` "pinentry cancelled" → user dismissed or no GUI; ask user to run `rbw unlock` in their own terminal, then re-run remaining steps.
- `gpg-preset-passphrase` "Not implemented" → `allow-preset-passphrase` line missing or agent not restarted (`gpgconf --kill gpg-agent`).
- Passphrase preset expires with gpg-agent cache TTL (default ~10 min / max-cache-ttl). git-crypt unlock needs it only once per repo — re-running the skill re-presets.
- New machine with no rbw config → `rbw config set email <bitwarden-email>` first, then `rbw login`.
