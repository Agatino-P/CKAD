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

- In the exam they really don't want to load the image onto a registry, leaking exam info.

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

* Removal is refused if a container (running or stopped) uses the image.
* `-f` with a tag only removes the tag; the image itself stays.
* `-f` with the image ID deletes the image if only stopped containers use it; if a running container uses it, removal is refused even with `-f`: stop and remove the container first.
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

 * To be able to push it to a remote repository, you need to add the name of the repository to the beginning of the tag. And the exam gives you the name of the repository, just don't push it on the registry (e.g. dockerhub)
 * if you push to docker hub and use docker, you don't need to prefix the repository with `docker.io/`, but with other tools or other registries, you need it.

## Understanding Jobs and CronJobs

<mark>Exam: if you get a question asking to make sure that a pod runs through to successful completion, it might look like a 'Pod question' but it's a 'Job question', asking to wrap a pod in a Job</mark>

Structure of the yaml file, with increasing indentation

- CronJob section with "attributes" creates the Job against the given schedule
  - Job Template section with "attributes" in charge of running the Pods
    - Pod Template section with "attributes" makes sure that the container can run on K8s
      - Container section with "attributes" runs the App

Each outer creates the inner: Cronjob -> Job -> Pod -> Container

### Jobs

* Jobs are about running a specific number of pods all the way through to completion.
* If needed, Pods can be run in parallel, a given number at a time.
* Jobs are managed by the Job Controller in the control plane that manages them through successful completion.
* Jobs can offer intelligence (e.g.: Restart the Pod, Retries, Kill long-running, Clean-up).
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
`"0 2 4 * *"` runs at 02:00 on day 4 of every month  
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
* Init containers run one at a time, in the order that you list them.
  * A regular init container must complete successfully before the next one starts.
  * A sidecar (an init container with `restartPolicy: Always`) keeps running; the next one starts as soon as the sidecar has started.
* Normal containers start only after all regular init containers have completed and all sidecars have started.

### List all containers within pod

* Quick trick `kubectl logs <pod-name>` on a multi-container pod picks the first container and prints `Defaulted container "<name>" out of: <list of all containers>`. (The message does not appear if the pod has the annotation `kubectl.kubernetes.io/default-container`.)

* `kubectl get pods <podname> -o yaml` and check name and ready status of each container.

## Volumes

* Without volumes, containers write to their own temporary filesystem on the node they're running on: the files are lost when the container crashes or is restarted.
* This creates problems in case of node down or moving pods to another node.
* Typically, on prem clusters use on-prem storage, and cloud clusters use cloud storage.
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
<!-- REORDER: the Volumes headings (Storage classes (SC), PV, PVC, Storage Classes) need reordering; to be decided with User, see prompts/status.md 1.9 -->

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
* `--port` is optional too: without it, the port is copied from the exposed resource. If the containers declare no `ports`, expose fails with "couldn't find port via --port flag or introspection": pass `--port` explicitly.
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

# Application Observability and Maintenance

## Understanding API Deprecations

### Admission controllers

* Is involved after authentication and authorization but before persisting (mutating admission controllers run first, then validating ones).
* Can reject a request (e.g.: PVC asking for too much storage) and or mutate a request
* Can block requests to create, delete and modify objects, and custom verbs (e.g. a request to connect to a Pod via an API server proxy)
* Cannot block requests to read (get, watch, list)
* Can enforce security policies
* Can block insecure images from running
* The admission controllers are compiled into the kube-apiserver binary, and may only be configured by the cluster administrator
* Not necessarily all compiled admission controllers are enabled

#### Examples

##### LimitRanger

* Applies default Pod memory/cpu requests and limits for a namespace, to the containers that don't set them.
* You set a `LimitRange` for a namespace, which is then enforced by the `LimitRanger` admission controller.
* A Pod that violates a `LimitRange` constraint (e.g. above the max) is rejected (`403 Forbidden`).
* The defaults are not checked for consistency: a Pod that sets a request higher than the `LimitRange` default limit, without setting a limit, fails (request must be less than or equal to the limit). It works if you also specify a limit value for that Pod inside the yaml.

##### PersistentVolumeClaimResize

* By default prevents resizing of all claims, unless the claim storage class enables it by setting the `allowVolumeExpansion` property to `true`

##### NamespaceAutoProvision

Examines requests on namespaced resources, creates the namespace if it does not exist

#### Where are these configured

* Stored in `/etc/kubernetes/manifests/kube-apiserver.yaml` (kubeadm clusters, on the control plane node)
* It's the static Pod running the api-server; the flag is in the container command:
```yaml
#...
spec:
  containers:
  - command:
    - kube-apiserver
    - --....
    - --enable-admission-plugins=NamespaceAutoProvision,another-plugin,...
    #...
```

