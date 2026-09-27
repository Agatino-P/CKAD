# CKAD Activity Tracker

## Tracking rule

Codex records useful decisions, constraints, preferences, research findings, and next actions exchanged by User and Codex during repository work.

## Standing context

- User is preparing for another CKAD exam.
- The official CKAD environment was Kubernetes v1.35 on 2026-09-20; Codex must verify the version again near the exam date.
- User wants a later study plan built around a local `kind` cluster.
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
