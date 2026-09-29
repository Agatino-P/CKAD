#!/usr/bin/env bash
# Runs a ckad-dojo script against the lab, with the docker shim on PATH and the registry skipped.
#   practice/scripts/dojo.sh setup   -e ckad-simulation1
#   practice/scripts/dojo.sh score   -e ckad-simulation1 -q 2
#   practice/scripts/dojo.sh cleanup -e ckad-simulation1
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
dojo="$here/../sources/tipunchlabs-ckad-dojo"
export PATH="$here/shim:$PATH"
# The scripts resolve the answer directory ./exam/course against the current directory.
cd "$dojo"
action="${1:-}"; shift || true
case "$action" in
  setup)   bash scripts/ckad-setup.sh --skip-registry "$@" ;;
  score)   bash scripts/ckad-score.sh "$@" ;;
  cleanup) bash scripts/ckad-cleanup.sh -y "$@" ;;
  *) echo "usage: $0 setup|score|cleanup -e <simulation> [more options]" >&2; exit 2 ;;
esac
