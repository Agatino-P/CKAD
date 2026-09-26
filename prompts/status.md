# Status — CKAD appunti rebuild

Current state only. No history, no dates, no log. Delete a resolved point instead of striking it through.

Target: `Study notes/CKAD appunti.md`
Sources: `Study notes/backup/CKAD appunti.md` (base), `Study notes/backup/CKAD 2 appunti.md` (file 2), `Study notes/backup/CKAD 3 appunti.md` (file 3)

## Current step

Section 0 is finished and committed (push goes with section 1). The next step is section 1, state `todo`: dispatch the Writer in write mode.

## Agent running

none

## Sections

| # | Section | Source mapping | State | Round |
|---|---|---|---|---|
| 0 | Preamble | Base: CSS `<style>` block and audit header. Re-verify the current CKAD Kubernetes version online and update the header. | done | 1 |
| 1 | Application Design and Build | Base: "Application Design and Build" (images, Docker/Podman, Jobs, CronJobs, multi-container Pods, volumes) | todo | 0 |
| 2 | Application Deployment | Base: "Application Deployment". File 2: create/expose/dry-run Deployment, edit, scale, Deployment `spec`/`strategy`, `--save-config`, rollout history and rollback, Helm. File 3: `k run` Pod YAML, NodePort expose. | todo | 0 |
| 3 | Application Observability and Maintenance | Base: "Application Observability and Maintenance". File 3: admission controllers, K8s version, API groups/versions, `kubectl proxy`, probes, monitoring/Metrics Server, logs, events, `kubectl debug`. | todo | 0 |
| 4 | Application Environment, Configuration and Security | Base: "Application Environment, Configuration and Security" | todo | 0 |
| 5 | Services and Networking | Base: "Services and Networking" | todo | 0 |
| 6 | General Knowledge | Base: "General Knowledge". File 2: general hints (spaces not tabs), tmux, alias, kubeconfig/context commands incl. `config unset`, namespace create/check/set/`-n`, `KUBE_EDITOR`, `k create -f ./`, jq. File 3: field selectors. | todo | 0 |
| 7 | Final audit | All three sources against the whole new file (reviewer in audit mode). | todo | 0 |

States: `todo` → `review` → `fix` → `review` … → `done` or `done-with-open-points`.

## Open points

- **0.1** — `user-decision` — Audit header: the header states CKAD uses Kubernetes v1.35, as the Linux Foundation FAQ and CKAD page say, while kubernetes.io lists v1.36 and v1.37 as released; the LF pages may lag their own 4–8-week alignment policy. Recheck the LF FAQ before the exam. https://docs.linuxfoundation.org/tc-docs/certification/faq-cka-ckad-cks , https://kubernetes.io/releases/
- **0.2** — `user-decision` — `<style>` block: the h5/h6 rules now use `counter-increment: h5` / `h6` and a `"."` separator, a repair none of the three sources had verbatim (file 3 fixed only the counter). Keep or revert.
