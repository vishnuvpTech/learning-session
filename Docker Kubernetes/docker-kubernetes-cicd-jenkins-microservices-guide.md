# Practical Guide: Docker, Kubernetes, CI/CD, Jenkins & Microservice Setup

A hands-on reference for containerizing, orchestrating, automating, and architecting Python (FastAPI/Django) applications as microservices.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Docker](#2-docker)
3. [Kubernetes](#3-kubernetes)
4. [CI/CD Concepts](#4-cicd-concepts)
5. [Jenkins](#5-jenkins)
6. [Microservice Setup](#6-microservice-setup)
7. [End-to-End Reference Architecture](#7-end-to-end-reference-architecture)
8. [Troubleshooting & Common Pitfalls](#8-troubleshooting--common-pitfalls)
9. [Appendix — Command Cheat Sheets](#9-appendix--command-cheat-sheets)

---

## 1. Introduction

These five topics form one continuous pipeline:

```
 Code  →  Docker (package)  →  Jenkins/CI (build, test, scan)  →  CD (deploy)  →  Kubernetes (run & scale)
                                                                                        ↑
                                                                  Microservice architecture (design)
```

- **Docker** packages an app and its dependencies into a portable, reproducible unit.
- **Kubernetes** runs, scales, heals, and network-connects many containers across a cluster.
- **CI/CD** automates the build → test → deploy pipeline so every commit is validated and shippable.
- **Jenkins** is one popular engine for implementing that CI/CD pipeline (self-hosted, highly extensible).
- **Microservice architecture** is the application design pattern that these tools are built to support — many small, independently deployable services instead of one large monolith.

> **Tip:** Learn them in this order — Docker first (you can't do anything else without a container), then Kubernetes (run containers at scale), then CI/CD/Jenkins (automate the process), then microservices (apply the pattern once the tooling is second nature).

---

## 2. Docker

### 2.1 Core Concepts

| Term | Meaning |
|---|---|
| **Image** | Immutable, layered filesystem snapshot — the "class" |
| **Container** | A running instance of an image — the "object" |
| **Dockerfile** | Recipe for building an image |
| **Registry** | Where images are stored (Docker Hub, ECR, ACR, GCR/Artifact Registry) |
| **Volume** | Persistent storage that outlives a container |
| **Network** | Virtual network connecting containers |

### 2.2 Writing a Production Dockerfile (Multi-Stage Build)

Multi-stage builds keep the final image small by discarding build-time dependencies (compilers, dev headers).

**FastAPI:**
```dockerfile
# ---------- Stage 1: build dependencies ----------
FROM python:3.12-slim AS builder
WORKDIR /app
ENV PIP_NO_CACHE_DIR=1
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# ---------- Stage 2: runtime ----------
FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PATH=/root/.local/bin:$PATH

# Run as non-root
RUN useradd -m appuser
COPY --from=builder /root/.local /root/.local
COPY . .
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s CMD curl -f http://localhost:8000/health || exit 1

CMD ["gunicorn", "app.main:app", "-k", "uvicorn.workers.UvicornWorker", \
     "-w", "4", "-b", "0.0.0.0:8000", "--timeout", "60"]
```

**Django:**
```dockerfile
FROM python:3.12-slim AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PATH=/root/.local/bin:$PATH
RUN apt-get update && apt-get install -y --no-install-recommends libpq5 && rm -rf /var/lib/apt/lists/*
RUN useradd -m appuser
COPY --from=builder /root/.local /root/.local
COPY . .
RUN python manage.py collectstatic --noinput
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s CMD curl -f http://localhost:8000/health || exit 1

CMD ["gunicorn", "myproject.wsgi:application", "-w", "4", "-b", "0.0.0.0:8000", "--timeout", "60"]
```

> **Warning:** Never run the container process as `root` in production, and never `COPY .env` or bake secrets into an image layer — anyone with `docker history` or image pull access can extract them.

### 2.3 `.dockerignore`

```
__pycache__/
*.pyc
.git
.env
.venv
*.sqlite3
node_modules
tests/
```

### 2.4 Build & Run

```bash
docker build -t myapp:1.0 .
docker run -d --name myapp -p 8000:8000 --env-file .env myapp:1.0
docker logs -f myapp
docker exec -it myapp /bin/sh
docker stop myapp && docker rm myapp
```

### 2.5 docker-compose for Local Multi-Container Dev

```yaml
# docker-compose.yml
version: "3.9"

services:
  web:
    build: .
    ports:
      - "8000:8000"
    env_file: .env
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    volumes:
      - .:/app        # live-reload in dev only — remove for prod images

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: myapp_dev
      POSTGRES_USER: appuser
      POSTGRES_PASSWORD: devpassword
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U appuser"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  mongo:
    image: mongo:7
    environment:
      MONGO_INITDB_ROOT_USERNAME: appuser
      MONGO_INITDB_ROOT_PASSWORD: devpassword
    volumes:
      - mongodata:/data/db

volumes:
  pgdata:
  mongodata:
```
```bash
docker compose up -d --build
docker compose logs -f web
docker compose exec web python manage.py migrate
docker compose down -v      # -v also removes volumes
```

### 2.6 Image Size & Security Best Practices

- Use `-slim` or `-alpine` base images (verify glibc-vs-musl compatibility with `alpine` for compiled deps like `psycopg2`).
- Combine `RUN` layers with `&&` and clean apt cache in the same layer to avoid bloated intermediate layers.
- Pin base image tags to a digest or specific version — never `latest` in production.
- Scan images before pushing:
```bash
docker scout cves myapp:1.0
# or
trivy image myapp:1.0
```
- Sign and verify images in regulated environments (`cosign sign`, `cosign verify`).

---

## 3. Kubernetes

### 3.1 Core Objects

| Object | Purpose |
|---|---|
| **Pod** | Smallest deployable unit — one or more tightly-coupled containers |
| **Deployment** | Declaratively manages a set of replica Pods, handles rolling updates |
| **Service** | Stable network endpoint (ClusterIP/NodePort/LoadBalancer) in front of Pods |
| **Ingress** | HTTP(S) routing into the cluster (host/path-based) |
| **ConfigMap** | Non-sensitive configuration, injected as env vars or files |
| **Secret** | Sensitive configuration (base64-encoded, ideally backed by an external secret store) |
| **HorizontalPodAutoscaler (HPA)** | Auto-scales replica count based on CPU/memory/custom metrics |
| **Namespace** | Logical isolation boundary (e.g., `dev`, `staging`, `prod`) |
| **PersistentVolumeClaim (PVC)** | Requests durable storage for stateful workloads |

### 3.2 Deployment Manifest (FastAPI/Django)

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  namespace: prod
  labels:
    app: myapp
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
        - name: myapp
          image: myregistry.example.com/myapp:1.0.0
          ports:
            - containerPort: 8000
          envFrom:
            - configMapRef:
                name: myapp-config
            - secretRef:
                name: myapp-secrets
          resources:
            requests:
              cpu: "250m"
              memory: "256Mi"
            limits:
              cpu: "500m"
              memory: "512Mi"
          readinessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 10
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 15
            periodSeconds: 20
```

### 3.3 Service + Ingress

```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-svc
  namespace: prod
spec:
  selector:
    app: myapp
  ports:
    - port: 80
      targetPort: 8000
  type: ClusterIP
---
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
  namespace: prod
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  ingressClassName: nginx
  tls:
    - hosts: ["myapp.example.com"]
      secretName: myapp-tls
  rules:
    - host: myapp.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: myapp-svc
                port:
                  number: 80
```

### 3.4 ConfigMap & Secret

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: myapp-config
  namespace: prod
data:
  DJANGO_SETTINGS_MODULE: "myproject.settings.prod"
  DEBUG: "False"
```
```bash
kubectl create secret generic myapp-secrets \
  --from-literal=SECRET_KEY='<value>' \
  --from-literal=DB_PASSWORD='<value>' \
  -n prod
```
> **Tip:** For production, back Secrets with **External Secrets Operator** pulling from AWS Secrets Manager / Azure Key Vault / GCP Secret Manager rather than storing raw base64 Secrets in Git.

### 3.5 Horizontal Pod Autoscaler

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
  namespace: prod
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 3
  maxReplicas: 15
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 65
```

### 3.6 Deploying & Managing

```bash
kubectl apply -f deployment.yaml -f service.yaml -f ingress.yaml -f hpa.yaml
kubectl get pods -n prod -w
kubectl rollout status deployment/myapp -n prod
kubectl rollout undo deployment/myapp -n prod          # rollback
kubectl logs -f deploy/myapp -n prod
kubectl exec -it deploy/myapp -n prod -- /bin/sh
kubectl scale deployment/myapp --replicas=5 -n prod
```

### 3.7 Helm (Templated, Reusable Manifests)

Helm packages the manifests above into a reusable, versioned "chart" with environment-specific values.

```
myapp-chart/
├── Chart.yaml
├── values.yaml
├── values-staging.yaml
├── values-prod.yaml
└── templates/
    ├── deployment.yaml
    ├── service.yaml
    ├── ingress.yaml
    └── hpa.yaml
```
```yaml
# values.yaml
image:
  repository: myregistry.example.com/myapp
  tag: "1.0.0"
replicaCount: 3
resources:
  requests: { cpu: 250m, memory: 256Mi }
  limits: { cpu: 500m, memory: 512Mi }
```
```bash
helm install myapp ./myapp-chart -f values-prod.yaml -n prod
helm upgrade myapp ./myapp-chart -f values-prod.yaml -n prod
helm rollback myapp 1 -n prod
```

---

## 4. CI/CD Concepts

### 4.1 The Pipeline Stages

```
Commit → Lint/Static Analysis → Unit Tests → Build Image → Security Scan
       → Push to Registry → Deploy to Staging → Integration Tests
       → Manual/Auto Approval → Deploy to Production → Smoke Tests
```

| Stage | Purpose | Typical Tools |
|---|---|---|
| Lint | Enforce code style, catch obvious bugs | `flake8`, `ruff`, `black --check` |
| Unit test | Validate logic in isolation | `pytest`, `pytest-django`, coverage |
| Build | Produce a deployable artifact | `docker build` |
| Scan | Catch known CVEs before shipping | `trivy`, `docker scout`, `snyk` |
| Push | Publish the versioned artifact | ECR / ACR / GCR / Docker Hub |
| Deploy | Roll the artifact out to an environment | `kubectl`, `helm`, `argo cd` |
| Verify | Confirm the deploy actually works | smoke tests, synthetic checks |

### 4.2 CI vs CD vs Continuous Deployment

- **Continuous Integration** — every commit is automatically built and tested.
- **Continuous Delivery** — every passing build is automatically packaged and *ready* to deploy, with a manual gate before production.
- **Continuous Deployment** — every passing build is automatically deployed to production with no manual gate.

> **Tip:** Most real-world teams do CI + Continuous **Delivery** (auto-deploy to staging, manual approval to prod) rather than full Continuous Deployment, at least for the production environment.

### 4.3 Environment Promotion Strategy

```
feature-branch → PR → main → auto-deploy → staging → manual approval → prod
```
Use immutable, versioned image tags (git SHA or semver) — promote the *same* image through environments rather than rebuilding per environment, to guarantee what you tested is what you ship.

---

## 5. Jenkins

### 5.1 Why Jenkins

Jenkins is a self-hosted automation server — the most widely deployed CI/CD engine for teams that want full control (custom plugins, on-prem runners, complex approval workflows) rather than a fully managed SaaS pipeline.

### 5.2 Installing Jenkins (Docker, quick start)

```bash
docker run -d --name jenkins \
  -p 8080:8080 -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkins/jenkins:lts-jdk17

docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```
Open `http://localhost:8080`, paste the initial admin password, install suggested plugins, and create your admin user.

**Required plugins** for a Docker+Kubernetes pipeline: `Docker Pipeline`, `Kubernetes`, `Git`, `Credentials Binding`, `Blue Ocean` (nicer UI, optional).

### 5.3 Declarative Jenkinsfile — Build, Test, Push, Deploy

```groovy
// Jenkinsfile
pipeline {
    agent any

    environment {
        IMAGE_NAME = "myregistry.example.com/myapp"
        IMAGE_TAG  = "${env.GIT_COMMIT.take(7)}"
        REGISTRY_CREDS = credentials('registry-creds')     // Jenkins credential ID
        KUBECONFIG_CREDS = credentials('kubeconfig-prod')
    }

    options {
        timeout(time: 30, unit: 'MINUTES')
        disableConcurrentBuilds()
    }

    stages {
        stage('Checkout') {
            steps { checkout scm }
        }

        stage('Lint & Unit Tests') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt -r requirements-dev.txt
                    ruff check .
                    pytest --cov=app --cov-report=xml
                '''
            }
            post {
                always { junit 'test-results/*.xml' }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -t ${IMAGE_NAME}:latest ."
            }
        }

        stage('Security Scan') {
            steps {
                sh "trivy image --exit-code 1 --severity CRITICAL,HIGH ${IMAGE_NAME}:${IMAGE_TAG}"
            }
        }

        stage('Push to Registry') {
            steps {
                sh '''
                    echo $REGISTRY_CREDS_PSW | docker login myregistry.example.com -u $REGISTRY_CREDS_USR --password-stdin
                    docker push ${IMAGE_NAME}:${IMAGE_TAG}
                    docker push ${IMAGE_NAME}:latest
                '''
            }
        }

        stage('Deploy to Staging') {
            steps {
                sh """
                    export KUBECONFIG=${KUBECONFIG_CREDS}
                    helm upgrade --install myapp ./myapp-chart \
                      -f values-staging.yaml \
                      --set image.tag=${IMAGE_TAG} \
                      -n staging
                """
            }
        }

        stage('Integration Tests') {
            steps {
                sh 'pytest tests/integration --base-url=https://staging.myapp.example.com'
            }
        }

        stage('Approve Production Deploy') {
            steps {
                input message: 'Deploy to production?', ok: 'Deploy'
            }
        }

        stage('Deploy to Production') {
            steps {
                sh """
                    export KUBECONFIG=${KUBECONFIG_CREDS}
                    helm upgrade --install myapp ./myapp-chart \
                      -f values-prod.yaml \
                      --set image.tag=${IMAGE_TAG} \
                      -n prod
                """
            }
        }
    }

    post {
        success { echo "✅ Deployed ${IMAGE_TAG} successfully" }
        failure { echo "❌ Pipeline failed — check logs" }
        always  { sh 'docker system prune -f' }
    }
}
```

> **Tip:** Store the `Jenkinsfile` in the app repo (`Pipeline as Code`) and configure the Jenkins job as **Multibranch Pipeline** so every branch/PR automatically gets its own pipeline run.

### 5.4 Jenkins Agents on Kubernetes (scalable build runners)

Instead of one static Jenkins server running all builds, use the **Kubernetes plugin** to spin up ephemeral pod agents per build:

```groovy
pipeline {
    agent {
        kubernetes {
            yaml """
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: docker
    image: docker:24-dind
    securityContext:
      privileged: true
  - name: python
    image: python:3.12-slim
    command: ['cat']
    tty: true
"""
        }
    }
    stages {
        stage('Test') {
            steps {
                container('python') {
                    sh 'pip install -r requirements.txt && pytest'
                }
            }
        }
        stage('Build') {
            steps {
                container('docker') {
                    sh 'docker build -t myapp:${GIT_COMMIT} .'
                }
            }
        }
    }
}
```

### 5.5 Managing Secrets in Jenkins

- Store credentials in **Manage Jenkins → Credentials**, never hardcoded in the `Jenkinsfile`.
- Reference via `credentials('id')` (as above) — Jenkins masks the values in console output automatically.
- For cloud deploys, prefer short-lived OIDC tokens over static keys where the Jenkins plugin supports it (e.g., AWS `assume role` via OIDC).

---

## 6. Microservice Setup

### 6.1 When to Use Microservices vs. a Monolith

| Signal | Lean toward |
|---|---|
| Small team, early-stage product, unclear domain boundaries | **Monolith** (or a "modular monolith") |
| Multiple teams needing independent deploy cadence | **Microservices** |
| Different components have very different scaling profiles | **Microservices** |
| Need for polyglot tech stacks per component | **Microservices** |
| Simpler ops, single deploy pipeline preferred | **Monolith** |

> **Tip:** Most successful microservice migrations start as a monolith and split out services only once real scaling or team-boundary pain shows up — premature microservices add massive operational overhead for little benefit.

### 6.2 Example Architecture

```
                        ┌───────────────┐
                        │   API Gateway  │  (routing, auth, rate limiting)
                        └───────┬───────┘
          ┌───────────────┬────┴────┬───────────────┐
          ▼               ▼         ▼               ▼
   ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
   │ users-svc   │ │ orders-svc  │ │ payments-svc│ │ notify-svc  │
   │ (FastAPI)   │ │ (Django)    │ │ (FastAPI)   │ │ (FastAPI)   │
   └──────┬──────┘ └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
          │               │               │               │
    ┌─────▼─────┐   ┌─────▼─────┐   ┌─────▼─────┐   ┌─────▼─────┐
    │ Postgres  │   │ Postgres  │   │ Postgres  │   │  MongoDB  │
    │ (users)   │   │ (orders)  │   │ (payments)│   │ (events)  │
    └───────────┘   └───────────┘   └───────────┘   └───────────┘
                               │
                        ┌──────▼──────┐
                        │ Message Bus  │  (Kafka / RabbitMQ / SNS+SQS)
                        └─────────────┘
```

**Core principles:**
- **Database-per-service** — each service owns its data; no service reaches directly into another's database.
- **API Gateway** (Kong, NGINX, AWS API Gateway, Azure APIM) handles auth, routing, and rate limiting so individual services don't reimplement it.
- **Async communication** for cross-service workflows (order placed → payment charged → notification sent) via a message broker, to avoid tight synchronous coupling and cascading failures.
- **Synchronous REST/gRPC** for direct, low-latency lookups where async doesn't make sense (e.g., `orders-svc` calling `users-svc` to validate a user exists).

### 6.3 Project Structure (per-service repo pattern)

```
users-svc/
├── app/
│   ├── main.py
│   ├── api/
│   ├── models/
│   └── core/config.py
├── tests/
├── Dockerfile
├── requirements.txt
├── Jenkinsfile
└── k8s/
    ├── deployment.yaml
    ├── service.yaml
    └── hpa.yaml
```
Each service gets its **own repo (or monorepo package)**, own Dockerfile, own CI/CD pipeline, own Kubernetes manifests, and own database — independently deployable and independently scalable.

### 6.4 Inter-Service Communication Example

**Synchronous (FastAPI → FastAPI via HTTP, with resilience):**
```python
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.5))
async def get_user(user_id: str) -> dict:
    async with httpx.AsyncClient(timeout=2.0) as client:
        resp = await client.get(f"http://users-svc.prod.svc.cluster.local/users/{user_id}")
        resp.raise_for_status()
        return resp.json()
```

**Asynchronous (event-driven via a message broker):**
```python
# orders-svc: publish an event after order creation
import json
from aiokafka import AIOKafkaProducer

async def publish_order_created(order: dict):
    producer = AIOKafkaProducer(bootstrap_servers="kafka:9092")
    await producer.start()
    try:
        await producer.send_and_wait("order.created", json.dumps(order).encode())
    finally:
        await producer.stop()
```
```python
# payments-svc: consume the event
from aiokafka import AIOKafkaConsumer

async def consume_orders():
    consumer = AIOKafkaConsumer("order.created", bootstrap_servers="kafka:9092", group_id="payments-svc")
    await consumer.start()
    async for msg in consumer:
        order = json.loads(msg.value)
        await charge_payment(order)
```

> **Warning:** Synchronous service-to-service chains (A calls B calls C calls D) create cascading failure risk — if D is slow, A, B, and C all back up. Add timeouts, retries with backoff, and circuit breakers (e.g., `pybreaker`) on every synchronous call, and prefer async events for anything that isn't a real-time lookup.

### 6.5 Service Discovery & Networking in Kubernetes

Kubernetes gives you DNS-based service discovery for free — no separate service registry needed for in-cluster traffic:
```
http://<service-name>.<namespace>.svc.cluster.local
```
For cross-cutting concerns (mTLS between services, retries, circuit breaking, observability) at scale, add a **service mesh** (Istio, Linkerd) rather than hand-rolling it into every service.

### 6.6 Centralized Config & Secrets Across Services

- Namespace-scoped `ConfigMap`/`Secret` per service (Section 3.4), or
- A shared config service (Consul, or cloud-native: AWS AppConfig / Azure App Configuration / GCP Runtime Config) for values shared across services, combined with per-service secrets in Secrets Manager/Key Vault/Secret Manager.

### 6.7 Observability Across Services

| Concern | Tooling |
|---|---|
| Centralized logs | ELK/EFK stack, or cloud-native (CloudWatch/Log Analytics/Cloud Logging) |
| Metrics | Prometheus + Grafana |
| Distributed tracing (follow one request across services) | OpenTelemetry + Jaeger/Tempo |
| Alerting | Prometheus Alertmanager, or cloud-native alerting |

> **Tip:** Propagate a `trace_id`/`correlation_id` through every request header across service calls from day one — retrofitting distributed tracing after an incident is far harder than instrumenting it up front.

---

## 7. End-to-End Reference Architecture

```
Developer → git push → Jenkins (lint, test, build, scan, push to registry)
    → Helm deploy to staging namespace on K8s → integration tests
    → manual approval → Helm deploy to prod namespace
    → K8s Deployment rolls out Pods → Service + Ingress expose it
    → HPA scales replicas under load
    → Prometheus/Grafana + centralized logging observe it
    → Requests flow through API Gateway → individual microservices
    → sync calls (HTTP/gRPC) for lookups, async events (Kafka/RabbitMQ) for workflows
```

---

## 8. Troubleshooting & Common Pitfalls

| Symptom | Likely Cause | Fix |
|---|---|---|
| `CrashLoopBackOff` in K8s | App crashes on startup (bad env var, missing migration, wrong port) | `kubectl logs <pod> --previous`; verify `containerPort` matches app bind port |
| `ImagePullBackOff` | Wrong image tag, private registry auth missing | Check `imagePullSecrets`, verify tag exists in registry |
| Pod `Running` but Service returns 502/connection refused | `readinessProbe` failing, or Service `selector` labels don't match Pod labels | `kubectl describe svc`; confirm label match; check `/health` endpoint directly with `kubectl port-forward` |
| Jenkins pipeline can't reach `docker` daemon | Docker socket not mounted into Jenkins container, or DinD not configured | Mount `/var/run/docker.sock`, or use a `docker:dind` sidecar in Kubernetes agents |
| Image builds fine locally but fails in Jenkins | Different base image cache state, missing `.dockerignore`, or build context too large | Clear cache stage (`docker build --no-cache`), review `.dockerignore` |
| Rolling update causes brief 5xx spike | No `readinessProbe`, or `maxUnavailable` too aggressive | Add readiness probe; set `maxUnavailable: 0` in `RollingUpdate` strategy |
| Service A times out calling Service B intermittently | No retry/backoff, DNS caching issues, or B under-provisioned | Add `tenacity`/circuit breaker; check HPA thresholds on B |

---

## 9. Appendix — Command Cheat Sheets

### Docker
```bash
docker build -t myapp:1.0 .
docker run -d -p 8000:8000 --env-file .env myapp:1.0
docker compose up -d --build
docker system prune -af          # reclaim disk space
docker scout cves myapp:1.0
```

### Kubernetes
```bash
kubectl apply -f k8s/
kubectl get pods,svc,ingress -n prod
kubectl rollout status deployment/myapp -n prod
kubectl rollout undo deployment/myapp -n prod
kubectl top pods -n prod
kubectl port-forward svc/myapp-svc 8080:80 -n prod
```

### Helm
```bash
helm install myapp ./chart -f values-prod.yaml -n prod
helm upgrade myapp ./chart -f values-prod.yaml -n prod
helm history myapp -n prod
helm rollback myapp 1 -n prod
```

### Jenkins
```bash
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
# In Jenkinsfile: credentials('id'), input message: '...', container('name') { sh '...' }
```
