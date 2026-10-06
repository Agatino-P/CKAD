# Study plan

Topics studied outside the exercise loop, when a practice miss shows a gap worth a lesson.\
Each topic is split into bites, taught one at a time as the interactive-teaching guideline describes.\
The lessons are condensed in `practice/study/LESSONS.md`.\
Gotchas go to `Study notes/CKAD cheat sheet.md`.

## Running commands with args in Docker and K8s

Opened on 2026-10-05 after exercise DGK-A-17 in `practice/RESULTS_LEDGER.md`.\
When every bite is checked, the lesson moves into `Study notes/CKAD appunti.md` under this title, as Agatino Pesce asked.\
Agatino Pesce asked for: passing a command with several arguments on the `kubectl run` command line, when to use `args`, when a multi-line script, and when `sh -c` is needed.

| Bite | Content | State |
| --- | --- | --- |
| a | Docker images: the process is `ENTRYPOINT` words + `CMD` words, and words after the image name in `docker run` take the place of the `CMD` words. | checked |
| b | Pods: `command` replaces `ENTRYPOINT`, `args` replaces `CMD`. | checked |
| c | One list element is one word of the process, and `sh -c` takes one element as its script. | checked |
| d | `kubectl run ... -- words`: the words become `args`, or `command` with `--command`. | checked |
| e | Quoting: the local shell splits the words, so one quoted string becomes one list element. | checked |
| f | When a shell is needed: `;`, `&&`, pipes, redirection, `$VAR` and loops. | checked |
| g | Writing it in YAML: flow list, block list, and a `- \|` multi-line script. | checked |
| h | `$(VAR)` expanded by Kubernetes versus `$VAR` expanded by a shell. | checked |
| i | `--rm` on `kubectl run`, and why it needs `-i` or `-it`. | taught |
