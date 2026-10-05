# CKAD Activity Tracker

## Tracking rule

Codex records useful decisions, constraints, preferences, research findings, and next actions exchanged by User and Codex during repository work.

## Standing context

- User is preparing for another CKAD exam.
- The official CKAD page listed Kubernetes v1.37 on 2026-09-30; Codex must verify the version again near the exam date.
- User wants a later study plan built around a local `kind` cluster, defined inside this repository.
- User asked on 2026-09-29 to ignore the sibling repository `~/GitLocalCopy/CKAD-LF`.
- User holds the exam voucher and targets early November 2026 for the exam, stated on 2026-09-29.
- User does not want to be asked about weekly schedule or available hours, and does not want a timeline planned. When phases and sessions run is User's own call.
- User wants free, reliable, selective practice material rather than large unverified resource lists.
- User does not want low-quality or unverified Udemy exam simulators.
- User intends the study notes to remain a short record of concepts and exam mechanics that were not obvious, not a complete CKAD syllabus.
- User may retain real-world Kubernetes knowledge while losing exam-specific recall or speed; future recommendations should distinguish knowledge gaps from practice gaps.

## Activity log

### 2026-09-20 — Free CKAD practice-material research

- **User already knew:** Killercoda and `dgkanatsios/CKAD-exercises`.
- **Research standard:** Prefer official ownership, visible source material, recent maintenance, solutions or validation, and coverage of current CKAD domains.
- **Selected core:** Killercoda free scenarios, `dgkanatsios/CKAD-exercises`, and `bmuschko/ckad-crash-course`.
- **Verification base:** Linux Foundation CKAD information and the Kubernetes v1.35 documentation snapshot.
- **Local direction:** Re-run suitable exercises on `kind`; account for add-ons when exercises need Ingress, metrics, storage, or NetworkPolicy enforcement.
- **Not selected:** Exam dumps, unverified course marketplaces, random question banks, and new self-scoring projects not yet locally validated.
- **Artifact:** `PRACTICE_RESOURCES.md`.
- **Next action:** Build a study plan only after User and Codex agree on available time, exam date, and baseline skill gaps.

### 2026-09-20 — Gap-focused notes workflow

- **Purpose:** Preserve the notes as a concise personal recall aid rather than expanding the notes into complete CKAD coverage.
- **Sequence:** User reviews the existing notes first, then uses practice tests to expose forgotten knowledge and exam-execution weaknesses.
- **Update rule:** Add short notes only when review or practice reveals a useful gap; avoid syllabus-driven expansion.
- **Study implication:** Separate conceptual gaps from speed, command recall, and other exam-only practice needs.
- **Next action:** Wait for User's note review; later update the notes from concrete practice-test findings.

### 2026-09-26 — Image save section rewritten

- **Change:** Rewrote "Dump an image as a tar file" in `Study notes/CKAD appunti.md` and removed the OUTDATED box.
- **Verified online:** `docker save` has only `-o/--output` and `--platform` (no `--format`); the Docker save tar is OCI-compliant (`oci-layout`, `index.json`, `blobs/`, plus `manifest.json`); `docker load` accepts gzip, bzip2, xz, and zstd archives; Podman `save --format` defaults to `docker-archive`.
- **User preference:** Notes state current behavior only, without version history.
- **Dropped as unverified:** The claim that `oci-archive` layers are compressed and `docker-archive` layers are not; Podman docs do not compare the two formats.
- **Open:** The official CKAD handbook was not checked for which container tools the exam provides; third-party 2026 guides say both Docker and Podman.

### 2026-09-26 — Notes restructure and review-tracker retirement

- **Structure decided:** Two note files: `Study notes/CKAD appunti.md` (full corrected reference) and `Study notes/CKAD appunti recap.md` (short exam-day sheet). The previous four note files are kept as-is in `Study notes/backup/`.
- **Main-file rebuild:** Runs as a writer ↔ adversarial-reviewer loop defined in `prompts/goal.md` and `prompts/loop.md`; progress and open points live in `prompts/status.md`.
- **Retired:** `NOTES_REVIEW_TRACKER.md`, whose content was duplicated here, superseded by `prompts/`, or stale. The points below were unique to that file.
- **Open — Killer Shell results:** `Study notes/Killer Shell - Exam Simulators - results.pdf` has not yet been compared with the topics covered by the notes.
- **Open — practice findings destination:** Decide where new findings from practice tests go; likely candidates are the recap for quick reminders and the main file for longer explanations.
- **Recap rebuild input:** Compared with the old files 2 and 3, the recap added OCI images and Dockerfiles; Jobs and CronJobs (including `sh -c` usage and `k logs job/<name>`); sidecars and storage scoping; CRDs; RBAC; quotas; ConfigMaps and `$(VAR)` in args; ServiceAccounts and their Secrets; security contexts; NetworkPolicies; service DNS names; Ingress; nano settings; and `helm ls -a`.

