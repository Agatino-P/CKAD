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

- A typical app Dockerfile contains (only the `FROM` base image line is strictly required): 
  - Reference to base Image
  - Apps and dependencies (nugets, or packages in general)
  - Commands to install dependencies (e.g.: `dotnet build`, which also runs `dotnet restore` implicitly)
  - Config (ports to expose etc)
  - Command to run the app

- In the exam they really don't want to load the image onto a registry, leaking exam info.

<mark>Exam: Dockerfiles are needed to be known for the exam </mark>

<mark>Exam: You might be tested on dumping this OCI image as a tar file or zipping it up. </mark>

### Docker 

#### Help

It is always allowed to use `--help`

#### Building and tagging

`docker image build -t <image_name> .`

* However, there is a structure to the name of an image. 
* A full image name (image reference) has the following structure:

`[HOST[:PORT]/][NAMESPACE/]REPOSITORY[:TAG]`

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

* By tag, when the image has other tags: only that tag is removed, even while a container uses the image.
* By its last tag, with no container using the image: the tag and the image are removed.
* Without `-f`, removing the last tag or removing by ID is refused while a container (running or stopped) uses the image.
* By last tag with `-f`, when a container uses the image: only the tag is removed; the image stays, shown as `<none>` by `docker image ls -a` (not by plain `docker image ls`).
* By image ID: refused without `-f` if the image has more than one tag. With `-f`, all its tags are removed and the image is deleted, unless a running container uses it: then removal is refused even with `-f` ("cannot be forced"); stop and remove the container first.
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
* Jobs can offer intelligence (e.g.: Retries, Kill long-running, Clean-up). On failure, with `restartPolicy: Never` the Job controller creates a replacement Pod; with `restartPolicy: OnFailure` the kubelet restarts the failed container inside the same Pod.
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
  The PVC names a StorageClass (or, if it names none, gets the cluster's default StorageClass, when one exists); storage is then dynamically provisioned as a Persistent Volume (PV), bound to the PVC, and mounted into the pod.  
  This is dynamic provisioning. With static provisioning, an administrator creates the PV in advance and the PVC binds to it: Pod -> PVC -> PV.

### Storage Classes 

* The normal pattern is to use a StorageClass to define a class of storage with all of the features that you want from the back‑end system.
* Then, when you deploy your Pods, you reference a PersistentVolumeClaim that makes a reference to the class.
* Storage on the back end then gets dynamically provisioned and bound to the PVC: when the PVC is created (`Immediate`) or when a Pod using it is scheduled (`WaitForFirstConsumer`). The volume is mounted into the Pod when the Pod runs.

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
* Modify a deployment from the command line (for example if you created it without a yaml): `kubectl edit deploy/<deploy-name>` opens the deployment in the configured editor (see "Change the editor for K8s commands edit" in General Knowledge)

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

* a public service (e.g. Load Balancer, or node port) that directs traffic from an externally used port to blue or green pods via a selector with the following (a LoadBalancer Service can expose e.g. port 443 externally; a NodePort Service is reached from outside at `<NodeIP>:<nodePort>`, with `nodePort` in the node port range, default 30000-32767)

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

### Deployment updates and change-cause

* **Triggering a revision:** a rollout, and with it a new revision, is triggered only when the Pod template (`spec.template`) changes, for example its labels or container images. Other updates, such as scaling, do not trigger a rollout.
* **Where history lives:** the revision history is stored in the ReplicaSets the Deployment controls (the current one and the old ones); `revisionHistoryLimit` sets how many old ReplicaSets are kept.
* **Recording changes:** annotate the Deployment to fill the `CHANGE-CAUSE` column of the rollout history (the `--record` flag is deprecated). The annotation is copied to the revision when the revision is created.

`kubectl annotate deployment <deployment-name> kubernetes.io/change-cause="Change details" --overwrite`

* `--overwrite` is needed when the annotation already exists; without it the command fails.

### Rollout status

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
  Searches Artifact Hub (the default hub), which lists charts from many repositories; a traditional chart repository found there can then be added locally with `helm repo add`. A chart hosted in an OCI registry is not added as a repository: use its `oci://` reference directly, e.g. `helm install <release-name> oci://<registry>/<path>/<chart>`.

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
  - Shows only the latest stable version of each chart (`--devel` includes pre-release versions: alpha, beta, rc); to see all versions use `--versions`.
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

* `helm upgrade <release-name> <repo/chart>`  
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
* The flag lists only the plugins enabled on top of the defaults; the default plugins do not appear here (see "Using `kube-apiserver`").
* Do a `k get pods -n kube-system` first to confirm the name of the apiserver pod: the static Pod name is suffixed with the node name (e.g. `kube-apiserver-cl1-control-plane`)
* `KUBE_EDITOR=nano k edit pod kube-apiserver-cl1-control-plane -n kube-system` opens the Pod, but this is a mirror Pod of a static Pod: it is visible on the API server but cannot be controlled from there. Change the manifest file instead.

#### Using `kube-apiserver`

* You can invoke the `kube-apiserver` executable inside the `kube-apiserver` pod in the `kube-system` namespace.
* `kube-apiserver -h` gives information about the options available.
* `kube-apiserver -h | grep enable-admission-plugins` prints two lines: the `--enable-admission-plugins` line lists the plugins enabled by default; the deprecated `--admission-control` line lists every plugin.
* `k config set-context --current --namespace=kube-system`
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
* Stable (GA) versions: `v<number>`, e.g. `v1`
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
* Stable, also called GA (General Availability) = release. E.g: `v2`

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
  * These are the versions of the whole group: a given version may not serve that resource. Check a version for the resource with `kubectl explain <resource> --api-version=<group>/<version>` (it fails with `couldn't find resource` if that version does not serve it)  
  `kubectl explain deployments --api-version=apps/v1`

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

* A failed liveness or startup probe makes the kubelet kill the container, which is then restarted according to the restart policy; the Pod is not recreated. A failed readiness probe does not restart anything: the container is marked not ready and the Pod is removed from the Services' endpoints.

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

* On each node there's a `kubelet` that collects Pod and container usage statistics with its embedded `cAdvisor` (for the containers started by the container runtime, such as containerd). Only with the alpha feature gate `PodAndContainerStatsFromCRI` enabled (off by default) does the kubelet get them from the runtime through the Container Runtime Interface (CRI) instead.
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

# Application Environment, Configuration and Security

## Discover and use resources that extend kubernetes

### Defining custom resources and operators

* A resource is an endpoint in the Kubernetes API that stores a collection of API objects of a certain kind (e.g. the built-in `pods` resource contains a collection of Pod objects).

#### Custom resources

* A custom resource is a way to extend k8s by creating new object types.
* Once installed, custom resources are served by the Kubernetes API itself, at a new API endpoint: their objects are created and accessed with `kubectl`, just like built-in resources (e.g. `kubectl get applications`).

##### Custom resource definitions

* Custom resource definitions, or CRDs, are how we define the custom resources that we can then use either with operators or as a method of grouping or clustering like objects.

```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: applications.example.com # must be <names.plural>.<group>, i.e. the plural name and the group below
spec:
  group: example.com
  scope: Namespaced  # or Cluster
  names:
    plural: applications # this has to match with beginning of metadata.name above
    singular: application
    kind: Application
    shortNames:
    - app
  versions:
  - name: v1
    served: true  # served=true means the version is enabled (served via the REST API)
    storage: true # storage=true means this is the version used when the objects are persisted (stored in etcd)
    # you can serve more than one version, but one and only one must be set to storage=true
    schema:
      openAPIV3Schema:
        type: object
        properties:
          spec:
            type: object
            properties:
              frontend:
                type: object 
                properties:
                  image:
                    type: string
                  replicas:
                    type: integer
              # ... backend: 
              
```              

* Note that the schema is indented: each field goes under the `properties:` of its parent. A field placed at the wrong level (e.g. `replicas:` next to `properties:` instead of under it) makes `kubectl apply` fail with `strict decoding error: unknown field`.

* Note that just because we called the properties image and replicas k8s is not going to spin up an application with this image and replicas. Telling k8s what to do with these properties is the job of an operator set up and installed, associated with this custom resource.

* To create such an object of this kind we'd have a yaml file (let's call it for example app.yaml) similar to this:

