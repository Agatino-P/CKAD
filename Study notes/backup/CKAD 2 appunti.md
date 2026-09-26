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

# General hints

* Use spaces when you edit, not tabs

## Running multiple terminals using tmux

https://github.com/tmux/tmux/wiki/Getting-Started

* most important Ctrl-b ? for help

# Commands to memorize

## Alias

* alias k="kubectl"

## K8s clusters in config

### view current config

`k config view`

### View in which context we are

`k config current-context`

### creates a new entry in kubeconfig under the clusters section with a cluster called test pointing towards https://127.0.0.1:52807

`kubectl config set-cluster test --server=https://127.0.0.1:52807`

### creates a new context in kubeconfig called test and tells that context to point to a cluster called test

`kubectl config set-context test --cluster=test`

### changes the the current context in kubeconfig to a context called test (which you just created).

`kubectl config use-context test`

### remove the namespace property setting from   the docker-desktop context
k config unset contexts.docker-desktop.namespace

## K8s namespace 

### Create

`k create ns <namespace-name>`

### Check

k get ns 

### Set

kubectl config set-context --current --namespace=<nameOfTheNamespace>

### Specify namespace manually

`-n <namespace name>` option on the command line of each command

## Change the editor for K8s commands edit

`KUBE_EDITOR="nano" k edit svc/<service-name>`

## Create using all yaml files in current folder

`k create -f ./`

# Create

As an alternative to writing yaml

## Create without yaml

`k create ... (e.g.: deploy)`

## Create a service for a deployment

`k expose deploy <deploy-name`> --port=<desired port> --target-port=<pod's port> --type=NodePort --name=<service-desired-name>

* Note that this will crerate a NodePort as specified but with a random external port in the allowed range (30000-32767) which we can get from k get svc

## Create a temporary pod as an interactive TTY using image alpine and set restart to Never, named temp-pod

`k run -it --restart=Never -image=alpine temp-pod`

## Dry-run to create yaml imperatively

`k create deploy <deploy-name> --image=<image>[:tag] --dry-run=client -o yaml > deploy.yaml` 



# Modify a deployment from the command line (for example if you created it without a yaml)

`k edit deploy/<deploy-name>` will open the deployment in the KUBE_EDITOR

# Scale a deployment from the command line 

`k scale deploy <deployment-name> --replicas=<number of pods>` 

# Deployments and rolling updates

## spec: properties

```yaml
spec:
  minReadySeconds: 1
  progressDeadlineSeconds: 60
  revisionHistoryLimit: 5
```

* `minReadySeconds`

Seconds new Pod should be ready to be considered
healthy (default 0)

* `progressDeadlineSeconds`

Seconds to wait before reporting stalled Deployment (default 600)

* `revisionHistoryLimit`

Number of ReplicaSets that can be rolled back (default 10)

## strategy: properties

```yaml
strategy:
   type: RollingUpdate
   rollingUpdate:
     maxUnavailable: 1
```

*`type` 

RollingUpdate (default) or Recreate

* `maxSurge` 1 Max Pods that can exceed the replicas count (25%)
* `maxUnavailable` Max Pods that are not operational (25%)

 # Saving the configuration during a deployment

 `kubectl create –f file.deployment.yml --save-config`

 Saves the configuration in resource's annotations

 # Deployment Updates & Rollout History

* **Triggering a Revision:** A new rollout revision is created *automatically* when the Pod template (`spec.template`) is modified.  
 Scaling or metadata changes do not generate a new revision.
* **Where History Lives:** History is inherently maintained by the older ReplicaSets preserved by the Deployment controller. 
* **Recording Changes (Replaces deprecated `--record`):** Annotate the deployment to manually populate the `CHANGE-CAUSE` column in the rollout history.

```bash
kubectl annotate deployment <deployment-name> kubernetes.io/change-cause="Change details" --overwrite
```

## Checking Status & History

**Check current rollout status:**
```bash
kubectl rollout status deployment/<deployment-name>
```

**View all revisions:**
```bash
kubectl rollout history deployment/<deployment-name>
```

**View details of a specific revision:**
```bash
kubectl rollout history deployment/<deployment-name> --revision=2
```

## Rollbacks (Undo)

**Rollback to the immediately previous revision:**
```bash
kubectl rollout undo deployment/<deployment-name>
```

**Rollback to a specific historical revision:**
```bash
kubectl rollout undo deployment/<deployment-name> --to-revision=2
```

# Jq

 Double quotes to escape slash and dash

* kubectl get deploy <deploy-name> -o json | jq '.metadata.annotations."kubernetes.io/change-cause"'  
or
* kubectl get deploy <deploy-name> -o json | jq '.metadata.annotations["kubernetes.io/change-cause"]'

# Helm
 
## Concepts

### Chart

Bundle of information used to create an instance of a Kubernetes application

### Config

Configuration information thatt can be merged into a chart to create a releasable object

### Release

Running instance of a chart (combined with a config) inside K8s

### Library

* Sort of "functions" short "blocks" that can be used across multiple charts

### Hub (defaults to Artifact Hub)

* hubs give repository info

### Repository

* repo's have charts

## Commands

### `helm -h`

* -h also works with subcommands

### `helm search hub` (defaults to Artifact Hub)

* Lists repos that you can then add locally
* --list-repo-url option  gives you repo's full URL but is hard to read in table format
* default is table format but you can do `-o yaml` or `-o json`
* you find the chart version and the app version (in simple case it looks like the image version)
* notice that the chart is identified with <repo local name>/<chart name>

###  `helm repo add <repo name> <repo url>`

### helm repo list

### `helm search repo`

* for charts, in our repos

`helm search repo  <chart>`

* given the newest versions, if you  want them all `--versions`

* to search for the option `helm search repo --help`

* to search for a version, `helm search repo <chart-name> --version=<version-number>`

* to update all repos, `helm repo update`

* to update a repo, `helm repo update <repo-name>`

### `helm show values`
 
* (overridable) values inside chart

### `helm pull --untar`

* "Unzip" it into a folder
* Allows you to look inside the chart.
* To look for values or whatever else

### `helm install`

* in this phase you can override value defaults and supply your own
* either via a file or with a `--set` command

### `helm list`

* lists installations

### `helm status`

### `helm upgrade`

### `helm uninstall`

