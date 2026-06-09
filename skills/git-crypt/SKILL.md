---
name: "git-crypt"
description: "Manage git-crypt encrypted repos end-to-end: UNLOCK (auto-fetch GPG key + passphrase from Bitwarden via rbw, non-interactive), LOCK (re-scramble the local working tree before leaving a shared machine), SETUP (encrypt internal docs in a new public repo: init, authorize key, .gitattributes patterns), and STATUS. Use when encrypted GITCRYPT blobs appear after a clone, when leaving a machine, when onboarding a new public repo, or to check what's encrypted."
license: "MIT"
metadata: {"version":"1.2.0","triggers":["unlock git-crypt","git-crypt unlock","解锁仓库","解锁加密文档","解密 AGENTS.md","decrypt internal docs","lock repo","锁定仓库","锁上文档","git-crypt lock","encrypt this repo","给仓库加密","上 git-crypt","encrypt internal docs","git-crypt status","加密状态"],"tags":["git-crypt","gpg","bitwarden","rbw","encryption","developer-tools"]}
---

# git-crypt Manager

Four operations on git-crypt repos. Pick by user intent:

| User says | Operation |
|---|---|
| "解锁仓库 / unlock / 文件是乱码" | **UNLOCK** |
| "锁定仓库 / lock / 我要离开这台机器" | **LOCK** |
| "给这个仓库加密 / encrypt this repo / 上 git-crypt" | **SETUP** |
| "加密状态 / 哪些文件加密了" | **STATUS** |

Mental model (explain to user if confused): day-to-day **encryption is automatic** — files matched by `.gitattributes` are encrypted by the filter on `git add`/commit; pushed content is always ciphertext. `lock` only re-scrambles the LOCAL working tree; `unlock` reverses that.

## Personal configuration (this user)

| Setting | Value |
|---|---|
| GPG key id | `25FFD2B10C7545B6` (uid `clarezoe`, sign ed25519 + encrypt cv25519 subkey) |
| Bitwarden item (rbw) | `GPG key - git-crypt (clarezoe)` — item **password** = key passphrase; custom field **`key`** = armored private key (stored single-line: Bitwarden web-UI fields strip newlines — MUST reconstruct, see U4); field **`rev`** = revocation cert |
| gpg-preset-passphrase | `/opt/homebrew/opt/gnupg/libexec/gpg-preset-passphrase` |

Never echo the passphrase or private key into output/logs; pipe directly between commands.

---

## STATUS

```bash
cd "$(git rev-parse --show-toplevel)"
ls .git-crypt 2>/dev/null || { echo "repo not git-crypt managed"; exit 0; }
git-crypt status -e        # encrypted files
# Locked or unlocked? Inspect one encrypted file's working copy:
f=$(git-crypt status -e 2>/dev/null | awk '{print $2}' | head -1)
[ -n "$f" ] && { head -c 9 "$f" | grep -q GITCRYPT && echo "working tree: LOCKED" || echo "working tree: UNLOCKED (plaintext locally)"; }
```

---

## UNLOCK

Run steps in order; skip any step whose check already passes (idempotent).

### U1. Preconditions
```bash
which git-crypt gpg rbw || brew install git-crypt gnupg rbw
git rev-parse --show-toplevel    # must be a git repo with .git-crypt/
```

### U2. Already unlocked? → use STATUS; if "UNLOCKED" → done.

### U3. GPG key present?
```bash
gpg --list-secret-keys 25FFD2B10C7545B6 >/dev/null 2>&1 || echo "missing → U4"
```

### U4. Import key from Bitwarden (only if missing)
`rbw unlock` pops a pinentry for the **Bitwarden master password — the user types it** (the single interactive moment).
```bash
rbw unlock
N="GPG key - git-crypt (clarezoe)"
# Field 'key' is single-line (web UI strips newlines) — reconstruct armor, pipe to import:
rbw get "$N" --field key | python3 -c "
import sys,re
s=sys.stdin.read().strip()
m=re.match(r'-----BEGIN PGP PRIVATE KEY BLOCK-----\s*(.*?)\s*-----END PGP PRIVATE KEY BLOCK-----', s, re.S)
print('-----BEGIN PGP PRIVATE KEY BLOCK-----'); print()
for t in m.group(1).split(): print(t)
print('-----END PGP PRIVATE KEY BLOCK-----')
" | gpg --batch --import
gpg --list-secret-keys 25FFD2B10C7545B6   # verify imported
```
If the item is missing: `rbw list | grep -i gpg`; do not guess at other vault items. If `rbw sync` fails with `missing field access_token` (vaultwarden token incompat): `rbw purge` then `rbw login` (fresh token chain fixes it). rbw pinentry must be GUI: `rbw config set pinentry /opt/homebrew/bin/pinentry-mac`.

