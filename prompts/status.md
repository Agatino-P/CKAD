# Status — CKAD appunti rebuild

Current state only. No history, no dates, no log. Delete a resolved point instead of striking it through.

Target: `Study notes/CKAD appunti.md`
Sources: `Study notes/backup/CKAD appunti.md` (base), `Study notes/backup/CKAD 2 appunti.md` (file 2), `Study notes/backup/CKAD 3 appunti.md` (file 3)

## Current step

Sections 0 and 1 are finished, committed and pushed. The next step is section 2, state `todo`: dispatch the Writer in write mode.

## Agent running

none

## Sections

| # | Section | Source mapping | State | Round |
|---|---|---|---|---|
| 0 | Preamble | Base: CSS `<style>` block and audit header. Re-verify the current CKAD Kubernetes version online and update the header. | done | 1 |
| 1 | Application Design and Build | Base: "Application Design and Build" (images, Docker/Podman, Jobs, CronJobs, multi-container Pods, volumes) | done | 1 |
| 2 | Application Deployment | Base: "Application Deployment". File 2: create/expose/dry-run Deployment, edit, scale, Deployment `spec`/`strategy`, `--save-config`, rollout history and rollback, Helm. File 3: `k run` Pod YAML, NodePort expose. File 2: `k run -it --restart=Never -image=alpine temp-pod` (source typo `-image` → `--image`). | todo | 0 |
| 3 | Application Observability and Maintenance | Base: "Application Observability and Maintenance". File 3: admission controllers, K8s version, API groups/versions, `kubectl proxy`, probes, monitoring/Metrics Server, logs, events, `kubectl debug`. | todo | 0 |
| 4 | Application Environment, Configuration and Security | Base: "Application Environment, Configuration and Security" | todo | 0 |
| 5 | Services and Networking | Base: "Services and Networking" | todo | 0 |
| 6 | General Knowledge | Base: "General Knowledge". File 2: general hints (spaces not tabs), tmux, alias, kubeconfig/context commands incl. `config unset`, namespace create/check/set/`-n`, `KUBE_EDITOR`, `k create -f ./`, jq. File 3: field selectors. | todo | 0 |
| 7 | Final audit | All three sources against the whole new file (reviewer in audit mode). | todo | 0 |

States: `todo` → `review` → `fix` → `review` … → `done` or `done-with-open-points`.

## Open points

- **0.1** — `user-decision` — Audit header: the header states CKAD uses Kubernetes v1.35, as the Linux Foundation FAQ and CKAD page say, while kubernetes.io lists v1.36 and v1.37 as released; the LF pages may lag their own 4–8-week alignment policy. Recheck the LF FAQ before the exam. https://docs.linuxfoundation.org/tc-docs/certification/faq-cka-ckad-cks , https://kubernetes.io/releases/
- **0.2** — `user-decision` — `<style>` block: the h5/h6 rules now use `counter-increment: h5` / `h6` and a `"."` separator, a repair none of the three sources had verbatim (file 3 fixed only the counter). Keep or revert.
- **1.1** — `unverified` — "Image Management - OCI Images": exam rule that the image must not be loaded onto a registry because doing so leaks exam info.
- **1.2** — `unverified` — "Fixing image names for pushing": the exam gives the repository name, and the image must not be pushed.
- **1.3** — `unverified` — "Fixing image names for pushing": tools other than Docker may need the `docker.io/` prefix even for Docker Hub; the podman-push docs do not settle the point.
- **1.4** — `unverified` — "Volumes": on-prem clusters typically use on-prem storage, and cloud clusters use cloud storage.
- **1.5** — `user-decision` — "Init pattern" (minor): "each init container must complete before the next starts" and "normal containers start after all init containers complete" hold only for regular init containers; a sidecar (`restartPolicy: Always`) never completes. Consider qualifying as "regular init containers". https://v1-35.docs.kubernetes.io/docs/concepts/workloads/pods/sidecar-containers/
- **1.6** — `user-decision` — "Remove an image" (minor): the note says `-f` forces removal when a container uses the image; the Docker daemon source refuses removal even with `-f` when a *running* container uses the image, while the docs page is less specific. https://docs.docker.com/reference/cli/docker/image/rm/
- **1.7** — `user-decision` — "Cronjobs" (minor): "`0 2 4 * *` runs at 2:00 every 4th day of the month" reads like "every 4 days"; the expression means 02:00 on day 4 of each month.
- **1.8** — `user-decision` — "Jobs" (minor): the bullet "Jobs can create multiple Pods and even run them in parallel" nearly repeats the first bullet on parallel Pods.
- **1.9** — `user-decision` — "Volumes" (minor): "Storage classes (SC)" and "Storage Classes" are two headings on one subject, and the third bullet under "Storage Classes" restates the provisioning timing given under "VolumeBindingMode". Structure inherited from the base.
