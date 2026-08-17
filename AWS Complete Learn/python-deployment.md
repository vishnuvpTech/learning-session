# Deploying and Hosting Python Web Applications (FastAPI & Django) on AWS, Azure, and GCP

A practical, developer-facing reference for shipping FastAPI and Django applications to production on the three major clouds.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Prerequisites](#2-prerequisites)
3. [AWS Deployment](#3-aws-deployment)
4. [Azure Deployment](#4-azure-deployment)
5. [GCP Deployment](#5-gcp-deployment)
6. [CI/CD Pipelines](#6-cicd-pipelines)
7. [Production Best Practices](#7-production-best-practices)
8. [Troubleshooting](#8-troubleshooting)
9. [Appendix](#9-appendix)

---

## 1. Introduction

Python web frameworks fall into two deployment models on the cloud:

- **WSGI (Django, Flask)** — synchronous request/response, served by Gunicorn (optionally behind Uvicorn/Daphne workers for ASGI features like Channels).
- **ASGI (FastAPI, Django with async views/Channels)** — async-native, served by Uvicorn/Hypercorn, typically wrapped by Gunicorn using `uvicorn.workers.UvicornWorker` for process management.

All three clouds offer roughly the same three deployment shapes:

| Shape | AWS | Azure | GCP |
|---|---|---|---|
| **PaaS (git-push / buildpack)** | Elastic Beanstalk | App Service | App Engine |
| **Managed containers (serverless)** | ECS/Fargate | Container Apps | Cloud Run |
| **Kubernetes** | EKS | AKS | GKE |
| **Functions (event/HTTP serverless)** | Lambda + API Gateway | Azure Functions | Cloud Functions / Cloud Run |

> **Tip:** If you're unsure where to start, containerized serverless (ECS Fargate, Azure Container Apps, Cloud Run) is the best default for both FastAPI and Django in 2026 — no server management, scales to zero (except ECS), and predictable via a single Dockerfile that works identically across all three clouds.

### 1.1 Decision Matrix (quick pick)

| Need | Recommended |
|---|---|
| Fastest path from `git push` to a URL, minimal config | AWS Elastic Beanstalk / Azure App Service / GCP App Engine Standard |
| Full control over container runtime, no server ops | Cloud Run (GCP) — best cold-start + true scale-to-zero |
| Already standardized on Kubernetes | EKS / AKS / GKE |
| Spiky/event-driven traffic, pay-per-request, simple FastAPI microservice | Lambda + API Gateway (via Mangum) |
| Django (sessions, ORM, admin, WebSockets/Channels) | Container-based options (ECS Fargate, Container Apps, Cloud Run) — avoid pure Lambda for Django |
| Heavy background workers / long-running WebSocket connections | ECS/Fargate, AKS, or GKE (avoid pure serverless functions) |
| Lowest ops overhead, small team | Cloud Run or Azure App Service |
| Full OS-level control, custom system packages, predictable flat-rate pricing | AWS EC2 with Supervisor + Nginx (or equivalent Azure/GCP VMs) |

### 1.2 Comparison Table

| Criteria | AWS Elastic Beanstalk | AWS ECS/Fargate | AWS Lambda + API GW | AWS EC2 (Supervisor+Nginx) | Azure App Service | Azure Container Apps | Azure Functions | GCP App Engine | GCP Cloud Run | GKE/EKS/AKS |
|---|---|---|---|---|---|---|---|---|---|---|
| **Pricing model** | EC2 + ELB hourly | Fargate vCPU/GB-hour | Per-request + GB-sec | Flat EC2 instance-hour | App Service Plan tier | vCPU/GB-sec, scale-to-zero | Per-execution (Consumption) | Instance hours (Standard free tier available) | vCPU/GB-sec, scale-to-zero | Node/cluster hourly + control plane fee |
| **Ease of setup** | Easy (CLI wizard) | Moderate (Dockerfile, task defs, ALB) | Moderate (packaging, adapters) | Manual (OS, Nginx, Supervisor, TLS all self-configured) | Very easy (`az webapp up`) | Easy | Easy for simple triggers | Easy (declarative `app.yaml`) | Very easy (`gcloud run deploy`) | Hard (cluster, manifests, networking) |
| **Scalability** | Auto Scaling groups | Excellent, fine-grained | Excellent, automatic | Manual, or via Auto Scaling group + ALB | Good (scale rules per plan) | Excellent, KEDA-based | Excellent | Good (Standard auto-scales; Flexible slower) | Excellent, request-concurrency based | Excellent, most configurable |
| **Cold start** | None (always-on instances) | Low (tasks stay warm) | Noticeable (100ms–several sec, worse for Django/large deps) | None (always-on instance) | Low (Basic+ tiers always-on) | Low–moderate (scale-to-zero adds cold start) | Moderate–high on Consumption plan | Standard: moderate; Flexible: low (always-on) | Low (fast container cold start, min-instances=1 removes it) | None if nodes/pods kept warm |
| **Best framework fit** | Django & FastAPI | Both | FastAPI (Mangum); Django possible but heavier | Both — good for either when you need full control | Both | Both | FastAPI (lightweight endpoints) | Both | Both — generally best all-around fit | Both, at scale |
| **Free tier** | EC2/RDS free tier applies | No dedicated free tier | 1M requests/month free | EC2 free tier (t2/t3.micro, 750 hrs/mo, 12 months) | 60 min/day (F1 free tier) | Generous monthly free grant | 1M executions/month free | Free daily quota (Standard) | 2M requests/month free | No free control-plane on AWS/Azure; GKE has one free zonal cluster |

---

## 2. Prerequisites

### 2.1 Python Version

- Use **Python 3.11 or 3.12** for new deployments — best performance/async support and broad platform compatibility as of 2026. Avoid 3.9 or earlier unless a dependency forces it.
- Pin your version explicitly:
  - `runtime.txt` (Beanstalk, App Engine legacy) → `python-3.12`
  - `Dockerfile` base image tag (`python:3.12-slim`)
  - `pyproject.toml` / `Pipfile` `python_requires`

### 2.2 Framework Production Readiness

**FastAPI (ASGI):**
```txt
fastapi>=0.115
uvicorn[standard]>=0.30
gunicorn>=22.0        # process manager wrapping uvicorn workers
```
Production start command:
```bash
gunicorn app.main:app -k uvicorn.workers.UvicornWorker -w 4 -b 0.0.0.0:8000 --timeout 60
```

**Django (WSGI, or ASGI if using async views/Channels):**
```txt
django>=5.0
gunicorn>=22.0
whitenoise>=6.6        # static files without a CDN dependency
psycopg[binary]>=3.1   # or mysqlclient
```
WSGI start command:
```bash
gunicorn myproject.wsgi:application -w 4 -b 0.0.0.0:8000 --timeout 60
```
ASGI (Channels/WebSockets) start command:
```bash
gunicorn myproject.asgi:application -k uvicorn.workers.UvicornWorker -w 4 -b 0.0.0.0:8000
```

> **Warning:** Never run `runserver` (Django) or `uvicorn --reload` (FastAPI dev mode) in production. Always use Gunicorn (or Gunicorn+Uvicorn workers) behind a managed load balancer/proxy.

### 2.3 Required CLI Tools

| Tool | Install | Verify |
|---|---|---|
| AWS CLI v2 | `curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o AWSCLIV2.pkg` (macOS) or platform installer | `aws --version` |
| Azure CLI | `curl -sL https://aka.ms/InstallAzureCLIDeb \| sudo bash` (Linux) | `az --version` |
| gcloud CLI | Google Cloud SDK installer | `gcloud --version` |
| Docker | Docker Desktop / `docker-ce` | `docker --version` |
| EB CLI (optional, AWS) | `pip install awsebcli` | `eb --version` |

### 2.4 Account Setup & Billing Basics

1. Create an account on each provider and enable billing (all three require a payment method even for free-tier usage).
2. Set up **budget alerts** immediately:
   - AWS: Billing → Budgets
   - Azure: Cost Management → Budgets
   - GCP: Billing → Budgets & alerts
3. Create a dedicated IAM identity for deployments rather than using root/owner credentials:
   - AWS: IAM user or role with `AdministratorAccess-Deployment` scoped policy, or better, an OIDC role for GitHub Actions.
   - Azure: Service principal (`az ad sp create-for-rbac`).
   - GCP: Service account with `roles/run.admin`, `roles/iam.serviceAccountUser`, etc.
4. Authenticate CLIs locally:
```bash
aws configure
az login
gcloud init && gcloud auth application-default login
```

---

## 3. AWS Deployment

### 3.1 Option A — AWS Elastic Beanstalk

Best for teams wanting `git push`-style deploys without managing containers.

**App structure:**
```
myapp/
├── application.py        # or wsgi.py / main.py
├── requirements.txt
├── Procfile
└── .ebextensions/
    └── django.config
```

**Procfile:**
```
web: gunicorn myproject.wsgi:application --bind 0.0.0.0:8000
```
For FastAPI:
```
web: gunicorn app.main:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

**Steps:**
```bash
pip install awsebcli
eb init -p python-3.12 myapp --region us-east-1
eb create myapp-prod-env --envvars DJANGO_SETTINGS_MODULE=myproject.settings.prod
eb deploy
eb open
```

> **Tip:** Use `.ebextensions/` config files to run `python manage.py migrate` and `collectstatic` as container commands on deploy.

```yaml
# .ebextensions/django.config
container_commands:
  01_migrate:
    command: "source /var/app/venv/*/bin/activate && python manage.py migrate --noinput"
    leader_only: true
  02_collectstatic:
    command: "source /var/app/venv/*/bin/activate && python manage.py collectstatic --noinput"
```

### 3.2 Option B — AWS ECS/Fargate with Docker

Best for full control without managing servers.

**1. Dockerfile** — see [Appendix 9.1](#91-sample-dockerfiles).

**2. Build & push to ECR:**
```bash
aws ecr create-repository --repository-name myapp
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin <account_id>.dkr.ecr.us-east-1.amazonaws.com

docker build -t myapp .
docker tag myapp:latest <account_id>.dkr.ecr.us-east-1.amazonaws.com/myapp:latest
docker push <account_id>.dkr.ecr.us-east-1.amazonaws.com/myapp:latest
```

**3. Task definition (excerpt):**
```json
{
  "family": "myapp-task",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "containerDefinitions": [
    {
      "name": "myapp",
      "image": "<account_id>.dkr.ecr.us-east-1.amazonaws.com/myapp:latest",
      "portMappings": [{ "containerPort": 8000 }],
      "environment": [{ "name": "DJANGO_SETTINGS_MODULE", "value": "myproject.settings.prod" }],
      "secrets": [
        { "name": "SECRET_KEY", "valueFrom": "arn:aws:secretsmanager:us-east-1:<account_id>:secret:myapp/secret_key" }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/myapp",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

**4. ALB + ECS Service:**
```bash
aws ecs create-cluster --cluster-name myapp-cluster
aws elbv2 create-load-balancer --name myapp-alb --subnets subnet-a subnet-b --security-groups sg-xxxx
aws elbv2 create-target-group --name myapp-tg --protocol HTTP --port 8000 --vpc-id vpc-xxxx --target-type ip --health-check-path /health
aws ecs create-service --cluster myapp-cluster --service-name myapp-svc \
  --task-definition myapp-task --desired-count 2 --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-a,subnet-b],securityGroups=[sg-xxxx],assignPublicIp=ENABLED}" \
  --load-balancers "targetGroupArn=<tg-arn>,containerName=myapp,containerPort=8000"
```

### 3.3 Option C — AWS Lambda + API Gateway

Best for lightweight FastAPI microservices with spiky traffic.

**FastAPI with Mangum:**
```python
# app/main.py
from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

handler = Mangum(app)   # Lambda entry point
```

```bash
pip install mangum -t package/
cp -r app package/
cd package && zip -r ../deployment.zip . && cd ..

aws lambda create-function \
  --function-name myapp-api \
  --runtime python3.12 \
  --handler app.main.handler \
  --zip-file fileb://deployment.zip \
  --role arn:aws:iam::<account_id>:role/lambda-exec-role \
  --timeout 30 --memory-size 512

aws apigatewayv2 create-api --name myapp-http-api --protocol-type HTTP \
  --target arn:aws:lambda:us-east-1:<account_id>:function:myapp-api
```

> **Warning:** Django on Lambda is possible (e.g., via Zappa or Mangum + a WSGI-to-ASGI shim), but cold starts, 15-minute execution limits, ephemeral filesystem, and lack of persistent connections make it a poor fit for admin-heavy, session-based, or WebSocket-using Django apps. Prefer ECS/Fargate for Django unless traffic is very low and intermittent.

### 3.4 Option D — AWS EC2 with Supervisor and Nginx

Best when you want full OS-level control (custom system packages, long-lived processes, predictable always-on pricing) without container tooling.

**1. Launch and prepare the instance:**
```bash
aws ec2 run-instances \
  --image-id ami-0abcdef1234567890 \
  --instance-type t3.small \
  --key-name my-keypair \
  --security-group-ids sg-xxxx \
  --subnet-id subnet-xxxx \
  --count 1

ssh -i my-keypair.pem ubuntu@<public-ip>
```

**2. Install system dependencies:**
```bash
sudo apt update && sudo apt install -y python3.12 python3.12-venv python3-pip \
  nginx supervisor postgresql-client git
```

**3. Deploy the application code:**
```bash
sudo mkdir -p /opt/myapp && sudo chown ubuntu:ubuntu /opt/myapp
git clone https://github.com/myorg/myapp.git /opt/myapp
cd /opt/myapp
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**4. Configure Supervisor** to keep Gunicorn running and restart it on crash/reboot:
```ini
# /etc/supervisor/conf.d/myapp.conf

[program:myapp]
directory=/opt/myapp
command=/opt/myapp/venv/bin/gunicorn myproject.wsgi:application -w 4 -b 127.0.0.1:8000 --timeout 60
; For FastAPI, use:
; command=/opt/myapp/venv/bin/gunicorn app.main:app -k uvicorn.workers.UvicornWorker -w 4 -b 127.0.0.1:8000
user=ubuntu
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stdout_logfile=/var/log/myapp/access.log
stderr_logfile=/var/log/myapp/error.log
environment=DJANGO_SETTINGS_MODULE="myproject.settings.prod",PYTHONUNBUFFERED="1"
```
```bash
sudo mkdir -p /var/log/myapp
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl status myapp
```

**5. Configure Nginx** as a reverse proxy in front of Gunicorn:
```nginx
# /etc/nginx/sites-available/myapp

server {
    listen 80;
    server_name myapp.example.com;

    location /static/ {
        alias /opt/myapp/staticfiles/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
```bash
sudo ln -s /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl restart nginx
```

**6. Enable HTTPS with Let's Encrypt:**
```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d myapp.example.com
```

**7. Common operational commands:**
```bash
sudo supervisorctl restart myapp     # restart app after a deploy
sudo supervisorctl tail -f myapp     # follow stdout logs
sudo nginx -s reload                 # reload nginx after config changes
```

> **Tip:** Put your instance in an Auto Scaling group behind an ALB if you need horizontal scaling with this approach — EC2 alone doesn't scale automatically the way ECS/Fargate does.

> **Warning:** Unlike Beanstalk/ECS, EC2 gives you no managed patching, scaling, or zero-downtime deploys out of the box. Budget time for OS updates (`unattended-upgrades`), log rotation (`logrotate`), and a deploy script that runs migrations, `collectstatic`, and `supervisorctl restart myapp` in sequence.

### 3.5 Environment Variables & Secrets

- **Non-sensitive config:** SSM Parameter Store (`aws ssm put-parameter --name /myapp/DEBUG --value false --type String`)
- **Sensitive values:** Secrets Manager (`aws secretsmanager create-secret --name myapp/secret_key --secret-string '...'`)
- Reference secrets directly in ECS task definitions (`secrets` block above) or fetch at boot via `boto3` for Beanstalk/Lambda.

### 3.6 Database Connectivity

#### 3.6.1 PostgreSQL via RDS

**Create the instance:**
```bash
aws rds create-db-instance \
  --db-instance-identifier myapp-db \
  --db-instance-class db.t4g.micro \
  --engine postgres \
  --engine-version 16.4 \
  --master-username appadmin \
  --master-user-password '<use Secrets Manager instead>' \
  --allocated-storage 20 \
  --vpc-security-group-ids sg-xxxx \
  --db-subnet-group-name myapp-db-subnet-group \
  --no-publicly-accessible
```
```bash
aws rds wait db-instance-available --db-instance-identifier myapp-db
aws rds describe-db-instances --db-instance-identifier myapp-db \
  --query "DBInstances[0].Endpoint.Address" --output text
```

**Create the application database and a scoped user** (run from a host inside the VPC, or a bastion/EC2 instance with `psql` access):
```bash
psql -h <rds-endpoint> -U appadmin -d postgres <<'SQL'
CREATE DATABASE myapp_prod;
CREATE USER myapp_user WITH PASSWORD 'use-a-secrets-manager-value';
GRANT ALL PRIVILEGES ON DATABASE myapp_prod TO myapp_user;
\c myapp_prod
GRANT ALL ON SCHEMA public TO myapp_user;
SQL
```

**Self-hosted PostgreSQL on EC2** (if not using RDS — e.g., for a dev box or cost-sensitive workload):
```bash
sudo apt install -y postgresql postgresql-contrib
sudo -u postgres psql <<'SQL'
CREATE DATABASE myapp_prod;
CREATE USER myapp_user WITH PASSWORD 'strong-password-here';
GRANT ALL PRIVILEGES ON DATABASE myapp_prod TO myapp_user;
SQL
sudo systemctl enable --now postgresql
```

Django `settings.py`:
```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["DB_NAME"],       # myapp_prod
        "USER": os.environ["DB_USER"],       # myapp_user
        "PASSWORD": os.environ["DB_PASSWORD"],
        "HOST": os.environ["DB_HOST"],       # RDS endpoint or localhost
        "PORT": "5432",
    }
}
```
Then run migrations:
```bash
python manage.py migrate
```

> **Tip:** Place RDS in private subnets only, and allow inbound 5432 solely from your ECS/Lambda/EC2 security group.

#### 3.6.2 MongoDB via Amazon DocumentDB (or self-hosted)

**Managed option — Amazon DocumentDB** (MongoDB-compatible API):
```bash
aws docdb create-db-cluster \
  --db-cluster-identifier myapp-docdb \
  --engine docdb \
  --master-username appadmin \
  --master-user-password '<use Secrets Manager instead>' \
  --vpc-security-group-ids sg-xxxx \
  --db-subnet-group-name myapp-docdb-subnet-group

aws docdb create-db-instance \
  --db-instance-identifier myapp-docdb-instance-1 \
  --db-instance-class db.t4g.medium \
  --engine docdb \
  --db-cluster-identifier myapp-docdb
```
Create the application database/collection and a scoped user via `mongosh` (DocumentDB requires TLS by default):
```bash
mongosh "mongodb://appadmin:<password>@<docdb-cluster-endpoint>:27017/?tls=true&tlsCAFile=global-bundle.pem&replicaSet=rs0" <<'JS'
use myapp_prod
db.createUser({
  user: "myapp_user",
  pwd: "strong-password-here",
  roles: [{ role: "readWrite", db: "myapp_prod" }]
})
db.createCollection("startup_check")
JS
```

**Self-hosted MongoDB on EC2** (simpler for dev/small workloads; use DocumentDB or Atlas for production HA):
```bash
curl -fsSL https://pgp.mongodb.com/server-7.0.asc | sudo gpg --dearmor -o /usr/share/keyrings/mongodb-server-7.0.gpg
echo "deb [signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | \
  sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
sudo apt update && sudo apt install -y mongodb-org
sudo systemctl enable --now mongod

mongosh <<'JS'
use myapp_prod
db.createUser({
  user: "myapp_user",
  pwd: "strong-password-here",
  roles: [{ role: "readWrite", db: "myapp_prod" }]
})
JS
```

Application connection (works the same for both FastAPI via `motor`/`pymongo` and Django via `djongo`/`mongoengine`):
```python
from pymongo import MongoClient

client = MongoClient(os.environ["MONGO_URI"])  # e.g. mongodb://myapp_user:<pwd>@<host>:27017/myapp_prod
db = client.get_default_database()
```

> **Warning:** DocumentDB clusters are VPC-internal only (no public endpoint) — connect from ECS/EC2/Lambda inside the same VPC, or via a bastion host / SSM port forwarding for local development.

### 3.7 Static/Media Files (S3 + CloudFront)

```bash
aws s3 mb s3://myapp-static
aws s3 sync ./staticfiles s3://myapp-static --acl public-read
aws cloudfront create-distribution --origin-domain-name myapp-static.s3.amazonaws.com
```
Django (`django-storages`):
```python
STORAGES = {
    "default": {"BACKEND": "storages.backends.s3.S3Storage"},
    "staticfiles": {"BACKEND": "storages.backends.s3.S3StaticStorage"},
}
AWS_STORAGE_BUCKET_NAME = "myapp-static"
AWS_S3_CUSTOM_DOMAIN = "d1234abcd.cloudfront.net"
```

### 3.8 Logging & Monitoring (CloudWatch)

- ECS/Fargate and Lambda ship logs to CloudWatch Logs automatically via `awslogs` driver.
- Set up **CloudWatch Alarms** on 5xx rate, CPU/memory, and Lambda error count.
- Use **CloudWatch Container Insights** for ECS cluster-level metrics.
- For **EC2**, install the CloudWatch Agent to ship Nginx/Supervisor/Gunicorn logs and host metrics:
```bash
sudo apt install -y amazon-cloudwatch-agent
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
  -a fetch-config -m ec2 -c file:/opt/aws/amazon-cloudwatch-agent/etc/config.json -s
```
```bash
aws logs tail /ecs/myapp --follow
aws logs tail /ec2/myapp/error.log --follow
```

---

## 4. Azure Deployment

### 4.1 Option A — Azure App Service

```bash
az group create --name myapp-rg --location eastus
az appservice plan create --name myapp-plan --resource-group myapp-rg --sku B1 --is-linux
az webapp create --resource-group myapp-rg --plan myapp-plan --name myapp-web \
  --runtime "PYTHON:3.12"

az webapp config set --resource-group myapp-rg --name myapp-web \
  --startup-file "gunicorn myproject.wsgi:application --bind=0.0.0.0"

# Deploy via local git
az webapp deployment source config-local-git --name myapp-web --resource-group myapp-rg
git remote add azure <deployment-git-url>
git push azure main
```
FastAPI startup command:
```bash
az webapp config set --resource-group myapp-rg --name myapp-web \
  --startup-file "gunicorn app.main:app -k uvicorn.workers.UvicornWorker --bind=0.0.0.0"
```
Or deploy directly via CLI convenience command:
```bash
az webapp up --name myapp-web --resource-group myapp-rg --runtime "PYTHON:3.12" --sku B1
```

### 4.2 Option B — Azure Container Apps / AKS

**Container Apps (recommended default for containers on Azure):**
```bash
az containerapp env create --name myapp-env --resource-group myapp-rg --location eastus

az acr create --resource-group myapp-rg --name myappacr --sku Basic
az acr build --registry myappacr --image myapp:latest .

az containerapp create \
  --name myapp \
  --resource-group myapp-rg \
  --environment myapp-env \
  --image myappacr.azurecr.io/myapp:latest \
  --target-port 8000 \
  --ingress external \
  --min-replicas 1 --max-replicas 10 \
  --registry-server myappacr.azurecr.io
```

**AKS** (Kubernetes) is recommended only if you already run Kubernetes elsewhere:
```bash
az aks create --resource-group myapp-rg --name myapp-aks --node-count 2 --generate-ssh-keys
az aks get-credentials --resource-group myapp-rg --name myapp-aks
kubectl apply -f k8s/deployment.yaml
```

### 4.3 Option C — Azure Functions

Best for narrow FastAPI HTTP endpoints; Django is not a good fit (no native ASGI/WSGI host — you'd need the `azure-functions` HTTP trigger wrapper and lose most PaaS conveniences).

```python
# function_app.py
import azure.functions as func
from app.main import app as fastapi_app

app = func.AsgiFunctionApp(app=fastapi_app, http_auth_level=func.AuthLevel.ANONYMOUS)
```
```bash
func azure functionapp publish myapp-func
```

> **Warning:** For Django, prefer App Service or Container Apps. Azure Functions' request/response model and cold-start profile on the Consumption plan work poorly with Django's middleware stack, sessions, and admin interface.

### 4.4 Environment Variables & Secrets

```bash
az webapp config appsettings set --resource-group myapp-rg --name myapp-web \
  --settings DJANGO_SETTINGS_MODULE=myproject.settings.prod

az keyvault create --name myapp-kv --resource-group myapp-rg
az keyvault secret set --vault-name myapp-kv --name "DbPassword" --value "..."
```
Reference Key Vault secrets in App Service via **Key Vault references**:
```
@Microsoft.KeyVault(SecretUri=https://myapp-kv.vault.azure.net/secrets/DbPassword/)
```

### 4.5 Database Connectivity

```bash
az postgres flexible-server create \
  --resource-group myapp-rg --name myapp-pg \
  --admin-user appadmin --admin-password '<from Key Vault>' \
  --sku-name Standard_B1ms --tier Burstable \
  --public-access None
```

### 4.6 Static Files (Blob Storage + CDN)

```bash
az storage account create --name myappstatic --resource-group myapp-rg --sku Standard_LRS
az storage container create --name static --account-name myappstatic --public-access blob
az storage blob upload-batch -d static -s ./staticfiles --account-name myappstatic
az cdn profile create --name myapp-cdn --resource-group myapp-rg --sku Standard_Microsoft
```
Django (`django-storages[azure]`):
```python
STORAGES = {"staticfiles": {"BACKEND": "storages.backends.azure_storage.AzureStorage"}}
AZURE_ACCOUNT_NAME = "myappstatic"
AZURE_CONTAINER = "static"
```

### 4.7 Logging & Monitoring (Application Insights)

```bash
az monitor app-insights component create --app myapp-insights --location eastus --resource-group myapp-rg
```
```python
pip install opencensus-ext-azure
```
```python
import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler

logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(connection_string="InstrumentationKey=<key>"))
```

---

## 5. GCP Deployment

### 5.1 Option A — Cloud Run (recommended default for both frameworks)

```bash
gcloud builds submit --tag gcr.io/my-project/myapp

gcloud run deploy myapp \
  --image gcr.io/my-project/myapp \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --min-instances 1 \
  --max-instances 10 \
  --set-env-vars DJANGO_SETTINGS_MODULE=myproject.settings.prod
```
> **Tip:** Set `--min-instances 1` to eliminate cold starts for latency-sensitive endpoints; leave at 0 for cost-sensitive, low-traffic services.

### 5.2 Option B — App Engine (Standard/Flexible)

**app.yaml (Standard):**
```yaml
runtime: python312
entrypoint: gunicorn -b :$PORT myproject.wsgi:application
env_variables:
  DJANGO_SETTINGS_MODULE: "myproject.settings.prod"
automatic_scaling:
  min_instances: 1
  max_instances: 10
```
```bash
gcloud app deploy
```
Flexible environment (Docker-based, more control, slower scaling) uses `env: flex` in `app.yaml` and supports a custom Dockerfile.

### 5.3 Option C — GKE

```bash
gcloud container clusters create-auto myapp-cluster --region us-central1
gcloud container clusters get-credentials myapp-cluster --region us-central1
kubectl apply -f k8s/deployment.yaml
```

### 5.4 Environment Variables & Secrets (Secret Manager)

```bash
echo -n "supersecret" | gcloud secrets create django-secret-key --data-file=-

gcloud run deploy myapp \
  --update-secrets=SECRET_KEY=django-secret-key:latest
```

### 5.5 Database Connectivity (Cloud SQL)

```bash
gcloud sql instances create myapp-db --database-version=POSTGRES_15 \
  --tier=db-f1-micro --region=us-central1

gcloud run deploy myapp --add-cloudsql-instances my-project:us-central1:myapp-db
```
Django:
```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": "/cloudsql/my-project:us-central1:myapp-db",
        "NAME": os.environ["DB_NAME"],
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASSWORD"],
    }
}
```

### 5.6 Static Files (Cloud Storage + Cloud CDN)

```bash
gsutil mb gs://myapp-static
gsutil -m rsync -r ./staticfiles gs://myapp-static
gsutil iam ch allUsers:objectViewer gs://myapp-static
```
Django (`django-storages[google]`):
```python
STORAGES = {"staticfiles": {"BACKEND": "storages.backends.gcloud.GoogleCloudStorage"}}
GS_BUCKET_NAME = "myapp-static"
```

### 5.7 Logging & Monitoring (Cloud Logging/Monitoring)

Cloud Run and App Engine ship stdout/stderr to Cloud Logging automatically — no extra agent needed.
```bash
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=myapp" --limit 50
```
Set up alerting policies in Cloud Monitoring on request latency, error rate, and container memory.

---

## 6. CI/CD Pipelines

### 6.1 GitHub Actions — AWS (ECS/Fargate)

```yaml
name: Deploy to AWS ECS
on:
  push:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install -r requirements.txt
      - run: pytest

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::<account_id>:role/github-deploy-role
          aws-region: us-east-1
      - uses: aws-actions/amazon-ecr-login@v2
        id: ecr
      - run: |
          docker build -t $ECR_REGISTRY/myapp:${{ github.sha }} .
          docker push $ECR_REGISTRY/myapp:${{ github.sha }}
        env:
          ECR_REGISTRY: ${{ steps.ecr.outputs.registry }}
      - run: |
          aws ecs update-service --cluster myapp-cluster --service myapp-svc --force-new-deployment
```

### 6.2 GitHub Actions — Azure (App Service)

```yaml
name: Deploy to Azure App Service
on:
  push:
    branches: [main]
jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install -r requirements.txt && pytest
      - uses: azure/login@v2
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
      - uses: azure/webapps-deploy@v3
        with:
          app-name: myapp-web
          package: .
```

### 6.3 GitLab CI — GCP (Cloud Run)

```yaml
stages: [test, deploy]

test:
  image: python:3.12
  stage: test
  script:
    - pip install -r requirements.txt
    - pytest

deploy:
  stage: deploy
  image: google/cloud-sdk:slim
  script:
    - echo "$GCP_SA_KEY" > key.json
    - gcloud auth activate-service-account --key-file=key.json
    - gcloud builds submit --tag gcr.io/$GCP_PROJECT/myapp
    - gcloud run deploy myapp --image gcr.io/$GCP_PROJECT/myapp --region us-central1 --platform managed
  only: [main]
```

> **Tip:** Always gate `deploy` jobs behind a passing `test` stage, and use OIDC-based federated credentials (GitHub ↔ AWS/Azure/GCP) instead of long-lived static keys stored as CI secrets where the provider supports it.

---

## 7. Production Best Practices

### 7.1 HTTPS/SSL

| Provider | Managed cert option |
|---|---|
| AWS | AWS Certificate Manager (free, auto-renewing) attached to ALB/CloudFront |
| Azure | App Service Managed Certificate (free) or Key Vault-issued cert |
| GCP | Google-managed SSL certs on Cloud Run/Load Balancer (free, auto-renewing) |

Self-managed origins (e.g., a raw VM/K8s ingress without a cloud LB) can use **Let's Encrypt** via `certbot` or `cert-manager` (Kubernetes).

### 7.2 Environment Separation

- Maintain distinct **dev / staging / prod** resource groups, projects, or accounts (GCP projects and separate AWS accounts via Organizations give the strongest isolation).
- Never share databases or secret stores across environments.
- Use environment-specific settings modules: `myproject/settings/{base,dev,staging,prod}.py`.

### 7.3 Auto-Scaling Configuration

| Provider/Service | Key scaling knobs |
|---|---|
| ECS/Fargate | Target tracking on CPU/memory, or ALB request count per target |
| EC2 (Supervisor+Nginx) | Wrap instances in an Auto Scaling group + ALB target group; scale on CPU or ALB request count — this is not automatic by default |
| App Service | Scale rules on CPU %, memory, or HTTP queue length |
| Cloud Run | `--min-instances`, `--max-instances`, `--concurrency` (requests per instance) |
| Kubernetes (EKS/AKS/GKE) | HPA on CPU/custom metrics; cluster autoscaler for node pools |

### 7.4 Health Checks & Readiness Probes

FastAPI/Django should expose a lightweight, dependency-free endpoint:
```python
@app.get("/health")
def health():
    return {"status": "ok"}
```
Wire this into:
- ALB target group health check path
- ECS task `HEALTHCHECK` in Dockerfile
- Kubernetes `livenessProbe` / `readinessProbe`
- Cloud Run / App Service startup and liveness probe settings

> **Warning:** Don't make health checks hit the database or external APIs — that turns transient downstream issues into full outages via cascading restarts.

### 7.5 Cost Optimization Tips

| Provider | Tips |
|---|---|
| AWS | Use Fargate Spot for non-critical workloads; right-size RDS instance class; set S3 lifecycle rules; use Savings Plans for steady-state EC2/Fargate usage |
| Azure | Use B-series burstable App Service/DB tiers for low-traffic apps; scale Container Apps to zero for dev/staging; enable auto-shutdown on dev VMs |
| GCP | Use Cloud Run scale-to-zero for staging; committed use discounts for steady GKE/Compute usage; lifecycle rules on Cloud Storage |

---

## 8. Troubleshooting

### 8.1 Common Errors by Platform

**AWS**
- *Elastic Beanstalk "502 Bad Gateway"* — usually the app isn't binding to `0.0.0.0:8000`, or the Procfile's start command is wrong.
- *ECS tasks stuck "PROVISIONING → STOPPED"* — check `stoppedReason` in `aws ecs describe-tasks`; commonly missing IAM permissions to pull from ECR or a failing health check.
- *Lambda "Task timed out"* — increase timeout or investigate cold-start-heavy imports (large ML libs, unoptimized package size).

**Azure**
- *App Service "Application Error"* — check `--startup-file` matches your actual Gunicorn entry point; view via `az webapp log tail`.
- *Container Apps revision stuck "Provisioning"* — usually a bad `--target-port` or the container crashing on boot; check `az containerapp logs show`.

**GCP**
- *Cloud Run "Container failed to start and listen on PORT"* — app must read the `PORT` env var (Cloud Run injects it) rather than hardcoding 8000.
- *App Engine `DeadlineExceededError`* — request exceeded the 60s (Standard) timeout; move long tasks to Cloud Tasks/Pub-Sub.

### 8.2 Debugging Tips

```bash
# AWS
aws logs tail /ecs/myapp --follow
eb logs
aws ecs execute-command --cluster myapp-cluster --task <task-id> --container myapp --interactive --command "/bin/sh"

# Azure
az webapp log tail --name myapp-web --resource-group myapp-rg
az containerapp exec --name myapp --resource-group myapp-rg --command "/bin/sh"

# GCP
gcloud run services logs read myapp --region us-central1
gcloud run services proxy myapp --region us-central1   # local tunnel for debugging
```

---

## 9. Appendix

### 9.1 Sample Dockerfiles

**FastAPI:**
```dockerfile
FROM python:3.12-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
HEALTHCHECK CMD curl --fail http://localhost:8000/health || exit 1

CMD ["gunicorn", "app.main:app", "-k", "uvicorn.workers.UvicornWorker", \
     "-w", "4", "-b", "0.0.0.0:8000", "--timeout", "60"]
```

**Django:**
```dockerfile
FROM python:3.12-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN python manage.py collectstatic --noinput

EXPOSE 8000
HEALTHCHECK CMD curl --fail http://localhost:8000/health || exit 1

CMD ["gunicorn", "myproject.wsgi:application", "-w", "4", "-b", "0.0.0.0:8000", "--timeout", "60"]
```

### 9.2 Sample `requirements.txt`

**FastAPI:**
```
fastapi>=0.115
uvicorn[standard]>=0.30
gunicorn>=22.0
pydantic-settings>=2.4
mangum>=0.18          # only if targeting Lambda
sqlalchemy>=2.0
psycopg[binary]>=3.1
python-dotenv>=1.0
```

**Django:**
```
django>=5.0
gunicorn>=22.0
whitenoise>=6.6
psycopg[binary]>=3.1
django-storages[s3,azure,google]>=1.14
python-dotenv>=1.0
```

### 9.3 CLI Cheat Sheet

**AWS**
```bash
aws configure                          # set credentials
eb init / eb create / eb deploy        # Elastic Beanstalk
aws ecs update-service --force-new-deployment
aws logs tail /ecs/myapp --follow
aws secretsmanager get-secret-value --secret-id myapp/secret_key

# EC2 + Supervisor + Nginx
ssh -i my-keypair.pem ubuntu@<public-ip>
sudo supervisorctl restart myapp
sudo supervisorctl tail -f myapp
sudo nginx -t && sudo systemctl restart nginx

# PostgreSQL (RDS or self-hosted)
psql -h <host> -U appadmin -d postgres -c "CREATE DATABASE myapp_prod;"
psql -h <host> -U appadmin -d myapp_prod -c "\dt"     # list tables

# MongoDB (DocumentDB or self-hosted)
mongosh "mongodb://<user>:<pwd>@<host>:27017/myapp_prod"
mongosh --eval "db.runCommand({ ping: 1 })"
```

**Azure**
```bash
az login
az webapp up --runtime "PYTHON:3.12"
az containerapp up --name myapp --source .
az webapp log tail --name myapp-web
az keyvault secret show --vault-name myapp-kv --name DbPassword
```

**GCP**
```bash
gcloud init
gcloud run deploy myapp --source .
gcloud app deploy
gcloud logging read "resource.type=cloud_run_revision" --limit 50
gcloud secrets versions access latest --secret=django-secret-key
```

---

> **Final tip:** Regardless of provider, keep your Dockerfile as the single source of truth for how the app runs. It lets you move between ECS, Container Apps, and Cloud Run (or even a plain VM) with minimal rework — the main things that change are IAM/secrets wiring, networking, and the deploy command itself.
