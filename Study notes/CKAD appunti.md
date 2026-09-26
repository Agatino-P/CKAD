<style>
mark{
  background-color: lightgrey;
  color: black;
  font-weight: bold;
}
body {
  counter-reset: h1;
}

h1 {
  font-size: 1.5em;
  font-weight: bold;
  counter-reset: h2;
}

h2 {
  font-size: 1.4em;
  font-weight: bold;
  counter-reset: h3;
}

h3 {
  font-size: 1.3em;
  font-style: italic;
  counter-reset: h4;
  margin-left: 1em;
}

h4 {
  font-size: 1.2em;
  font-style: italic;
  counter-reset: h5;
  margin-left: 1em;
}

h5 {
  font-size: 1.1em;
  font-style: italic;
  counter-reset: h6;
  margin-left: 1em;
}

h6 {
  font-size: 1em;
  font-style: italic;
  margin-left: 1em;
}

h1:before {
  counter-increment: h1;
  content: counter(h1) ". "
}

h2:before {
  counter-increment: h2;
  content: " " counter(h1) "." counter(h2) ". "
}

h3:before {
  counter-increment: h3;
  content: counter(h1) "." counter(h2) "." counter(h3) ". "
}

h4:before {
  counter-increment: h4;
  content: counter(h1) "." counter(h2) "." counter(h3) "." counter(h4) ". "
}

h5:before {
  counter-increment: h5;
  content: counter(h1) "." counter(h2) "." counter(h3) "." counter(h4) "." counter(h5) ". "
}

h6:before {
  counter-increment: h6;
  content: counter(h1) "." counter(h2) "." counter(h3) "." counter(h4) "." counter(h5) "." counter(h6) ". "
}

</style>

