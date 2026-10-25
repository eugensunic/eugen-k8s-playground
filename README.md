# eugen-k8s-playground

Local demo of the flow: docker build, push to a registry, Helm chart in git, ArgoCD
syncs git into Kubernetes. Step by step in [STEPS.md](STEPS.md).

## ArgoCD web UI

```sh
kubectl -n argocd port-forward svc/argocd-server 8443:443
```

- URL: https://localhost:8443 (accept the self-signed certificate)
- User: `admin`
- Password:

```sh
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath='{.data.password}' | base64 -d; echo
```
