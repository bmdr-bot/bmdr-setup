# BMDR Setup - Kubernetes Deployment

Deploy to your existing Kubernetes cluster.

## Prerequisites

- kubectl configured for your cluster
- Ingress controller (nginx recommended)
- cert-manager (for TLS)

## Deploy

```bash
cd k8s/

# Create namespace and deploy everything
kubectl apply -k .

# Or step by step:
kubectl apply -f namespace.yaml
kubectl apply -f secrets.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f ingress.yaml
```

## Update Image

```bash
# Set new image tag
kubectl set image deployment/bmdr-app app=ghcr.io/bmdr-bot/bmdr-setup:v1.0.0 -n bmdr-setup

# Or use kustomize
kustomize edit set image ghcr.io/bmdr-bot/bmdr-setup:v1.0.0
kubectl apply -k .
```

## Check Status

```bash
kubectl get all -n bmdr-setup
kubectl logs -f deployment/bmdr-app -n bmdr-setup
```

## Access Locally

```bash
kubectl port-forward svc/bmdr-app 8080:80 -n bmdr-setup
# Open http://localhost:8080
```
