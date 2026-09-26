# Goal — rebuild `Study notes/CKAD appunti.md`

All paths are relative to the repository root (`git rev-parse --show-toplevel`).

## Outcome

A new `Study notes/CKAD appunti.md` that merges the three source files below into one corrected reference:

- `Study notes/backup/CKAD appunti.md` — the base file; its structure and heading order are kept.
- `Study notes/backup/CKAD 2 appunti.md`
- `Study notes/backup/CKAD 3 appunti.md`

The goal is complete when every section in `prompts/status.md` is `done` or `done-with-open-points` and the final completeness audit has passed.

## Scope decisions made by User

- **Full reference.** All content from the three sources is kept. Exact duplicates are merged into one copy; nothing else is dropped. No new topics are added — the notes stay a personal record, not a CKAD syllabus.
- **All corrections applied.** Every technical claim, command, flag, field and YAML block is checked against official documentation **online**: Kubernetes docs for the current CKAD version, plus the official Docker, Podman, Helm and Linux Foundation docs. A claim that cannot be verified online is not guessed: the claim stays in the file with an HTML comment `<!-- UNVERIFIED: see prompts/status.md -->`, and an open point is recorded in `prompts/status.md`.
- **Current behaviour only.** The notes state how things work now. No version history such as "since v1.29" or "starting with Docker 25". Once a section is corrected, its `> **OUTDATED**` boxes are removed.
- **Keep the current style.** Keep the CSS `<style>` block, the audit header, the CKAD-domain headings and the `<mark>` exam tips.
- **When 2/3 and the base disagree,** the version confirmed by the official docs wins. Files 2 and 3 are often, but not always, the corrected version.
- **Out of scope:** `CKAD appunti recap.md`. The recap gets its own goal later.

## Process

A writer ↔ adversarial-reviewer loop, one section per cycle, followed by one final completeness cycle. Each writer run and each reviewer run is a **fresh subagent**. The orchestrator (the session running the loop) never writes note content itself; it only dispatches the agents, updates `prompts/status.md`, commits and pushes.

- A section finishes when the reviewer reports **no blocking findings**, or after **3 review rounds**. After round 3, the remaining blocking findings become open points in `prompts/status.md`.
- After each finished section, the orchestrator makes **one git commit**.
- The repository is pushed at major steps: before the loop begins, after each main CKAD section (sections 1–6), and after the final audit. The details are in `prompts/loop.md`.
- `prompts/status.md` is the single source of truth for progress and open points. It holds the **current state only**: no history, no log and no dated entries. A resolved point is deleted from the file, because the fix itself now lives in the notes.

## Preconditions (check before starting)

1. The three source files exist under `Study notes/backup/`.
2. The move of the old files into `Study notes/backup/` is already committed (`git status` shows no staged renames). If the move is not committed, stop and ask User. Do not commit the move on User's behalf.
3. Nothing is left unpushed before the loop begins. If `git status -sb` shows the branch ahead of `origin`, run `git push` first; that push is the "before we begin" major step.
4. `prompts/status.md` exists. If every section in `prompts/status.md` is still `todo`, the run starts fresh; otherwise the run resumes from the recorded state.

## Start

Once the preconditions hold, start the loop by invoking the `loop` skill with no interval (self-paced) and these arguments:

```
Follow prompts/loop.md exactly: read prompts/status.md, perform the next step, update prompts/status.md.
```

When `prompts/status.md` shows the goal complete, the loop stops itself and reports to User:
- a summary of what was merged and corrected;
- the open points left for User.

Finally, add one concise entry to `ACTIVITY_TRACKER.md` recording that the rebuild is done and pointing to `prompts/status.md` for the open points. Then commit only `ACTIVITY_TRACKER.md` and push:

```
git add ACTIVITY_TRACKER.md
git commit -m "docs: record CKAD appunti rebuild" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" -- ACTIVITY_TRACKER.md
git push
```
