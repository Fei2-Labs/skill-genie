#!/usr/bin/env bash
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel 2>/dev/null || true)"
if [[ -z "${repo_root}" ]]; then
  echo "ERROR: not inside a git repository" >&2
  exit 1
fi

common_dir="$(git rev-parse --git-common-dir)"
if [[ "${common_dir}" != /* ]]; then
  common_dir="${repo_root}/${common_dir}"
fi
common_dir="$(cd "${common_dir}" && pwd)"

shared_root="${common_dir}/trellis-shared"
mkdir -p \
  "${shared_root}/handoffs" \
  "${shared_root}/knowledge" \
  "${shared_root}/agents" \
  "${shared_root}/events"

trellis_dir="${repo_root}/.trellis"
link_path="${trellis_dir}/shared"
mkdir -p "${trellis_dir}"

# Preserve a repository's existing branch-local handoffs the first time its
# runtime store is initialized. Later worktrees use the populated shared copy.
legacy_handoff_dir="${trellis_dir}/handoffs"
if [[ -d "${legacy_handoff_dir}" ]] \
  && [[ -z "$(find "${shared_root}/handoffs" -mindepth 1 -maxdepth 1 -print -quit)" ]]; then
  cp -pR "${legacy_handoff_dir}/." "${shared_root}/handoffs/"
  if [[ -f "${shared_root}/handoffs/CURRENT" ]]; then
    sed -i.bak 's#\.trellis/handoffs/#.trellis/shared/handoffs/#g' \
      "${shared_root}/handoffs/CURRENT"
    rm -f "${shared_root}/handoffs/CURRENT.bak"
  fi
  if [[ -f "${shared_root}/handoffs/INDEX.md" ]]; then
    sed -i.bak 's#\.trellis/handoffs/#.trellis/shared/handoffs/#g' \
      "${shared_root}/handoffs/INDEX.md"
    rm -f "${shared_root}/handoffs/INDEX.md.bak"
  fi
  echo "OK: migrated legacy handoffs into shared memory"
fi

if [[ -L "${link_path}" ]]; then
  current_target="$(readlink "${link_path}")"
  if [[ "${current_target}" == "${shared_root}" ]]; then
    echo "OK: shared memory link already configured"
    echo "repo_root=${repo_root}"
    echo "shared_root=${shared_root}"
    exit 0
  fi
  echo "ERROR: ${link_path} already links to '${current_target}', expected '${shared_root}'" >&2
  exit 1
fi

if [[ -e "${link_path}" ]]; then
  echo "ERROR: ${link_path} exists and is not a symlink. Move it first." >&2
  exit 1
fi

ln -s "${shared_root}" "${link_path}"

echo "OK: configured worktree shared memory"
echo "repo_root=${repo_root}"
echo "git_common_dir=${common_dir}"
echo "shared_root=${shared_root}"
echo "link_path=${link_path}"
