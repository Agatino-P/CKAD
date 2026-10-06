# General

## Setting alias for Kubectl

* Linux `alias k=kubectl`

## Change the editor for K8s commands edit (memorize this)

* `KUBE_EDITOR="nano" k edit svc/<service-name>`
* `alias ke="KUBE_EDITOR='nano' kubectl"` and then  `ke edit pod nginx-6cf46f5666-mbbms`

### personalize nano if needed

```
set tabsize 2
set tabstospaces
set constantshow
set mouse

help ctrl-G
mouse alt-m
search F6
```

```
echo "set tabsize 2
set tabstospaces
"> ~/.nanorc
```

## manifest file for api-server

* Stored in `/etc/kubernetes/manifests/kube-apiserver.yaml` on the control plane node (kubeadm clusters), might need to sudo to edit it
* It's the static pod running the api-server (get pods in `kube-system` namespace)

## Run a temporay pod

* `k run tmp --restart=Never --rm --image=nginx:alpine -i -- curl http://project-plt-6cc-svc.pluto:3333`
* Don't forget pod name (e.g. `tmp`)

# Application Design and Build

## Define, Build, and Modify Container Images

### Image Management - OCI Images

* Open Container Initiative (OCI) images, build mostly from `Dockerfile`

* `docker image build -t <image_name> .` multiple tags are allowed, creating multiple entries with same ImageId
* Image name: `[HOST[:PORT_NUMBER]/]PATH[:TAG]` Host and port of repository (default Docker Hub, `docker.io`, for docker). Default tag: `latest`.
* Docker Hub uses `<Owners_name>/repository[:TAG]` (official images have no owner: `alpine` = `docker.io/library/alpine:latest`)
* know how to dump an image to a OCI compliant tar file, or tar.gz. Use help as needed

#### Dockerfile

* Mind the order of parameters vs args, use help: options go before the image name, everything after the image is the container command and its args (`docker run [OPTIONS] IMAGE [COMMAND] [ARG...]`)
* `--name` when creating a container (`docker run --name <container-name> <image>`)

* Inside DOCKERFILE use json array notation (exec form) for what has to be executed when running the container
* ```CMD ["python", "app.py"]```

## Understanding Jobs and CronJobs

<mark>Exam: if you get a question asking to make sure that a pod runs through to successful completion, it might look like a 'Pod question' but it's a 'Job question', asking to wrap a pod in a Job</mark>

### Imperatively create a job that runs a shell command

`k create job <job_name> --image=busybox -- /bin/sh -c 'echo hello;sleep 30;echo world' `

### When to Use `sh -c`

#### Multiple Commands
* If you need to run multiple commands, you should use sh -c to execute them in a single shell session.
* `command: ["sh", "-c", "echo Hello && echo World"]` This example uses && to chain commands, which requires a shell to interpret.
* `command: ["sh", "-c", "echo 'Starting'; sleep 5; echo 'Done'"]`

#### Environment Variables
* When you need to use environment variables in your command with the shell syntax `$VAR`, sh -c ensures the variables are expanded by the shell.
* `command: ["sh", "-c", "echo $MY_VARIABLE"]`
* Without a shell, Kubernetes itself expands only the `$(VAR)` syntax (see "Using environment variables to define arguments" below).
    
#### Shell Features
* To leverage shell features such as redirection, piping, or subshells.
* `command: ["sh", "-c", "cat /var/log/myapp.log | grep ERROR"]`

### When Not to Use sh -c
* Single, Simple Command: If your command is simple and does not require shell features
* `command: ["echo", "Hello World"]`

### See a job's logs

