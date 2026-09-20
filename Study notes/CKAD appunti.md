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
  counter-increment: h4;
  content: counter(h1) "." counter(h2) "." counter(h3) "." counter(h4) ". " counter(h5) ". "
}

h6:before {
  counter-increment: h4;
  content: counter(h1) "." counter(h2) "." counter(h3) "." counter(h4) ". " counter(h5) ". " counter(h6) ". "
}

</style>

> **AUDIT BASELINE — 2026-09-20**
> CKAD currently uses Kubernetes v1.35; recheck near exam day because the environment follows Kubernetes releases.
> Ref: [CKAD FAQ](https://docs.linuxfoundation.org/tc-docs/certification/faq-cka-ckad-cks) · [v1.35 docs](https://v1-35.docs.kubernetes.io/docs/)
  
# Application Design and Build

## Define, Build, and Modify Container Images

### Image Management - OCI Images

<mark> Exam: Open Container Initiative (OCI) images . Is the format of containers images we use </mark> 

* Docker, Buildah or Podman are all build tools that create an OCI Image from a Dockerfile. FYI other exist that don't use dockerfile (even Buildah can).

- They need in a Dockerfile: 
  - Reference to base Image
  - Apps and dependencies (nugets, or packages in general)
  - Commands to install dependencies (e.g.: dotnet build which does also restore)
  - Config (ports to expose etc)
  - Command to run the app

- In the exam they really don't want to load the image onto a registry, leaking exam info.

<mark>Exam: Dockerfiles are needed to be known for the exam </mark>

<mark>Exam: You might be tested on dumping this OCI image as a tar file or zipping it up. </mark>

### Docker 

##### Help

Is always allowed to use `--help`

#### Building and tagging

`docker image build -t <image_name> .`

* However, there is a structure to the name of an image. 
* A full image name has the following structure:

`[HOST[:PORT_NUMBER]/]PATH[:TAG]`

  * HOST: The optional registry hostname where the image is located.  
    If no host is specified, Docker's public registry at docker.io is used by default.  
  * PORT_NUMBER: The registry port number if a hostname is provided  
  * PATH: The path of the image, consisting of slash-separated components.  
    For Docker Hub, the format follows [NAMESPACE/]REPOSITORY  
    * NAMESPACE is either a user's or organization's name.  
      If no namespace is specified, library is used, which is the namespace for Docker Official Images.
  * TAG: A custom, human-readable identifier.  
    Typically used to identify different versions or variants of an image.  
    If no tag is specified, latest is used by default

Multiple tags are allowed  
If you run a `docker image ls`, all images with different tags will share the same `Image ID`  

[full tag specifications](https://docs.docker.com/engine/reference/commandline/tag/)

#### Tag a running container which might have differences from the image it's based on

* Not very common or recommended

`docker commit container-name> <image-name>`

#### Renaming or retagging images

```sh
docker image tag <old-name> <new-name>
docker image ckad:docker apesce/ckad:docker
```

dopesn't remove the old image, and you can find to images with the same id `docker image ls`

#### Pullinmg an image

`docker image pull <image_name>[:<image_tag>]` or   
`docker  pull <image_name>[:<image_tag>]`

#### Listing Images

`docker image ls`

#### Remove an image

`docker image rm <image-name>`

Only if no container is using it. and also more than one at once

#### Dump an image as a tar file

> **OUTDATED**
> Docker `save` has no `--format oci-archive`; the flag shown below is Podman syntax.
> New: Docker writes a loadable tar; Podman can explicitly write `oci-archive`.
> Ref: [Docker save](https://docs.docker.com/reference/cli/docker/image/save/) · [Podman save](https://docs.podman.io/en/stable/markdown/podman-save.1.html)

`docker save -o output-file.tar image-name:tag`

It always saves images in the OCI (Open Container Initiative) format, which is the default format used by Docker for saving images.

The resulting output is a tar archive containing the image layers and metadata

`docker save ckad:latest --output ckad.tar `

`docker save ckad:pluralsight | gzip > ckad-image.zip`

<mark> Exam: careful that if they want the OCI format you need `--format oci-archive`.
 This seems no more the case with Docker, now defaulting to oci-archive</mark>

* The layers inside the oci-archive are compressed while the layers inside the docker-archive are not compressed. That can make quite a difference in size.

#### Fixing image names for pushing 

 * To be able to push it to a remote repository, you need to add the name of the repository to the beginning of the tag. And the exam gives you the name of the repositoy, just don't push it on the registry (e.g. dockerhub)
 * if you push to docker hub and use docker , you don't need to prefix the repository with `docker.io/` but with other tools or other registries, you need it.

## Understanding Jobs and CronJobs

<mark>Exam: if you get a question asking to make sure that a pod runs through to successful completion, it might look like a 'Pod question' but it's a 'Job question', asking to wrap a pod in a Job</mark>

Structure of the yaml file, with increasing indentation

- CronJob section with "attributes" creates the Job against the given schedule
  - Job Template section with "attributes" in charge of running the Pods
    - Pod Template section with "attributes" makes sure that the container can run on K8s
      - Container section with "attributes" runs the App

Each outer creates the inner: Cronjob -> Job -> Pod -> Container

### Jobs

* Jobs are about running a specific number of pods all the way through to completion. And if needed Pos can be run in parallel a given number at a time .
* Jobs are managed by the Job Controller in the control plane that manages  them through successful completion.
* Jobs can offer intelligence (e.g.: Restart the Pod, Retries, Kill long-running, Clean-up).
* Jobs can create multiple Pods and even run them in parallel.
* Deleting the jobs also deletes the pods he created.

#### Yaml 

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: pi
spec:
  activeDeadlineSeconds: 10     # Max number of seconds before a job gets stopped. If not completed, will be marked as Failed instead of Completed
  ttlSecondsAfterFinished: 120  # TTL  mechanism to limit the lifetime of Job objects that have finished execution
  parallelism: 1
  completions: 5
  backoffLimit: 4               # Max retries if a pod fails, against an exponential delay, starting with 10s
  template:
    spec:
      restartPolicy: Never      # It's useful for debugging g because you can see the logs of failing pods.
      containers:
      - name: ctr
        image: alpine:latest
        command: ["echo",  "simplest pod ever"]
```

* a command that runs for longer

`['sh', '-c' 'echo "this will be slow" && sleep60']`

* A yaml multi line commands

```yaml
command: ["/bin/sh"]
args: 
  - "-c"
  - |
    while true; do echo hello; sleep 10; done
    echo "this will never happen of course!"
    echo "here's some more text" && \
        _c="chocolate chip"; printf "here's a %s cookie" $_c
```

### Cronjobs

* Cron strings "* * * * *" meaning 

1) minute
2) hour
3) Day of the month
4) Month
5) Day of thew week

`"* * * * *"` runs every minute  
`"0 2 4 * *"` runs at 2:00 every 4th day of the month
`"*/2 * * * *"` runs every two minutes

* TimeZone

> **OUTDATED**
> The schedule need not inherit the controller's local time zone.
> New: in v1.35, set `.spec.timeZone`, for example `Etc/UTC`.
> Ref: [CronJob time zones](https://v1-35.docs.kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/#time-zones)

Timezone comes from the control panel of your k8s API Server

#### Cronjob Controller 

Only checks for new tasks every ten seconds, and checks if there's any job scheduled while he was "sleeping".  
Starts the jobs and then lets the Job controller take over

##### Job creation

A CronJob creates a Job object approximately once per execution time of its schedule.  
The scheduling is approximate because there are certain circumstances where two Jobs might be created, or no Job might be created.  
Kubernetes tries to avoid those situations, but does not completely prevent them. Therefore, the Jobs that you define should be idempotent.

* Deadline for delayed Job start `startingDeadlineSeconds`
The .spec.startingDeadlineSeconds field is optional. This field defines a deadline (in whole seconds) for starting the Job, if that Job misses its scheduled time for any reason.

 If you set it to less than 10 seconds, then jobs might be missed. 

##### Missed jobs

It is important to note that if the startingDeadlineSeconds field is set (not nil), the controller counts how many missed Jobs occurred from the value of startingDeadlineSeconds until now rather than from the last scheduled time until now. For example, if startingDeadlineSeconds is 200, the controller counts how many missed Jobs occurred in the last 200 seconds.

A CronJob is counted as missed if it has failed to be created at its scheduled time. For example, if concurrencyPolicy is set to Forbid and a CronJob was attempted to be scheduled when there was a previous schedule still running, then it would count as missed.

For example, suppose a CronJob is set to schedule a new Job every one minute beginning at 08:30:00, and its startingDeadlineSeconds field is not set. If the CronJob controller happens to be down from 08:29:00 to 10:21:00, the Job will not start as the number of missed Jobs which missed their schedule is greater than 100.

To illustrate this concept further, suppose a CronJob is set to schedule a new Job every one minute beginning at 08:30:00, and its startingDeadlineSeconds is set to 200 seconds. If the CronJob controller happens to be down for the same period as the previous example (08:29:00 to 10:21:00,) the Job will still start at 10:22:00. This happens as the controller now checks how many missed schedules happened in the last 200 seconds (i.e., 3 missed schedules), rather than from the last scheduled time until now.

* `concurrencyPolicy`

It  governs whether new jobs will start if previous instances are still running. So it can be any of Allow, which is the default, and Forbid, and Replace.

* `SuccessfulJobsHistoryLimit`
 
 How many jobs and associated pods to keep around from previous runs. It defaults to 3. 
 
* `failedJobsHistoryLimit`, that's the same, only this time it's for failed jobs, and this one defaults to 1
 
* only `spec:schedule` is required. All of the rest, totally optional
   
## Multi container pods

* Used when a container needs some more logic to better integrate with the environment. (e.g. istio service mesh )

### Sidecar pattern

> **OUTDATED**
> The generic “second app container” model omits Kubernetes-native sidecars.
> New: v1.35 sidecars are `initContainers` with `restartPolicy: Always`; the feature is stable since v1.33.
> Ref: [Sidecar containers](https://v1-35.docs.kubernetes.io/docs/concepts/workloads/pods/sidecar-containers/)

* Main container and sidecar

#### Ambassador pattern

* This is part of the generic sidecar pattern 
* The sidecar pods runs alongside the app container for as long as the pod runs
* As an example the ambassador can act as localhost proxy to a remote db, so that the app can talk to localhost port, isolated from remote DB concerns

#### Adapter pattern

* A variation of the sidecar pattern
* As an example can translate the app logging into the format accepted by the specific environment.

### Init pattern 

* for activities that are needed only at startup. As an example the FrontEnd has to wait for the backEnd to start, that logic can go into the sidecar container
* `initContainers:` inside the `spec:` section of the yaml file.
* Normal containers run after the init Containers, which run in the order that you list them

### List all containers within pod

* Quick trick `kubectl logs <pod-name>` gives an error message listing all containers inside that pod.

* `kubectl get pods <podname> -o yaml` and check name and ready status of each container.

## Volumes

* Without volumes, pods (aka containers) write on temp storage on the node they're running on. Temp storage on that node.
* This creates problems in case of node down or moving pods to another node.
* On prem clusters use on-prem storage only, cloud clusters only use cloud storage.
* You need the specific driver for a given type of storafe to make it available to K8s.
* Storage systems can be external to K8s, like EMC (on-prem) or AWS Elastic Block Store or Azure File.
* Storage plugins run as system pods managed by a daemon set. This makes sure they run on every mode. 
  `kubectl get pods -n kube-system` shows this pods (and more)

* Volumes are exposed to K8s that can be used by apps.
* As the storage is external to K8s, it can be visible to all nodes, regardless on what node it is.

* Storage Class (SC) <- Persistent Volume Claim (PVC) <- Persistent Volume (PV)  
  As the Pods are deployed storage gets dinamically provisioned and attached to the pod as Persisten Volume (PV)

### Storage classes (SC)

`kubectl get sc`

#### Reclaim policy

* `Delete` will delete volumes no longer bound to a pod

* `Retain` will not delete volumes no longer bound to a pod

#### VolumeBindingMode

* `immediate` will provision storage to the pod immediately. This poses the risk that the volume gets created early on a node, and the pod being deployed then to a node that doesn't have access to that volume.  
This can happen if a single cluster spans several zones or regions.

* `WaitForFirstConsumer` makes sure the the volume is created in the same zone or region of the pod.  
if we create a PVC referring a WaitForFirstConsumer SC, it will stay pending until it gets claimed by a pod.

### Persistent Volumes (PV) 

Are referred inside the pod as containers[].volumeMounts.name, which referres to the PVC described in the volumes part of the yaml

### Persistent Volume Claims (PVC)

Are referred inside the pod in spec.volumes[].persistentVolumeClaim.claimName

### Storage Classes 

* The normal pattern is to use a StorageClass to define a class of storage with all of the features that you want from the back‑end system.
* Then, when you deploy your Pods, you reference a PersistentVolumeClaim that makes a reference to the class.
* And when the is Pod scheduled, storage on the back end here gets dynamically provisioned and attached to the Pod.

 ### Ephemeral Volumes   

 * Ephemeral volumes are specified inline in the Pod spec, which simplifies application deployment and management.
 
# Application Deployment

## Use Kubernetes Primitives to Implement Common Deployment Strategies

### Use `kubectl create` to get a deployment yaml file, to later modify

`kubectl create deployment nginx --image=nginx:alpine --dry-run=client -o yaml > deploy.yaml`

### Use `kubectl run` to get  a pod yaml file, to later modify

`kubectl run <pod-name> --image=nginx:alpine --dry-run=client -o yaml > deploy.yaml`

### Imperative commands

* Scale a deployment: `kubectl scale deployment <deployment_name> --replicas=<howmany>`
* Change image: `kubectl set image deployment/ngnix nginx`

### Imperatively changing the selector on a resource (e.g.: a service)

`kubectl set selector svc <svc_name> 'role=green'`

* Equivalent to going inside the yaml, looking for `spec.selector.matchLabels` and changing `role: blue` to `role: green`

### Imperatively Create a service for a deployment

`kubectl expose deploy <deploy-name`> --port=<desired port> --target-port=<pod's port> --type=NodePort --name=<service-desired-name>


### Structure  of Blue Green

* a set of pods with labels (e.g.: role) identifying tham as blue, which might mean v1.0 (in addition to potentially other labels)

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

* a set of pods with labels identifying tham as green, which might mean v1.1 (in addition to potentially other labels)

```yaml
spec:
  #....
    matchLabels:
      role: green
  #....
      labels:
      role: green
#....
```

* a blue service (e.g. Load Balancer, or node port) that directs traffic from an internally used port (e.g.: 9000) to "blue" pods via a selector with a 

```yaml
  #....
  selector:
      #....
      role: blue
#...
```

* a green service (e.g. Load Balancer, or node port) that directs traffic from an internally used port (e.g.: 9001) to "green" pods via a selector with 

```yaml
#....
     role: green
#...
```

* a public service (e.g. Load Balancer, or node port) that directs traffic from an externally used port (e.g.: 443) to blue or green pods via a selector with 

```yaml
#.... 
     role: green # or role: blue
#...
```

* And we'd swap to which group pf pods the public service would direct traffic by changing his selector only

## Understand Deployments and How to Perform Rolling Updates

### spec: properties

```yaml
spec:
  minReadySeconds: 1           # Seconds new Pod should be ready to be considered healthy (default 0)
  progressDeadlineSeconds: 60  # Seconds to wait before reporting stalled Deployment (default 600)
  revisionHistoryLimit: 5      # Number of ReplicaSets that can be rolled back (default 10)
```

### spec.strategy: properties

```yaml
strategy:
   type: RollingUpdate   #RollingUpdate (default) or Recreate which deletes all first
   rollingUpdate:
     maxUnavailable: 1
     maxSurge: 1         # Max Pods that can exceed the replicas count. Default 25%
*    maxUnavailable: 1   # Max Pods that are not operational. Default 25%
```

### Saving the configuration during a deployment

 `kubectl create –f file.deployment.yml --save-config`

 Saves the configuration in resource's annotations


### Other option to Update deployment annotation

kubectl annotate deployment [name] kubernetes.io/change-cause="Change details" --overwrite=true

#### Get information about a Deployment

* `kubectl rollout status deployment [deployment-name]`
* `kubectl rollout status –f file.deployment.yml`

#### Get information about a Deployment

> **OUTDATED**
> `--save-config` stores last-applied data; it does not create Deployment rollout history.
> New: ReplicaSets retain revisions; annotate `kubernetes.io/change-cause` only when explanatory text is useful.
> Ref: [Deployment history](https://v1-35.docs.kubernetes.io/docs/concepts/workloads/controllers/deployment/#checking-rollout-history-of-a-deployment)

* There is a history if you use things like `‑‑save‑config` that will be tracked for you, and that's done through the annotations

`kubectl rollout history deployment [deployment-name]`

* Get information about a specific Deployment revision

`kubectl rollout history deployment [deployment-name] --revision=2`

### Rollback a Deployment

`kubectl rollout undo –f file.deployment.yml`

* Rollback to a specific revision

`kubectl rollout undo –f file.deployment.yml --to-revision=2`

## Use the Helm Package Manager to Deploy Existing Packages

### Concepts

* Chart - Bundle of information used to create an instance of a Kubernetes application.

* Config - Configuration information thatt can be merged into a chart to create a releasable object.

* Release - Running instance of a chart (combined with a config) inside K8s. If you install the same chart twice, you get two releases.

* Library - Sort of "functions" short "blocks" that can be used across multiple charts.

* Hubs - Repositories that store helm charts.

### Helm commands

* `helm -h`

* `helm search hub`  
  Defaults to Artifact Hub, Searchs in a lot of repo.  

- `helm search hub` options  
  - `--list-repo-url` option  gives you repo's full URL but is hard to read in table format.  
  - Table format is the deault but you can do `-o yaml` or `-o json`  
  - You find the chart version and the app version (in simple case it looks like the image version).    
  - Each chart is identified with <repo_local_name>/<chart_name>

* `helm repo add <repo_name_you_chose> <repo_url_from_search>`  
  Adds a repo to your local client

* `helm repo udate`
Updates all the locally added repos.

* `helm search repo`   
  - Searches the repositories that you have added to your local helm client (with helm repo add ).
  - This search is done over local data, no public network needed.
  - If we want all versions and not just the lates use `--version` option.

* `helm show values`  
  To know what values can be overridden in the chart  

* `helm pull -untar`
  - As some charts have a lot of values, it can be useful to have the chart "unzipped" to a folder, to check the different files.
  - Note that helm pull doesn't actually install the chart.

* `helm values`
  - Allows to override templates that the charts have (e.g. : admin usr & pwd)
  - Values can be done via file or via --set commands

* `helm install <name_you_chose> <repo/chart>`
  This name is used for deploy (and therefore pods) and svc. At least in my test with bitnami/nginx.  
  It also shows up when you do helm list

* `helm upgrade`  
When doing upgrade, typically to a next version, you can also override some values

* `helm status`

* `helm list`

* `helm uninstall`

# Application Observability and Maintenance

## Understanding API Deprecations

### Admission controllers

* Is involved after authentication and authorization but before persisting.
* Can reject a request (e.g.: PVC asking for too much storage) and or mutate a request
* Can block request to create, delete and modify
* Cannot block request to read
* Can enforce security policies
* Can block insecure images from running
* Any admission controller we use is compiled into the kube-apiserver binary
* Not necessarily all compiled admission controllers are enabled

#### Examples

##### LimitRanger

* Applies default Pod memory/cpu limits for a namespace.
* You can create a LimitRanger for a namespace and then you enforce it with LimitRanger controller.
* If you try to create a Pod with a resource of the limit specified in the limit range it will fail, but not if you specify a limit value for that pod inside the yaml to create it.

##### PersistentVolumeClaimResize

* By default prevents resizing of all claims, unless the claim storage class enables it by setting  `allowVolumeExpansion` property to `true` 

##### NamespaceAutoProvision

Exams requests, creates namespaces if not existing

#### Where are these configured

* Stored in `/etc/kubernetes/manifest/kube-apiserver.yaml` 
* It's the pod running as api-server there's 
```yaml
#...
spec:
  containers:
  - command
    - kube-apiserver
    - --....
    - --enableadmission-plugins=NamespaceAutoProvision,another-plugin,...
    #...
```

* You need to sudo to be able to `cat` this

#### View admission controller plugins for kube-apiserver

* `kubectl describe pod kube-apiserver -n kube-system`
* `kubectl describe pod kube-apiserver -n kube-system | grep enable-admission-plugins`
* Do a `k get pods` first to confirm the name of the apiserver pod, in case it's slightly different because of version
* `KUBE_EDITOR=nano k edit pod kube-apiserver-cl1-control-plane -n kube-system`

#### Using `kube-apiserver`

* If you shell into the `kube-apiserver` pod inside the `kube-system` namespace, you can invoke the executable directly.
* `kube-apiserver -h` gives information about the options avaliable.

#### Modify admission controllers settings

* One way is edit the `/etc/kubernetes/manifest/kube-apiserver.yaml` file and re-apply it in the `kube-system namespace`.

* Another way is to shell into the pod and run

`kube-apiserver --enable-admission-plugins=<plugin1>,<plugin2>`
or
`kube-apiserver --disable-admission-plugins=<plugin1>,<plugin2>`

#### K8s version

`k version -o yaml` major.minor.patch as usual
* GA is for General availability = release
* Otherwise `v<number>alpha<alpha number>` or `v<number>beta<beta number>`, e.g.: `batch/v2alpha1`

#### ApiGroups

* List the resources, their group and versions by `k api-resources`
* optionally sort them e.g.: `k api-resources --sort-by-name`

* note that `v1` is the api version of that specific group

##### Core Group 

* When there's no group name the resource is in the Core Group

* apiVersion: <no-groupname-here>v1
* e.g.: pods

##### Named Groups

* apiVersion: batch/v1
* e.g.: cron jobs

#### View api resources

* `k api-resources --sort-by=name`
* `k api-resources --api-group=rbac.authorization.k8s.io`

#### View Api Group for a given resource

* `k explain deploy`
* KIND: Deployment  
  VERSION: apps/v1

* Gives kind, version and group. No group means Core group
* KIND: ConfigMap  
  VERSION: v1

#### Enabling alpha versions

* Alpha versions are not enabled by default.
as a parameter in `kube-apiserver.yaml` there can be an option `--runtimeconfig=<group>/<version>

#### Order of versions

* Alpha. E.g: `v1alpha3`
* Beta. E.g: `v1beta2`
* Stable. E.g: `v2` //Also called GA General availability

##### Removal of API elements

* It can appen only with a version increment of the API group
* API Objects must round trio between API versions without information loss. Co from V2 to v1 to V2, either adding properties to lower versions or using meannotation. Anyhow the system must be able to handle it.
* GA is basically forever, less stable version can be deprecated and then removed not before a given deprecation time  proportional to their stability (i.e. Beta last longer, 9 months or 3 minor whichever is longer; alpha, have no deprecation at all).

#### All Versions

* `kubectl api-versions`
* `kubectl api-versions | grep autoscaling`

#### Preferred version for an API group

* e.g.: for certificates
* First you have to call `kubectl proxy 8001 &` 
* `&` so that it stays in the background untill later you kill it with `ps -a grep kubectl` and `kill -9 <pid>`
* Then `curl localhost:8001/apis/certificates.k8s.io`
* preferredVersion is in the payload

* `curl localhost:8001/apis/batch`
* `curl localhost:8001/apis/`

* in the exam context not having multiple terminals `k proxy 8001 & curl` wil put you into interactive curl where you can run curl commands
* in the exam context not having multiple terminals `k proxy 8001 & ` wil run k proxy in the backgroung and you can later kill process with `kill <PID>`
* if unsure of the PID `ps -a | grep kubectl`

## Implementing Probes and Health Checks

### Probe definition

* A Probe is a diagnostic performed periodically by the kubelet on a container. Somehow like a health check.

* Probes can be used in Pds's definition (yaml) but of course also in deployments.

### Types of Probes

> **OUTDATED**
> Startup probes are not legacy, and the mechanism list below omits gRPC.
> New: v1.35 has three probe purposes and four mechanisms: exec, HTTP, TCP, and gRPC.
> Ref: [v1.35 probes](https://v1-35.docs.kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/)

* Two (Readiness and Liveness) plus one legacy (Startup)

#### Readiness Probe

* Completed initialization and is therefore able to receive requests

```yaml
spec:
  readinessProbe:
    tcpSocket:
      port: 8080
    initialDelaySeconds: 15 //default is 0
    periodSeconds: 10 //default is 10
```

#### Liveness Probe determines if a Pod is healthy and running as expected.

```yaml
spec:
  livenessProbe:
        exec:
          command:
          - cat 
          - /tmp/healthy
        initialDelaySeconds: 2 //wait to let the pod start
        timeoutSeconds: 3
        periodSeconds: 5 
        failureThreshold: 1 //default is 3. Number of allowed failures is failureThreshold -1
```

* Note that the liveness probe doesn't wait for the readiness probe to succeed, they're independent

* Startup is meant for containers with a long time to start, so that we dont' start checking if it's healthy before ir starts up.

### Restart Policy

* Defaults to Always, can be overwritten if needed.

* Failure at either Startup or Health checks causes Pod to be recreated

### Probe Types 

#### ExecActions 

* Execute an action inside the container. Check for a file, run a command... success on exit 0

#### TCPSocketAction

* Just tcp check against a container's ip address and port

#### HTTPGetAction 

* As long as it returns in the 200 range

### Probes results

Only trhree types of resul:

* Success
* Failure
* Unknown 

## Using Provided Tools to Monitor Kubernetes Applications

### Options
- Web UI Dashboard
- Metrics Server
- kube-state-metrics
- Prometheus (e ven with alerts) & Graphana. 
- etc..

### Metrics Server

* Metrics Server collects resource metrics from Kubelets and exposes them in Kubernetes apiserver through Metrics API for use by Horizontal Pod Autoscaler and Vertical Pod Autoscaler. 
* Metrics API can also be accessed by `kubectl top`, making it easier to debug autoscaling pipelines.
* Metrics Server is not meant for non-autoscaling purposes.
* For example, don't use it to forward metrics to monitoring solutions, or as a source of monitoring solution metrics. 
* In such cases please collect metrics from Kubelet /metrics/resource endpoint directly.

#### Installing Metrics Server

* Where it's not installed by default, like Docker Desktop
* Just follow the instructions
* Check prerequisites
* Note that the command to be added it's not on the command line but inside the yaml

#### How Metrics Server works

* On each node there's a `kubelet` who gets input from `cAdvisor` (who gets it for `Container Runtimes, such as containerd`) and from `PodData`.
* Kubelet is the copmmunication mechanism between a node and the master node.
* Metrics Server gets input from kubelets via `Summary Api`.
* Kubectl can then use connect to Api Server who connects to Metrics Server via `Metrics Api`.
* Note that metrics are not updated in real time, there's a delay
 
#### Verifying that Metrics Server it's installed

* Easiest way is to look for all pods in kube-system namespace and grep for metrics-server

#### kubectl top to interrogate Metrics Server

* `k top nodes` gives resources usage (CPU and Memory)
* `k top pods`

## Utilizing Container Logs

### Container logs

* `k get logs <pod-name>`
* `k get logs <pod-name> -c <container-name>` //for multi- container pods
* `k logs deployment/<deployment-name>`
* `k get logs -p <pod-name>` //previous. I  f there is a container that was terminated but still available
* `k get logs -f <pod-name>` //follow. streams the logs to the console 
* `k get logs --tail=20 <pod-name>` //last 20 log lines
* `k get logs --since==10s <pod-name>` //or 2m of 1h
* `k get logs -l app=backend --all-containers=true ` //or 2m of 1h

#### terminated containers' logs that you could access wit -p

* By default, if a container restarts, the kubelet keeps one terminated container with its logs.
* If a pod is evicted from the node, all corresponding containers are also evicted, along with their logs.
* The kubelet makes logs available to clients via a special feature of the Kubernetes API.

## Debugging Kubernetes
 
### Get events `kubectl get events`

* For a pod `k describe <pod>`
* For a namespace `k get events`
* For all namespaces `k get events --all-namespaces`

### `kubectl debug`

Create an ephemeral debug container and even make a copy of a pod adding some debug utilities for debugging purposes.

* `kubectl debug <failed-but-existing-podname> -it --image=<image-name> --copy-to=<name-of-the-new-pod>`

`kubectl debug <failed-but-existing-podname> -it --image=<image-name> --copy-to=<name-of-the-new-pod> --container=<container-we-need-to-debug> -- sh`

# Application Environment, Configuration and Security

## Discover and use resources that extend kubernetes

### Defining custom resources and operators

* A resource is anything created within our cluster.

#### Custom resources

* A custom resource is a way to extend k8s by creating new object types.
* Instead of being accessed by the kubernetes aAPI , we'd create our custom API to access them

##### Custom resource definitions

*Custom resource definitions, or CRDs, are how we define the custom resources that we can then use either with operators or as a method of grouping or clustering like objects.

```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: applications.example.com # has to match with the plural name below
spec:
  group: example.com
  scope: Namespaced  # or CLuster
  names:
    plural: applications # this has to match with beginning of metadata.name above
    singular: application
    kind: Application
    shortNames:
    - app
  versions:
  - name: v1
    served: true  # served=true means usable version
    storage: true # storage=true means that it has access to our storage
    # you can serve more than one version, but only one can be set to storage=true
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

* Note that just because we called the properties image and replicas k8s is going to spin app an application with this image and replicas. Telling k8s what to do with this properties is the job of an operator setup and installed, associated with this custom resource.

* To create suche an object of this kind we'd have a yanl file (let's call it for example app.yaml) similar to this:

```yaml
apiVersion: example.com/v1 # group and version from previous one
kind: Application # names.plural from previous one
metadata:
  name: my-app
spec: 
  frontend:
    image: nginx:latest
    replicas: 2
```

#### Operators

* Custom resources are used with custom operators (e.g.: Watch, Update) wgo perform actrivities on those resource defined by what we write in their code. Code can be Go, Phython, and more.
* The Operator works using the priciple of control loop and functions as a controller.
* The operator will monitor our custom resources. And then based on the information it gathers from these custom resources, it will then bring that information into the operator code, and the operator can then take action on an object (not necessarily the one that was being monitored?) or otherwise, depending on what its code tells.
<mark>Custom resources definition is in scope for the exam, writing operators is not<mark/>

## Understand Authentication, Authorization and Admission Control

### RBAC Role-Based Authentication Control

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
kind: RoleBinding    # or ClusterRoleBinding
metadata:
  name: read-pods
  namespace: default
subjects:            # You can specify more than one "subject"
- kind: User         # User, Service or Group
  name: jane         # "name" is case sensitive
  apiGroup: rbac.authorization.k8s.io
roleRef:             # "roleRef" specifies the binding to a Role / ClusterRole
  kind: Role         # Role or ClusterRole
  name: pod-reader   # this must match the name of the Role or ClusterRole you wish to bind to
  apiGroup: rbac.authorization.k8s.io
  ```

* After you create a binding, you cannot change the Role or ClusterRole that it refers to.  
  If you try to change a binding's roleRef, you get a validation error. 

### ABAC Attribute-Based Access Control

* Out of scope for the exam
* To enable ABAC mode, specify --authorization-policy-file=SOME_FILENAME and --authorization-mode=ABAC on startup.
* The file format is one JSON object per line. There should be no enclosing list or map, only one map per line. Each line is a "policy object".

### Admission Controllers
 
#### Mutating Controllers

* E.G.: The default storage class mutating controller adds a storage volume to objects that deploy without one.

#### Checking if an admission controller is enabled

Based on K8s docs you can use `ps -ef | grep kube-apiserver`, but it actually depends on the specific k8s configuration.
  * `-e` selects all porocesses (just like `-A`) 
  * `-f` provides a full-format listing for each process.
  
Note:  without the `-A` , ps will only print the processes belonging to the current session. Think of it like "absolutely everything". 
On a related note `-a`  does the same thing, but restricting it to the session-owner (username).

<mark>For the exam the recommended way is looking into `/etc/kubernetes/manifest/kube-apiserver.yaml`</mark>

### EventRateLimit controller 

* An example of admission controller that uses configuration is `EventRateLimit` which controls how many events can reache the Kubernetes Api.  
  Once enabled the controller,  it needs some configuration to know what to stop.

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

## Understand and Define Resource Requirements, Limits ands Quotas

### Resource Requests and Limits

* Request and limits are for `Pods`

* In the Pod yaml template there are 
  * spec.containers[].resources.limits.cpu
  * spec.containers[].resources.limits.memory
  * spec.containers[].resources.limits.hugepages-<size>
  * spec.containers[].resources.requests.cpu
  * spec.containers[].resources.requests.memory
  * spec.containers[].resources.requests.hugepages-<size>

* limits must be higher than requests otherwise the pod won't deploy

* `rquestes ` are Estimates.

* The CPU limit defines a hard ceiling on how much CPU time that the container can use. During each scheduling interval (time slice), the Linux kernel checks to see if this limit is exceeded; if so, the kernel waits before allowing that cgroup to resume execution.

* The CPU request typically defines a weighting. If several different containers (cgroups) want to run on a contended system, workloads with larger CPU requests are allocated more CPU time than workloads with small requests.

* If a container exceeds its memory request and the node that it runs on becomes short of memory overall, it is likely that the Pod the container belongs to will be evicted.

* A container might or might not be allowed to exceed its CPU limit for extended periods of time. However, container runtimes don't terminate Pods or containers for excessive CPU usage.

 ### Resource Quotas

> **OUTDATED**
> The “starting with v1.29” qualifier is not useful for the CKAD v1.35 environment.
> New: v1.35 lists `ResourceQuota` among the admission plugins enabled by default.
> Ref: [Admission controllers](https://v1-35.docs.kubernetes.io/docs/reference/access-authn-authz/admission-controllers/#which-plugins-are-enabled-by-default)

* Quotas set limitations on the `namespace` level 

* Quotas can limit not only resource but also can limit the amount of any kind of object created, like number of pods.

* Resource quotas are an admission controller enabled by default on K8S starting with version 1.29

* You define ResourceQuotas via a kind:ResourceQuota yaml file, inside which there is `metadata.namespace` to assign it to a namespace

* `spec.hard` section has requests, limits, number of pods

* `spec.scopes` it's a tricky topic, better refer to docs, but know it exists
  * Each quota can have an associated set of scopes. 
  * A quota will only measure usage for a resource if it matches the intersection of enumerated scopes.

## Understanding ConfigMaps

* ConfigMaps should not contain secrets
* The key and values in a ConfigMap can only be strings.
* If we want a value with boolean values we need to quote the values, like "true" or "false". Same for numbers, like "100".

<mark>EXAM: In the exam they might try to induce into error by providing secrets and not secrets data together, you have to put them in ConfigMaps and Secrests</mark>

### Defining ConfigMaps

* `ConfigMap` is a kind
* In the yaml, the KeyValuePairs are under the `data:` section 
* Values can also be multiple lines of content
* Data has to be under 1MB

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

1 Inside a container command and args
2 Environment variables for a container
3 Add a file in read-only volume, for the application to read
4 Write code to run inside the Pod that uses the Kubernetes API to read a ConfigMap (Totally Not in scope for the exam)

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
      args: ["$(PLAYER_INITIAL_LIVES)"] # Notice that is different here
                                        # from the key name in the ConfigMap.
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

* if the names that we want in the pod are the same of the ones in the config map, we can load the whole config map iat once

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

1 Create a ConfigMap or use an existing one. Multiple Pods can reference the same ConfigMap.
2 Modify your Pod definition to add a volume under .spec.volumes[]. Name the volume anything, and have a .spec.volumes[].configMap.name field set to reference your ConfigMap object.
3 Add a .spec.containers[].volumeMounts[] to each container that needs the ConfigMap. Specify .spec.containers[].volumeMounts[].readOnly = true and .spec.containers[].volumeMounts[].mountPath to an unused directory name where you would like the ConfigMap to appear.
4 Modify your image or command line so that the program looks for files in that directory. Each key in the ConfigMap data map becomes the filename under mountPath.

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

* There are four different ways that you can use Secrets to configure a container inside a Pod:

1 Inside a container command and args
2 Environment variables for a container
3 Add a file in read-only volume, for the application to read
4 Write code to run inside the Pod that uses the Kubernetes API to read a ConfigMap (Totally Not in scope for the exam)

```yaml 
apiVersion: v1
kind: Secret
metadata:
  name: db-pass-secret
type: Opaque     # it is the default           
data:
  db-pass: dmFsdWUtMg0KDQo=
```

<mark> Opaque works in most user supplied data, but if  the task description might contain keywords like TLS or Docker config, in  that case check docs</mark>

* K8S Secrets do not do the encryption, it's up to the one who creates them

* Secrets arte used very similarly to ConfigMaps inside Pods

## Understand Service Accounts

* A service account is a type of non-human account that, in Kubernetes, provides a distinct identity in a Kubernetes cluster.
* Instead of passwords, ServiceAccounts use tokens.
* ServiceAccounts let our pods access the Kubernetes API.
* Application Pods, system components, and entities inside and outside the cluster can use a specific ServiceAccount's credentials to identify as that ServiceAccount.
* This identity is useful in various situations, including authenticating to the API server or implementing identity-based security policies.
* They are Namespaced: Each service account is bound to a Kubernetes namespace. 
* Every namespace gets a default ServiceAccount upon creation.

### Creating a Service Account

> **OUTDATED**
> The example uses `kubernetes.io/enforce-mountable-secrets`, deprecated since v1.32.
> New: use separate namespaces to isolate access to mounted Secrets.
> Ref: [Annotation reference](https://v1-35.docs.kubernetes.io/docs/reference/labels-annotations-taints/#kubernetes-io-enforce-mountable-secrets)

* via yaml

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  annotations:
    kubernetes.io/enforce-mountable-secrets: "true"
  name: my-serviceaccount
  namespace: my-namespace
```

* imperatively

`kubectl create serviceaccount reader-service`

### Assign a ServiceAccount to a Pod

* To assign a ServiceAccount to a Pod, you set the spec.serviceAccountName field in the Pod specification. Kubernetes then automatically provides the credentials for that ServiceAccount to the Pod. 
* In v1.22 and later, Kubernetes gets a short-lived, automatically rotating token using the TokenRequest API and mounts the token as a projected volume.

* By default, Kubernetes provides the Pod with the credentials for an assigned ServiceAccount, whether that is the default ServiceAccount or a custom ServiceAccount that you specify.

* To prevent Kubernetes from automatically injecting credentials for a specified ServiceAccount or the default ServiceAccount, set the `automountServiceAccountToken` field in your Pod specification to false.

### Using a service token

* You need to bind it to a Role by a `RoleBinding` or a `ClusterRoleBinding`, depending if you are connecting to a `Role` or to a `ClusterRole`.
* Within the RoleBinding yaml definition file the subjects[n].kind is defined as `Service`, as it's not a user.
* You also connect the ServiceAccount to the Pod by setting `spec.serviceAccountName` to the name o the service account.

### confirming that the service account got associated with a pod, use `kubectl describe pod <pod_name>`

## Understand Security Contexts

* A security context defines privilege and access control settings for a Pod or Container by adding to their spec section as `spec.securityContext...` or `spec.containers[x].spec.securityContext...`

* When setting security context for volumes, that has to go under the Pod section `spec.securityContext`, not the container one

* Security context settings include, but are not limited to:

  * Discretionary Access Control: Permission to access an object, like a file. PodPermission for a Pod/Container to run with a certain  user ID (UID) and group ID (GID).

  * Security Enhanced Linux (SELinux): Objects are assigned security labels.

  * Running as privileged or unprivileged (root or not).
  
  * Filesystem settings to restric access only to certain filesystems.

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

* Note that tyhe opposite of `add:` capabilities is `drop:`

# Services and Networking

## Demonstrate Basic Understanding of Network Policies

* The Pods connect to the `Pod network` created by the `Network plugin`.
* Network policies only work if your network plugin supports them.

* If you apply more than one policy to some pods, the policies combine into a `Policies aggregate`.
* Policies that you create are always allow policies, there's no way specifically deny a particular traffic flow.

* Network policies are namespaced, which means that they can be targeted at particular Namespaces. If you don't specify one, it's the default namespace.
* Policies can be targeting specific namespaces, unfortunately with a rather complicated key of type   
  `ingress.from.podSelector[].namespaceSelector.matchLabels[].kubernetes.io/metadata.name:`  
  or `egress` of course.

* Policies are only on Pods, but can have other types of kubernetes entities on the other end.
* `kubectl get netpol` with netpol being the short name for network policies.
* The most common way to specify Pods for a policy is via `matchLabels`
* You can also block with `ipBlock` criteria but it's used only for internal cluster network, otherwise NATting gets in the way.
* The easiest way to get Pods' labels is `kubectl get pods --show-labels`

* The entities that a Pod can communicate with are identified through a combination of the following three identifiers:

  1 Other pods that are allowed (exception: a pod cannot block access to itself)
  2 Namespaces that are allowed
  3 IP blocks (exception: traffic to and from the node where a Pod is running is always allowed, regardless of the IP address of the Pod or the node)  

  When defining a pod- or namespace-based NetworkPolicy, you use a selector to specify what traffic is allowed to and from the Pod(s) that match the selector.

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

* Be very carefull at the difference of voices under `- from` or ` - to`
* If the voices like `nameSelector:` doesn'h have a dash `-` it means it's not a rule by itself by goes together witrh the previous one

Single rule, so namespaceSelector is under podSelector. Therefore allow Pods with `ckad` AND in `ps`

```yaml
- from:
  - podSelector:
    matchLabels:
      project: ckad
    namespaceSelector:
      matchLabels:
        kubernetes.io/metadata.name: ps
```

Two separate rules. Therefore allow Pods with `ckad` or in `ps`
```yaml
- from:
  - podSelector:
    matchLabels:
      project: ckad
  - namespaceSelector:
      matchLabels:
        kubernetes.io/metadata.name: ps
```

* Note that in `kubectl describe netpol` you will see the differenty policies as different `From:`
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
* A Service's Name and IpAdress don't change while it exists.
* The name gets automatically recorded in the clusters's internal DNS that all PODs have access to.

### ClusterIP

* It's the default type if you don't specify a `type:`
* Internal Ip and port on the Pod network, therefore is avalable to other apps and pods inside the same cluster.
* Unless there are specific needs (and in that case, restrictions and risk of collision) the ip gets autmatically assigned by K8S.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-clusterip-service # this gets registered in the cluster's internal DNS
spec:
  type: ClusterIp
  selector:
    app: ckad
  ports:
    - port: 9000
      targetPort: 8080
            # By default and for convenience, the `targetPort` is set to
            # the same value as the `port` field.
 ```

 * `kubectl describe svc <service-name>`  gives also the target Pods under the row: `Endpoints`

### NodePort 

* Works on top of Cluster IP. It exposes the service to the outside world, via static port on all cluster nodes' IP.
* NodePorts services build their own ClusterIP services behind the scenes to build on.
* External clients can hit any cluster node on the chosen port and reach the service.
* By default the NodePorts are TCP and between 30000 and 32767.


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

* Integrates with cloud load-balancer
* Make a service accessible via an external load balancer
* Extrnal clients cna reach a service via a highly available internet-facing load balancer, and also give it a friendly DNS name.

### Exam tips

* If direct connection to Pods are causing issues, you need a service.
* If you need to connect only between Pods in the same cluster, you need a cluster IP service.
* If it has to be exposed via known port on all nodes, than it'a NodePort service.
* If you need to expose via cloud load-balancer, it's a LoadBalancer Service.
* If the service exists but it's not working, first of all check selector vs pods' labels.
* It's ok if the selector lists 2 of 3 labels on pods, but not if it lists 3 and pod has only 2 matching

### DNS

> **OUTDATED**
> Modern clusters normally run CoreDNS Pods, not Pods named `kube-dns`.
> New: the Service remains named `kube-dns` for compatibility, while the backing Pods are usually CoreDNS.
> Ref: [CoreDNS service](https://v1-35.docs.kubernetes.io/docs/tasks/administer-cluster/dns-custom-nameservers/)

* There's a `kube-dns` service and `kube-dns` pods in the kube-system namespaces.
* Every pods get the address of the dns service injected inside it's configuration, for instance inside `/etc/resolve.conf` file as `nameserver`

## Use Ingress Rules to Expose Applications

> **OUTDATED**
> Ingress remains in CKAD scope, but the API is frozen; the community Ingress-NGINX controller is retired.
> New: keep Ingress for the exam; prefer Gateway API or a maintained controller for new production work.
> Ref: [v1.35 Ingress](https://v1-35.docs.kubernetes.io/docs/concepts/services-networking/ingress/) · [retirement](https://kubernetes.io/blog/2025/11/11/ingress-nginx-retirement/)

* Load balancers can expose only one service via a load balancer on the cloud, so if you need to expose more, you need more load balancers in the cloud which means cost.

* Ingress can expose many services, each of course with his own (behind the scenes) ClusterIP.
* Ingress is only for HTTP and HTTPS
* Ingress creates a single load blancer and puts it on port 80 or 443. Then it uses host and/or path based routing to send traffic to backend services. 

* Ingress are working via Ing Spec (defines the rules) and Ing Controller (implements the rules)
* Kubernetes doesn't ship with a native controller, one has to be installed. In the exam, it's already installed.
* Should you need it it's just enough for exemple to get the https address of nginx ingress controller from github and apply it.

`kubectl get ing` //short for ingress

### IngressClass

* It's a way to run more than one ingress controller on the same cluster.

`kubectl get ingressclass` 

* what you get here must match the `spec.ingressClass` in the ingress definition 
<mark>Exam importan when copying from the docs, ingressClass must be checked/corrected<mark>

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: minimal-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
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

<mark>Exam: environment are all linux</mark>

<mark>exam It's totally ok to copy paste examples from https://kubernetes.io/docs/</mark>

## Setting alias for Kubectl

* Powershell `set-alias k kubectl`
* Linux `alias k=kubectl`

## Change the editor for K9s commands edit (memorize this)

* `KUBE_EDITOR="nano" k edit svc/<service-name>`
* `alias ke="KUBE_EDITOR='nano' kubectl"` and then  `ke edit pod nginx-6cf46f5666-mbbms`

* The keyboard combination to display the current line number whilst you are using nano is CTRL+C.

## Using jq (example)

`k get deploy <deploy-name> -o json | jq '.metadata.annotations." kubernetes.io/change-cause"'` // double quotes to escape slash and dash

## Field selectors

* Field selectors let you select Kubernetes objects based on the value of one or more resource fields. 
* It even allows to get events for more than one "object" at once
`kubectl get events --field-selector type=warning --all-namespaces`
* Supports operator like =, ==, !=
* example `kubectl get services  --all-namespaces --field-selector metadata.namespace!=default`

## Running multiple terminals using tmux

https://github.com/tmux/tmux/wiki/Getting-Started

* most important Ctrl-b ? for help

## Imperatively make changes to kubeconfig

* Create Cluster entry in config `kubectl config set-cluster test-cluster --server=https://127.0.0.1:52807`
* Creates a new context entry in kubeconfig called test-context pointing to a cluster called test-cluster `kubectl config set-context test-context --cluster=test-cluster`

## K8s Context

* View current config `k config view`, this also gives the default namespace, if not listed, it's default.
* View in which context we are `k config current-context`
* Change the the current context `kubectl config use-context test-context`

## K8s Namespace (memorize this)

* ` kubectl config set-context --current --namespace=<nameOfTheNamespace> `
* ` alias kn='kubectl config set-context --current --namespace ' `
* ` kn default ` 
* ` alias kn='KUBE_EDITOR="nano"' `

When not specified, not a bad idea to switch to default namespace

## Kubectl Apply vs. Kubectl Create 

* Both accept JSON and YAML formats.
* Both can work by file name or stdin

`kubectl apply` is a declarative command.

* Applies a configuration to a resource by file name or stdin. The resource name must be specified.
* This resource will be created if it doesn’t exist yet.
* If the resource already exists, this command will not error.

`kubectl create` is an imperative command.

* Creates  a resource from a file or from stdin.
* If the resource already exists, kubectl create will error.

## redeploy once you fix a yaml file (e.g. Job, Cronjob)

`kubectl apply -f <YamlFile.yaml>`

## Modify a deployment from the command line (for example if you created it without a yaml)

`k edit deploy/<deploy-name>` will open the deployment in the KUBE_EDITOR

## Create a temporary pod as an interactive TTY using image alpine and set restart to Never, named temp-pod

`k run -it --restart=Never --image=alpine temp-pod`
`k run -it --restart=Never --image=alpine temp-pod -- /bin/sh`     //apk add bash and then bash, if needed, same with curl 
`k run -it mycurlpod --image=curlimages/curl  -- sh`               //No bash
`k run -it al --image=alpine -- /bin/sh --restar=never`

## K8 commands

* `kubectl logs <podname>`
* `kubectl get jobs --watch`
* `kubectl get pods --watch`
* `kubectl get all`

## Clusters

* List the available clusters: `kubectl config get-contexts`
* Switch to a different cluster: `kubectl config use-context <context-name>`
* Verify the active cluster: `kubectl cluster-info`

