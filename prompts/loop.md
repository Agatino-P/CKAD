# Loop — writer ↔ adversarial reviewer

All paths are relative to the repository root (`git rev-parse --show-toplevel`).
Context and scope decisions: `prompts/goal.md`. Read `prompts/goal.md` once per iteration before acting.

## Roles

- **Orchestrator** — the session running this loop. It dispatches the subagents, edits `prompts/status.md`, commits and pushes. It never writes note content itself.
- **Writer** — a fresh subagent per run. It writes one section of `Study notes/CKAD appunti.md`.
- **Reviewer** — a fresh subagent per run, independent of the writer. It never edits the notes; it only reports findings.

A subagent's report reaches only the orchestrator. The orchestrator copies what matters into `prompts/status.md`.

## Temporary files

- Any scratch file goes in `prompts/tmp/`. That includes drafts, saved subagent reports, downloaded doc pages and diff outputs.
- No agent creates files anywhere else. That means nothing in the repository root and nothing in `Study notes/` except the target file.
- `prompts/tmp/` is never committed.

## One iteration

1. Read `prompts/status.md`.
2. **If an agent is marked running,** do not dispatch another agent. Wait for that agent's completion notice. If no notice arrives, schedule a fallback wakeup (120 s) and end the iteration.
3. **If every section is `done` or `done-with-open-points` and the final audit is `done`,** stop the loop, report to User and update `ACTIVITY_TRACKER.md` as `prompts/goal.md` says.
4. **Otherwise,** take the first section that is not finished and act on the section's state:

| State | Action | Next state |
|---|---|---|
| `todo` | Dispatch the **Writer** in *write* mode. | `review`, round 1 |
| `review` | Dispatch the **Reviewer**. Then apply the decision rule below. | `fix` or finished |
| `fix` | Dispatch the **Writer** in *fix* mode, passing the section's open blocking findings. | `review`, round + 1 |

   **Decision rule after a review:**
   - **No blocking findings:** the section is `done`. Record any minor findings the writer did not fix as open points.
   - **Blocking findings and round < 3:** the section goes to `fix`. Record the findings under the section in `prompts/status.md`.
   - **Blocking findings and round = 3:** the section is `done-with-open-points`. The remaining findings stay as open points for User.

5. **When a section becomes finished, commit.** Stage only `Study notes/CKAD appunti.md` and `prompts/status.md`, then commit only those two paths:
   ```
   git add "Study notes/CKAD appunti.md" prompts/status.md
   git commit -m "notes: rebuild <section name> in CKAD appunti" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" -- "Study notes/CKAD appunti.md" prompts/status.md
   ```
   Never commit other files.
6. **Push at major steps.** In this repository a major step is:
   - each main CKAD section (sections 1–6);
   - the final audit.

   After committing one of these, run `git push`. The preamble (section 0) is not a major step on its own: its commit is pushed together with section 1. If `git push` fails, stop the loop and report the error to User. Do not force-push, and do not rewrite history.
7. Update `Current step` in `prompts/status.md`.
8. Schedule the next wakeup (60 s) and end the iteration.

The **final audit** is the last row in the status table. The final audit runs the reviewer in *audit* mode, then the writer in *fix* mode if needed. The final audit uses the same state machine and the same limit of 3 rounds.

## Rules for `prompts/status.md`

- Current state only: no history, no log, no dates, no "round 1 said…".
- A resolved finding is deleted, not struck through.
- Every open point has an ID (`<section #>.<n>`, e.g. `3.2`), a type, a one-line description, and the location (heading) in the notes. When relevant, an open point also cites a doc URL.
- Open point types:
  - `blocking` — a pending fix;
  - `disputed` — the writer rejected the finding and gave evidence; User decides;
  - `unverified` — could not be confirmed online;
  - `user-decision` — a choice that belongs to User.

---

## Writer prompt (pass verbatim, filling the `{…}` fields)

> Role: writer. The task is to write section **{section name}** of `Study notes/CKAD appunti.md` in mode **{write | fix}**. Read `prompts/goal.md` for the scope decisions; those decisions are binding.
>
> **Sources.** Read all three source files in full: `Study notes/backup/CKAD appunti.md`, `Study notes/backup/CKAD 2 appunti.md` and `Study notes/backup/CKAD 3 appunti.md`. Coverage is decided by reading the files, never by grep alone. This section corresponds to: {source mapping from status.md}.
>
> **Write mode:**
> - Produce the section with its heading order following the base file.
> - Merge in everything from files 2 and 3 that belongs to this section.
> - Merge exact duplicates into one copy.
> - Correct every error, verifying online against official docs (for Kubernetes, the docs for the CKAD version stated in the audit header).
> - Remove `> **OUTDATED**` boxes after applying the fix they describe.
> - State current behaviour only, with no version history.
> - Keep the style: headings, `<mark>` exam tips, fenced YAML and commands.
> - If a claim cannot be verified, keep the claim and add `<!-- UNVERIFIED: see prompts/status.md -->`.
> - Do not add topics the sources do not have.
> - Replace only this section in the target file. Leave the other sections byte-identical.
> - Scratch files go only in `prompts/tmp/`. Create no other files.
>
> **Fix mode:**
> - Address each finding listed below: {findings}.
> - For each finding, either fix it, or reject it with a doc URL proving the current text right.
> - Do not touch anything else.
>
> **Report back** (plain list, no prose):
> - what changed;
> - each rejected finding with its evidence URL;
> - each UNVERIFIED claim with its heading;
> - each source item deliberately merged away as a duplicate, naming the item kept in its place.

## Reviewer prompt (pass verbatim, filling the `{…}` fields)

> Role: adversarial reviewer. The task is to review section **{section name}** of `Study notes/CKAD appunti.md` (mode **{section | audit}**). Read `prompts/goal.md` for the scope decisions. Assume the section contains errors and try to find them. Do not edit any file. Scratch files, if needed, go only in `prompts/tmp/`.
>
> **Section mode.** Check:
> 1. **Correctness:** every command, flag, field name, path, default value and YAML block against the official docs, **online**. YAML must be valid and correctly nested.
> 2. **Completeness:** read the three source files in full (never grep alone). Every item from the sources that belongs to this section must be present, merged, or corrected. List any item lost.
> 3. **Scope rules:**
>    - no version history;
>    - no leftover OUTDATED boxes;
>    - no new topics;
>    - style kept;
>    - other sections untouched (compare the section boundaries).
> 4. **Duplicates** inside the section, and duplicates with sections already `done`.
>
> **Audit mode (final cycle).**
> - Walk every heading and every bullet of all three source files.
> - For each item, state where the item now lives in the new file, or flag the item as lost.
> - Check that the whole file renders: the CSS block is intact and every code fence is closed.
> - Check cross-section duplicates and consistency, e.g. the same command written two ways.
>
> **Report** as a list of findings, each with:
> - severity:
>   - `blocking` — factually wrong, broken YAML or command, content lost, version history, or a rule violation;
>   - `minor` — typo, wording or formatting;
> - the heading where the finding is;
> - a one-line description;
> - for correctness findings, the official doc URL that proves the finding.
>
> A finding without evidence may be reported only as `minor`. An empty list is a valid result.
