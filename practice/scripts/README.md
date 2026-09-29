# Scripts

Every script of the practice program, runnable from any directory.

```bash
practice/scripts/setup.sh        # from a fresh clone: tools, submodules, lab, checks
practice/scripts/lab-up.sh       # cluster, metrics-server, ingress-nginx
practice/scripts/lab-check.sh    # StorageClass, kubectl top, NetworkPolicy enforcement, Ingress, helm
practice/scripts/lab-down.sh     # delete the cluster
practice/scripts/dojo.sh         # ckad-dojo setup, score and cleanup against the lab
practice/scripts/build-index.py  # regenerate practice/EXERCISE_INDEX.md from the sources
```

`shim/docker` forwards to podman for the ckad-dojo scripts, which need a `docker` command to start.\
Only `dojo.sh` puts it on PATH.