### 2026-09-27 — CKAD appunti rebuild done

- **Result:** `Study notes/CKAD appunti.md` is rebuilt from the three backup files (base, file 2, file 3) through the writer ↔ adversarial-reviewer loop; every section is reviewed, and the final audit found no lost content.
- **Verification:** Claims were checked against the v1.35 docs online and, where possible, by running commands on the local `kind-ckad` cluster and Docker in throwaway namespaces and containers.
- **User rules set during the run:** statements from User's own exam experience count as verified; an open point is recorded only when something is left to change or decide; Claude runs checks itself instead of asking User to run them.
- **Open:** The remaining open points, including one blocking wording fix in "Remove an image", are in `prompts/status.md`.
- **Next action:** Work through the open points with User; the recap (`Study notes/CKAD appunti recap.md`) gets its own goal later.

### 2026-09-27 — Codex review pass of CKAD appunti started

- **Decision (User):** A second adversarial loop reviews `Study notes/CKAD appunti.md` with the Codex CLI (`gpt-5.6-sol`) as reviewer, per section and then a final audit; scope is wrong or missing content only, cosmetic findings ignored; no writer subagent — Claude verifies each Codex finding and applies confirmed fixes directly.
- **Protocol:** `prompts/codex-review.md` (run command, reviewer prompt template, rules); progress and disputed findings in `prompts/status.md`. Scratch files in `prompts/tmp/`, now gitignored.
- **Codex constraint:** Codex runs stop at the ChatGPT plan's usage limit; a run that hits the limit does not count as a round and is rerun after the reset time printed in its log.
- **Next action:** Run the pending reviews listed in `prompts/status.md`, then the final audit.

### 2026-09-27 — Codex review pass of CKAD appunti done

- **Result:** Codex (`gpt-5.6-sol`) reviewed sections 0–6 and ran the final audit of `Study notes/CKAD appunti.md`; Claude verified each finding and applied 23 fixes of wrong or missing content and rejected 1 finding (docs online plus checks on the local `kind-ckad` cluster). The final audit found no lost content.
- **Lesson:** a fix proposed by Codex can itself be wrong (the round-1 "kubelet stats via CRI" wording was reversed in round 2: embedded cAdvisor is the default, CRI stats need an alpha feature gate); later rounds must re-check accepted fixes.

### 2026-09-28 — CKAD cheat sheet created from the recap

