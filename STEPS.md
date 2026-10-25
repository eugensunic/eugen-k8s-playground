# eugen-k8s-playground

Local version of the standard flow: build an image, push it to a registry, describe the
app in a Helm chart in git, let ArgoCD sync git into Kubernetes.

```
app/                      the application and its Dockerfile
charts/my-app/            Helm chart: Chart.yaml, values.yaml, templates/
argocd/values.yaml        settings for ArgoCD itself
argocd/my-app.yaml        the ArgoCD Application: which repo, which path, which namespace
```

Stand-ins: a `registry` container plays Artifactory, kind plays the cluster.

## 1. Cluster and registry

```sh
kind create cluster --name eugen-k8s-playground
docker run -d --restart=always -p 127.0.0.1:5001:5000 --network bridge --name docker-playground-registry registry:3
```

Tell every node that `localhost:5001` means the registry container (inside a node,
localhost is the node itself):

```sh
for node in $(kind get nodes --name eugen-k8s-playground); do
  docker exec "$node" mkdir -p /etc/containerd/certs.d/localhost:5001
  echo '[host."http://docker-playground-registry:5000"]' | docker exec -i "$node" cp /dev/stdin /etc/containerd/certs.d/localhost:5001/hosts.toml
done
docker network connect kind docker-playground-registry
```

## 2. Build and push the image

```sh
docker build --tag localhost:5001/data-anonimization-app:1.0.0 app
docker push localhost:5001/data-anonimization-app:1.0.0
curl localhost:5001/v2/data-anonimization-app/tags/list
```

`localhost:5001` is the registry, `data-anonimization-app` the repository, `1.0.0` the tag.

## 3. The chart

`charts/my-app/values.yaml` holds the image and the replica count. The templates turn
them into a Deployment and a Service. Render without touching the cluster:

```sh
helm template my-app charts/my-app
```

The image line in the rendered Deployment is what the node will pull. Helm never pulls
images, it only writes the address.

## 4. ArgoCD

Install, with polling set to 60 seconds in `argocd/values.yaml`:

```sh
helm repo add argo https://argoproj.github.io/argo-helm
helm upgrade --install argocd argo/argo-cd -n argocd --create-namespace -f argocd/values.yaml
```

Web UI:

```sh
kubectl -n argocd port-forward svc/argocd-server 8443:443
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath='{.data.password}' | base64 -d; echo
```

https://localhost:8443, user `admin`, accept the self-signed certificate.

## 5. Sync git into the cluster

The repo must be on GitHub, ArgoCD clones it from there. Then hand it the Application:

```sh
kubectl apply -f argocd/my-app.yaml
kubectl -n argocd get applications -w        # Synced, Healthy
kubectl -n my-app get pods                   # 2 pods Running
```

See the app:

```sh
kubectl -n my-app port-forward svc/my-app 8080:80
open http://localhost:8080
```

## 6. Release a new version

```sh
# edit app/Dockerfile: ENV APP_VERSION=1.1.0
docker build --tag localhost:5001/data-anonimization-app:1.1.0 app
docker push localhost:5001/data-anonimization-app:1.1.0
# edit charts/my-app/values.yaml: tag: "1.1.0"
git commit -am "release 1.1.0" && git push
kubectl -n my-app get pods -w                # new pods within a minute
```

The commit is the deploy. Nobody runs helm or kubectl against the app namespace.

## Teardown

```sh
kind delete cluster --name eugen-k8s-playground
docker rm -f docker-playground-registry
```
