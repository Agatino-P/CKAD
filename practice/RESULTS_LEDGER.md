# CKAD results ledger

One row per attempt, appended by Claude after grading.\
The exercise ids are those of `practice/EXERCISE_INDEX.md`.\
Results and gap classes are defined under "Grading" in `practice/PRACTICE_PLAN.md`.\
The retry queue is derived from this table by the mastery rule and is never stored.

| Date | Id | Result | Minutes | Gap | Note |
| --- | --- | --- | --- | --- | --- |
| 2026-10-05 | DGK-A-01 | partial | — | slip | Pod named `ngnix` instead of `nginx`. Namespace, image and Running state were correct. |
| 2026-10-05 | DGK-A-02 | pass | — | — | Pod created with `kubectl apply -f` from a generated manifest. |
| 2026-10-05 | DGK-A-03 | pass | — | — | Created with `kubectl apply` from a manifest, running `env` through `sh -c`. |
| 2026-10-05 | DGK-A-04 | pass | — | — | Created with `kubectl apply` from a manifest with command `env`. |
| 2026-10-05 | DGK-A-08 | pass | — | — | `kubectl run` with `--port=80`. |
| 2026-10-05 | DGK-A-16 | partial | — | slip | Output was `hello World` instead of `hello world`. Pod ran once and completed. |
| 2026-10-05 | DGK-A-17 | fail | — | recall | Did not recall `--rm` on `kubectl run`, after a hint. Practice paused to study command, args and `sh -c`. |
| 2026-10-06 | DGK-B-01 | pass | — | — | Two containers with `args: ["sh", "-c", "echo hello; sleep 3600"]`, `ls` run with `kubectl exec -c`. |
| 2026-10-06 | DGK-B-02 | pass | — | — | Init container wrote the page into an `emptyDir`, and `wget` from a busybox Pod returned `Test`. |
| 2026-10-06 | DGK-C-01 | pass | — | — | Three nginx Pods with label `app=v1`. |
| 2026-10-06 | DGK-C-02 | pass | — | — | `kubectl get pod --show-labels`. |
| 2026-10-06 | DGK-C-03 | pass | — | — | `nginx2` relabelled to `app=v2`. |
| 2026-10-06 | DGK-C-04 | pass | — | — | `kubectl get pod -L app`. |
| 2026-10-06 | DGK-C-05 | pass | — | — | `kubectl get pod -l app=v2`. |
| 2026-10-06 | DGK-C-06 | partial | — | recall | Selector `app=v2` only, without `tier!=frontend`. |
| 2026-10-06 | DGK-C-07 | pass | — | — | Two `kubectl label -l` commands, one per `app` value. |
| 2026-10-06 | DGK-C-08 | pass | — | — | `owner=marketing` on `nginx2` only. |
| 2026-10-06 | DGK-C-09 | pass | — | — | `app` label removed from the three Pods. |
| 2026-10-06 | DGK-C-10 | pass | — | — | `description` annotation on the three Pods. |
| 2026-10-06 | DGK-C-11 | pass | — | — | `kubectl describe pod nginx1 \| grep -i description`. |