```yaml
apiVersion: example.com/v1 # group and version from previous one
kind: Application # names.kind from previous one
metadata:
  name: my-app
spec: 
  frontend:
    image: nginx:latest
    replicas: 2
```

#### Operators

* Custom resources are used with operators, i.e. custom controllers that watch those resources and perform activities (e.g. create, update) defined by what we write in their code. Code can be Go, Python, and more.
* The Operator works using the principle of control loop and functions as a controller.
* The operator will monitor our custom resources. And then based on the information it gathers from these custom resources, it will then bring that information into the operator code, and the operator can then take action on an object (not necessarily the one that was being monitored) or otherwise, depending on what its code tells.

<mark>Custom resources definition is in scope for the exam, writing operators is not</mark>

## Understand Authentication, Authorization and Admission Control

### RBAC Role-Based Access Control

#### Role

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: default
  name: pod-reader
rules:
- apiGroups: [""] # "" indicates the core API group
  resources: ["pods"]
  verbs: ["get", "watch", "list"]
```

* A Role always sets permissions within a particular namespace.
* When you create a Role, you have to specify the namespace it belongs in.

#### ClusterRole

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  # "namespace" omitted since ClusterRoles are not namespaced
  name: secret-reader
rules:
- apiGroups: [""]
  #
  # at the HTTP level, the name of the resource for accessing Secret
  # objects is "secrets"
  resources: ["secrets"]
  verbs: ["get", "watch", "list"]
```

* A ClusterRole can be used to grant the same permissions as a Role.
* Because ClusterRoles are cluster-scoped, you can also use them to grant access to:
  - cluster-scoped resources (like nodes)
  - non-resource endpoints (like /healthz)
  - namespaced resources (like Pods), across all namespaces

#### RoleBinding / ClusterRoleBinding

