# eugen-playground

Local Kubernetes sandbox: kind + ArgoCD + External Secrets Operator + Helm.

## Prereqs

Docker Desktop (or OrbStack) running, then:

```sh
brew install kind kubectl helm
```

## Up

```sh
./setup.sh
```

Creates a kind cluster `eugen-playground`, installs ArgoCD and ESO, prints the ArgoCD admin password.

ArgoCD UI:

```sh
kubectl -n argocd port-forward svc/argocd-server 8080:443
# https://localhost:8080  user: admin
```

## Play

```sh
# Helm: install the demo chart directly
helm install hello charts/hello

# ESO: fake-provider SecretStore + ExternalSecret (no cloud needed)
kubectl apply -f eso/
kubectl get externalsecret,secret hello-credentials

# ArgoCD: deploy guestbook from a public repo via GitOps
kubectl apply -f argocd/guestbook-app.yaml
```

## Down

```sh
kind delete cluster --name eugen-playground
```
