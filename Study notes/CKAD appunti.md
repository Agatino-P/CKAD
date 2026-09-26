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

# Application Deployment

## Use Kubernetes Primitives to Implement Common Deployment Strategies

### Create without yaml

As an alternative to writing yaml, `kubectl create` builds a resource directly from the command line:

`kubectl create deployment <deploy-name> --image=<image>[:tag]` (short form: `k create deploy ...`)

### Use `kubectl create` to get a deployment yaml file, to later modify

`kubectl create deployment <deploy-name> --image=<image>[:tag] --dry-run=client -o yaml > deploy.yaml`  
`kubectl create deployment nginx --image=nginx:alpine --dry-run=client -o yaml > deploy.yaml`

### Use `kubectl run` to get a pod yaml file, to later modify

* For a Pod, instead of the usual `kubectl create <resource> ... --dry-run=client -o yaml`, use `kubectl run`:

`kubectl run <pod-name> --image=<image>[:tag] --dry-run=client -o yaml > pod.yaml`  
`kubectl run nginx --image=nginx:alpine --dry-run=client -o yaml > pod.yaml`

### Create a temporary pod as an interactive TTY using image alpine and set restart to Never, named temp-pod

`kubectl run -it --restart=Never --image=alpine temp-pod`

### Imperative commands

* Scale a deployment: `kubectl scale deployment <deployment-name> --replicas=<number of pods>`
* Change the image of a container: `kubectl set image deployment/<deployment-name> <container-name>=<image>[:tag]`  
  `kubectl set image deployment/nginx nginx=nginx:1.16.1`
* Modify a deployment from the command line (for example if you created it without a yaml): `kubectl edit deploy/<deploy-name>` opens the deployment in the editor set by `KUBE_EDITOR` (or `EDITOR`; fallback `vi` on Linux)

### Imperatively changing the selector on a service

`kubectl set selector svc <svc-name> 'role=green'`

* `kubectl set selector` works only on Service objects.
* The new selector **replaces** the whole old selector: `'role=green'` alone leaves only `role: green` in `spec.selector`, and any other selector labels are gone. Pass every label needed, e.g. `'app=web,role=green'`.
* Equivalent to going inside the Service yaml, looking for `spec.selector` (a plain label map in a Service, no `matchLabels`) and changing `role: blue` to `role: green`

### Imperatively Create a service for a deployment

`kubectl expose deploy <deploy-name> --port=<desired port> --target-port=<pod's port> --type=NodePort --name=<service-desired-name>`

* `--target-port` is optional: without it, the target port is the same as `--port`. So `kubectl expose deploy <deploy-name> --port=<container-port> --type=NodePort` creates a NodePort Service whose port and target port are both the container port.
* `--port` is optional too: without it, the port is copied from the exposed resource.
* With `--type=NodePort` and no node port given, Kubernetes picks the node port from the allowed range (default 30000-32767); read it with `kubectl get svc`.

### Structure of Blue Green

* a set of pods with labels (e.g.: role) identifying them as blue, which might mean v1.0 (in addition to potentially other labels)

```yaml
spec:
  #....
  selector:
    matchLabels:
      #....
      role: blue
  template:
    metadata:
      labels:
        #....
        role: blue
#....
```

* a set of pods with labels identifying them as green, which might mean v1.1 (in addition to potentially other labels)

```yaml
spec:
  #....
  selector:
    matchLabels:
      #....
      role: green
  template:
    metadata:
      labels:
        #....
        role: green
#....
```

* a blue service (e.g. Load Balancer, or node port) that directs traffic from an internally used port (e.g.: 9000) to "blue" pods via a selector with

```yaml
spec:
  #....
  selector:
    #....
    role: blue
#...
```

* a green service (e.g. Load Balancer, or node port) that directs traffic from an internally used port (e.g.: 9001) to "green" pods via a selector with

```yaml
spec:
  #....
  selector:
    #....
    role: green
#...
```

* a public service (e.g. Load Balancer, or node port) that directs traffic from an externally used port (e.g.: 443) to blue or green pods via a selector with

```yaml
spec:
  #....
  selector:
    #....
    role: green # or role: blue
#...
```

* And we'd swap to which group of pods the public service directs traffic by changing its selector only

## Understand Deployments and How to Perform Rolling Updates

### spec: properties

```yaml
spec:
  minReadySeconds: 1           # Seconds a new Pod must be ready, without any container crashing, to be considered available (default 0)
  progressDeadlineSeconds: 60  # Seconds to wait for progress before reporting the Deployment as failed progressing (default 600); must be greater than minReadySeconds
  revisionHistoryLimit: 5      # Number of old ReplicaSets to retain to allow rollback (default 10)
```

### spec.strategy: properties

```yaml
strategy:
   type: RollingUpdate   # RollingUpdate (default) or Recreate, which kills all existing Pods before new ones are created
   rollingUpdate:
     maxSurge: 1         # Max Pods that can be created over the desired replicas count. Absolute number or percentage. Default 25%
     maxUnavailable: 1   # Max Pods that can be unavailable during the update. Absolute number or percentage. Default 25%
```

