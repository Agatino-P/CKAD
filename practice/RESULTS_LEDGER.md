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
