# TODO

- [ ] prod values: add `charts/my-app/values-prod.yaml` with `replicaCount: 3` and
      `helm.valueFiles: [values-prod.yaml]` in `argocd/my-app.yaml`
- [ ] secret: install External Secrets Operator, a `SecretStore` (fake provider) and an
      `ExternalSecret` for `my-app-secret`, wire `APP_PASSWORD` into the Deployment
- [ ] release loop: build and push `1.1.0`, bump `image.tag` in `values.yaml`, commit,
      watch ArgoCD roll it out
- [ ] README: write the steps of the diagram as done here
- [ ] drift: change the app by hand, e.g. `kubectl -n my-app scale deploy/my-app --replicas=5`
      or `kubectl apply` of an edited Deployment, then watch ArgoCD show OutOfSync and
      put it back. Needs `selfHeal: true` under `syncPolicy.automated` in
      `argocd/my-app.yaml`, without it ArgoCD only reports the drift