`k logs job/<job_name>` (shows the logs of one of the Job's Pods)

###  Each outer creates the inner: Cronjob -> Job -> Pod -> Container

# Understanding multi-container Pod design pattenrs

## Sidecar containers

* Sidecar containers in K8s are initContainers with restartPolicy: Always. Search for "Sidecar Containers" in the K8s Docs.

### Volumes

* Storage plugins (CSI drivers) run their node part as system pods managed by a DaemonSet.

###  Storage Class (SC)  <- Persistent Volume (PV)  <- Persistent Volume Claim (PVC) <- `volumes:`  <- `volumeMounts:`

* Storage Class (SC) is cluster scoped, has no namespace
* Persistent Volume (PV) is cluster scoped, has no namespace
* Persistent Volume Claim (PVC) is namespaced (same namespace as the Pod that uses it)

* `kubectl get sc`

###  `Persistent Volumes` (PV) are not referenced directly by the pod: `containers[].volumeMounts[].name` refers to an entry in `spec.volumes[]`, which refers to the PVC, and the PVC is bound to the PV

###  `Persistent Volume Claims` (PVC) Are referred inside the pod in spec.volumes[].persistentVolumeClaim.claimName

### `Ephemeral volumes` are specified inline in the Pod spec, which simplifies application deployment and management.

# Application Deployment

## Deployments

* ((( ( Containers) Pods )  ReplicaSets ) Deployments )

* Under the hood deployments use `ReplicaSet`s to actually ensure that Pods are deployed, desired state vs actual.

### Use `kubectl run` to get  a pod yaml file, to later modify

`kubectl run <pod-name> --image=nginx:alpine --dry-run=client -o yaml > pod.yaml`

### Change an existing label

`kubectl label pod nginx2 app=v2 --overwrite` (without `--overwrite`, an existing key is refused)

### Imperatively Create a service for a deployment

* E.g.: `kubectl expose deploy <deploy-name> --port=<desired port> --target-port=<pod's port> --type=NodePort [--name=<service-desired-name>]`

### Get information about a Deployment

* `kubectl rollout status deployment [deployment-name]`
* `kubectl rollout status -f file.deployment.yml`

### Save configuration for a deployment in order to be able to Rollback

* Ensure your deployment yaml file includes changes to spec.template: only a Pod template change creates a new revision. E.g.: replicas is not enough.
* `kubectl create -f deployment.yml --save-config` Saves the configuration in the resource's annotation `kubectl.kubernetes.io/last-applied-configuration` (so a later `kubectl apply` works as if the resource had been created with `apply`)
* `kubectl apply -f deployment.yml --record=true` (Deprecated)
* `kubectl annotate deployment [name] kubernetes.io/change-cause="Change details" --overwrite=true` (fills the `CHANGE-CAUSE` column of `kubectl rollout history`)
* Note that `create` fails when a resource already exists, `apply` updates it.

### Rollback a Deployment

* `kubectl rollout history deployment <deployment_name>` (list the revisions)
* `kubectl rollout undo -f file.deployment.yml`
* `kubectl rollout undo -f file.deployment.yml --to-revision=2`

## Helm

* It's a package Manager using `Chart`s, `Config`s, `Release`s (a live instance of a chart combined with a specific config). 
* Charts are in `repo`s and there are `hub`s (default is Artifact Hub)
* Even possible to have multiple releases of the same chart at the same time

* `helm search hub` => `helm repo add` => (`helm repo update` if we already have the repo) => `helm search repo` 
  (a chart hosted in an OCI registry is not added as a repo: use its `oci://` reference directly with `helm install` / `helm pull`)
* `helm show values` => `helm pull --untar` 
* `helm install` => `helm list` => `helm status` => `helm upgrade` => `helm uninstall` 
* To find and delete a broken release stuck in pending-upgrade state: `helm -n mercury ls --pending` (works in Helm 3 and Helm 4). Plain `helm ls` hides pending releases in Helm 3 (there `helm -n mercury ls -a` shows all); Helm 4 lists every status by default and has no `-a`. Check `helm version` in the exam environment.

# Application Observability and maintenance
 
## Admission controllers

* You can create a LimitRange object for a namespace and then it's enforced by the LimitRanger admission controller. It applies default container memory/cpu requests/limits for a namespace.
* Stored in `/etc/kubernetes/manifests/kube-apiserver.yaml` under the `spec.containers[].command` there's a command line option: 
* `- --enable-admission-plugins=NamespaceAutoProvision,<another-plugin>,...`
* you can edit the file if you're able to shell into the control plane node (the file is on the node, not inside the pod)
* `kubectl describe pod <kube-apiserver-pod-name> -n kube-system | grep enable-admission-plugins`
* you can also run the `kube-apiserver -h` command, inside the api-server container: `k -n kube-system exec <kube-apiserver-pod-name> -- kube-apiserver -h | grep enable-admission-plugins`
* the plugins are set with the kube-apiserver options `--enable-admission-plugins=<comma separated plugins list>` or `--disable-admission-plugins=<comma separated plugins list>`.

* It's the static pod running the api-server. It's enough to change the yaml to redeploy it (the kubelet recreates the pod), but it might take a moment.

## Api Versions

* `k api-resources --sort-by=name`
* `k api-resources --api-group=rbac.authorization.k8s.io`
* `k explain <deploy>` or any other resource
* `k api-versions` gives all versions for all api groups (as `group/version`), of course you can use grep. A version of a group may not serve every resource of that group: check with `k explain <resource> --api-version=<group>/<version>`

* Alpha versions are enabled via `--runtime-config=<group>/<version>` option of kube-apiserver

### Preferred versions

* First you have to call `kubectl proxy --port=8001 &` so that it stays in the background untill later you kill it: find the PID with `ps -a | grep kubectl` and `kill -9 <pid>`
* Then `curl localhost:8001/apis` or `curl localhost:8001/apis/<name of api group>`  
  Preferred Version is in the payload

## Implementing Probes and healthchecks

* On Liveness probe failure, the container gets killed and then restarted according to the Pod's restartPolicy (default Always). Meant for unrecoverable issues.
* On Readiness probe failure, the container is marked as unready, removing it from service load balancers, but the container is not restarted. Meant for transient issues.

## Using Provided Tools to Monitor Kubernetes Applications

`kubectl top` once Metrics Server is enabled

## Debugging Kubernetes

* `kubectl get events`
* `kubectl get pods -o jsonpath="{.items[*].spec.containers[*].image}"` (for a single pod: `kubectl get pod <pod-name> -o jsonpath="{.spec.containers[*].image}"`)
* If the pod is created but not acting properly, check the yaml for mistakes.  
  A mistyped field name is not ignored: kubectl validates by default (`--validate=strict`), so `kubectl apply -f mypod.yaml` with `command` misspelled as `commnd` fails with `strict decoding error: unknown field "spec.containers[0].commnd"`. `--validate=warn` only warns, `--validate=ignore` (or `false`) accepts the file and silently drops the unknown field.

# Application Environment, Configuration and Security

* Note mostly how names (singlular, plural, lower and upper case) have to match

```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: applications.example.com # has to be <plural>.<group>
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
    served: true  # served=true means usable version
    storage: true # storage=true means this is the version used when the objects are persisted (stored in etcd)
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

## RBAC

### Role and ClusterRole

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role #if ClusterRole, than namespace below is omitted
metadata:
  namespace: default
  name: pod-reader
rules:
- apiGroups: [""] # "" indicates the core API group
  resources: ["pods"]
  verbs: ["get", "watch", "list"]
```

#### RoleBinding and ClusterRoleBinding

```yaml
# This role binding allows "jane" to read pods in the "default" namespace.
# You need to already have a Role named "pod-reader" in that namespace.
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding    # or ClusterRoleBinding (then namespace below is omitted)
metadata:
  name: read-pods
  namespace: default
subjects:            # You can specify more than one "subject"
- kind: User         # User, ServiceAccount or Group
  name: jane         # "name" is case sensitive
  apiGroup: rbac.authorization.k8s.io   # for kind: ServiceAccount, omit apiGroup and set the ServiceAccount's namespace
roleRef:             # "roleRef" specifies the binding to a Role / ClusterRole
  kind: Role         # Role or ClusterRole (a RoleBinding to a ClusterRole grants its permissions only in the RoleBinding's namespace)
  name: pod-reader   # this must match the name of the Role or ClusterRole you wish to bind to
  apiGroup: rbac.authorization.k8s.io
```

## Understand and Define Resource Requirements, Limits ands Quotas

* `Requests` and `Limits` are set for each container of a Pod (`spec.containers[].resources`), or for the whole Pod (`spec.resources`: Pod-level resources, cpu/memory/hugepages; feature gate `PodLevelResources`, beta and enabled by default). If a container exceeds its memory limit, the kernel may kill it (OOMKilled); a container exceeding its CPU limit is throttled, not killed.
* `Quotas` (ResourceQuota) are for `Namespaces`

## Understanding ConfigMaps

* ConfigMaps should not contain secrets
<mark>EXAM: In the exam they might try to induce into error by providing secrets and not secrets data together, you have to put them in ConfigMaps and Secrests</mark>
 
* The key and values in a ConfigMap `data` can only be strings.
* If we want a value with boolean values we need to quote the values, like "true" or "false". Same for numbers, like "100".

## Using environment variables to define arguments (environment variables migh of course come from a ConfigMap)
```yaml 
env:
- name: MESSAGE
  value: "hello world"
command: ["/bin/echo"]
args: ["$(MESSAGE)"]
```

## Understand Service Accounts

* A service account is a type of non-human account that, in Kubernetes, provides a distinct identity in a Kubernetes cluster.
* Instead of passwords, ServiceAccounts use tokens.
* ServiceAccounts let application Pods, system components, and entities inside and outside the cluster use a specific ServiceAccount's credentials to identify as that ServiceAccount and access the Kubernetes API.
* ServiceAccounts are Namespaced: Each service account is bound to a Kubernetes namespace. 
* Every namespace gets a default ServiceAccount upon creation.

### Using a ServiceAccount

* Create it, bind it to a `Role` (or `ClusterRole`) via `RoleBinding`, bind it to a Pod via `spec.serviceAccountName`

### getting secrets decoded

* `k get secret <secretname> -oyaml` gives the secrets base64-encoded; decode one value with `k get secret <secretname> -o jsonpath='{.data.<key>}' | base64 -d`
* `k describe secret <secretname>` does not show the values of a generic Secret, only their size in bytes. Exception: for a ServiceAccount token Secret (`type: kubernetes.io/service-account-token`) it shows the `token` already decoded.

### ServiceAccountsSecrets

* Secrets won't be created automatically for ServiceAccounts, but it's possible to create a Secret manually (`type: kubernetes.io/service-account-token`) and attach it to a ServiceAccount by setting the annotation `kubernetes.io/service-account.name` on the Secret.
* to get annotations `k -n neptune get secrets -oyaml | grep annotations -A 1` # shows secrets with first annotation
If a Secret belongs to a ServiceAccont, it'll have the annotation kubernetes.io/service-account.name.

## Understand Security Contexts

* A security context defines privilege and access control settings for a Pod or Container by adding to their spec section as `spec.securityContext...` or `spec.containers[x].securityContext...`

* Note that when configuring Linux capabilities, the opposite of `add:` capabilities is `drop:`
* When setting security context for volumes (`fsGroup`), that has to go under the Pod section `spec.securityContext`, not the container one

# Services and Networking

## Demonstrate Basic Understanding of Network Policies

* The Pods connect to the `Pod network` created by the `Network plugin`.
* Network policies only work if your network plugin supports them.
* Network policies are namespaced: a NetworkPolicy selects (`podSelector`) Pods only in its own namespace. If you don't specify a namespace when creating it, it goes in the current namespace of the context (normally `default`).

### Full DNS for a service

* Kubernetes provides built-in DNS for service discovery, and the full DNS name for a service can be constructed as follows: `<service-name>.<namespace>.svc.cluster.local`
* or even shorter `<service-name>.<namespace>`

### Pod isolation

* By default, a pod is non-isolated for ingress (egress); all inbound (outbound) connections are allowed. A pod is isolated for ingress (egress) if there is any NetworkPolicy that both selects the pod and has "Ingress" ("Egress")  in its `spec.policyTypes`.

## Exam question logical OR vs logical AND

* In a `from:` (or `to:`) list, a `podSelector` and a `namespaceSelector` inside the same array entry (one `-`) go as AND. If they are two separate `-` entries, that counts as OR.

## Use Ingress Rules to Expose Applications 

* Ingress is only for HTTP and HTTPS (typically ports 80 and 443); other protocols or ports are exposed with a Service of type NodePort or LoadBalancer
