# Free CKAD Practice Resources

Verified on 2026-09-29.\
The official CKAD page listed Kubernetes v1.37 on 2026-09-30.\
Recheck the version near the exam date.

## Selection standard

Resources enter the core list only when the material is free, hands-on, inspectable, relevant to current CKAD domains, and backed by credible maintenance or authorship.\
Popularity alone is not enough.

## Core practice set

### 1. Killer Shell simulator archive, own copy

- **File:** `Study notes/Killer Shell - Exam Simulators - results.pdf`
- **Why selected:** The file is the question and answer archive of the killer.sh CKAD simulator session taken in October 2024, on Kubernetes 1.31, with 22 questions and 3 preview questions. The format is the closest to the real exam. The file holds no personal score.
- **Use:** Exam-style practice questions on the lab.
- **Caveat:** Every answer was written for Kubernetes 1.31 and is checked against v1.37 at first use. killer.sh has since moved to 17 questions per session in two variants, so the live sessions will not repeat this archive.
- **Verification:** `pdfinfo` on the file (37 pages, created 2024-12-15) and the [killer.sh CKAD page](https://killer.sh/ckad) fetched on 2026-09-29.

### 2. `dgkanatsios/CKAD-exercises`

- **Link:** [CKAD-exercises](https://github.com/dgkanatsios/CKAD-exercises)
- **Why selected:** The repository is open under the MIT licence, organised by domain, solution-oriented, widely reviewed, and its last commit is from 2026-08-18.
- **Use:** Short drills by topic on the lab, solution hidden, timed.
- **Caveat:** The README still shows the older seven-domain structure and weights. Each question is mapped to the v1.35 curriculum (the newest in cncf/curriculum on 2026-09-30) in `practice/EXERCISE_INDEX.md`, and each solution is checked against v1.37 before use. Question count: the `###` headings in the ten exercise files, counted at commit `d7b9a5c`.
- **Verification:** [Commit history](https://github.com/dgkanatsios/CKAD-exercises/commits/main/) and a clone inspected on 2026-09-29.

### 3. `bmuschko/ckad-crash-course`

- **Link:** [CKAD crash-course exercises](https://github.com/bmuschko/ckad-crash-course)
- **Why selected:** Benjamin Muschko's repository provides 32 numbered exercises, each with its own instructions and a separate solution folder, some with setup manifests. Coverage includes images, workloads, Helm, Kustomize, probes, RBAC, services, Ingress, and NetworkPolicy. The last commit is from 2026-05-19.
- **Use:** Longer scenario drills after the topic drills.
- **Caveat:** The repository has no licence file, so it is linked as a submodule and never copied. The exercises target minikube. Exercise 31 needs an Ingress controller and exercise 32 a NetworkPolicy-enforcing CNI, both covered by the lab steps in `practice/PRACTICE_PLAN.md`. Version-sensitive answers are checked against v1.37 at first use.
- **Exercise index:** [All exercises](https://github.com/bmuschko/ckad-crash-course/tree/master/exercises)

### 4. `TiPunchLabs/ckad-dojo`, pending local validation

- **Link:** [ckad-dojo](https://github.com/TiPunchLabs/ckad-dojo)
- **Why selected:** The project provides 398 questions in 20 timed simulations. Each question carries its CNCF domain, and each simulation ships setup manifests, solutions, and bash scoring functions that check cluster state with kubectl. Simulations 6 to 9 adapt `dgkanatsios/CKAD-exercises`. The licence is CC BY-NC-SA 4.0 and the last push was on 2026-09-28.
- **Use:** Practice questions with ready-made setup manifests and automatic checks, once one question has been run end to end on the lab.
- **Caveat:** The project is young, with 100 stars and 8 open issues on 2026-09-29. It needs helm and uv. docker is needed only for its local image registry, which `--skip-registry` disables, and ttyd only for its web terminal, which the plan does not use. Question quality is checked at first use.
- **Verification:** GitHub API on 2026-09-29, plus `README.md`, `exams/ckad-simulation1/` and `scripts/lib/` inspected.

### 5. killer.sh live simulator sessions

- **Link:** [killer.sh CKAD](https://killer.sh/ckad)
- **Why selected:** The simulator is the official one and comes with the exam purchase: two sessions, each 120 minutes of exam time plus 36 hours of cluster access, 17 questions each, in the variants CKAD-A and CKAD-B.
- **Use:** Agatino Pesce's own, outside this plan.
- **Verification:** killer.sh CKAD page and the Linux Foundation CKAD page, both fetched on 2026-09-29.

## Authoritative verification material

The following sources are not mock exams.\
They are the correctness baseline for checking community exercises and for building lab drills.

- [Current CKAD exam page](https://training.linuxfoundation.org/certification/certified-kubernetes-application-developer-ckad/): domains, weights, and current environment version.
- [CKAD curriculum v1.35](https://github.com/cncf/curriculum): the five domains, their weights, and the topic bullets under each.
- [Kubernetes tasks](https://kubernetes.io/docs/tasks/): official task walkthroughs for workloads, configuration, debugging, networking, and security.
- [kubectl cheat sheet](https://v1-35.docs.kubernetes.io/docs/reference/kubectl/quick-reference/): imperative commands, output formats, and productivity patterns.
- [kind quick start](https://kind.sigs.k8s.io/docs/user/quick-start/): versioned local clusters and local image loading.
- [Helm documentation](https://helm.sh/docs/): authoritative Helm command and chart reference.

## Local `kind` compatibility

Pod, Deployment, Job, CronJob, ConfigMap, Secret, RBAC, Service, probe, and rollout exercises run on a bare kind cluster.

Ingress, metrics, dynamic storage, and NetworkPolicy exercises need the add-ons and the checks listed under "Environment steps" in `practice/PRACTICE_PLAN.md`.

## Deliberately outside the core list

- Killercoda: on 2026-09-29 the [Killercoda CKAD page](https://killercoda.com/ckad) lists the Killer Shell CKAD Scenario Course as included in the paid course membership, and two community scenario sets by Chad M. Crowell and Omkar Shelke. The scenarios run only in the browser, so no attempt on them can be graded on the lab or recorded in the ledger. They stay an optional extra.
- Udemy and marketplace simulators without inspectable questions, maintenance history, or independent validation.
- Exam dumps or material claiming to reproduce real exam questions.
- Large "awesome" lists that aggregate links without quality control.
- AWS-heavy lab platforms when a resource cannot transfer cleanly to the local kind workflow.

## Next review

Recheck the exam version on the Linux Foundation page from time to time before the exam.