* You need to sudo to be able to `cat` this

* To access it in Docker Desktop:
  * `docker run -it --privileged --pid=host debian nsenter -t 1 -m -u -n -i sh`
  * `cd /etc/kubernetes/manifests`
  * `vi kube-apiserver.yaml`

#### View admission controller plugins for kube-apiserver

* `kubectl describe pod kube-apiserver -n kube-system` (`describe` also matches a name prefix)
* `kubectl describe pod kube-apiserver -n kube-system | grep enable-admission-plugins`
* This shows only the plugins enabled with the flag, in addition to the default enabled ones.
* Do a `k get pods -n kube-system` first to confirm the name of the apiserver pod: the static Pod name is suffixed with the node name (e.g. `kube-apiserver-cl1-control-plane`)
* `KUBE_EDITOR=nano k edit pod kube-apiserver-cl1-control-plane -n kube-system` opens the Pod, but this is a mirror Pod of a static Pod: it is visible on the API server but cannot be controlled from there. Change the manifest file instead.

#### Using `kube-apiserver`

* You can invoke the `kube-apiserver` executable inside the `kube-apiserver` pod in the `kube-system` namespace.
* `kube-apiserver -h` gives information about the options available.
* `kube-apiserver -h | grep enable-admission-plugins` shows the admission plugins enabled by default.
* `k config set-context --current --namespace=kube-system`
* `k get pods` to get the api-server pod
* `k exec -it kube-apiserver-docker-desktop -- kube-apiserver -h` executes `kube-apiserver -h` inside the container. The double dashes end the `kubectl` command and start the command given to the container.
* `k exec -it kube-apiserver-master -- sh` fails: the kube-apiserver image is distroless (built on the `go-runner` image) and has no shell. Run the binary directly as above.

#### Modify admission controllers settings

* The flags are given to `kube-apiserver` when it starts:

`kube-apiserver --enable-admission-plugins=<plugin1>,<plugin2>`
or
`kube-apiserver --disable-admission-plugins=<plugin1>,<plugin2>`

* To change them on the running cluster, edit `/etc/kubernetes/manifests/kube-apiserver.yaml` on the control plane node. The kubelet watches that directory and recreates the static Pod by itself: no `kubectl apply` needed.
* The api-server Pod might need a moment to come back online
* Better make a copy (`cp`) of the file first, but put the copy outside `/etc/kubernetes/manifests` (e.g. in `/tmp`): the kubelet reads every file not starting with a dot in that directory, whatever the extension, so a `kube-apiserver.yaml.backup` there would be read as a second Pod.

#### K8s version

`k version -o yaml` major.minor.patch as usual
* GA is for General availability = release
* Otherwise `v<number>alpha<alpha number>` or `v<number>beta<beta number>`, e.g.: `coordination.k8s.io/v1alpha2`

#### ApiGroups

* List the resources, their group and versions by `k api-resources`

* note that `v1` is the api version of that specific group

##### Core Group 

* When there's no group name the resource is in the Core Group (also called legacy group), REST path `/api/v1`

* apiVersion: v1 (no group name)
* e.g.: pods

##### Named Groups

* apiVersion: batch/v1, REST path `/apis/<group>/<version>`
* e.g.: cron jobs

#### View api resources

* `k api-resources --sort-by=name` (can sort by `name` or `kind`)
* `k api-resources --api-group=rbac.authorization.k8s.io`

#### View Api Group for a given resource

* `k explain deploy`
* GROUP: apps  
  KIND: Deployment  
  VERSION: v1

* Gives kind, version and group. No group (no `GROUP:` line) means Core group
* KIND: ConfigMap  
  VERSION: v1

#### Enabling alpha versions

* Alpha versions are not enabled by default.
* They are enabled with the option `--runtime-config=<group>/<version>` of kube-apiserver (in `/etc/kubernetes/manifests/kube-apiserver.yaml`), e.g. `--runtime-config=coordination.k8s.io/v1alpha2`
* The group/version must exist in that Kubernetes release (check the API reference for the release): an unknown one (e.g. `batch/v2alpha1`) makes kube-apiserver fail to start with `group version ... that has not been registered`.
* The same option in that file also lists the alpha versions that are enabled.

#### Order of versions

* Alpha. E.g: `v1alpha3`
* Beta. E.g: `v1beta2`
* Stable. E.g: `v2` //Also called GA General availability

##### Removal of API elements