* `maxSurge` and `maxUnavailable` cannot both be 0.

### Saving the configuration during a deployment

`kubectl create -f file.deployment.yml --save-config`

* Saves the configuration of the object in its annotations (`kubectl.kubernetes.io/last-applied-configuration`), so that `kubectl apply` can be used on the object later.
* `--save-config` does not create rollout history (see below).

### Deployment updates and rollout history

* **Triggering a revision:** a rollout, and with it a new revision, is triggered only when the Pod template (`spec.template`) changes, for example its labels or container images. Other updates, such as scaling, do not trigger a rollout.
* **Where history lives:** the revision history is stored in the old ReplicaSets that the Deployment keeps (how many: `revisionHistoryLimit`).
* **Recording changes:** annotate the Deployment to fill the `CHANGE-CAUSE` column of the rollout history (the `--record` flag is deprecated). The annotation is copied to the revision when the revision is created.

`kubectl annotate deployment <deployment-name> kubernetes.io/change-cause="Change details" --overwrite`

* `--overwrite` is needed when the annotation already exists; without it the command fails.

### Get information about a Deployment

* Check the current rollout status (watches the latest rollout until it is done):

`kubectl rollout status deployment/<deployment-name>`  
`kubectl rollout status -f file.deployment.yml`

### Rollout history

* View all revisions:

`kubectl rollout history deployment/<deployment-name>`

* Get information about a specific Deployment revision:

`kubectl rollout history deployment/<deployment-name> --revision=2`

### Rollback a Deployment

* Rollback to the immediately previous revision:

`kubectl rollout undo deployment/<deployment-name>`  
`kubectl rollout undo -f file.deployment.yml`

* Rollback to a specific revision:

`kubectl rollout undo deployment/<deployment-name> --to-revision=2`  
`kubectl rollout undo -f file.deployment.yml --to-revision=2`

## Use the Helm Package Manager to Deploy Existing Packages

### Concepts

* Chart - A Helm package: bundle of the resource definitions used to create an instance of a Kubernetes application.

* Config - Configuration information (a set of values, typically from a `values.yaml` file) that Helm merges with a chart to create a release.

* Release - Running instance of a chart (combined with a config) inside K8s. If you install the same chart twice, you get two releases, each with its own release name.

* Library - A library chart defines chart primitives or definitions, sort of "functions" or short "blocks", that can be shared by the templates of multiple charts.

* Repository - The place where charts are collected and shared: repos have charts.

* Hub (defaults to Artifact Hub) - Hubs give repository info: Artifact Hub lists charts from many repositories.

### Helm commands

* `helm -h`  
  `-h` also works with subcommands (e.g. `helm search repo -h`)

* `helm search hub`  
  Searches Artifact Hub (the default hub), which lists charts from many repositories; a repository found there can then be added locally with `helm repo add`.

- `helm search hub` options  
  - `--list-repo-url` option gives you the chart repository's full URL but is hard to read in table format.  
  - Table format is the default but you can do `-o yaml` or `-o json`.  
  - You find the chart version and the app version (in simple case it looks like the image version).

* `helm repo add <repo_name_you_chose> <repo_url_from_search>`  
  Adds a repo to your local client

* `helm repo list`  
  Lists the repos added to your local client

* `helm repo update`  
  Updates all the locally added repos. `helm repo update <repo-name>` updates only the given repo.

* `helm search repo` / `helm search repo <chart>`
  - Searches the repositories that you have added to your local helm client (with `helm repo add`).
  - This search is done over local data, no public network needed.
  - Each chart is identified as `<repo_local_name>/<chart_name>`.
  - Shows only the newest version of each chart; to see all versions use `--versions`.
  - To search for a version (a semantic versioning constraint): `helm search repo <chart-name> --version=<version-number>`
  - To see all the options: `helm search repo --help`

* `helm show values <repo/chart>`  
  To know what values can be overridden in the chart

* `helm pull <repo/chart> --untar`
  - As some charts have a lot of values, it can be useful to have the chart "unzipped" to a folder, to check the different files (values or whatever else).
  - Note that `helm pull` doesn't actually install the chart.

* Values
  - Supplying values overrides the defaults of the chart (e.g.: admin user & password).
  - Values are supplied at `helm install` or `helm upgrade` time, either via a file (`-f` / `--values <file>`) or with `--set` (e.g. `--set name=value`).

* `helm install <name_you_chose> <repo/chart>`  
  This name is used for deploy (and therefore pods) and svc. At least in my test with bitnami/nginx.  
  It also shows up when you do `helm list`

* `helm upgrade`  
  When doing upgrade, typically to a next version, you can also override some values

* `helm status <release-name>`  
  Shows the state of a release

* `helm list`  
  Lists releases (installations), in the current namespace unless one is specified

* `helm uninstall <release-name>`  
  Removes the release from the cluster
