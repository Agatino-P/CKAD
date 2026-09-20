# Free CKAD Practice Resources

Verified on 2026-09-20. The official CKAD environment was Kubernetes v1.35 on that date. Recheck the version near the exam date.

## Selection standard

Resources enter the core list only when the material is free, hands-on, inspectable, relevant to current CKAD domains, and backed by credible maintenance or authorship. Popularity alone is not enough.

## Core practice set

### 1. Killercoda — Killer Shell scenarios

- **Link:** [Killercoda: Killer Shell](https://killercoda.com/killer-shell)
- **Why selected:** The Killer Shell team maintains disposable browser-based Kubernetes scenarios with solutions. The platform is useful for quick, repeatable topic drills.
- **Best use:** Learn a topic interactively, then repeat the same task without hints on the local `kind` cluster.
- **Caveat:** Free individual scenarios and paid Scenario Courses are different products. The free tier excludes Courses.
- **Verification:** [Platform comparison](https://killercoda.com/killer-shell) · [pricing](https://killercoda.com/pricing)

### 2. `dgkanatsios/CKAD-exercises`

- **Link:** [CKAD-exercises](https://github.com/dgkanatsios/CKAD-exercises)
- **Why selected:** The repository is open, domain-organised, solution-oriented, widely reviewed, and still received corrections in April 2026.
- **Best use:** Work through individual prompts on `kind`, hide the solution, and time repeated attempts.
- **Caveat:** The README still shows an older CKAD domain structure and weights. Use the exercises, but map topics to the current curriculum and verify syntax against v1.35 docs.
- **Verification:** [Commit history](https://github.com/dgkanatsios/CKAD-exercises/commits/main/)

### 3. `bmuschko/ckad-crash-course`

- **Link:** [CKAD crash-course exercises](https://github.com/bmuschko/ckad-crash-course)
- **Why selected:** Benjamin Muschko's repository provides 32 focused exercises with separate solutions. Coverage includes images, workloads, Helm, Kustomize, probes, RBAC, services, Ingress, and NetworkPolicy.
- **Best use:** Use the repository as the main structured exercise bank after basic topic drills.
- **Caveat:** The repository does not promise exact CKAD v1.35 alignment. Verify version-sensitive answers, and install required `kind` add-ons for cluster-dependent exercises.
- **Exercise index:** [All exercises](https://github.com/bmuschko/ckad-crash-course/tree/master/exercises)

## Authoritative verification material

The following sources are not mock exams. The sources are the correctness baseline for checking community exercises and building later `kind` drills.

- [Current CKAD exam page](https://training.linuxfoundation.org/certification/certified-kubernetes-application-developer-ckad/) — domains, weights, and current environment version.
- [Kubernetes v1.35 tasks](https://v1-35.docs.kubernetes.io/docs/tasks/) — official task walkthroughs for workloads, configuration, debugging, networking, and security.
- [kubectl cheat sheet](https://v1-35.docs.kubernetes.io/docs/reference/kubectl/quick-reference/) — imperative commands, output formats, and productivity patterns.
- [kind quick start](https://kind.sigs.k8s.io/docs/user/quick-start/) — versioned local clusters and local image loading.
- [Helm documentation](https://helm.sh/docs/) — authoritative Helm command and chart reference.

## Local `kind` compatibility

Most Pod, Deployment, Job, CronJob, ConfigMap, Secret, RBAC, Service, probe, and rollout exercises can run directly on `kind`.

Ingress, metrics, dynamic storage, and NetworkPolicy exercises may need extra components. The later study plan should define one reproducible CKAD lab cluster instead of adding components ad hoc.

## Practice-to-notes workflow

The notes are a selective personal recall aid, not a complete CKAD guide. Review the existing notes first; afterward, use practice tests to identify knowledge, recall, speed, or environment gaps and record only concise, useful findings.

## Deliberately outside the core list

- Udemy and marketplace simulators without inspectable questions, maintenance history, or independent validation.
- Exam dumps or material claiming to reproduce real exam questions.
- Large “awesome” lists that aggregate links without quality control.
- New self-scoring projects such as [`ckad-dojo`](https://github.com/TiPunchLabs/ckad-dojo) until local validation confirms question quality, scoring accuracy, and v1.35 behavior.
- AWS-heavy lab platforms when a resource cannot transfer cleanly to the planned local `kind` workflow.

## Next review

After User reviews the existing notes, verify the CKAD exam version and locally test the selected repositories against the chosen `kind` node image.
