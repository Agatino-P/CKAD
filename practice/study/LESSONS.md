# Lessons

Condensed lessons, one section per topic in `practice/study/STUDY_PLAN.md`.

## Running commands with args in Docker and K8s

Moved on 2026-10-06 to the section "Running commands with args in Docker and K8s" of `Study notes/CKAD appunti.md`, under "Application Design and Build".

## Node affinity

### a. Node labels and `nodeSelector`

Node affinity places a Pod by the labels of the nodes, so it starts with labelling a node.\
`nodeSelector` is the simplest match: the scheduler places the Pod only on a node that carries every listed label.\
A Pod that no node matches stays `Pending`, with a `FailedScheduling` event.\
Every node already carries built-in labels, such as `kubernetes.io/hostname`.

| Command | Outcome | Notes |
| --- | --- | --- |
| `kubectl label node ckad-worker2 disktype=ssd` | `node/ckad-worker2 labeled` | |
| `kubectl get nodes -L disktype` | A `DISKTYPE` column, `ssd` on `ckad-worker2` only | |
| `kubectl get nodes -l disktype=ssd` | Only `ckad-worker2` | |
| Pod `web` with `spec.nodeSelector: {disktype: ssd}` | `Running` on `ckad-worker2` | |
| Pod `nomatch` with `spec.nodeSelector: {disktype: hdd}` | `Pending`: `0/3 nodes are available: 1 node(s) had untolerated taint(s), 2 node(s) didn't match Pod's node affinity/selector.` | The taint is on the control plane node. |
| `kubectl label node ckad-worker2 disktype-` | `node/ckad-worker2 unlabeled` | A trailing `-` removes the label. |
