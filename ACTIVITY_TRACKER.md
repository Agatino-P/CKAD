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
