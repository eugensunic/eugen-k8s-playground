#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

CLUSTER=eugen-playground

if ! kind get clusters | grep -qx "$CLUSTER"; then
  kind create cluster --name "$CLUSTER" --config kind-config.yaml
else
  echo "cluster $CLUSTER already exists, skipping create"
fi

kubectl config use-context "kind-$CLUSTER"

helm repo add argo https://argoproj.github.io/argo-helm >/dev/null
helm repo add external-secrets https://charts.external-secrets.io >/dev/null
helm repo update >/dev/null

helm upgrade --install argocd argo/argo-cd \
  --namespace argocd --create-namespace --wait

helm upgrade --install external-secrets external-secrets/external-secrets \
  --namespace external-secrets --create-namespace --wait

echo
echo "ArgoCD admin password:"
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath='{.data.password}' | base64 -d
echo
echo
echo "UI: kubectl -n argocd port-forward svc/argocd-server 8080:443  ->  https://localhost:8080"
