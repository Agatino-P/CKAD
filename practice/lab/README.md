# Lab

The kind cluster definition for the exercises in `practice/EXERCISE_INDEX.md`.\
The scripts that create, check and delete it are in `practice/scripts/`.

`kind-cluster.yaml` pins the node image to the Kubernetes minor version the exam runs on.\
Each folder under `addons/` holds an unmodified upstream manifest and a `kustomization.yaml` whose comments say why it is patched.
