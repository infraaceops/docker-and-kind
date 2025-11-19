## dev → qa → prod, using Kustomize overlays, GitHub Actions, and repository dispatch for promotion.
```
base/
  configmap/configmap.yaml
  deployment/deployment.yaml
  service/service.yaml
  kustomization.yaml

development/
  kustomization.yaml
  manifests/configmap.yaml
  overlays/

pre-releases/
  kustomization.yaml
  manifests/configmap.yaml
  overlays/
  replicas.yaml

releases/
  kustomization.yaml
  manifests/configmap.yaml
  overlays/
  replicas.yaml

```
base/ → common resources

development/ → dev environment overlay

pre-releases/ → QA/Pre-release overlay

releases/ → Prod overlay

---

## Step 1 — Strategy Overview

Step 1: Developer pushes changes → development/** or base/**

Step 2: Deployment workflow runs → deploys development overlay to dev cluster using Kustomize

Step 3: Rollout check → wait until the deployment stabilizes

Step 4: On success → trigger auto-promotion workflow via repository_dispatch

Step 5: Auto-promotion workflow → creates PR to dev, qa, or prod branch based on folder changed

Step 6: Manual review or auto-merge PR → PR is merged → triggers next environment deployment if desired

---
## Step 2 — Auto-Promotion Rules

Source Folder	Deploy Target Cluster	Target Branch	Next Auto-Promotion

development/**	Dev Cluster	dev	Pre-release/QA

pre-releases/**	QA Cluster	qa	Releases/Prod

releases/**	Prod Cluster	prod	None

base/**	Dev Cluster	dev	Pre-release/QA

---

## Step 3 — Workflow Setup
### A. Deploy Workflow (deploys overlay + triggers promotion)

Trigger: push on development/**, pre-releases/**, releases/**, base/**

#### Steps:

Detect which folder changed → set kustomize_path

kustomize build $kustomize_path | kubectl apply -f -

Wait for rollout success

Trigger repository_dispatch → payload: { "source": "./development" }

### B. Auto-Promotion Workflow

Trigger: repository_dispatch type: k8s-deploy-success

#### Steps:

---

3️⃣ Step-by-Step Testing Strategy
Step 1 — Dev Deployment Test

Make a change in development/manifests/configmap.yaml

Push to main branch

Deploy workflow triggers → deploys to dev cluster

Rollout logs appear → check kubectl get deploy

Step 2 — Dev Promotion PR

After successful rollout, repository dispatch triggers auto-promotion workflow

PR created: auto-promote-dev-<run_number> → target branch: dev

Merge PR → dev branch updated

Step 3 — QA Promotion Test

Make change in pre-releases/manifests/configmap.yaml

Push → deploy workflow deploys QA overlay

Rollout success → triggers auto-promotion → PR to qa branch

Merge PR → QA branch updated

Step 4 — Prod Promotion Test

Make change in releases/manifests/configmap.yaml or merge QA PR

Push → deploy workflow deploys Prod overlay

Rollout success → triggers auto-promotion → PR to prod branch

Merge PR → Production updated





## Pre-Req to install docker and kind
``` bash
sudo apt install docker.io
sudo snap install kubectl --classic
curl -Lo ./kind https://github.com/kubernetes-sigs/kind/releases/download/v0.20.0/kind-linux-amd64 # Replace v0.20.0 with the latest release version if desired
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind
```

## Commands to interact docker
``` bash
cd docker/
docker build -t shadabshah1680/master-project:http-server .
docker run -it  -p 80:80 shadabshah1680/master-project:http-server
docker push shadabshah1680/master-project:http-server
```

## Commands to interact with kind
``` bash
kubectl apply -f .
kubectl port-forward -n http-server svc/http-server-service 8080:83
ssh -R 80:localhost:8080 ssh.localhost.run
![alt text](image.png)
```
Please look for link  https://c2e0a26115c0fb.lhr.life


