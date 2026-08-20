# eugen-playground

Local Kubernetes sandbox to experiment with the same stack we run in GCP —
but disposable, offline, and free.

## What's in here

| Piece | What it is | Why it's here |
|---|---|---|
| **kind** | Kubernetes cluster running inside Docker containers | Real k8s API in ~30s, deleted in 5s — no cloud |
| **ArgoCD** | GitOps controller: watches a git repo, applies its manifests to the cluster | Same tool that deploys our real clusters |
| **ESO** | External Secrets Operator: syncs secrets from an external store into k8s Secrets | Same flow as GCP Secret Manager → cluster, here with a `fake` provider (hardcoded values, no cloud login) |
| **charts/hello** | Minimal Helm chart (nginx + Service) | Playground for Helm templating; can mount the ESO-synced secret |

## How the pieces fit

```
git repo ──(ArgoCD watches)──> cluster <──(ESO writes k8s Secrets)── secret store
                                  ▲
                        helm install (you, directly)
```

## Prereqs

Docker Desktop (or OrbStack) running, then: `brew install kind kubectl helm`

## Up

```sh
./setup.sh
```

Creates the kind cluster `eugen-playground`, installs ArgoCD + ESO via Helm,
prints the ArgoCD admin password.

ArgoCD UI: `kubectl -n argocd port-forward svc/argocd-server 8080:443`
→ https://localhost:8080 (user `admin`).

## Play

**Helm** — install the demo chart, then poke at `values.yaml` / templates and `helm upgrade`:

```sh
helm install hello charts/hello
```

**ESO** — apply the fake store + ExternalSecret, watch it materialize a k8s Secret:

```sh
kubectl apply -f eso/
kubectl get externalsecret,secret hello-credentials   # wait for SecretSynced
```

Then set `useEsoSecret: true` in `charts/hello/values.yaml` and `helm upgrade hello charts/hello` —
the pod now gets `HELLO_PASSWORD` from the ESO-synced secret. That's the full
store → ESO → k8s Secret → pod chain from the real setup.

**ArgoCD** — deploy an app the GitOps way (from argoproj's public example repo):

```sh
kubectl apply -f argocd/guestbook-app.yaml
```

Watch it sync in the UI; delete a guestbook pod and watch selfHeal recreate it.

## Down

```sh
kind delete cluster --name eugen-playground
```

Everything is throwaway — recreate with `./setup.sh` anytime.
