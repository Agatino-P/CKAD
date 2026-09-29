#!/usr/bin/env bash
# Sets up the CKAD practice environment on a macOS machine with Homebrew, from a fresh clone.
# Idempotent: every step checks before acting, so re-running after a partial failure is safe.
#   git clone --recurse-submodules <repo> && <repo>/practice/scripts/setup.sh
set -euo pipefail
cd "$(dirname "$0")/../.."

echo "==> 1/4 tools"
for tool in kind kubectl helm; do
  if command -v "$tool" >/dev/null; then echo "$tool present"; else brew install "$tool"; fi
done
if command -v docker >/dev/null; then
  docker info >/dev/null 2>&1 || { echo "docker is installed but its daemon is not running" >&2; exit 1; }
elif command -v podman >/dev/null; then
  # kind falls back to podman by itself when docker is absent; only the machine must be up.
  podman machine list --format '{{.Running}}' | grep -q true \
    || { echo "podman machine is not running: podman machine start" >&2; exit 1; }
else
  echo "no container engine: install Docker Desktop, or podman with a machine (brew install podman; podman machine init; podman machine start)" >&2
  exit 1
fi

echo "==> 2/4 exercise sources (git submodules)"
git submodule update --init --recursive

echo "==> 3/4 lab cluster and add-ons"
practice/scripts/lab-up.sh

echo "==> 4/4 lab checks"
practice/scripts/lab-check.sh
