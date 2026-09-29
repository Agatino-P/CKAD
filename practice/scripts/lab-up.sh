#!/usr/bin/env bash
# Creates the CKAD practice cluster and its add-ons, waiting until each is usable.
# Safe to re-run: an existing cluster is reused.
set -euo pipefail
cd "$(dirname "$0")/../lab"

if kind get clusters 2>/dev/null | grep -qx ckad; then
  echo "cluster ckad exists"
else
  kind create cluster --config kind-cluster.yaml
fi
kubectl config use-context kind-ckad
kubectl wait --for=condition=Ready nodes --all --timeout=180s

kubectl apply -k addons/metrics-server
kubectl -n kube-system rollout status deployment/metrics-server --timeout=180s
kubectl wait --for=condition=Available apiservice/v1beta1.metrics.k8s.io --timeout=180s

kubectl apply -k addons/ingress-nginx
kubectl -n ingress-nginx rollout status deployment/ingress-nginx-controller --timeout=240s
# The admission webhook refuses connections for a moment after the controller is Ready.
for _ in $(seq 1 60); do
  if kubectl create ingress webhook-probe --class=nginx --rule='/*=webhook-probe:80' \
       --dry-run=server -o name >/dev/null 2>&1; then
    break
  fi
  sleep 1
done

kubectl get nodes -o wide
echo "Ready. Context: kind-ckad. Ingress from the host: http://localhost:8080"