### U5. Preset passphrase into gpg-agent (non-interactive unlock)
```bash
grep -q allow-preset-passphrase ~/.gnupg/gpg-agent.conf 2>/dev/null || { echo allow-preset-passphrase >> ~/.gnupg/gpg-agent.conf; gpgconf --kill gpg-agent; }
for grip in $(gpg --list-secret-keys --with-keygrip 25FFD2B10C7545B6 | awk '/Keygrip/{print $3}'); do
  rbw get "GPG key - git-crypt (clarezoe)" | /opt/homebrew/opt/gnupg/libexec/gpg-preset-passphrase --preset "$grip"   # item password = passphrase
done
```

### U6. Unlock + verify
```bash
cd "$(git rev-parse --show-toplevel)" && git-crypt unlock
head -c 9 "$f" | grep -q GITCRYPT && echo "STILL LOCKED — investigate" || echo "unlocked ✓"
```

---

## LOCK

Re-scrambles the local working tree (remote is always ciphertext regardless).

```bash
cd "$(git rev-parse --show-toplevel)"
git status --short            # encrypted files must be committed first — lock refuses dirty encrypted files
git-crypt lock
# Verify:
f=$(git-crypt status -e 2>/dev/null | awk '{print $2}' | head -1)
head -c 9 "$f" | grep -q GITCRYPT && echo "locked ✓" || echo "NOT locked — investigate"
```
If `git-crypt lock` complains about staged/modified files: commit or stash the encrypted-file changes first, then retry. After lock, editing those files is meaningless until the next unlock — warn the user.

---

## SETUP (encrypt internal docs in a repo)

For PUBLIC repos holding internal docs. (PRIVATE repos don't need this — commit docs plainly.)
Confirm with `gh repo view --json visibility` first; if PRIVATE, tell the user it's unnecessary and stop unless they insist.

```bash
cd "$(git rev-parse --show-toplevel)"
git-crypt init
git-crypt add-gpg-user --trusted 25FFD2B10C7545B6     # makes its own commit
cat >> .gitattributes <<'EOF'

# git-crypt: internal docs encrypted in this PUBLIC repo (key: gpg clarezoe)
AGENTS.md filter=git-crypt diff=git-crypt
docs/internal/** filter=git-crypt diff=git-crypt
EOF
# Un-ignore the files being encrypted (they're usually gitignored today), e.g.:
#   remove the AGENTS.md line from .gitignore
git add .gitattributes .gitignore AGENTS.md
# VERIFY ciphertext in index BEFORE committing:
git show :AGENTS.md | head -c 9 | grep -q GITCRYPT && echo "encrypted ✓" || echo "ABORT: plaintext in index!"
git commit -m "chore: encrypt internal docs with git-crypt"
```

⚠️ CRITICAL ordering: the `.gitattributes` filter line must be in place BEFORE `git add` of the target file. If a target file was EVER committed plaintext before, history still leaks it — needs `git filter-repo` to scrub; flag this to the user instead of silently proceeding.

---

## Failure notes

- `rbw unlock` "pinentry cancelled" → user dismissed or no GUI; ask the user to run `rbw unlock` in their own terminal, then re-run remaining steps.
- `gpg-preset-passphrase` "Not implemented" → `allow-preset-passphrase` missing or agent not restarted (`gpgconf --kill gpg-agent`).
- Preset passphrase expires with gpg-agent cache TTL; re-running UNLOCK re-presets.
- New machine, no rbw config → `rbw config set email <bitwarden-email>` then `rbw login`.
- New machine checklist: brew install git-crypt gnupg rbw → rbw login → say "解锁仓库" in the target repo.