```yaml
# This role binding allows "jane" to read pods in the "default" namespace.
# You need to already have a Role named "pod-reader" in that namespace.
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding    # a ClusterRoleBinding has no metadata.namespace and its roleRef.kind can only be ClusterRole
metadata:
  name: read-pods
  namespace: default
subjects:            # You can specify more than one "subject"
- kind: User         # User, Group or ServiceAccount
  name: jane         # "name" is case sensitive
  apiGroup: rbac.authorization.k8s.io
roleRef:             # "roleRef" specifies the binding to a Role / ClusterRole
  kind: Role         # Role or ClusterRole
  name: pod-reader   # this must match the name of the Role or ClusterRole you wish to bind to
  apiGroup: rbac.authorization.k8s.io
```

* After you create a binding, you cannot change the Role or ClusterRole that it refers to.  
  If you try to change a binding's roleRef, you get a validation error (`cannot change roleRef`). 

### ABAC Attribute-Based Access Control

* Out of scope for the exam
* To enable ABAC mode, specify `--authorization-policy-file=SOME_FILENAME` and `--authorization-mode=ABAC` on startup (of kube-apiserver).
* The file format is one JSON object per line. There should be no enclosing list or map, only one map per line. Each line is a "policy object".

### Admission Controllers
 
#### Mutating Controllers

* E.G.: The `DefaultStorageClass` mutating admission controller observes the creation of PersistentVolumeClaims that do not request any specific storage class, and adds the default storage class to them.

#### Checking if an admission controller is enabled

On the control plane node, `ps -ef | grep kube-apiserver` shows the running kube-apiserver command line with its flags (e.g. `--enable-admission-plugins=...`), but where the flags are set actually depends on the specific k8s configuration.
  * `-e` selects all processes (identical to `-A`) 
  * `-f` provides a full-format listing for each process (and prints the command arguments).
  
Note: without `-e`/`-A`, ps only selects the processes with the same effective user ID as the current user and associated with the same terminal. Think of `-A` like "absolutely everything". 
On a related note `-a` is different: it selects all processes except both session leaders and processes not associated with a terminal.

<mark>For the exam the recommended way is looking into `/etc/kubernetes/manifests/kube-apiserver.yaml`</mark>

### EventRateLimit controller 

* An example of admission controller that uses configuration is `EventRateLimit` (alpha, disabled by default) which controls how many event requests can reach the Kubernetes API.  
  Once the controller is enabled, it needs some configuration to know what to stop: the configuration file is referenced from the file given to the kube-apiserver flag `--admission-control-config-file`.

```yaml
apiVersion: eventratelimit.admission.k8s.io/v1alpha1
kind: Configuration
limits:
  - type: Namespace
    qps: 50
    burst: 100
    cacheSize: 2000
  - type: User
    qps: 10
    burst: 50
```

## Understand and Define Resource Requirements, Limits and Quotas

### Resource Requests and Limits

