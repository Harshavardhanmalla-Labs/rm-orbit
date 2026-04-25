#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEMPLATE_PATH="${ROOT_DIR}/scripts/pre-push-orbit.sh"
MARKER="# RM_ORBIT_PRE_PUSH_HOOK"

REPOS=(
  "Gate"
  "Atlas"
  "Control Center"
  "Mail"
  "Connect"
  "Planet"
  "Meet"
  "Learn"
  "Capital Hub"
  "Secure"
  "Snitch"
)

MODE="install"
DRY_RUN="false"

usage() {
  cat <<EOF
Usage: ./scripts/install-prepush-hooks.sh [--dry-run] [--remove]

Options:
  --dry-run   Show actions without writing hooks
  --remove    Remove Orbit-managed pre-push hooks
  --help      Show this help
EOF
}

for arg in "$@"; do
  case "$arg" in
    --dry-run)
      DRY_RUN="true"
      ;;
    --remove)
      MODE="remove"
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: ${arg}" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ "${MODE}" == "install" && ! -f "${TEMPLATE_PATH}" ]]; then
  echo "Template not found: ${TEMPLATE_PATH}" >&2
  exit 1
fi

if [[ "${MODE}" == "install" ]]; then
  chmod +x "${TEMPLATE_PATH}"
fi

timestamp="$(date +%Y%m%d%H%M%S)"

install_hook() {
  local repo_path="$1"
  local hook_path="${repo_path}/.git/hooks/pre-push"
  local backup_path="${repo_path}/.git/hooks/pre-push.backup.${timestamp}"

  if [[ ! -d "${repo_path}/.git" ]]; then
    echo "skip: ${repo_path} (no .git directory)"
    return
  fi

  if [[ -f "${hook_path}" ]] && ! rg -q "${MARKER}" "${hook_path}"; then
    if [[ "${DRY_RUN}" == "true" ]]; then
      echo "would-backup: ${hook_path} -> ${backup_path}"
    else
      cp "${hook_path}" "${backup_path}"
      echo "backup: ${hook_path} -> ${backup_path}"
    fi
  fi

  if [[ "${DRY_RUN}" == "true" ]]; then
    echo "would-install: ${hook_path}"
    return
  fi

  cp "${TEMPLATE_PATH}" "${hook_path}"
  chmod +x "${hook_path}"
  echo "installed: ${hook_path}"
}

remove_hook() {
  local repo_path="$1"
  local hook_path="${repo_path}/.git/hooks/pre-push"

  if [[ ! -d "${repo_path}/.git" ]]; then
    echo "skip: ${repo_path} (no .git directory)"
    return
  fi

  if [[ ! -f "${hook_path}" ]]; then
    echo "skip: ${hook_path} (not present)"
    return
  fi

  if ! rg -q "${MARKER}" "${hook_path}"; then
    echo "skip: ${hook_path} (not Orbit-managed)"
    return
  fi

  if [[ "${DRY_RUN}" == "true" ]]; then
    echo "would-remove: ${hook_path}"
    return
  fi

  rm -f "${hook_path}"
  echo "removed: ${hook_path}"
}

for repo in "${REPOS[@]}"; do
  repo_path="${ROOT_DIR}/${repo}"
  if [[ "${MODE}" == "install" ]]; then
    install_hook "${repo_path}"
  else
    remove_hook "${repo_path}"
  fi
done

echo "done: mode=${MODE} dry_run=${DRY_RUN}"
