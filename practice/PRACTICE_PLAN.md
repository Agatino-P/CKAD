# CKAD practice plan

Written on 2026-09-29.\
This is practice, not exam simulation.\
Everything Claude writes for it is in English.

## Goal

Practise CKAD exercises one at a time on a local kind cluster.\
Claude grades each attempt, names the gap, teaches when needed, and records the result.\
A failed exercise comes back until it is mastered.

## Facts

- The exam runs on Kubernetes v1.37 and lasts 2 hours: [Linux Foundation CKAD page](https://training.linuxfoundation.org/certification/certified-kubernetes-application-developer-ckad/), read on 2026-09-30.
- The five domains and their weights are in `CKAD_Curriculum_v1.35.pdf` in [cncf/curriculum](https://github.com/cncf/curriculum), still the newest CKAD curriculum file there on 2026-09-30.
- Agatino Pesce holds the exam voucher and targets early November 2026. When he practises is his own business.

## Files

Everything for the program lives under `practice/`, and the repository root keeps only the trackers, the study notes and the certificate.

- `practice/scripts/`: every script, with `setup.sh` as the one command that prepares a machine from a fresh clone. It installs the missing tools, pulls the submodules, builds the lab and runs its checks.
- `practice/PRACTICE_PLAN.md`, this file.
- `practice/PRACTICE_RESOURCES.md`: each source, why it was chosen, and its caveats.
- `practice/EXERCISE_INDEX.md`: one row per exercise. A row holds the id, the exam domain, a one-sentence topic, the source pointer (file and heading), what the lab must provide, and the verification state.
- `practice/RESULTS_LEDGER.md`: one row per attempt. A row holds the date, the exercise id, the result, the minutes taken, the gap class, and one note.
- `practice/sources/`: the upstream exercise repositories as git submodules pinned to a commit. A submodule pins the commit, restores on a fresh clone, keeps upstream content out of this history, and is the only clean option for a source without a licence file.
- `practice/exercises/`: only what a source lacks, such as a setup manifest or a check script.
- `practice/lab/`: the kind cluster definition and the add-on manifests.
- `Study notes/CKAD cheat sheet.md`: the cheat sheet. A gotcha found in practice is added there as a short line.

## Sources

Detail, links and caveats are in `practice/PRACTICE_RESOURCES.md`.

| Source | What it gives | How an attempt is graded |
| --- | --- | --- |
| `dgkanatsios/CKAD-exercises` | Short questions by topic, with solutions | Claude inspects the cluster |
| `bmuschko/ckad-crash-course` | Longer scenarios, with solutions and some setup manifests | Claude inspects the cluster |
| `TiPunchLabs/ckad-dojo` | Questions tagged by domain, with setup manifests, solutions and scoring scripts | The project's scoring function for that question |
| Killer Shell simulator archive, own PDF | Exam-style questions with solutions, written for Kubernetes 1.31 | Claude inspects the cluster |

## The loop

One exercise at a time.

1. **Pick.** A new exercise while any exercise in the index has no attempt yet: from the domain with the most failures in the ledger, or the next domain in curriculum order while there are no failures yet. Once every exercise has had a first attempt, the retry queue.
2. **Prepare.** Claude applies the setup manifest if there is one, runs the reference solution once to confirm it works on v1.37, records that version as `verified` in the exercise's entry in `practice/scripts/exercise-map.json` and regenerates the index, resets the lab, writes the acceptance criteria down before the attempt, and states the time budget while budgets are in use.
3. **Attempt.** Agatino Pesce works in his own terminal on the lab cluster and says "start", then "done", "skip" or "hint". A hint caps the result at partial.
4. **Grade.** Claude inspects the cluster state with kubectl against the written criteria, or runs the ckad-dojo scoring function when one exists, and reports the result, the failed criteria, and the reference solution.
5. **Classify a miss** as knowledge, recall, speed, environment or slip.
6. **Teach** when the class is knowledge or recall: one bite as the interactive-teaching guideline describes, then stop and wait.
7. **Record** the ledger row, and add a line to the cheat sheet only when the miss revealed a gotcha.
8. **Clean up** the exercise's namespaces. The cluster stays up.

## Grading

Results:

- **pass**: every acceptance criterion met within the time budget.
- **pass-slow**: every criterion met, over the time budget.
- **partial**: some criteria met, or a hint was used.
- **fail**: the task was not achieved or was skipped.

Gap classes:

- **knowledge**: the concept was not known.
- **recall**: the concept was known but the command, flag or field could not be recalled.
- **speed**: known and done, but too slowly.
- **environment**: the editor, shell or tooling got in the way.
- **slip**: the concept and the command were right, but a name or a value was mistyped or misread.

Mastery rule, set by Agatino Pesce: an exercise is done after one success at the first attempt, or after two successes following a failure.\
A success is a pass.\
Pass-slow, partial and fail count as failures, Claude's reading, because the exam is timed.\
The retry queue is derived from the ledger and never stored separately.\
Retries start only after every exercise in the index has had its first attempt, set by Agatino Pesce on 2026-10-05, so that a retry tests the concept rather than the memory of the exercise.\
The retry queue is then worked through in rounds, with one attempt per exercise per round, so the two successes after a failure fall in different rounds.

Time budget: Claude states one before each attempt, from the size of the task.\
Agatino Pesce suspended time budgets on 2026-10-05.\
While they are suspended, Claude states no budget, an attempt that meets every criterion is a pass, and pass-slow does not apply.

## Setup, on any machine

```bash
git clone --recurse-submodules <this repository>
practice/scripts/setup.sh
```

The script needs Homebrew and a container engine, either Docker Desktop or podman with a running machine.\
It installs kind, kubectl and helm when missing, pulls the submodules, creates the cluster from `practice/lab/kind-cluster.yaml` with metrics-server and ingress-nginx, and runs `practice/scripts/lab-check.sh`.\
The checks prove the `standard` StorageClass, `kubectl top`, NetworkPolicy enforcement by kindnet, an Ingress reachable on port 8080 of localhost, NodePort 30080 reachable on port 9080 of localhost, and helm.\
Ports 9080 and 9443 of localhost map to NodePorts 30080 and 30443, reserved for a Gateway API implementation.\
Every step checks before acting, so the script can be re-run after a failure.

ckad-dojo's scripts run through `practice/scripts/dojo.sh`, which puts a docker-to-podman shim on PATH and skips the project's image registry.\
`practice/scripts/build-index.py` regenerates the exercise index when a submodule is updated.

Every exercise is verified at first use, in the "Prepare" step, not up front.

## Decisions

Set by Agatino Pesce on 2026-09-29:

- Practice, not exam simulation.
- All practice files live under `practice/`, never in the repository root.
- Mastery is per exercise: one success from scratch, or two successes after a failure.
- Everything is in English.
- New gotchas go to the cheat sheet, `Study notes/CKAD cheat sheet.md`.
- Scheduling is his own and is not part of this plan.

Claude's defaults, adopted on 2026-09-29 without objection:

- Sources are git submodules under `practice/sources/`.
- ckad-dojo is used for its per-question setup manifests and scoring scripts.