- **Result:** `Study notes/CKAD cheat sheet.md` starts from `Study notes/backup/CKAD appunti recap.md`: every recap item kept, wrong items corrected (checked against the v1.35 docs and the local `kind-ckad` cluster), nothing added (User's choice).
- **Review:** three Claude reviewer-agent rounds (2 fixes: Helm pending releases, Pod-level resources), then Codex (`gpt-5.6-sol`), which found no wrong or missing content.
- **Open:** the CKAD exam's Helm version is not verified; the cheat sheet gives `helm ls --pending` (Helm 3 and 4) and notes that `helm ls -a` exists only in Helm 3.

### 2026-09-29 — Practice program planning

- **User request:** Build one exercise pool from all usable sources, run each exercise as a graded attempt with Claude as teacher and evaluator, rate performance, classify gaps, track results, and bring failed exercises back after study. Planning only in this session.
- **Machine state, on the Mac named CH-LAM-WS052:** kind v0.33.0 on podman, kubectl v1.37.0, uv and jq present, helm missing. A stopped kind cluster `ckad` and a stale context `kind-kind` are left over.
- **Findings:** The Killer Shell PDF in the study notes is a 22-question simulator archive on Kubernetes 1.31, not a score sheet. `TiPunchLabs/ckad-dojo` ships setup manifests, solutions and kubectl-based scoring for 398 questions and is the only source with automatic grading. The Killercoda CKAD course is now paid.
- **Proposed, pending User:** submodules under `practice/sources/`, a lab definition under `practice/lab/`, an exercise index and an attempt ledger, a four-value result scale, the four gap classes, a retry rule, and three phases from baseline mock to killer.sh rehearsal.
- **Artifacts:** `practice/PRACTICE_PLAN.md` drafted. `practice/PRACTICE_RESOURCES.md` re-verified and rewritten in place.
- **Answered by User the same day:** voucher bought, exam in early November 2026. Scheduling stays with User and is not part of the plan.
- **Decided by User the same day:** practice, not exam simulation, so no mocks, phases or exam conditions. All practice files live under `practice/`, never in the repository root. Mastery per exercise (one success from scratch, or two successes after a failure), everything in English, gotchas go to the cheat sheet `Study notes/CKAD cheat sheet.md`.
- **Claude's defaults adopted without objection:** submodules under `practice/sources/`, ckad-dojo used for its per-question setup manifests and scoring scripts.
- **Setup done the same day, on CH-LAM-WS052:** helm installed, version 4.3.0 from Homebrew. Cluster `ckad` created from `practice/lab/` on the v1.35 node image, with metrics-server and ingress-nginx. Checked on the cluster: the `standard` StorageClass exists, `kubectl top` answers, kindnet blocks traffic under a deny-all NetworkPolicy, and an Ingress answers on `http://localhost:8080`. The leftover cluster, the stale `kind-kind` context and the old `kind` network were deleted. Submodules added under `practice/sources/`. `practice/RESULTS_LEDGER.md` created empty.
- **ckad-dojo on the lab:** its scripts refuse to start without a `docker` command, so `practice/scripts/shim/docker` forwards to podman when prepended to PATH. With the shim and `--skip-registry`, the simulation 1 setup and cleanup scripts ran, and its per-question scoring script works on its own.
- **User direction:** Track everything done, and script it, because the setup may have to be repeated on another machine.
- **Scripted, all under `practice/scripts/`:** `setup.sh` (tools, submodules, cluster, checks), `lab-up.sh`, `lab-check.sh` (the five lab checks), `lab-down.sh`, `dojo.sh` (ckad-dojo setup, score, cleanup with the shim), and `build-index.py` for the index. Any machine-specific state recorded in this file names the machine, because the file is shared through git.
- **Index built:** `practice/EXERCISE_INDEX.md`, regenerated byte for byte by `practice/scripts/build-index.py` from the submodules, the Killer Shell PDF and the hand-written `practice/scripts/exercise-map.json`. Row counts per source are in the index's Counts section. Two source anomalies are unindexed: a plain-line item at the end of dgkanatsios `j.podman.md`, and a stray task block before the title of ckad-dojo simulation 12.
- **Next action:** Start the loop in `practice/PRACTICE_PLAN.md` with the first exercise.

### 2026-09-30 — Local practice-cluster readiness review

- **Exam baseline:** The official Linux Foundation CKAD page now lists Kubernetes v1.37.
- **Cluster direction:** Rebuild the reproducible practice cluster from the digest-pinned `kindest/node:v1.37.0` image supplied by `kind` v0.33.0.
- **Required capabilities:** Keep a multi-node topology, default dynamic storage, Metrics Server, NetworkPolicy enforcement through the default `kindnet`, and a maintained Ingress implementation.
- **Next action:** Done in the entry "Practice lab moved to Kubernetes v1.37" below.

### 2026-09-30 — Kubernetes v1.37 notes-impact review

- **Baseline:** Updated the `Study notes/CKAD appunti.md` audit baseline and documentation links from Kubernetes v1.35 to v1.37.
- **Metrics:** Changed `PodAndContainerStatsFromCRI` from alpha to beta, kept the disabled-by-default status, and recorded the cAdvisor deprecation in Kubernetes v1.37.
- **Command behavior:** Recorded that `kubectl debug` now defaults to the `general` profile instead of `legacy`; the existing examples remain valid.
- **Cheat sheet:** No existing statement in `Study notes/CKAD cheat sheet.md` required a Kubernetes v1.37 correction.
- **No affected content:** The v1.36 and v1.37 API removals, `kubectl run -f` deprecation, static-Pod API-reference restriction, and Service `externalIPs` deprecation do not occur in the current notes.
- **Optional additions:** The stable `metrics.k8s.io/v1` API, stable image volumes, and stable `kubectl get -o kyaml` are current features but do not make existing note content wrong.

### 2026-09-30 — Practice lab moved to Kubernetes v1.37

- **User decision:** Replace the practice cluster with one on Kubernetes v1.37.
- **Lab:** `practice/lab/kind-cluster.yaml` pins both nodes to `kindest/node:v1.37.0@sha256:a1ed56cf…580ae5`, the digest in the kind v0.33.0 release notes. The existing lifecycle scripts in `practice/scripts/` were kept unchanged.
- **Verified:** `lab-down.sh` then `setup.sh` rebuilt the cluster on v1.37.0 with metrics-server and ingress-nginx, and every `lab-check.sh` check passed.
- **Version references:** `practice/PRACTICE_PLAN.md` and `practice/PRACTICE_RESOURCES.md` now say v1.37 for the exam and for solution checks. The CKAD curriculum file in cncf/curriculum was still `CKAD_Curriculum_v1.35.pdf` on 2026-09-30, so that reference stays; recheck for a newer file near the exam date.
- **kubectl skew:** kubectl is supported within one minor version of the API server, so a v1.36 client works with the v1.37 lab; a v1.35 client does not.
- **Next action:** Start the loop in `practice/PRACTICE_PLAN.md` with the first exercise.

### 2026-10-05 — Podman machine and lab rebuilt after a macOS reinstall, on CH-LAM-WS052

- **Found:** On CH-LAM-WS052 the `ckad` cluster still ran Kubernetes v1.35.8, from a node image created on 2026-09-29, so the v1.37 rebuild above had not reached this machine. The podman client was 6.1.1 while the podman machine ran 5.8.2, and `podman machine os upgrade` cannot cross that major version.
- **User decision:** Start clean. Removing the podman machine is acceptable, because User recreates the other containers from compose files.
- **Done:** Homebrew upgraded podman and kubectl. The podman machine was removed and recreated with 8 CPUs, 16 GiB of memory and a 100 GiB disk, so the client and the machine run the same podman version. `practice/scripts/lab-down.sh` then `practice/scripts/setup.sh` built the cluster on the pinned v1.37.0 digest, and every `lab-check.sh` check passed.
- **Not enabled:** Rosetta is installed on the Mac, but the new machine reports `"Rosetta": false` and runs amd64 images through qemu. The lab's node image is arm64, so the lab does not need Rosetta.
- **Not installed:** `podman-mac-helper`, which provides the default Docker socket. The lab does not use that socket, because `practice/scripts/shim/docker` calls podman directly.
- **Fixed:** `practice/scripts/lab-up.sh` failed at its node wait when it ran right after stopped kind containers were started, because the API server was not ready yet. The script now polls `/readyz` first, tested by stopping and starting the three node containers.
- **User decision, same day:** Add a second worker now rather than rebuild later, so exercises that spread Pods across nodes have two schedulable nodes. `practice/lab/kind-cluster.yaml` now defines one control plane and two workers. After a rebuild, every lab check passed.
- **Gateway ports reserved, same day:** ingress-nginx is retired upstream (confirmed by User), and kind sets port mappings only at cluster creation. User asked to reserve ports now for a Gateway API implementation: `localhost:9080` and `localhost:9443` map to NodePorts 30080 and 30443 on the control plane node. `practice/scripts/lab-check.sh` gained a check that NodePort 30080 answers on `localhost:9080`.
- **User decision, same day:** Keep ingress-nginx and install no Gateway API implementation. The official CKAD page lists only Ingress under Services and Networking, and an unsupported controller does not matter for a practice cluster. Ports 9080 and 9443 stay reserved.

### 2026-10-05 — First practice exercise

- **User decisions:** Time budgets are suspended for now, so an attempt that meets every criterion is a pass. A fifth gap class, **slip**, covers a mistyped or misread name or value. Both are recorded in `practice/PRACTICE_PLAN.md`.
- **First attempt:** DGK-A-01 graded partial with gap class slip, recorded in `practice/RESULTS_LEDGER.md`. It is now in the retry queue.
- **User decision:** Retries start only after every exercise in the index has had its first attempt, then run in rounds of one attempt per exercise. An immediate retry would test the memory of the exercise rather than the concept. Recorded in the "Pick" step and under "Grading" in `practice/PRACTICE_PLAN.md`.
- **Learned:** The dgkanatsios solutions still pass `--restart=Never` to `kubectl run` for long-running Pods. The flag only sets the Pod's `restartPolicy`, so an exercise that does not ask for it is not graded on it.
- **Verification state:** An entry in `practice/scripts/exercise-map.json` now carries `verified`, the Kubernetes minor version its reference solution was run on. `practice/scripts/build-index.py` shows it as "verified on v1.37" in `practice/EXERCISE_INDEX.md`, and every other row stays "unverified". The "Prepare" step in `practice/PRACTICE_PLAN.md` records it.
- **User decision:** In the first pass, the pick follows the domain rule strictly, even for exercises that build on the previous one, such as DGK-A-09 to DGK-A-15 on the `nginx` Pod. In the retry rounds, such a chain is taken in source order. Recorded in the "Pick" step of `practice/PRACTICE_PLAN.md`.
