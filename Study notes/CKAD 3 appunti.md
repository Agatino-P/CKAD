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
  content: counter(h1) "." counter(h2) "." counter(h3) "." counter(h4) ". " counter(h5) ". "
}

h6:before {
  counter-increment: h6;
  content: counter(h1) "." counter(h2) "." counter(h3) "." counter(h4) ". " counter(h5) ". " counter(h6) ". "
}

</style>

> **AUDIT BASELINE — 2026-09-20**
> CKAD currently uses Kubernetes v1.35; recheck near exam day because the environment follows Kubernetes releases.
> Ref: [CKAD FAQ](https://docs.linuxfoundation.org/tc-docs/certification/faq-cka-ckad-cks) · [v1.35 docs](https://v1-35.docs.kubernetes.io/docs/)

# Admission controllers

* Is involved after authentication and authorization but before persisting.
* Can reject a request (e.g.: PVC asking for too much storage) and or mutate a request
* Can block request to create, delete and modify
* Cannot block request to read
* Can enforce security policies
* Can block insecure images from running
* Any admission controller we use is compiled into the kube-apiserver binary
* Not necessarily all compiled admission controllers are enabled

## Examples

### LimitRanger

* Applies default Pod memory/cpu limits for a namespace
* You can set a LimitRanger for a namespace but then you enforce it with LimitRanger controller

### PersistentVolumeClaimResize

* By default prevents resizing of all claims, unless the claim storage class enables it by setting allow allowVolumeExpansion property to true

### NamespaceAutoProvision

Exams requests, creates namespaces if not existing

## Properties

* Stored in /etc/kubernetes/manifest/kube-apiserver.yaml 

* to access it in docker desktop 
* `docker run -it --privileged --pid=host debian nsenter -t 1 -m -u -n -i sh`
* `cd /etc/kubernetes/manifests`
* `vi kube-apiserver.yaml`
 

### Enabling alpha versions or listing enabled alpha versions

* in /etc/kubernetes/manifest/kube-apiserver.yaml 
* --runtime-config=

## view admission controller plugins for kube-apiserver

* `kubectl describe pod kube-apiserver -n kube-system`
* `kubectl describe pod kube-apiserver -n kube-system | grep enable-admission-plugins`
* Do a `k get pods` first to confirm the name of the apiserver pod, in case it's slightly different because of version

## Modify settings

* `k config set-context --current --namespace=kube-system`
* `k get pods` to get the api-server pod
* `k exec -it kube-apiserver-master -- sh` the double dashes end the first command (shelling into the container) and start the second (shell)
// kind of commands we give to the container
* `k exec -it kube-apiserver-docker-desktop -- kube-apiserver -h ` executes `kube-apiserver -h`

* Edit the file above or invoking kube-apiserver on a master node (shelling into it)
* Master Pod might need a moment to come back online
* Better make a copy (cp) of the file first

# K8s version

`k version -o yaml` major.minor.patch as usual
* GA is for General availability = release
* Otherwise `v<number>alpha<alpha number>` or `v<number>beta<beta number>`, e.g.: `batch/v2alpha1`

## ApiGroups

* note that `v1` is the api version of that specific group

### Core Group 

* apiVersion: v1
* e.g.: pods

### Named Groups

* apiVersion: batch/v1
* e.g.: cron jobs

## View api resources

* `k api-resources --sort-by=name`
* `k api-resources --api-group=rbac.authorization.k8s.io`

## View Api Group for a given resource

* `k explain deploy`
* Gives kind, version and group. No group means Core group

## All versions for a given resource

* ` ` 

## Preferred version for an API group

* e.g.: for certificates
* `kubectl proxy 8001`
* `curl localhost:8001/apis/certificates.k8s.io`

* `curl localhost:8001/apis/batch`

* `curl localhost:8001/apis/`

* in the exam context not having multiple terminals `k proxy 8001 & curl` wil put you into interactive curl where you can run curl commands
* in the exam context not having multiple terminals `k proxy 8001 & ` wil run k proxy in the backgroung and you can later kill process with `kill <PID>`
* if unsure of the PID `ps -a | grep kubectl`

# Probes

* In a pod or deployment, doesn't matter
* Note that the liveness probe doesn't wait for the readiness probe to succeed, they're independent

## Readiness Probe

* Completed initialization and is therefore able to receive requests

```yaml
spec:
  readinessProbe:
    tcpSocket:
      port: 8080
    initialDelaySeconds: 15
    periodSeconds: 10
```

## Liveness Probe

* Healthy, running as expected, Is able to answer calls

```yaml
spec:
  livenessProbe:
        exec:
          command:
          - cat 
          - /tmp/healthy
        initialDelaySeconds: 2 //wait to let the pod start
        timeoutSeconds: 3
        periodSeconds: 5 //default is 10
        failureThreshold: 1 //default is 3. Number of allowed failures is failureThreshold -1
```

## Startup Probe (Legacy only)

> **OUTDATED**
> Startup probes are not legacy, and the mechanism list below omits gRPC.
> New: v1.35 has three probe purposes and four mechanisms: exec, HTTP, TCP, and gRPC.
> Ref: [v1.35 probes](https://v1-35.docs.kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/)

* Slow starting container

### Failing probes

* Default of restartPolicy is Always
* kubelet eventually sends a request to restart the probe

## Probe Types 

### ExecActions 

* Execute an action inside the container. Check for a file, run a command, success on exit 0

### TCPSocketAction

* Just tcp check against a container's ip address and port

### HTTPGetAction 

* As long as it returns in the 200 range

## Probes results

* Success
* Failure
* Unknown 

# Create yaml for a pod

* Instead of the usual `k create <resource> -o yaml --dry-run=client > my-resource.yaml` we're gonna do
* `k run <desired-pod-name> --image=<image-name:tag> -o yaml --dry-run=client > my-pod.yaml`

# Monitoring

## Options
- Web UI Dashboard
- Metrics Server
- kube-state-metrics
- Prometheus
- Graphana
- etc..

## Metrics Server

* Metrics Server collects resource metrics from Kubelets and exposes them in Kubernetes apiserver through Metrics API for use by Horizontal Pod Autoscaler and Vertical Pod Autoscaler. 
* Metrics API can also be accessed by `kubectl top`, making it easier to debug autoscaling pipelines.

* Metrics Server is not meant for non-autoscaling purposes.
* For example, don't use it to forward metrics to monitoring solutions, or as a source of monitoring solution metrics. 
* In such cases please collect metrics from Kubelet /metrics/resource endpoint directly.

### Installing Metrics Server

* Just follow the instructions
* Check prerequisites
* Note that the command to be added it's not on the command line but inside the yaml

## kubectl top

* `k top nodes` gives resources usage
* `k top pods`

* Note that metrics are not updated in real time, there's a delay
 
## verifying that it's installed

* Easiest way is to look for all pods in kube-system namespace and grep for metrics-server

# Container logs

* `k get logs <pod-name>`
* `k get logs <pod-name> -c <container-name>` //for multi- container pods
* `k logs deployment/<deployment-name>`
* `k get logs -p <pod-name>` //previous. I  f there is a container that was terminated but still available
* `k get logs -f <pod-name>` //follow. streams the logs to the console 
* `k get logs --tail=20 <pod-name>` //last 20 log lines
* `k get logs --since==10s <pod-name>` //or 2m of 1h
* `k get logs -l app=backend --all-containers=true ` //or 2m of 1h
  
## terminated containers' logs that you could access wit -p

* By default, if a container restarts, the kubelet keeps one terminated container with its logs.
* If a pod is evicted from the node, all corresponding containers are also evicted, along with their logs.
* The kubelet makes logs available to clients via a special feature of the Kubernetes API.

# Debugging  Kubernetes

## Get events `kubectl get events`

* For a pod `k describe <pod>`
* For a namespace `k get events`
* For all namespaces `k get events --all-namespaces`

## `kubectl debug`

Create en ephemeral debug container and even make a copy of a pod adding some debug utilities for debugging purposes
 
# Creating a NodePort for a deploy

* `k expose deploy <deploy-name> --port=<container-port> -type=NodePort 

# Field selectors

* Field selectors let you select Kubernetes objects based on the value of one or more resource fields. 
* Supports operator like =, ==, !=
* example `kubectl get services  --all-namespaces --field-selector metadata.namespace!=default`
