# Status — CKAD appunti rebuild

Current state only. No history, no dates, no log. Delete a resolved point instead of striking it through.

Target: `Study notes/CKAD appunti.md`
Sources: `Study notes/backup/CKAD appunti.md` (base), `Study notes/backup/CKAD 2 appunti.md` (file 2), `Study notes/backup/CKAD 3 appunti.md` (file 3)

## Current step

Section 7 (Final audit), `review` round 1: the Reviewer is running in audit mode. On completion, apply the decision rule in `prompts/loop.md`.

## Agent running

Reviewer — section 7 (Final audit), audit mode, round 1.

## Sections

| # | Section | Source mapping | State | Round |
|---|---|---|---|---|
| 0 | Preamble | Base: CSS `<style>` block and audit header. Re-verify the current CKAD Kubernetes version online and update the header. | done | 1 |
| 1 | Application Design and Build | Base: "Application Design and Build" (images, Docker/Podman, Jobs, CronJobs, multi-container Pods, volumes) | done | 1 |
| 2 | Application Deployment | Base: "Application Deployment". File 2: create/expose/dry-run Deployment, edit, scale, Deployment `spec`/`strategy`, `--save-config`, rollout history and rollback, Helm. File 3: `k run` Pod YAML, NodePort expose. File 2: `k run -it --restart=Never -image=alpine temp-pod` (source typo `-image` → `--image`). | done | 1 |
| 3 | Application Observability and Maintenance | Base: "Application Observability and Maintenance". File 3: admission controllers, K8s version, API groups/versions, `kubectl proxy`, probes, monitoring/Metrics Server, logs, events, `kubectl debug`. | done | 2 |
| 4 | Application Environment, Configuration and Security | Base: "Application Environment, Configuration and Security" | done | 2 |
| 5 | Services and Networking | Base: "Services and Networking" | done | 2 |
| 6 | General Knowledge | Base: "General Knowledge". File 2: general hints (spaces not tabs), tmux, alias, kubeconfig/context commands incl. `config unset`, namespace create/check/set/`-n`, `KUBE_EDITOR`, `k create -f ./`, jq. File 3: field selectors. Note: section 2 already holds "Modify a deployment from the command line" and the temp-pod item; merge the base General Knowledge copies there as duplicates (the extra `k run` variants carry the typo `--restar=never`). | done | 1 |
| 7 | Final audit | All three sources against the whole new file (reviewer in audit mode). | review | 1 |

States: `todo` → `review` → `fix` → `review` … → `done` or `done-with-open-points`.

## Open points

- **1.9** — `user-decision` — "Volumes": the headings "Storage classes (SC)", "Persistent Volumes (PV)", "Persistent Volume Claims (PVC)" and "Storage Classes" need reordering; they stay separate (separate Kubernetes APIs). A `<!-- REORDER -->` note marks the spot. To be decided with User.
- **2.2** — `user-decision` — "Helm commands" (minor): "`helm search repo` shows only the newest version of each chart" omits that development versions are excluded unless `--devel` is passed. https://helm.sh/docs/helm/helm_search_repo/
- **2.3** — `user-decision` — "Deployment updates and rollout history" / "Rollout history" (minor): sibling headings with nearly the same name; "Get information about a Deployment" now holds only `rollout status`.
- **3.1** — `user-decision` — "Using `kube-apiserver`": `kube-apiserver -h | grep enable-admission-plugins` also prints the deprecated `--admission-control` line, which lists every plugin; only the `--enable-admission-plugins` line lists the defaults. https://v1-35.docs.kubernetes.io/docs/reference/command-line-tools-reference/kube-apiserver/
- **3.2** — `user-decision` — "View admission controller plugins for kube-apiserver": "This shows only the plugins enabled with the flag, in addition to the default enabled ones" reads as if the defaults were shown; they are not.
- **3.3** — `user-decision` — "Restart Policy": the second bullet repeats the failure actions given under the three probe headings; keep only "the Pod is not recreated".
- **3.4** — `user-decision` — "K8s version" / "Order of versions": GA is defined twice; merge into one.
- **3.5** — `user-decision` — "View admission controller plugins for kube-apiserver" / "Using `kube-apiserver`": the step "run `k get pods` in kube-system to find the apiserver Pod name" appears in both; merge.
- **5.1** — `user-decision` — "Use Ingress Rules to Expose Applications": "exposed through a single load balancer on port 80 or 443" reads as one port or the other; the controller normally serves both, so "80 and 443".
- **6.1** — `user-decision` — "Using jq (example)": the reason for quoting the key is partly wrong — only `/` and `-` break compilation (read as division and subtraction); an unquoted `.` instead splits the key into a nested path and returns the wrong value (tested with jq 1.7.1).