* It can happen only with a version increment of the API group
* API Objects must round trip between API versions without information loss. Go from v1 to v2 to v1, and the v1 object is identical: a field added in v2 needs an equivalent field in v1, or is represented as an annotation. Anyhow the system must be able to handle it.
* GA is basically forever: may be deprecated, but not removed within a major version.
* Beta: deprecated no more than 9 months or 3 minor releases (whichever is longer) after introduction, and no longer served 9 months or 3 minor releases (whichever is longer) after deprecation.
* Alpha: may be removed in any release without prior deprecation notice.

#### All Versions

* `kubectl api-versions`
* `kubectl api-versions | grep autoscaling`

* All versions for a given resource:
  * Find the API group for the resource (e.g., Deployments use `apps`).  
  `kubectl api-resources | grep deployment`
  * List all available versions for that specific API group.  
  `kubectl api-versions | grep <api-group>/`  
  `kubectl api-versions | grep apps/`

#### Preferred version for an API group

* e.g.: for certificates
* First you have to call `kubectl proxy --port=8001 &` (8001 is the default port)
* `&` so that it stays in the background until later you kill it: find the PID with `ps -a | grep kubectl` and `kill <pid>`. In the exam context, not having multiple terminals, running the proxy in the background lets you run the `curl` commands below in the same terminal.
* Then `curl localhost:8001/apis/certificates.k8s.io`
* preferredVersion is in the payload

* `curl localhost:8001/apis/batch`
* `curl localhost:8001/apis/`

## Implementing Probes and Health Checks

### Probe definition

* A Probe is a diagnostic performed periodically by the kubelet on a container. Somehow like a health check.

* Probes are configured at the container level: `spec.containers[].<probeType>` in a Pod, `spec.template.spec.containers[].<probeType>` in a Deployment.

### Types of Probes

