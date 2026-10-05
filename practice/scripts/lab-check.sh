#!/usr/bin/env bash
# Proves the lab can host every kind of exercise in the index, then removes what it created.
# Exits non-zero at the first failed check.
set -euo pipefail
kc() { kubectl --context kind-ckad "$@"; }
fail() { echo "FAIL: $*" >&2; exit 1; }

echo "-- StorageClass named standard"
kc get storageclass standard >/dev/null || fail "no StorageClass standard"

echo "-- metrics-server answers kubectl top (up to 60 s after install)"
for _ in $(seq 1 12); do kc top nodes >/dev/null 2>&1 && break; sleep 5; done
kc top nodes >/dev/null || fail "kubectl top nodes has no data"

echo "-- kindnet enforces NetworkPolicy"
kc delete namespace netpol-check --ignore-not-found --wait=true >/dev/null
kc create namespace netpol-check >/dev/null
kc -n netpol-check run web --image=nginx:alpine --port=80 --labels=app=web >/dev/null
kc -n netpol-check expose pod web --port=80 >/dev/null
kc -n netpol-check wait --for=condition=Ready pod/web --timeout=120s >/dev/null
before=$(kc -n netpol-check run c1 --image=busybox:1.36 --restart=Never --rm -i -q -- \
  sh -c 'wget -qO- --timeout=3 http://web >/dev/null && echo open || echo closed' 2>/dev/null | tail -1)
[[ "$before" == open ]] || fail "web pod unreachable before any policy ($before)"
cat <<'YAML' | kc -n netpol-check apply -f - >/dev/null
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all-ingress
spec:
  podSelector: {}
  policyTypes: ["Ingress"]
YAML
sleep 3
after=$(kc -n netpol-check run c2 --image=busybox:1.36 --restart=Never --rm -i -q -- \
  sh -c 'wget -qO- --timeout=3 http://web >/dev/null && echo open || echo closed' 2>/dev/null | tail -1)
kc delete namespace netpol-check --wait=false >/dev/null
[[ "$after" == closed ]] || fail "deny-all NetworkPolicy is not enforced: the CNI ignores policies"

echo "-- Ingress reachable from the host on port 8080"
kc delete namespace ingress-check --ignore-not-found --wait=true >/dev/null
kc create namespace ingress-check >/dev/null
kc -n ingress-check create deployment web --image=nginx:alpine --port=80 >/dev/null
kc -n ingress-check expose deployment web --port=80 >/dev/null
kc -n ingress-check create ingress web --class=nginx --rule='ingress-check.local/*=web:80' >/dev/null
kc -n ingress-check rollout status deployment/web --timeout=120s >/dev/null
title=""
for _ in $(seq 1 20); do
  title=$(curl -s -m 3 -H 'Host: ingress-check.local' http://localhost:8080/ | grep -o '<title>.*</title>' || true)
  [[ "$title" == *nginx* ]] && break
  sleep 2
done
kc delete namespace ingress-check --wait=false >/dev/null
[[ "$title" == *nginx* ]] || fail "Ingress did not answer on localhost:8080 (${title:-no response})"

echo "-- NodePort 30080 reachable from the host on port 9080, reserved for a gateway"
kc delete namespace nodeport-check --ignore-not-found --wait=true >/dev/null
kc create namespace nodeport-check >/dev/null
kc -n nodeport-check create deployment web --image=nginx:alpine --port=80 >/dev/null
kc -n nodeport-check create service nodeport web --tcp=80:80 --node-port=30080 >/dev/null
kc -n nodeport-check rollout status deployment/web --timeout=120s >/dev/null
title=""
for _ in $(seq 1 20); do
  title=$(curl -s -m 3 http://localhost:9080/ | grep -o '<title>.*</title>' || true)
  [[ "$title" == *nginx* ]] && break
  sleep 2
done
kc delete namespace nodeport-check --wait=false >/dev/null
[[ "$title" == *nginx* ]] || fail "NodePort 30080 did not answer on localhost:9080 (${title:-no response})"

echo "-- helm talks to the cluster"
helm --kube-context kind-ckad list -A >/dev/null || fail "helm cannot list releases"

echo "all checks passed"