* Requests and limits are usually set for each container of a `Pod`; the Pod's request/limit for a resource is then the sum of its app containers' requests/limits (init and sidecar containers and Pod overhead change the calculation: see [sidecar resource sharing](https://v1-35.docs.kubernetes.io/docs/concepts/workloads/pods/sidecar-containers/#resource-sharing-within-containers)).
* They can also be set for the whole Pod in `spec.resources` (cpu, memory, hugepages; feature gate `PodLevelResources`, beta and enabled by default): see [Pod-level resource specification](https://v1-35.docs.kubernetes.io/docs/concepts/configuration/manage-resources-containers/#pod-level-resource-specification).

* In the Pod yaml template there are 
  * `spec.containers[].resources.limits.cpu`
  * `spec.containers[].resources.limits.memory`
  * `spec.containers[].resources.limits.hugepages-<size>`
  * `spec.containers[].resources.requests.cpu`
  * `spec.containers[].resources.requests.memory`
  * `spec.containers[].resources.requests.hugepages-<size>`

* Requests must be less than or equal to limits, otherwise the pod won't deploy (`must be less than or equal to cpu limit`)

* `requests` are what the kube-scheduler uses to decide which node to place the Pod on; the kubelet also reserves at least the request amount for that container. A container can use more than its request if the node has it available.

* The CPU limit defines a hard ceiling on how much CPU time that the container can use. During each scheduling interval (time slice), the Linux kernel checks to see if this limit is exceeded; if so, the kernel waits before allowing that cgroup to resume execution.

* The CPU request typically defines a weighting. If several different containers (cgroups) want to run on a contended system, workloads with larger CPU requests are allocated more CPU time than workloads with small requests.

* If a container exceeds its memory request and the node that it runs on becomes short of memory overall, it is likely that the Pod the container belongs to will be evicted.

* A container might or might not be allowed to exceed its CPU limit for extended periods of time. However, container runtimes don't terminate Pods or containers for excessive CPU usage.

### Resource Quotas

* Quotas set limitations on the `namespace` level 

* Quotas can limit not only resource but also can limit the amount of any kind of object created, like number of pods.

* `ResourceQuota` is an admission controller enabled by default in kube-apiserver. A quota is enforced in a namespace when there is a ResourceQuota in that namespace.

* You define ResourceQuotas via a `kind: ResourceQuota` yaml file, inside which there is `metadata.namespace` to assign it to a namespace

* `spec.hard` section has requests, limits, number of pods

* `spec.scopes` it's a tricky topic, better refer to docs, but know it exists
  * Each quota can have an associated set of scopes. 
  * A quota will only measure usage for a resource if it matches the intersection of enumerated scopes.

## Understanding ConfigMaps

* ConfigMaps should not contain secrets
* The values under `data` in a ConfigMap can only be strings (binary data goes under `binaryData`, base64-encoded).
* If we want a value with boolean values we need to quote the values, like "true" or "false". Same for numbers, like "100". Unquoted, the ConfigMap is rejected (`cannot unmarshal bool into Go struct field ConfigMap.data of type string`).

<mark>EXAM: In the exam they might try to induce into error by providing secrets and not secrets data together, you have to put them in ConfigMaps and Secrets</mark>

### Defining ConfigMaps

* `ConfigMap` is a kind
* In the yaml, the KeyValuePairs are under the `data:` section 
* Values can also be multiple lines of content
* Data cannot exceed 1 MiB

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: game-demo
data:
  # property-like keys; each key maps to a simple value
  player_initial_lives: "3"
  ui_properties_file_name: "user-interface.properties"

  # file-like keys
  game.properties: |
    enemy.types=aliens,monsters
    player.maximum-lives=5    
  user-interface.properties: |
    color.good=purple
    color.bad=yellow
    allow.textmode=true  
```

### Using ConfigMaps

* There are four different ways that you can use a ConfigMap to configure a container inside a Pod:

1. Inside a container command and args
2. Environment variables for a container
3. Add a file in read-only volume, for the application to read
4. Write code to run inside the Pod that uses the Kubernetes API to read a ConfigMap (Totally Not in scope for the exam)

* if the names that we want in the pod are different from the ones in the config map , can map them one by one

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: configmap-demo-pod
spec:
  containers:
    - name: demo
      image: alpine
      command: ["sleep", "3600"]
      args: ["$(PLAYER_INITIAL_LIVES)"] # $(VAR) expands the environment variable defined below.
                                        # args are appended to command: the container runs `sleep 3600 3`
      env:
        # Define the environment variable
        - name: PLAYER_INITIAL_LIVES # Notice that the case is different here
                                     # from the key name in the ConfigMap.
          valueFrom:
            configMapKeyRef:
              name: game-demo           # The ConfigMap this value comes from.
              key: player_initial_lives # The key to fetch.
        - name: UI_PROPERTIES_FILE_NAME
          valueFrom:
            configMapKeyRef:
              name: game-demo
              key: ui_properties_file_name
      volumeMounts:
      - name: config
        mountPath: "/config"
        readOnly: true
  volumes:
  # You set volumes at the Pod level, then mount them into containers inside that Pod
  - name: config
    configMap:
      # Provide the name of the ConfigMap you want to mount.
      name: game-demo
      # An array of keys from the ConfigMap to create as files
      items:
      - key: "game.properties"
        path: "game.properties"
      - key: "user-interface.properties"
        path: "user-interface.properties"
        
```

* if the names that we want in the pod are the same of the ones in the config map, we can load the whole config map at once

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: myconfigmap
data:
  username: k8s-admin
  access_level: "1"
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: env-configmap
spec:
  containers:
    - name: app
      command: ["/bin/sh", "-c", "printenv"]
      image: busybox:latest
      envFrom:
        - configMapRef:
            name: myconfigmap

```

* [Using ConfigMaps as files from a Pod](https://kubernetes.io/docs/concepts/configuration/configmap/#using-configmaps-as-files-from-a-pod)

To consume a ConfigMap in a volume in a Pod:

1. Create a ConfigMap or use an existing one. Multiple Pods can reference the same ConfigMap.
2. Modify your Pod definition to add a volume under `.spec.volumes[]`. Name the volume anything, and have a `.spec.volumes[].configMap.name` field set to reference your ConfigMap object.
3. Add a `.spec.containers[].volumeMounts[]` to each container that needs the ConfigMap. Specify `.spec.containers[].volumeMounts[].readOnly = true` and `.spec.containers[].volumeMounts[].mountPath` to an unused directory name where you would like the ConfigMap to appear.
4. Modify your image or command line so that the program looks for files in that directory. Each key in the ConfigMap `data` map becomes the filename under `mountPath`.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: mypod
spec:
  containers:
  - name: mypod
    image: redis
    volumeMounts:
    - name: foo
      mountPath: "/etc/foo"
      readOnly: true
  volumes:
  - name: foo
    configMap:
      name: myconfigmap
```

## Create and consume secrets

* Secrets can be mounted as data volumes or exposed as environment variables to be used by a container in a Pod. So, like ConfigMaps, you can use Secrets to configure a container inside a Pod:

1. Inside a container command and args (through an environment variable, `$(VAR)`)
2. Environment variables for a container
3. Add a file in read-only volume, for the application to read
4. Write code to run inside the Pod that uses the Kubernetes API to read a Secret (Totally Not in scope for the exam)

* Secrets are also used by the kubelet to pull container images from private registries (`imagePullSecrets`).

```yaml 
apiVersion: v1
kind: Secret
metadata:
  name: db-pass-secret
type: Opaque     # it is the default           
data:
  db-pass: dmFsdWUtMg0KDQo=   # values under data are base64-encoded; use stringData for plain text
```

<mark>Opaque works in most user supplied data, but if the task description contains keywords like TLS or Docker config, in that case check docs (types `kubernetes.io/tls`, `kubernetes.io/dockerconfigjson`)</mark>

* K8S Secrets do not do the encryption: base64 is only an encoding, and by default Secrets are stored unencrypted in etcd. Encryption at rest has to be enabled by the cluster administrator.

* Secrets are used very similarly to ConfigMaps inside Pods (`secretKeyRef` instead of `configMapKeyRef`, `secretRef` instead of `configMapRef`, and in volumes `secret.secretName` instead of `configMap.name`)

## Understand Service Accounts

* A service account is a type of non-human account that, in Kubernetes, provides a distinct identity in a Kubernetes cluster.
* Instead of passwords, ServiceAccounts use tokens.
* ServiceAccounts let our pods access the Kubernetes API.
* Application Pods, system components, and entities inside and outside the cluster can use a specific ServiceAccount's credentials to identify as that ServiceAccount.
* This identity is useful in various situations, including authenticating to the API server or implementing identity-based security policies.
* They are Namespaced: Each service account is bound to a Kubernetes namespace. 
* Every namespace gets a default ServiceAccount upon creation.

### Creating a Service Account

* Use separate namespaces to isolate access to mounted Secrets.

* via yaml

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-serviceaccount
  namespace: my-namespace
```

* imperatively

`kubectl create serviceaccount reader-service`

### Assign a ServiceAccount to a Pod

* To assign a ServiceAccount to a Pod, you set the `spec.serviceAccountName` field in the Pod specification. Kubernetes then automatically provides the credentials for that ServiceAccount to the Pod. 
* Kubernetes gets a short-lived, automatically rotating token using the TokenRequest API and mounts the token as a projected volume.

* By default, Kubernetes provides the Pod with the credentials for an assigned ServiceAccount, whether that is the default ServiceAccount or a custom ServiceAccount that you specify.

* To prevent Kubernetes from automatically injecting credentials for a specified ServiceAccount or the default ServiceAccount, set the `automountServiceAccountToken` field in your Pod specification to false.

### Using a service token

* To give the ServiceAccount RBAC permissions, bind it with a `RoleBinding` (to a `Role`, or to a `ClusterRole`, granting its permissions only in the RoleBinding's namespace) or with a `ClusterRoleBinding` (to a `ClusterRole`, cluster-wide).
* Within the RoleBinding yaml definition file the `subjects[n].kind` is defined as `ServiceAccount`, as it's not a user, together with the ServiceAccount's `namespace` (`kind: Service` is rejected: supported values are `ServiceAccount`, `User`, `Group`).

```yaml
subjects:
- kind: ServiceAccount
  name: reader-service
  namespace: default
```

### confirming that the service account got associated with a pod, use `kubectl describe pod <pod_name>`

* The output has a `Service Account:` line.

## Understand Security Contexts

* A security context defines privilege and access control settings for a Pod or Container by adding to their spec section as `spec.securityContext...` or `spec.containers[x].securityContext...`

* When setting security context for volumes (`fsGroup`), that has to go under the Pod section `spec.securityContext`, not the container one: `fsGroup` does not exist in the container `securityContext`.

* Security context settings include, but are not limited to:

  * Discretionary Access Control: Permission to access an object, like a file, is based on user ID (UID) and group ID (GID).

  * Security Enhanced Linux (SELinux): Objects are assigned security labels.

  * Running as privileged or unprivileged.

  * Linux Capabilities: Give a process some privileges, but not all the privileges of the root user.

  * AppArmor: Use program profiles to restrict the capabilities of individual programs.

  * Seccomp: Filter a process's system calls.

  * allowPrivilegeEscalation: Controls whether a process can gain more privileges than its parent process. This bool directly controls whether the no_new_privs flag gets set on the container process. 
    
    * allowPrivilegeEscalation is always true when the container:

      * is run as privileged, or
      * has CAP_SYS_ADMIN

  *  readOnlyRootFilesystem: Mounts the container's root filesystem as read-only.

```yaml 
apiVersion: v1
kind: Pod
metadata:
  name: security-context-demo
spec:
  securityContext:
    runAsUser: 1000
    runAsNonRoot: true
    runAsGroup: 3000
    fsGroup: 2000
    supplementalGroups: [4000]
  volumes:
  - name: sec-ctx-vol
    emptyDir: {}
  containers:
  - name: sec-ctx-demo
    image: busybox:1.28
    command: [ "sh", "-c", "sleep 1h" ]
    volumeMounts:
    - name: sec-ctx-vol
      mountPath: /data/demo
    securityContext:
      allowPrivilegeEscalation: false
      capabilities:
        add: ["NET_ADMIN", "SYS_TIME"]
```

* Note that the opposite of `add:` capabilities is `drop:`

# Services and Networking

## Demonstrate Basic Understanding of Network Policies

* The Pods connect to the `Pod network` created by the `Network plugin`.
* Network policies only work if your network plugin supports them: the network plugin is what enforces them.

* If you apply more than one policy to some pods, the policies do not conflict: they are additive, and the allowed traffic is the union of what the policies allow.
* Policies that you create are always allow policies, there's no way to specifically deny a particular traffic flow.

* Network policies are namespaced: a policy applies only to Pods in its own namespace. If you don't set `metadata.namespace` (or `-n`), kubectl creates the policy in the current context's namespace (`default` unless changed).
* To allow traffic from/to Pods in other namespaces, use a `namespaceSelector` under `spec.ingress[].from[]` (or `spec.egress[].to[]`). A policy cannot name a namespace directly; to select a namespace by name, match the label `kubernetes.io/metadata.name`, which the control plane sets automatically on every namespace with the namespace name as value:  
  `spec.ingress[].from[].namespaceSelector.matchLabels` with `kubernetes.io/metadata.name: <namespace-name>`  
  or `egress` / `to` of course.

* A policy applies only to Pods (selected by `spec.podSelector`), but the other end of a rule can be Pods, namespaces or IP blocks.
* `kubectl get netpol` with netpol being the short name for network policies.
* The most common way to specify Pods for a policy is via `matchLabels`
* You can also allow traffic with `ipBlock` criteria (CIDR ranges), but `ipBlock` is meant for cluster-external IPs, since Pod IPs are ephemeral and unpredictable. Cluster ingress and egress mechanisms often rewrite (NAT) the source or destination IP, and whether that happens before or after policy processing depends on the network plugin, cloud provider and Service implementation.
* The easiest way to get Pods' labels is `kubectl get pods --show-labels`

* The entities that a Pod can communicate with are identified through a combination of the following three identifiers:

  1. Other pods that are allowed (exception: a pod cannot block access to itself)
  2. Namespaces that are allowed
  3. IP blocks (exception: traffic to and from the node where a Pod is running is always allowed, regardless of the IP address of the Pod or the node)  

  When defining a pod- or namespace-based NetworkPolicy, you use a selector to specify what traffic is allowed to and from the Pod(s) that match the selector.

The example below selects namespaces by a custom label `namespace`, so the target namespaces must be labeled first:

```
kubectl label namespace frontend namespace=frontend
kubectl label namespace backend namespace=backend
```

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: egress-namespaces
spec:
  podSelector:
    matchLabels:
      app: myapp
  policyTypes:
  - Egress
  egress:
  - to:
    - namespaceSelector:
        matchExpressions:
        - key: namespace
          operator: In
          values: ["frontend", "backend"]
```

### Understanding what a policy does

`kubectl describe netpol <policy_name>`

### Pod isolation

* By default, a pod is non-isolated for egress; all outbound connections are allowed. A pod is isolated for egress if there is any NetworkPolicy that both selects the pod and has "Egress" in its policyTypes.

* By default, a pod is non-isolated for ingress; all inbound connections are allowed. A pod is isolated for ingress if there is any NetworkPolicy that both selects the pod and has "Ingress" in its policyTypes.

### Single rule versus many 

<mark>Possible exam tricky point</mark>

* Be very careful at the difference of items under `- from` or `- to`
* If an item like `namespaceSelector:` doesn't have a dash `-` it means it's not an element by itself but goes together with the previous one
* Indentation matters too: `matchLabels` must be indented under `podSelector` / `namespaceSelector`, otherwise the API server rejects the policy (`unknown field "spec.ingress[0].from[0].matchLabels"`).

Single `from` element, so `namespaceSelector` belongs to the same element as `podSelector`. Therefore allow Pods with `ckad` AND in `ps`

```yaml
- from:
  - podSelector:
      matchLabels:
        project: ckad
    namespaceSelector:
      matchLabels:
        kubernetes.io/metadata.name: ps
```

Two separate elements in the `from` array. Therefore allow Pods with `ckad` (in the policy's own namespace) OR any Pod in `ps`
```yaml
- from:
  - podSelector:
      matchLabels:
        project: ckad
  - namespaceSelector:
      matchLabels:
        kubernetes.io/metadata.name: ps
```

* Note that in `kubectl describe netpol` you will see the different elements as different `From:`
### Ingress and Egress

* Ingress is for incoming traffic
* Egress is for outgoing traffic


### Default policies

* By default, if no policies exist in a namespace, then all ingress and egress traffic is allowed to and from pods in that namespace. The following examples let you change the default behavior in that namespace.

* Making so that Default deny all ingress traffic  

Note the `podSelector: {}`  

You can create a "default" ingress isolation policy for a namespace by creating a NetworkPolicy that selects all pods but does not allow any ingress traffic to those pods.

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
spec:
  podSelector: {}
  policyTypes:
  - Ingress
```

This ensures that even pods that aren't selected by any other NetworkPolicy will still be isolated for ingress. This policy does not affect isolation for egress from any pod.

* Making so Allow all ingress traffic

If you want to allow all incoming connections to all pods in a namespace, you can create a policy that explicitly allows that.

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-all-ingress
spec:
  podSelector: {}
  ingress:
  - {}
  policyTypes:
  - Ingress
```

## Provide and Troubleshoot Access to Applications via Services

* A service is a stable network abstraction that sits in front of a set of pods
* A Service's Name and IP Address don't change while it exists (the cluster IP can change only when the `type` is changed to or from `ExternalName`; a headless Service, `clusterIP: None`, has no IP).
* The name gets automatically recorded in the cluster's internal DNS that all PODs have access to.

### ClusterIP

* It's the default type if you don't specify a `type:`
* Exposes the Service on a cluster-internal virtual IP and port (allocated from the Service IP range, not from the Pod network), therefore it is available only to other apps and pods inside the same cluster.
* Unless there are specific needs (and in that case, restrictions and risk of collision) the ip gets automatically assigned by K8S.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-clusterip-service # this gets registered in the cluster's internal DNS
spec:
  type: ClusterIP   # case-sensitive: `ClusterIp` is rejected
  selector:
    app: ckad
  ports:
    - port: 9000
      targetPort: 8080
            # By default and for convenience, the `targetPort` is set to
            # the same value as the `port` field.
 ```

 * `kubectl describe svc <service-name>`  gives also the target Pods (IP:port) under the row: `Endpoints`

### NodePort 

* Works on top of Cluster IP. It exposes the service to the outside world, via static port on all cluster nodes' IP.
* NodePorts services build their own ClusterIP services behind the scenes to build on.
* External clients can hit any cluster node on the chosen port and reach the service.
* By default the ports of a Service are TCP, and the NodePorts are allocated between 30000 and 32767.


```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  type: NodePort
  selector:
    app.kubernetes.io/name: MyApp
  ports:
    - nodePort: 30007       # Optional field
                            # By default and for convenience, the Kubernetes control plane
                            # will allocate a port from a range (default: 30000-32767)
      port: 80
      targetPort: 80        # By default and for convenience, the `targetPort` is set to
                            # the same value as the `port` field.


```

### LoadBalancer

* Integrates with cloud load-balancer: Kubernetes itself does not ship a load balancing component, the cloud provider (or another integration) provides it
* Make a service accessible via an external load balancer
* External clients can reach a service via the external load balancer. The load balancer's address appears in `.status.loadBalancer.ingress` as an IP, or as a DNS hostname for DNS-based load balancers (typically AWS).

### Exam tips

* If direct connection to Pods are causing issues, you need a service.
* If you need to connect only between Pods in the same cluster, you need a cluster IP service.
* If it has to be exposed via known port on all nodes, then it's a NodePort service.
* If you need to expose via cloud load-balancer, it's a LoadBalancer Service.
* If the service exists but it's not working, first of all check selector vs pods' labels.
* It's ok if the selector lists 2 of 3 labels on pods, but not if it lists 3 and pod has only 2 matching

### DNS

* There's a `kube-dns` Service in the kube-system namespace. The name stays `kube-dns` for compatibility, but the Pods behind the Service are normally CoreDNS Pods (label `k8s-app=kube-dns`).
* Every pod (with the default `dnsPolicy: ClusterFirst`) gets the address of the dns service injected inside its configuration, in the `/etc/resolv.conf` file as `nameserver`. Exception: a Pod with `hostNetwork: true` and `ClusterFirst` falls back to the node's DNS (policy `Default`); it needs `dnsPolicy: ClusterFirstWithHostNet` to use the cluster DNS.

## Use Ingress Rules to Expose Applications

* Ingress remains in CKAD scope, but the Ingress API is frozen: the Kubernetes project recommends Gateway API for new work. The community Ingress-NGINX controller is retired (no more releases or security fixes; existing installs keep working and the install artifacts stay available).

* Each LoadBalancer Service gets its own load balancer on the cloud, so if you need to expose more services, you need more load balancers in the cloud which means cost.

* Ingress can expose many services (referenced by name and port), each normally with its own (behind the scenes) ClusterIP.
* Ingress is only for HTTP and HTTPS
* The Ingress controller is usually exposed through a single load balancer on ports 80 and 443. Then it uses host and/or path based routing to send traffic to backend services. 

* Ingress are working via Ing Spec (defines the rules) and Ing Controller (implements the rules)
* Kubernetes doesn't ship with a native controller, one has to be installed. In the exam, it's already installed.
* Should you need one, install a maintained Ingress controller from its official install manifest or Helm chart.

`kubectl get ing` //short for ingress

### IngressClass

* It's a way to run more than one ingress controller on the same cluster.

`kubectl get ingressclass` 

* what you get here must match the `spec.ingressClassName` in the ingress definition. If `ingressClassName` is omitted, the IngressClass marked as default (annotation `ingressclass.kubernetes.io/is-default-class: "true"`) is used.
<mark>Exam important: when copying from the docs, ingressClassName must be checked/corrected</mark>

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: minimal-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /   # controller-specific: read by Ingress-NGINX (and controllers that emulate its annotations); others ignore it
spec:
  ingressClassName: nginx-example
  rules:
  - http:
      paths:
      - path: /testpath
        pathType: Prefix
        backend:
          service:
            name: test
            port:
              number: 80
```

# General Knowledge

<mark>Exam: the environment is all Linux</mark>

<mark>Exam: it's totally ok to copy paste examples from https://kubernetes.io/docs/ (the Kubernetes blog https://kubernetes.io/blog/ and the Helm docs https://helm.sh/docs/ are allowed too)</mark>

* Use spaces when you edit YAML, not tabs: YAML forbids tab characters in indentation.

## Setting alias for Kubectl

* Powershell `set-alias k kubectl`
* Linux `alias k=kubectl`

## Change the editor for K8s commands edit (memorize this)

* `KUBE_EDITOR="nano" k edit svc/<service-name>`
* `alias ke="KUBE_EDITOR='nano' kubectl"` and then `ke edit pod nginx-6cf46f5666-mbbms`
* Without `KUBE_EDITOR`, `kubectl edit` uses `EDITOR`, and falls back to `vi` on Linux.

* The keyboard combination to display the current line number whilst you are using nano is CTRL+C (nano: "Report cursor position").

## Using jq (example)

`k get deploy <deploy-name> -o json | jq '.metadata.annotations."kubernetes.io/change-cause"'`  
or  
`k get deploy <deploy-name> -o json | jq '.metadata.annotations["kubernetes.io/change-cause"]'`

* The key must be in double quotes: unquoted, `/` and `-` are read as division and subtraction, so the filter fails to compile, and `.` splits the key into a nested path (`.kubernetes.io` returns the wrong value).
* The quoted key must match exactly: a stray space, as in `." kubernetes.io/change-cause"`, silently returns `null`.

## Field selectors

* Field selectors let you select Kubernetes objects based on the value of one or more resource fields. 
* It even allows to get events for more than one "object" at once  
`kubectl get events --field-selector type=Warning --all-namespaces`
* The value is case-sensitive: the event type is `Warning` (or `Normal`); `type=warning` finds nothing.
* Supports the operators `=`, `==` (same as `=`) and `!=`
* example `kubectl get services --all-namespaces --field-selector metadata.namespace!=default`

## Running multiple terminals using tmux

https://github.com/tmux/tmux/wiki/Getting-Started

* most important Ctrl-b ? for help (lists all key bindings; Ctrl-b is the default prefix key)

## Imperatively make changes to kubeconfig

* Create a cluster entry in kubeconfig, under the `clusters` section, called test-cluster and pointing to https://127.0.0.1:52807  
`kubectl config set-cluster test-cluster --server=https://127.0.0.1:52807`
* Create a new context entry in kubeconfig called test-context pointing to a cluster called test-cluster  
`kubectl config set-context test-context --cluster=test-cluster`
* Remove the namespace property setting from the docker-desktop context  
`k config unset contexts.docker-desktop.namespace`

## K8s Context

* View current config `k config view`: for each context it also gives the namespace; if a context lists no namespace, that context uses `default`.
* View in which context we are `k config current-context`
* Change the current context (e.g. to test-context, just created above) `kubectl config use-context test-context`

## K8s Namespace (memorize this)

* Create `k create ns <namespace-name>`
* Check `k get ns`
* Set it as the namespace of the current context  
` kubectl config set-context --current --namespace=<nameOfTheNamespace> `
* ` alias kn='kubectl config set-context --current --namespace ' `
* ` kn default ` 
* Specify the namespace manually: the `-n <namespace-name>` option on the command line of each command

When not specified, not a bad idea to switch to default namespace

## Kubectl Apply vs. Kubectl Create 

* Both accept JSON and YAML formats.
* Both can work by file name or stdin

`kubectl apply` is a declarative command.

* Applies a configuration to a resource by file name or stdin. The resource name must be specified.
* This resource will be created if it doesn’t exist yet.
* If the resource already exists, this command does not fail because of that: the resource is updated. The update itself can still be rejected, e.g. when it changes an immutable field such as a Deployment's `spec.selector` (`field is immutable`).

`kubectl create` is an imperative command.

* Creates a resource from a file or from stdin.
* If the resource already exists, kubectl create will error (`AlreadyExists`).
* Create using all yaml files in current folder `k create -f ./` (only files ending in `.yaml`, `.yml` or `.json` are read)

## redeploy once you fix a yaml file (e.g. Job, Cronjob)

`kubectl apply -f <YamlFile.yaml>`

* For a Job that already exists, the Pod template (`spec.template`) is immutable: `apply` of a changed template fails with `field is immutable`. Delete and recreate the Job instead:  
`kubectl replace --force -f <YamlFile.yaml>` (deletes the Job, then creates it again)

## Create a temporary pod as an interactive TTY using image alpine and set restart to Never, named temp-pod

* The basic command is in Application Deployment. Variants:

`k run -it --restart=Never --image=alpine temp-pod -- /bin/sh`     //apk add bash and then bash, if needed, same with curl  
`k run -it mycurlpod --image=curlimages/curl --restart=Never -- sh`               //No bash  
`k run -it al --image=alpine --restart=Never -- /bin/sh`

* Flags such as `--restart=Never` go **before** `--`: everything after `--` is passed to the container as its command/args (`-- /bin/sh --restart=Never` makes `/bin/sh` fail with `bad option`, and the Pod keeps `restartPolicy: Always`).

## K8 commands

* `kubectl get jobs --watch`
* `kubectl get pods --watch`
* `kubectl get all` (`all` is a category: Pods, Services, Deployments, ReplicaSets, StatefulSets, DaemonSets, Jobs, CronJobs, HPAs, ReplicationControllers; ConfigMaps, Secrets, Ingresses etc. are not included. See the list with `kubectl api-resources --categories=all`)

## Clusters

* List the available contexts (each context points to a cluster): `kubectl config get-contexts`
* List the clusters defined in the kubeconfig: `kubectl config get-clusters`
* Verify the active cluster: `kubectl cluster-info`
