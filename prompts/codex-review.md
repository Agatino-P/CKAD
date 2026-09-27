# Codex review loop — CKAD appunti

All paths are relative to the repository root (`git rev-parse --show-toplevel`).

A second adversarial pass over `Study notes/CKAD appunti.md`, run after the rebuild described in `prompts/goal.md`. The scope decisions in `prompts/goal.md` still apply. Progress lives in `prompts/status.md`, exactly as in `prompts/loop.md`.

## Differences from `prompts/loop.md`

- **Reviewer:** the Codex CLI with model `gpt-5.6-sol`, one fresh non-interactive run per review (command below), instead of a subagent.
- **Scope:** wrong content and missing content only. Cosmetic findings (typos, wording, formatting, style, duplicates, ordering) are out of scope.
- **No writer subagent.** Claude (the orchestrator) verifies every Codex finding itself (docs online, or experiments on the local cluster/Docker), then:
  - applies a confirmed finding directly to the notes;
  - rejects an unconfirmed or nitpicking finding with a reason, and records the rejection in `prompts/status.md` as a `disputed` open point; the reason is passed to the next Codex round for that section.
- Same state machine and limit: a section is `done` when a Codex round reports no findings Claude accepts; after round 3 the section is `done` or `done-with-open-points`. Row 7 (final audit) runs Codex in audit mode on the whole file after sections 0–6 finish.
- Sections may be reviewed in parallel (one Codex run per section; each uses its own scratch namespace `codex-review-s<N>`).
- Commit per finished section and push per main section and after the audit, as in `prompts/loop.md`.

## Running a review

Scratch files go in `prompts/tmp/` (gitignored). Build the prompt from the template below, save it as `prompts/tmp/codex_s<N>_r<round>.prompt`, then run:

```
codex exec -m gpt-5.6-sol -s workspace-write \
  -c sandbox_workspace_write.network_access=true -c web_search=live \
  --ephemeral -o prompts/tmp/codex_s<N>_r<round>.out - \
  < prompts/tmp/codex_s<N>_r<round>.prompt > prompts/tmp/codex_s<N>_r<round>.out.log 2>&1
```

- `network_access=true` lets Codex fetch docs and reach the cluster with `kubectl`; `web_search=live` enables the web search tool.
- A run that stops with "You've hit your usage limit" does not count as a round: rerun the same prompt after the reset time printed in the log.
- After each run, `git status` must show no change made by Codex outside `prompts/tmp/`.

## Reviewer prompt template

Fill `{SECTION}` (e.g. `3 Application Observability and Maintenance`), `{MODE}` (`section` or `audit`), `{MAPPING}` (the section's source mapping from `prompts/status.md`), `{NS}` (`codex-review-s<N>`), `{AUDIT_EXTRA}` (empty in section mode; in audit mode: walk every heading and bullet of the three sources and state where each item lives now, or flag it as lost) and `{REJECTED}` (the section's `disputed` points from `prompts/status.md`, with the reason, or `none`; optionally also a short list of fixes applied in earlier rounds, to verify).

> Role: adversarial reviewer. The task is to review section **{SECTION}** of `Study notes/CKAD appunti.md` (mode **{MODE}**). Read `prompts/goal.md` for the scope decisions. Assume the section contains errors and try to find them. Do not edit any file. Scratch files, if needed, go only in `prompts/tmp/` with the prefix `codex_`.
>
> Focus ONLY on two kinds of problems. Ignore everything cosmetic (typos, wording, formatting, heading levels, style, duplicates, ordering).
> 1. **Wrong content:** a command, flag, field name, path, default value, behaviour claim or YAML block that is factually wrong or broken. Verify against the official docs **online** (Kubernetes docs for the CKAD version in the audit header; official Docker, Podman, Helm, Linux Foundation docs). A live cluster is reachable with `kubectl` (read-only experiments in a scratch namespace named `{NS}` are allowed; delete what is created) and `docker`/`jq` may be available locally; experiments count as evidence.
> 2. **Missing content:** read the three source files in full (never grep alone): `Study notes/backup/CKAD appunti.md` (base), `Study notes/backup/CKAD 2 appunti.md`, `Study notes/backup/CKAD 3 appunti.md`. Every item from the sources that belongs to this section must be present in the new file (merged or corrected). An item correctly moved to another section is NOT missing; check the whole new file before flagging. An item dropped because the source was wrong is fine only if the corrected version is present.
> Section source mapping: {MAPPING}
>
> {AUDIT_EXTRA}
>
> **Report** as a numbered list of findings. Each finding has:
> - kind: `wrong` or `missing`;
> - the heading in the new file (for `missing`: the source file + heading + the lost text quoted);
> - a one-line description, and the proposed correct text;
> - evidence: the official doc URL (with the relevant quote) or the exact experiment command and output.
> Report only findings with evidence. An empty list is a valid result: write "No findings." in that case. Do not repeat findings listed below as already rejected unless there is new evidence.
> Previously rejected findings for this section (with Claude's evidence): {REJECTED}