* Three purposes: Readiness, Liveness and Startup
* Liveness and Readiness probes run independently and in parallel (the liveness probe doesn't wait for the readiness probe to succeed), unless a Startup probe is defined to delay their execution.

#### Readiness Probe

* Determines if the container completed initialization and is therefore able to receive traffic.
* **Failure action:** the Pod's IP address is removed from the EndpointSlices of all matching Services, and the Pod's `Ready` condition is set to `false`. It does **not** restart the container.

```yaml
spec:
  containers:
  - name: app
    readinessProbe:
      tcpSocket:
        port: 8080
      initialDelaySeconds: 15 # default is 0
      periodSeconds: 10       # default is 10
```

#### Liveness Probe

* Determines if the container is healthy and running as expected, not trapped in a dead state.
* **Failure action:** the `kubelet` kills the container, and the container is subjected to the Pod's `restartPolicy`.

```yaml
spec:
  containers:
  - name: app
    livenessProbe:
      exec:
        command:
        - cat 
        - /tmp/healthy
      initialDelaySeconds: 2 # Time to wait before the first probe, to let the container start (default 0)
      timeoutSeconds: 3      # default is 1
      periodSeconds: 5       # Frequency of execution (default 10)
      failureThreshold: 1    # Consecutive failures that make the probe failed (default 3). Number of allowed failures is failureThreshold -1
```

#### Startup Probe

* Startup is meant for containers with a long or unpredictable time to start, so that we don't start checking if it's healthy before it starts up.
* Disables both Liveness and Readiness probes until the Startup probe succeeds.
* **Failure action:** the `kubelet` kills the container, and the container is subjected to the Pod's `restartPolicy`.

### Restart Policy

* Defaults to Always, can be overwritten if needed (`Always`, `OnFailure`, `Never`). In a Deployment's Pod template, `Always` is the only allowed value.

* Failure of the Startup or Liveness probe causes the container to be killed and restarted according to the restart policy (the Pod is not recreated). Failure of the Readiness probe does not restart anything.

### Probe Types (mechanisms)

Each probe defines exactly one of these four mechanisms.

#### ExecActions (`exec`)

* Execute an action inside the container. Check for a file, run a command... success on exit 0

#### TCPSocketAction (`tcpSocket`)

* Just tcp check against the Pod's IP address on a specified port: success if the port is open (a connection can be established)

#### HTTPGetAction (`httpGet`)

* HTTP GET request against the Pod's IP address on a port and path: success if the status code is at least 200 and less than 400

#### gRPC (`grpc`)

* Native gRPC health check: success if the `status` of the response is `SERVING`

### Probes results

Only three types of result:

* Success: the container passed the diagnostic
* Failure: the container failed the diagnostic (triggers the probe's failure action). A probe that times out (`timeoutSeconds`) counts as a failure.
* Unknown: the diagnostic itself failed; no action is taken, and the kubelet will make further checks

## Using Provided Tools to Monitor Kubernetes Applications

### Options
- Web UI Dashboard (deprecated and archived, no longer maintained; the Kubernetes docs suggest Headlamp for new installations)
- Metrics Server
- kube-state-metrics
- Prometheus (even with alerts)
- Grafana
- etc..

### Metrics Server

* Metrics Server collects resource metrics from Kubelets and exposes them in Kubernetes apiserver through Metrics API for use by Horizontal Pod Autoscaler and Vertical Pod Autoscaler. 
* Metrics API can also be accessed by `kubectl top`, making it easier to debug autoscaling pipelines.
* Metrics Server is meant only for autoscaling purposes.
* For example, don't use it to forward metrics to monitoring solutions, or as a source of monitoring solution metrics. 
* In such cases please collect metrics from Kubelet `/metrics/resource` endpoint directly.

#### Installing Metrics Server

* Where it's not installed by default, like Docker Desktop
* Just follow the instructions of the metrics-server repository: `kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml`
* Check prerequisites (e.g. the Kubelet certificate must be signed by the cluster Certificate Authority)
* Note that the command to be added is not on the command line but inside the yaml: e.g. `--kubelet-insecure-tls` (skip verifying the Kubelet certificates, for testing purposes only) goes in the args of the metrics-server container

#### How Metrics Server works

* On each node there's a `kubelet` who gets input from `cAdvisor` (who gets it from `Container Runtimes, such as containerd`) and from pod data.
* Kubelet is the communication mechanism between a node and the control plane.
* Metrics Server gets input from kubelets via the kubelet `/metrics/resource` endpoint.
* Kubectl can then connect to the Api Server, which serves the `Metrics Api` provided by Metrics Server.
* Note that metrics are not updated in real time, there's a delay (Metrics Server collects metrics every 15 seconds)
 
#### Verifying that Metrics Server is installed

* Easiest way is to look for all pods in kube-system namespace and grep for metrics-server: `k get pods -n kube-system | grep metrics-server`

#### kubectl top to interrogate Metrics Server

* `k top nodes` gives resources usage (CPU and Memory)
* `k top pods`

## Utilizing Container Logs

### Container logs

* `k logs <pod-name>`
* `k logs <pod-name> -c <container-name>` //for multi-container pods
* `k logs deployment/<deployment-name>`
* `k logs -p <pod-name>` //previous (`--previous`). Logs of the previous instance of a restarted container, see below
* `k logs -f <pod-name>` //follow. streams the logs to the console 
* `k logs --tail=20 <pod-name>` //last 20 log lines
* `k logs --since=10s <pod-name>` //or 2m or 1h
* `k logs -l app=backend --all-containers=true` //logs from all containers in the pods matching the label

#### terminated containers' logs that you could access with -p

Retrieves logs for a **restarted container** (e.g., during a `CrashLoopBackOff`). It does not retrieve logs for just any terminated pod.

* **When to use `-p`:** a pod is running or crashing, and the `kubelet` restarted its container. Use `-p` to fetch the logs of that *dead instance* to see why it crashed. By default, if a container restarts, the kubelet keeps one terminated container with its logs.
* **Completed Pods (no `-p` needed):** if a pod finishes its task (like a Job) but the pod object *still exists* in the cluster, standard `k logs <pod-name>` works.
* **Evicted or Deleted Pods:** if a pod is evicted from the node, or removed with `kubectl delete pod`, all corresponding containers are also removed, along with their logs. Neither standard `k logs` nor `-p` can retrieve them.
* The kubelet makes logs available to clients via a special feature of the Kubernetes API.

## Debugging Kubernetes
 
### Get events `kubectl get events`

* For a pod `k describe pod <pod-name>` (Events section at the end)
* For a namespace `k get events`
* For all namespaces `k get events --all-namespaces`

### `kubectl debug`

Create an ephemeral debug container and even make a copy of a pod adding some debug utilities for debugging purposes.

* Ephemeral container in the running pod: `kubectl debug -it <pod-name> --image=busybox:1.28 --target=<container-name>`

* Copy of the pod with a new debug container added:  
`kubectl debug <failed-but-existing-podname> -it --image=<image-name> --copy-to=<name-of-the-new-pod>`

* Copy of the pod changing an existing container: if `--container` names a container of the pod, that container is changed in the copy (image set by `--image`, command set after `--`) instead of a new container being added:  
`kubectl debug <failed-but-existing-podname> -it --image=<image-name> --copy-to=<name-of-the-new-pod> --container=<container-we-need-to-debug> -- sh`
