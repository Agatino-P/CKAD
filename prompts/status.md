# Status — CKAD appunti rebuild

Current state only. No history, no dates, no log. Delete a resolved point instead of striking it through.

Target: `Study notes/CKAD appunti.md`
Sources: `Study notes/backup/CKAD appunti.md` (base), `Study notes/backup/CKAD 2 appunti.md` (file 2), `Study notes/backup/CKAD 3 appunti.md` (file 3)

## Current step

Codex review pass: the rebuild is complete; a second adversarial loop now reviews each section with the Codex CLI (model `gpt-5.6-sol`) as reviewer. Scope: wrong or missing content only; cosmetic findings are ignored. Claude verifies each Codex finding and applies confirmed fixes directly (no writer subagent); rejected findings are dropped with evidence. Same 3-round limit, commit per section, push per main section and after the audit. Reviewer prompt: `prompts/tmp/codex_reviewer_prompt.md`.

## Agent running

none — Codex hit its usage limit (resets 15:46). Reviews to rerun: section 1 round 2 (if its run failed), section 2 round 3, section 3 round 2, section 4 round 2, section 5 round 2, section 6 round 3; prompts in `prompts/tmp/codex_s<N>_r<round>.prompt`.

## Sections

| # | Section | Source mapping | State | Round |
|---|---|---|---|---|
| 0 | Preamble | Base: CSS `<style>` block and audit header. Re-verify the current CKAD Kubernetes version online and update the header. | done | 1 |
| 1 | Application Design and Build | Base: "Application Design and Build" (images, Docker/Podman, Jobs, CronJobs, multi-container Pods, volumes) | review | 2 |
| 2 | Application Deployment | Base: "Application Deployment". File 2: create/expose/dry-run Deployment, edit, scale, Deployment `spec`/`strategy`, `--save-config`, rollout history and rollback, Helm. File 3: `k run` Pod YAML, NodePort expose. File 2: `k run -it --restart=Never -image=alpine temp-pod` (source typo `-image` → `--image`). | review | 3 |
| 3 | Application Observability and Maintenance | Base: "Application Observability and Maintenance". File 3: admission controllers, K8s version, API groups/versions, `kubectl proxy`, probes, monitoring/Metrics Server, logs, events, `kubectl debug`. | review | 2 |
| 4 | Application Environment, Configuration and Security | Base: "Application Environment, Configuration and Security" | review | 2 |
| 5 | Services and Networking | Base: "Services and Networking" | review | 2 |
| 6 | General Knowledge | Base: "General Knowledge". File 2: general hints (spaces not tabs), tmux, alias, kubeconfig/context commands incl. `config unset`, namespace create/check/set/`-n`, `KUBE_EDITOR`, `k create -f ./`, jq. File 3: field selectors. Note: section 2 already holds "Modify a deployment from the command line" and the temp-pod item; merge the base General Knowledge copies there as duplicates (the extra `k run` variants carry the typo `--restar=never`). | review | 3 |
| 7 | Final audit | All three sources against the whole new file (Codex reviewer in audit mode). | review | 1 |

States: `todo` → `review` → `fix` → `review` … → `done` or `done-with-open-points`.

## Open points

None.