> **AUDIT BASELINE — 2026-09-26**
> CKAD currently uses Kubernetes v1.35; recheck near exam day because the exam environment is aligned with the newest Kubernetes minor release within approximately 4 to 8 weeks of that release.
> Ref: [CKAD FAQ](https://docs.linuxfoundation.org/tc-docs/certification/faq-cka-ckad-cks) · [v1.35 docs](https://v1-35.docs.kubernetes.io/docs/)

# Application Design and Build

## Define, Build, and Modify Container Images

### Image Management - OCI Images

<mark> Exam: Open Container Initiative (OCI) images . Is the format of containers images we use </mark> 

* Docker, Buildah or Podman are all build tools that create an OCI Image from a Dockerfile (Podman and Buildah also accept the name `Containerfile`). FYI other ways exist that don't use a Dockerfile (even Buildah can build an image with its own commands, without a Dockerfile).

- They need in a Dockerfile: 
  - Reference to base Image
  - Apps and dependencies (nugets, or packages in general)
  - Commands to install dependencies (e.g.: `dotnet build`, which also runs `dotnet restore` implicitly)
  - Config (ports to expose etc)
  - Command to run the app

- In the exam they really don't want to load the image onto a registry, leaking exam info. <!-- UNVERIFIED: see prompts/status.md -->

<mark>Exam: Dockerfiles are needed to be known for the exam </mark>

<mark>Exam: You might be tested on dumping this OCI image as a tar file or zipping it up. </mark>

### Docker 

##### Help

It is always allowed to use `--help`

#### Building and tagging

`docker image build -t <image_name> .`

* However, there is a structure to the name of an image. 
* A full image name (image reference) has the following structure:

`[HOST[:PORT]/]NAMESPACE/REPOSITORY[:TAG]`

  * HOST: The optional registry hostname where the image is located.  
    If no host is specified, Docker Hub (`docker.io`) is used by default.  
  * PORT: The optional registry port number, if necessary (for example `:5000`)  
  * NAMESPACE: optional, usually a user's or organization's name.  
    If no namespace is specified, `library` is used, which is the namespace for Docker Official Images.
  * REPOSITORY: required, identifies the specific image.
  * TAG: A custom, human-readable identifier.  
    Typically used to identify different versions or variants of an image.  
    If no tag is specified, `latest` is used by default

Example: `example.com:5000/team/my-app:2.0` → host `example.com`, port `5000`, namespace `team`, repository `my-app`, tag `2.0`  
Example: `alpine` → `docker.io/library/alpine:latest`

Multiple tags are allowed  
If you run a `docker image ls`, all the tags that point to the same image show the same `IMAGE ID`  

[full tag specifications](https://docs.docker.com/reference/cli/docker/image/tag/)

#### Create an image from a running container, which might have differences from the image it's based on

* Not very common or recommended
* The new image contains the container's file changes, but not the data in mounted volumes.

`docker commit <container-name> <image-name>` (alias of `docker container commit`)

#### Renaming or retagging images

```sh
docker image tag <old-name> <new-name>
docker image tag ckad:docker apesce/ckad:docker
```

doesn't remove the old image name, and you can find two image names with the same id in `docker image ls`

#### Pulling an image

`docker image pull <image_name>[:<image_tag>]` or   
`docker pull <image_name>[:<image_tag>]`

#### Listing Images

`docker image ls`

#### Remove an image

`docker image rm <image-name>`

* Removal is refused if a container (running or stopped) uses the image; `-f` forces the removal.
* If the image has more than one tag, `docker image rm <name>:<tag>` only removes that tag; the image is deleted when its last tag is removed.
* More than one image can be removed at once: `docker image rm <image1> <image2>`

#### Dump an image as a tar file

`docker image save -o <file>.tar <image>[:<tag>]` (alias: `docker save`)
`docker save -o ckad.tar ckad:latest` → writes `ckad.tar` containing all layers + metadata

* Docker has **no `--format` flag** on `save`. Docker always writes one kind of tar, and `docker load` can read that tar back.
* The tar Docker writes is **OCI-compliant**: the tar has `oci-layout`, `index.json` and `blobs/`, plus the legacy `manifest.json` for older tools.
* `-o` / `--output` writes to a file. Without `-o`, Docker writes the tar to stdout, so the output can be piped:
  `docker save ckad:pluralsight | gzip > ckad-image.tar.gz`
  (the result is a gzip file, not a zip, so the extension is `.tar.gz`; `docker load -i ckad-image.tar.gz` reads the gzip directly — gzip, bzip2, xz and zstd are all accepted)
* `--platform os[/arch[/variant]]` saves only the given platform of a multi-platform image:
  `docker save --platform linux/amd64 -o ckad-amd64.tar ckad:latest`
* Several images can go into one tar: `docker save -o all.tar ckad:latest nginx:1.27`

**Podman** is the tool where the format is chosen explicitly:

`podman save --format <docker-archive|oci-archive|oci-dir|docker-dir> -o <file> <image>`
`podman save --format oci-archive -o ckad.tar ckad:latest` → OCI archive

* Podman's default is `docker-archive`, so `--format oci-archive` is required when an OCI archive is asked for.

<mark>Exam: if the task asks for an OCI-format archive, check which tool the task says to use.
 With Podman → add `--format oci-archive`. With Docker → plain `docker save -o` already produces an OCI-compliant tar.</mark>

Ref: [Docker save](https://docs.docker.com/reference/cli/docker/image/save/) · [Docker load](https://docs.docker.com/reference/cli/docker/image/load/) · [Podman save](https://docs.podman.io/en/stable/markdown/podman-save.1.html)

#### Fixing image names for pushing 

 * To be able to push it to a remote repository, you need to add the name of the repository to the beginning of the tag. And the exam gives you the name of the repository, just don't push it on the registry (e.g. dockerhub) <!-- UNVERIFIED: see prompts/status.md -->
 * if you push to docker hub and use docker, you don't need to prefix the repository with `docker.io/` (Docker's default host). For any other registry, the registry host (and port, if needed) must be in the name. Other tools may need the `docker.io/` prefix even for Docker Hub. <!-- UNVERIFIED: see prompts/status.md -->

## Understanding Jobs and CronJobs

<mark>Exam: if you get a question asking to make sure that a pod runs through to successful completion, it might look like a 'Pod question' but it's a 'Job question', asking to wrap a pod in a Job</mark>

Structure of the yaml file, with increasing indentation

- CronJob section with "attributes" creates the Job against the given schedule
  - Job Template section with "attributes" in charge of running the Pods
    - Pod Template section with "attributes" makes sure that the container can run on K8s
      - Container section with "attributes" runs the App

Each outer creates the inner: Cronjob -> Job -> Pod -> Container

### Jobs

* Jobs are about running a specific number of pods all the way through to completion. And if needed Pods can be run in parallel, a given number at a time.
* Jobs are managed by the Job Controller in the control plane that manages them through successful completion.
* Jobs can offer intelligence (e.g.: Restart the Pod, Retries, Kill long-running, Clean-up).
* Jobs can create multiple Pods and even run them in parallel.
* Deleting the Job also deletes the Pods it created.

#### Yaml 

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: pi
spec:
  activeDeadlineSeconds: 10     # Max number of seconds the Job may run. When reached, its running Pods are terminated and the Job is marked Failed (reason: DeadlineExceeded). Takes precedence over backoffLimit
  ttlSecondsAfterFinished: 120  # TTL mechanism: deletes the finished Job (Complete or Failed) this many seconds after it finishes
  parallelism: 1
  completions: 5
  backoffLimit: 4               # Max retries before the Job is marked Failed (default 6); retries use an exponential back-off delay (10s, 20s, 40s ...) capped at six minutes
  template:
    spec:
      restartPolicy: Never      # It's useful for debugging because you can see the logs of failing pods.
      containers:
      - name: ctr
        image: alpine:latest
        command: ["echo",  "simplest pod ever"]
```

* a command that runs for longer

`['sh', '-c', 'echo "this will be slow" && sleep 60']`

* A yaml multi line commands

```yaml
command: ["/bin/sh"]
args: 
  - "-c"
  - |
    while true; do echo hello; sleep 10; done
    echo "this will never happen of course!"
    echo "here's some more text" && \
        _c="chocolate chip"; printf "here's a %s cookie" "$_c"
```

### Cronjobs

* Cron strings "* * * * *" meaning 

1) minute
2) hour
3) Day of the month
4) Month
5) Day of the week

`"* * * * *"` runs every minute  
`"0 2 4 * *"` runs at 2:00 every 4th day of the month  
`"*/2 * * * *"` runs every two minutes

* TimeZone

Without `.spec.timeZone`, the schedule is interpreted in the local time zone of the kube-controller-manager.  
Set `.spec.timeZone` to a valid time zone name to fix it, for example `timeZone: "Etc/UTC"`.

Ref: [CronJob time zones](https://v1-35.docs.kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/#time-zones)

#### Cronjob Controller 

Checks things every ten seconds, and checks how many scheduled jobs were missed since the last scheduled time (see Missed jobs below).  
Creates the Jobs and then lets the Job controller take over the management of their Pods

##### Job creation

A CronJob creates a Job object approximately once per execution time of its schedule.  
The scheduling is approximate because there are certain circumstances where two Jobs might be created, or no Job might be created.  
Kubernetes tries to avoid those situations, but does not completely prevent them. Therefore, the Jobs that you define should be idempotent.

* Deadline for delayed Job start `startingDeadlineSeconds`
The .spec.startingDeadlineSeconds field is optional. This field defines a deadline (in whole seconds) for starting the Job, if that Job misses its scheduled time for any reason.

 If you set it to less than 10 seconds, then the CronJob may not be scheduled, because the controller checks every 10 seconds. 

##### Missed jobs

For every CronJob, the controller counts the schedules missed from the last scheduled time until now. If there are more than 100 missed schedules, it does not start the Job and logs the error.

It is important to note that if the startingDeadlineSeconds field is set (not nil), the controller counts how many missed Jobs occurred from the value of startingDeadlineSeconds until now rather than from the last scheduled time until now. For example, if startingDeadlineSeconds is 200, the controller counts how many missed Jobs occurred in the last 200 seconds.

A CronJob is counted as missed if it has failed to be created at its scheduled time. For example, if concurrencyPolicy is set to Forbid and a CronJob was attempted to be scheduled when there was a previous schedule still running, then it would count as missed.

For example, suppose a CronJob is set to schedule a new Job every one minute beginning at 08:30:00, and its startingDeadlineSeconds field is not set. If the CronJob controller happens to be down from 08:29:00 to 10:21:00, the Job will not start as the number of missed Jobs which missed their schedule is greater than 100.

To illustrate this concept further, suppose a CronJob is set to schedule a new Job every one minute beginning at 08:30:00, and its startingDeadlineSeconds is set to 200 seconds. If the CronJob controller happens to be down for the same period as the previous example (08:29:00 to 10:21:00,) the Job will still start at 10:22:00. This happens as the controller now checks how many missed schedules happened in the last 200 seconds (i.e., 3 missed schedules), rather than from the last scheduled time until now.

* `concurrencyPolicy`

It governs whether new jobs will start if previous instances are still running. So it can be any of Allow, which is the default, and Forbid, and Replace.

* `successfulJobsHistoryLimit`
 
 How many successful finished jobs (and their pods) to keep around from previous runs. It defaults to 3. 
 
* `failedJobsHistoryLimit`, that's the same, only this time it's for failed jobs, and this one defaults to 1
 
* only `spec.schedule` and `spec.jobTemplate` are required. All of the rest, totally optional
   
## Multi container pods

* Used when a container needs some more logic to better integrate with the environment. (e.g. istio service mesh )

### Sidecar pattern

* Main container and sidecar
* Kubernetes-native sidecars are declared in `initContainers` with `restartPolicy: Always`: they start before the app containers and keep running for the whole life of the Pod.
* A sidecar does not stop a Job's Pod from completing once the main container has finished.
* Containers listed together in `containers:` (no `restartPolicy`) still work as a multi-container Pod, but without control over which container starts or stops first.

```yaml
spec:
  containers:
  - name: myapp
    image: alpine:latest
    command: ['sh', '-c', 'while true; do echo "logging" >> /opt/logs.txt; sleep 1; done']
    volumeMounts:
    - name: data
      mountPath: /opt
  initContainers:
  - name: logshipper
    image: alpine:latest
    restartPolicy: Always       # makes this init container a sidecar
    command: ['sh', '-c', 'tail -F /opt/logs.txt']
    volumeMounts:
    - name: data
      mountPath: /opt
  volumes:
  - name: data
    emptyDir: {}
```

Ref: [Sidecar containers](https://v1-35.docs.kubernetes.io/docs/concepts/workloads/pods/sidecar-containers/)

#### Ambassador pattern

* This is part of the generic sidecar pattern 
* The sidecar container runs alongside the app container for as long as the pod runs
* As an example the ambassador can act as localhost proxy to a remote db, so that the app can talk to localhost port, isolated from remote DB concerns

#### Adapter pattern

* A variation of the sidecar pattern
* As an example can translate the app logging into the format accepted by the specific environment.

### Init pattern 

* for activities that are needed only at startup. As an example the FrontEnd has to wait for the backEnd to start, that logic can go into an init container
* `initContainers:` inside the `spec:` section of the yaml file.
* Init containers run one at a time, in the order that you list them; each must complete successfully before the next one starts.
* Normal containers start only after all the init containers have completed

### List all containers within pod

* Quick trick `kubectl logs <pod-name>` on a multi-container pod picks the first container and prints `Defaulted container "<name>" out of: <list of all containers>`. (The message does not appear if the pod has the annotation `kubectl.kubernetes.io/default-container`.)

* `kubectl get pods <podname> -o yaml` and check name and ready status of each container.

## Volumes

* Without volumes, containers write to their own temporary filesystem on the node they're running on: the files are lost when the container crashes or is restarted.
* This creates problems in case of node down or moving pods to another node.
* Typically, on prem clusters use on-prem storage, and cloud clusters use cloud storage. <!-- UNVERIFIED: see prompts/status.md -->
* You need the specific driver for a given type of storage to make it available to K8s.
* Storage systems can be external to K8s, like EMC (on-prem) or AWS Elastic Block Store or Azure File.
* Storage plugins (CSI drivers) run their node part as pods managed by a DaemonSet. This makes sure they run on every node. 
  `kubectl get pods -n kube-system` often shows these pods (and more); the namespace depends on the driver

* Volumes are exposed to K8s that can be used by apps.
* As the storage is external to K8s, it can be visible to all nodes, regardless on what node it is.

* Pod -> Persistent Volume Claim (PVC) -> Storage Class (SC)  
  The PVC names a StorageClass; storage is then dynamically provisioned as a Persistent Volume (PV), bound to the PVC, and mounted into the pod.

### Storage classes (SC)

`kubectl get sc`

#### Reclaim policy

Tells the cluster what to do with a PV after its PVC is deleted (the volume is "released" from its claim).

* `Delete` deletes the PV object and the associated storage asset in the external infrastructure. Default for PVs dynamically created by a StorageClass.

* `Retain` keeps the PV (status "released", not available to another claim) and its data, for manual reclamation.

#### VolumeBindingMode

* `Immediate` (the default) binds and provisions the volume as soon as the PVC is created. This poses the risk that the volume gets created in a place (zone) without knowledge of the pod's scheduling requirements, and the pod then can't be scheduled on a node that has access to that volume.  
This can happen if a single cluster spans several zones or regions.

* `WaitForFirstConsumer` delays binding and provisioning until a Pod using the PVC is created, so the volume is created according to the pod's scheduling constraints (e.g. in the same zone or region of the pod).  
if we create a PVC referring a WaitForFirstConsumer SC, it will stay pending until a pod uses it.

### Persistent Volumes (PV) 

Are not referenced directly by the pod: `containers[].volumeMounts[].name` refers to an entry in `spec.volumes[]`, which refers to the PVC, and the PVC is bound to the PV

### Persistent Volume Claims (PVC)

Are referred inside the pod in `spec.volumes[].persistentVolumeClaim.claimName`. The PVC must be in the same namespace as the pod.

### Storage Classes 

* The normal pattern is to use a StorageClass to define a class of storage with all of the features that you want from the back‑end system.
* Then, when you deploy your Pods, you reference a PersistentVolumeClaim that makes a reference to the class.
* Storage on the back end then gets dynamically provisioned and attached to the Pod: when the PVC is created (`Immediate`) or when the Pod using it is created (`WaitForFirstConsumer`).

### Ephemeral Volumes   

 * Ephemeral volumes are specified inline in the Pod spec, which simplifies application deployment and management.
