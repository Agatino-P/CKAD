#!/usr/bin/env bash
# Deletes the CKAD practice cluster: node containers, their volumes and the kubeconfig entries.
set -euo pipefail
kind delete cluster --name ckad
