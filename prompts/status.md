# Status — CKAD appunti rebuild

Current state only. No history, no dates, no log. Delete a resolved point instead of striking it through.

Target: `Study notes/CKAD appunti.md`
Sources: `Study notes/backup/CKAD appunti.md` (base), `Study notes/backup/CKAD 2 appunti.md` (file 2), `Study notes/backup/CKAD 3 appunti.md` (file 3)

## Current step

Codex review pass, defined in `prompts/codex-review.md` (Codex CLI, model `gpt-5.6-sol`, as reviewer; wrong or missing content only; Claude verifies each finding and applies confirmed fixes directly). Section 0 is done; every fix accepted so far is in the notes. Next: run the reviews shown in the table (State `review`, Round = the round to run next): section 1 round 2, section 2 round 3, section 3 round 2, section 4 round 2, section 5 round 2, section 6 round 3. Codex usage ran out; the earlier attempts at these runs failed on the limit and do not count as rounds.

## Agent running

Codex reviewers running: s1 r2, s2 r3, s3 r2, s4 r2, s6 r3 (outputs `prompts/tmp/codex_s<N>_r<round>.out`)

## Sections

| # | Section | Source mapping | State | Round |
|---|---|---|---|---|
| 0 | Preamble | Base: CSS `<style>` block and audit header. Re-verify the current CKAD Kubernetes version online and update the header. | done | 1 |
| 1 | Application Design and Build | Base: "Application Design and Build" (images, Docker/Podman, Jobs, CronJobs, multi-container Pods, volumes) | review | 2 |
| 2 | Application Deployment | Base: "Application Deployment". File 2: create/expose/dry-run Deployment, edit, scale, Deployment `spec`/`strategy`, `--save-config`, rollout history and rollback, Helm. File 3: `k run` Pod YAML, NodePort expose. File 2: `k run -it --restart=Never -image=alpine temp-pod` (source typo `-image` → `--image`). | review | 3 |
| 3 | Application Observability and Maintenance | Base: "Application Observability and Maintenance". File 3: admission controllers, K8s version, API groups/versions, `kubectl proxy`, probes, monitoring/Metrics Server, logs, events, `kubectl debug`. | review | 2 |
| 4 | Application Environment, Configuration and Security | Base: "Application Environment, Configuration and Security" | review | 2 |
| 5 | Services and Networking | Base: "Services and Networking" | done-with-open-points | 2 |
| 6 | General Knowledge | Base: "General Knowledge". File 2: general hints (spaces not tabs), tmux, alias, kubeconfig/context commands incl. `config unset`, namespace create/check/set/`-n`, `KUBE_EDITOR`, `k create -f ./`, jq. File 3: field selectors. Note: section 2 already holds "Modify a deployment from the command line" and the temp-pod item; merge the base General Knowledge copies there as duplicates (the extra `k run` variants carry the typo `--restar=never`). | review | 3 |
| 7 | Final audit | All three sources against the whole new file (Codex reviewer in audit mode). | review | 1 |

States: `todo` → `review` → `fix` → `review` … → `done` or `done-with-open-points`.

## Open points

- **5.2** · `disputed` · Services and Networking → "Provide and Troubleshoot Access to Applications via Services" · Codex asked to make Service DNS statements conditional on "if cluster DNS is enabled". Claude rejected the finding as a nitpick: the notes describe a standard cluster where the DNS add-on (CoreDNS) runs, and the real exception (a `hostNetwork` Pod with `dnsPolicy: ClusterFirst`) is now in the notes under "DNS". Ref: https://v1-35.docs.kubernetes.io/docs/concepts/services-networking/service/#dns
