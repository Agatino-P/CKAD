# CKAD Notes Review Tracker

## Goal

Preserve the CKAD study notes as a concise personal recall aid for concepts and exam mechanics that User found non-obvious, forgot, or needs to practise. Complete CKAD coverage is not the goal.

## Review method

For every topic User chooses to retain:

1. Read the existing explanation and examples.
2. Classify the content as **current**, **outdated**, **unclear**, **duplicate**, or **needs verification**.
3. Verify technical claims against primary sources, preferably the current Kubernetes and Linux Foundation documentation.
4. Use practice results to distinguish knowledge gaps from lost command recall, speed, and other exam-specific skills.
5. Add only concise reminders justified by User's observed gaps; do not expand the notes into a syllabus.
6. Record the source, verification date, completed changes, and remaining questions.

## Status key

- [ ] Not started
- [~] In progress
- [x] Reviewed
- [!] Blocked or needs a decision

## Files

| Status | File | Review findings | Corrections | Last verified |
| --- | --- | --- | --- | --- |
| [~] | `Study notes/CKAD appunti.md` | Outdated-content audit completed; User's personal review remains pending. | 9 concise outdated notes added. | 2026-09-20 |
| [~] | `Study notes/CKAD 2 appunti.md` | Inclusion audit completed: only partly represented in the recap; outdated-content audit completed. | 1 concise outdated note added. | 2026-09-20 |
| [~] | `Study notes/CKAD 3 appunti.md` | Inclusion audit completed: only partly represented in the recap; outdated-content audit completed. | 1 concise outdated note added. | 2026-09-20 |
| [~] | `Study notes/CKAD appunti recap.md` | Selective synthesis of files 2 and 3, with substantial additional material; not a complete merge. | — | — |

## Supporting material

| Status | File | Purpose | Findings |
| --- | --- | --- | --- |
| [ ] | `Study notes/Killer Shell - Exam Simulators - results.pdf` | Compare past simulator results with the topics covered by the notes. | — |
| [x] | `PRACTICE_RESOURCES.md` | Supply a selective practice base for later gap discovery. | Three core resources selected with caveats and verification links. |

## Review log

Add one entry for each review session. Keep findings concise and link each finding to the affected file or topic.

### Session template

- **Date:** YYYY-MM-DD
- **File or topic:**
- **Reviewed:**
- **Findings:**
- **Sources:**
- **Changes made:**
- **Open questions:**
- **Next action:**

### 2026-09-20 — Recap inclusion audit

- **Files compared:** `CKAD 2 appunti.md`, `CKAD 3 appunti.md`, and `CKAD appunti recap.md`
- **Question:** Does the recap include all material from the other two files?
- **Conclusion:** No. The recap compresses selected material from both files, omits multiple topics and details, and adds substantial material absent from both source files.
- **Material retained or compressed from file 2:** kubectl alias and editor, temporary Pod and service creation, selected Deployment and rollback commands, and a condensed Helm workflow.
- **Material omitted or incomplete from file 2:** tmux; kubeconfig cluster/context commands; namespace commands; bulk YAML creation; Deployment editing and scaling; `minReadySeconds`, `progressDeadlineSeconds`, `revisionHistoryLimit`, and rolling-update settings; rollout-history details; the `jq` example; and detailed Helm flags and version-search notes.
- **Material retained or compressed from file 3:** admission controllers, API resource/version discovery, readiness and liveness concepts, Pod YAML generation, `kubectl top`, events, and NodePort exposure.
- **Material omitted or incomplete from file 3:** admission-request behavior and several controller details; Kubernetes version notation and API-group explanations; probe YAML, probe types, startup probes, and probe results; monitoring options and Metrics Server details; container-log commands; `kubectl debug`; and field selectors.
- **Material added by the recap:** OCI images and Dockerfiles; Jobs and CronJobs; sidecars and storage; CRDs; RBAC; quotas; ConfigMaps; ServiceAccounts; security contexts; NetworkPolicies; DNS; and Ingress.
- **Sources:** Repository files only; no external technical validation performed during this inclusion audit.
- **Changes made:** Tracker updated; study-note contents unchanged.
- **Open questions:** Decide whether omitted material should be restored, discarded as obsolete or low-value, or kept in separate detailed notes.
- **Next action:** Build a topic-by-topic disposition list for the omitted material before consolidating or deleting any source file.

### 2026-09-20 — Notes purpose and practice-driven workflow

- **User direction:** The notes intentionally capture non-obvious material from User's first CKAD preparation rather than covering CKAD completely.
- **Decision:** Keep the notes short, selective, and personal; do not restore omitted topics merely for completeness.
- **Workflow:** User reviews the existing notes first. Practice tests then identify forgotten material and exam-specific execution weaknesses worth recording.
- **Changes made:** Review goal, method, file status, open questions, and next action aligned with the gap-focused workflow.
- **Sources:** User's stated study approach and repository files.
- **Next action:** Wait for User's review, then record only concrete gaps found during practice.

## Open questions

- When is User's target exam date, and how much weekly practice time is available?
- Which note file should receive new findings after the first practice test?
- Which CKAD environment version applies near the exam date? Recheck the official page before final preparation.

## Next action

User reviews the existing notes at User's own pace. After the first practice test, classify each miss as a knowledge, recall, speed, or environment gap and add only useful concise reminders.
