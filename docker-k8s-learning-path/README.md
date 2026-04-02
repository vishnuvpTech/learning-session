# Docker & Kubernetes Complete Learning Roadmap
## From Beginner to Container Orchestration Expert

**Version:** 1.0  
**Last Updated:** March 2026  
**Target Audience:** Backend developers, DevOps engineers, System administrators  
**Prerequisites:** Basic Linux, command line, and networking knowledge  
**Goal:** Master containerization and orchestration for production deployments

---

## Table of Contents

1. [Learning Path Overview](#overview)
2. [Phase 1: Docker Fundamentals (Weeks 1-4)](#phase-1)
3. [Phase 2: Advanced Docker (Weeks 5-8)](#phase-2)
4. [Phase 3: Docker Compose & Multi-Container Apps (Weeks 9-10)](#phase-3)
5. [Phase 4: Kubernetes Fundamentals (Weeks 11-14)](#phase-4)
6. [Phase 5: Kubernetes Core Concepts (Weeks 15-18)](#phase-5)
7. [Phase 6: Advanced Kubernetes (Weeks 19-22)](#phase-6)
8. [Phase 7: Production Kubernetes (Weeks 23-26)](#phase-7)
9. [Real-World Projects](#projects)
10. [Best Practices & Security](#best-practices)
12. [Learning Resources](#resources)

---

<a name="overview"></a>
## 1. Learning Path Overview

[Previous content from Phase 1-4 remains the same...]

---

<a name="phase-5"></a>
## 6. Phase 5: Kubernetes Core Concepts (Weeks 15-18)

### 6.1 ConfigMaps & Secrets

**ConfigMaps** store non-confidential configuration data.
**Secrets** store sensitive information (passwords, tokens, keys).

**ConfigMap Creation:**

```bash
# From literal values
kubectl create configmap app-config \
  --from-literal=APP_ENV=production \
  --from-literal=LOG_LEVEL=info

# From file
kubectl create configmap app-config --from-file=app.properties

# From directory
kubectl create configmap app-config --from-file=config/
```

**configmap.yaml:**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  APP_ENV: production
  LOG_LEVEL: info
  app.properties: |
    database.host=db.example.com
    database.port=5432
    cache.enabled=true
```

**Using ConfigMap in Pod:**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app-pod
spec:
  containers:
  - name: app
    image: myapp:1.0
    # Environment variables from ConfigMap
    env:
    - name: APP_ENV
      valueFrom:
        configMapKeyRef:
          name: app-config
          key: APP_ENV
    - name: LOG_LEVEL
      valueFrom:
        configMapKeyRef:
          name: app-config
          key: LOG_LEVEL
    
    # All ConfigMap data as environment variables
    envFrom:
    - configMapRef:
        name: app-config
    
    # Mount ConfigMap as volume
    volumeMounts:
    - name: config
      mountPath: /etc/config
  
  volumes:
  - name: config
    configMap:
      name: app-config
```

**Secrets Creation:**

```bash
# From literal values
kubectl create secret generic db-secret \
  --from-literal=username=admin \
  --from-literal=password=supersecret123

# From file
kubectl create secret generic ssh-key --from-file=ssh-privatekey=~/.ssh/id_rsa

# TLS secret
kubectl create secret tls tls-secret \
  --cert=path/to/cert.crt \
  --key=path/to/cert.key
```

**secret.yaml:**
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-secret
type: Opaque
data:
  # Base64 encoded values
  username: YWRtaW4=
  password: c3VwZXJzZWNyZXQxMjM=
```

**Create secret from command line:**
```bash
# Encode values
echo -n 'admin' | base64
echo -n 'supersecret123' | base64
```

**Using Secrets in Pod:**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app-pod
spec:
  containers:
  - name: app
    image: myapp:1.0
    
    # Environment variables from Secret
    env:
    - name: DB_USER
      valueFrom:
        secretKeyRef:
          name: db-secret
          key: username
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: db-secret
          key: password
    
    # Mount Secret as volume (recommended)
    volumeMounts:
    - name: secret
      mountPath: /etc/secrets
      readOnly: true
  
  volumes:
  - name: secret
    secret:
      secretName: db-secret
```

**Commands:**

```bash
# List ConfigMaps
kubectl get configmaps

# Describe ConfigMap
kubectl describe configmap app-config

# Edit ConfigMap
kubectl edit configmap app-config

# Delete ConfigMap
kubectl delete configmap app-config

# List Secrets
kubectl get secrets

# Describe Secret
kubectl describe secret db-secret

# View Secret data (decoded)
kubectl get secret db-secret -o jsonpath='{.data.password}' | base64 --decode
```

---

### 6.2 Persistent Volumes (PV) & Persistent Volume Claims (PVC)

**Storage Classes:**
- Define different types of storage (SSD, HDD, NFS, etc.)
- Support dynamic provisioning

**Persistent Volume (PV):**
- Piece of storage in the cluster
- Provisioned by admin or dynamically
- Has lifecycle independent of pods

**Persistent Volume Claim (PVC):**
- Request for storage by user
- Binds to available PV
- Used by pods

**Storage Architecture:**

```
┌─────────────────────────────────────────┐
│              Pod                        │
│  ┌──────────────────────────────┐      │
│  │   Container                   │      │
│  │  ┌────────────────────┐      │      │
│  │  │  Volume Mount      │      │      │
│  │  │  /data             │      │      │
│  │  └────────────────────┘      │      │
│  └──────────────────────────────┘      │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│    Persistent Volume Claim (PVC)        │
│    Request: 10Gi, ReadWriteOnce         │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│    Persistent Volume (PV)               │
│    Capacity: 20Gi                       │
│    Access: ReadWriteOnce                │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│    Actual Storage (Cloud/NFS/Local)     │
└─────────────────────────────────────────┘
```

**StorageClass Definition:**

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-storage
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp3
  fsType: ext4
  encrypted: "true"
reclaimPolicy: Retain
allowVolumeExpansion: true
volumeBindingMode: WaitForFirstConsumer
```

**Persistent Volume (Static Provisioning):**

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: my-pv
spec:
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: manual
  hostPath:
    path: /mnt/data
    type: DirectoryOrCreate
```

**Persistent Volume Claim:**

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
  storageClassName: fast-storage
```

**Using PVC in Pod:**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app-with-storage
spec:
  containers:
  - name: app
    image: nginx
    volumeMounts:
    - name: data
      mountPath: /usr/share/nginx/html
  volumes:
  - name: data
    persistentVolumeClaim:
      claimName: my-pvc
```

**Complete Example - Database with Persistent Storage:**

```yaml
# PersistentVolumeClaim
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
  storageClassName: fast-storage
---
# Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:15
        env:
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: password
        ports:
        - containerPort: 5432
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
          subPath: postgres
      volumes:
      - name: postgres-storage
        persistentVolumeClaim:
          claimName: postgres-pvc
---
# Service
apiVersion: v1
kind: Service
metadata:
  name: postgres
spec:
  selector:
    app: postgres
  ports:
  - port: 5432
    targetPort: 5432
  type: ClusterIP
```

**Commands:**

```bash
# List StorageClasses
kubectl get sc

# List PersistentVolumes
kubectl get pv

# List PersistentVolumeClaims
kubectl get pvc

# Describe PVC
kubectl describe pvc my-pvc

# Delete PVC
kubectl delete pvc my-pvc
```

---

### 6.3 Namespaces

**Namespaces** provide scope for names and allow resource isolation.

**Default Namespaces:**
- `default`: Default namespace for objects
- `kube-system`: System components
- `kube-public`: Public resources
- `kube-node-lease`: Node heartbeat data

**Create Namespace:**

```bash
# Imperative
kubectl create namespace development
kubectl create namespace production

# Declarative
kubectl apply -f namespace.yaml
```

**namespace.yaml:**
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: development
  labels:
    env: dev
```

**Using Namespaces:**

```bash
# List namespaces
kubectl get namespaces

# Get pods in specific namespace
kubectl get pods -n development

# Get pods in all namespaces
kubectl get pods --all-namespaces
kubectl get pods -A

# Set default namespace
kubectl config set-context --current --namespace=development

# Create resource in namespace
kubectl apply -f deployment.yaml -n development
```

**Resource with Namespace:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
  namespace: development
spec:
  replicas: 2
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: web
        image: nginx:latest
```

**Resource Quotas (Limit namespace resources):**

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: dev-quota
  namespace: development
spec:
  hard:
    requests.cpu: "10"
    requests.memory: 20Gi
    requests.storage: 100Gi
    persistentvolumeclaims: "10"
    pods: "50"
    services: "20"
```

**Limit Ranges (Set default limits):**

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: dev-limits
  namespace: development
spec:
  limits:
  - max:
      cpu: "2"
      memory: 4Gi
    min:
      cpu: "100m"
      memory: 128Mi
    default:
      cpu: "500m"
      memory: 512Mi
    defaultRequest:
      cpu: "200m"
      memory: 256Mi
    type: Container
```

---

### 6.4 Labels, Selectors & Annotations

**Labels** are key-value pairs attached to objects for identification.
**Selectors** filter objects based on labels.
**Annotations** store non-identifying metadata.

**Labels Example:**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-pod
  labels:
    app: web
    tier: frontend
    environment: production
    version: v1.2.0
spec:
  containers:
  - name: nginx
    image: nginx:latest
```

**Selectors:**

```bash
# Equality-based
kubectl get pods -l app=web
kubectl get pods -l environment=production
kubectl get pods -l app=web,tier=frontend

# Set-based
kubectl get pods -l 'environment in (production,staging)'
kubectl get pods -l 'tier notin (backend)'
kubectl get pods -l 'environment,tier'
```

**Using Selectors in Services:**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-service
spec:
  selector:
    app: web
    tier: frontend
  ports:
  - port: 80
    targetPort: 80
```

**Annotations Example:**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-pod
  labels:
    app: web
  annotations:
    description: "Frontend web server"
    contact: "devops@example.com"
    documentation: "https://wiki.example.com/web-pod"
    created-by: "kubectl create"
    last-updated: "2026-03-13"
spec:
  containers:
  - name: nginx
    image: nginx:latest
```

**Managing Labels:**

```bash
# Add label
kubectl label pod web-pod release=stable

# Update label
kubectl label pod web-pod environment=staging --overwrite

# Remove label
kubectl label pod web-pod version-

# Show labels
kubectl get pods --show-labels

# Filter by label
kubectl get pods -l app=web
```

---

### 6.5 Health Checks (Liveness, Readiness, Startup Probes)

**Probe Types:**
- **Liveness Probe**: Check if container is alive (restart if fails)
- **Readiness Probe**: Check if container is ready for traffic
- **Startup Probe**: Check if application has started

**Probe Mechanisms:**
- **HTTP GET**: HTTP request to endpoint
- **TCP Socket**: TCP connection to port
- **Exec**: Execute command in container

**Liveness Probe Example:**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-app
spec:
  containers:
  - name: app
    image: myapp:1.0
    ports:
    - containerPort: 8080
    
    # Liveness probe (restart if fails)
    livenessProbe:
      httpGet:
        path: /health
        port: 8080
        httpHeaders:
        - name: Custom-Header
          value: Awesome
      initialDelaySeconds: 30
      periodSeconds: 10
      timeoutSeconds: 5
      failureThreshold: 3
      successThreshold: 1
```

**Readiness Probe Example:**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-app
spec:
  containers:
  - name: app
    image: myapp:1.0
    ports:
    - containerPort: 8080
    
    # Readiness probe (remove from service if fails)
    readinessProbe:
      httpGet:
        path: /ready
        port: 8080
      initialDelaySeconds: 10
      periodSeconds: 5
      timeoutSeconds: 3
      failureThreshold: 3
      successThreshold: 1
```

**Startup Probe Example:**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: slow-app
spec:
  containers:
  - name: app
    image: slow-starting-app:1.0
    ports:
    - containerPort: 8080
    
    # Startup probe (allow slow startup)
    startupProbe:
      httpGet:
        path: /startup
        port: 8080
      initialDelaySeconds: 0
      periodSeconds: 10
      timeoutSeconds: 3
      failureThreshold: 30  # 30 * 10s = 5 minutes max startup time
      successThreshold: 1
    
    # Liveness probe (starts after startup succeeds)
    livenessProbe:
      httpGet:
        path: /health
        port: 8080
      periodSeconds: 10
```

**TCP Socket Probe:**

```yaml
livenessProbe:
  tcpSocket:
    port: 3306
  initialDelaySeconds: 15
  periodSeconds: 10
```

**Exec Probe:**

```yaml
livenessProbe:
  exec:
    command:
    - cat
    - /tmp/healthy
  initialDelaySeconds: 5
  periodSeconds: 5
```

**Complete Example with All Probes:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: app
        image: myapp:1.0
        ports:
        - containerPort: 8080
        
        # Startup probe - allow 5 minutes for startup
        startupProbe:
          httpGet:
            path: /startup
            port: 8080
          failureThreshold: 30
          periodSeconds: 10
        
        # Liveness probe - restart if unhealthy
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
          failureThreshold: 3
        
        # Readiness probe - remove from service if not ready
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
          failureThreshold: 3
        
        resources:
          requests:
            memory: "256Mi"
            cpu: "200m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

---

<a name="phase-6"></a>
## 7. Phase 6: Advanced Kubernetes (Weeks 19-22)

### 7.1 StatefulSets

**StatefulSets** manage stateful applications with:
- Stable network identities
- Stable persistent storage
- Ordered deployment and scaling
- Ordered rolling updates

**Use Cases:**
- Databases (MongoDB, MySQL, PostgreSQL)
- Message queues (Kafka, RabbitMQ)
- Distributed systems (Cassandra, Elasticsearch)

**StatefulSet Example:**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: mongodb
  labels:
    app: mongodb
spec:
  ports:
  - port: 27017
    name: mongodb
  clusterIP: None  # Headless service
  selector:
    app: mongodb
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mongodb
spec:
  serviceName: mongodb
  replicas: 3
  selector:
    matchLabels:
      app: mongodb
  template:
    metadata:
      labels:
        app: mongodb
    spec:
      containers:
      - name: mongodb
        image: mongo:7
        ports:
        - containerPort: 27017
          name: mongodb
        volumeMounts:
        - name: data
          mountPath: /data/db
        env:
        - name: MONGO_INITDB_ROOT_USERNAME
          value: admin
        - name: MONGO_INITDB_ROOT_PASSWORD
          valueFrom:
            secretKeyRef:
              name: mongodb-secret
              key: password
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: [ "ReadWriteOnce" ]
      storageClassName: fast-storage
      resources:
        requests:
          storage: 10Gi
```

**StatefulSet Features:**

```yaml
# Pod names are predictable
mongodb-0
mongodb-1
mongodb-2

# Network identities are stable
mongodb-0.mongodb.default.svc.cluster.local
mongodb-1.mongodb.default.svc.cluster.local
mongodb-2.mongodb.default.svc.cluster.local

# Ordered deployment
# Pods created sequentially: mongodb-0 → mongodb-1 → mongodb-2

# Ordered deletion
# Pods deleted in reverse: mongodb-2 → mongodb-1 → mongodb-0
```

**Commands:**

```bash
# Create StatefulSet
kubectl apply -f statefulset.yaml

# Get StatefulSets
kubectl get statefulsets

# Scale StatefulSet
kubectl scale statefulset mongodb --replicas=5

# Delete StatefulSet (keep PVCs)
kubectl delete statefulset mongodb

# Delete StatefulSet and PVCs
kubectl delete statefulset mongodb
kubectl delete pvc -l app=mongodb

# Rolling update
kubectl rollout status statefulset/mongodb
kubectl rollout history statefulset/mongodb
```

---

### 7.2 DaemonSets

**DaemonSets** ensure a copy of a pod runs on all (or some) nodes.

**Use Cases:**
- Node monitoring (Prometheus Node Exporter)
- Log collection (Fluentd, Filebeat)
- Storage daemons (Ceph, GlusterFS)
- Network plugins (Calico, Weave)

**DaemonSet Example:**

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: node-exporter
  namespace: monitoring
spec:
  selector:
    matchLabels:
      app: node-exporter
  template:
    metadata:
      labels:
        app: node-exporter
    spec:
      hostNetwork: true
      hostPID: true
      hostIPC: true
      containers:
      - name: node-exporter
        image: prom/node-exporter:latest
        ports:
        - containerPort: 9100
          hostPort: 9100
          name: metrics
        volumeMounts:
        - name: proc
          mountPath: /host/proc
          readOnly: true
        - name: sys
          mountPath: /host/sys
          readOnly: true
        securityContext:
          privileged: true
      volumes:
      - name: proc
        hostPath:
          path: /proc
      - name: sys
        hostPath:
          path: /sys
      tolerations:
      - effect: NoSchedule
        operator: Exists
```

**DaemonSet with Node Selector:**

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: gpu-driver
spec:
  selector:
    matchLabels:
      app: gpu-driver
  template:
    metadata:
      labels:
        app: gpu-driver
    spec:
      nodeSelector:
        gpu: "true"  # Only on nodes with gpu=true label
      containers:
      - name: gpu-driver
        image: nvidia/cuda:12.0-base
```

**Commands:**

```bash
# Get DaemonSets
kubectl get daemonsets

# Describe DaemonSet
kubectl describe daemonset node-exporter

# Update DaemonSet
kubectl apply -f daemonset.yaml

# Delete DaemonSet
kubectl delete daemonset node-exporter
```

---

### 7.3 Jobs & CronJobs

**Jobs** run pods to completion (batch processing).
**CronJobs** run jobs on a schedule.

**Job Example:**

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: data-migration
spec:
  completions: 1
  parallelism: 1
  backoffLimit: 3
  template:
    spec:
      containers:
      - name: migration
        image: postgres:15
        command:
        - sh
        - -c
        - |
          psql $DATABASE_URL -f /scripts/migration.sql
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        volumeMounts:
        - name: scripts
          mountPath: /scripts
      volumes:
      - name: scripts
        configMap:
          name: migration-scripts
      restartPolicy: OnFailure
```

**Parallel Job:**

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: parallel-job
spec:
  completions: 10  # Total successful completions needed
  parallelism: 3   # Run 3 pods in parallel
  template:
    spec:
      containers:
      - name: worker
        image: worker:1.0
        command: ["./process"]
      restartPolicy: Never
```

**CronJob Example:**

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: backup-job
spec:
  schedule: "0 2 * * *"  # Daily at 2 AM
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1
  concurrencyPolicy: Forbid
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: backup-tool:1.0
            command:
            - sh
            - -c
            - |
              pg_dump $DATABASE_URL > /backups/backup-$(date +%Y%m%d).sql
              aws s3 cp /backups/ s3://my-backups/ --recursive
            env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: db-secret
                  key: url
            - name: AWS_ACCESS_KEY_ID
              valueFrom:
                secretKeyRef:
                  name: aws-secret
                  key: access-key
            - name: AWS_SECRET_ACCESS_KEY
              valueFrom:
                secretKeyRef:
                  name: aws-secret
                  key: secret-key
            volumeMounts:
            - name: backups
              mountPath: /backups
          volumes:
          - name: backups
            emptyDir: {}
          restartPolicy: OnFailure
```

**Cron Schedule Format:**

```
# ┌───────────── minute (0 - 59)
# │ ┌───────────── hour (0 - 23)
# │ │ ┌───────────── day of month (1 - 31)
# │ │ │ ┌───────────── month (1 - 12)
# │ │ │ │ ┌───────────── day of week (0 - 6) (Sunday to Saturday)
# │ │ │ │ │
# * * * * *

Examples:
"0 0 * * *"      # Daily at midnight
"0 2 * * *"      # Daily at 2 AM
"*/15 * * * *"   # Every 15 minutes
"0 */4 * * *"    # Every 4 hours
"0 9 * * 1"      # Every Monday at 9 AM
"0 0 1 * *"      # First day of month
"0 0 * * 0"      # Every Sunday
```

**Commands:**

```bash
# Create Job
kubectl apply -f job.yaml

# Get Jobs
kubectl get jobs

# View Job logs
kubectl logs job/data-migration

# Delete Job
kubectl delete job data-migration

# Create CronJob
kubectl apply -f cronjob.yaml

# Get CronJobs
kubectl get cronjobs

# Manually trigger CronJob
kubectl create job --from=cronjob/backup-job backup-manual

# Suspend CronJob
kubectl patch cronjob backup-job -p '{"spec":{"suspend":true}}'

# Delete CronJob
kubectl delete cronjob backup-job
```

---

### 7.4 Ingress & Ingress Controllers

**Ingress** exposes HTTP/HTTPS routes from outside the cluster to services.
**Ingress Controller** implements the Ingress rules.

**Popular Ingress Controllers:**
- NGINX Ingress Controller
- Traefik
- HAProxy
- AWS ALB Ingress Controller
- GCE Ingress Controller

**Install NGINX Ingress Controller:**

```bash
# Using Helm
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
helm install ingress-nginx ingress-nginx/ingress-nginx

# Or using manifest
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.2/deploy/static/provider/cloud/deploy.yaml
```

**Simple Ingress:**

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: simple-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web-service
            port:
              number: 80
```

**Path-based Routing:**

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: path-based-ingress
spec:
  ingressClassName: nginx
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 8080
      - path: /web
        pathType: Prefix
        backend:
          service:
            name: web-service
            port:
              number: 80
```

**Host-based Routing:**

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: host-based-ingress
spec:
  ingressClassName: nginx
  rules:
  - host: api.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 8080
  - host: web.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web-service
            port:
              number: 80
```

**TLS/HTTPS Ingress:**

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: tls-ingress
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - myapp.example.com
    secretName: myapp-tls
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web-service
            port:
              number: 80
```

**Complete Example with Services:**

```yaml
# Deployment 1
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
      - name: frontend
        image: frontend:1.0
        ports:
        - containerPort: 3000
---
# Service 1
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
spec:
  selector:
    app: frontend
  ports:
  - port: 80
    targetPort: 3000
---
# Deployment 2
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
    spec:
      containers:
      - name: api
        image: api:1.0
        ports:
        - containerPort: 8080
---
# Service 2
apiVersion: v1
kind: Service
metadata:
  name: api-service
spec:
  selector:
    app: api
  ports:
  - port: 80
    targetPort: 8080
---
# Ingress
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/rate-limit: "100"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - app.example.com
    secretName: app-tls
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 80
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend-service
            port:
              number: 80
```

**Commands:**

```bash
# Get Ingresses
kubectl get ingress

# Describe Ingress
kubectl describe ingress app-ingress

# Get Ingress Controller pods
kubectl get pods -n ingress-nginx

# View Ingress Controller logs
kubectl logs -n ingress-nginx -l app.kubernetes.io/name=ingress-nginx
```

---

### 7.5 Helm - Kubernetes Package Manager

**Helm** is a package manager for Kubernetes that simplifies deployment and management.

**Install Helm:**

```bash
# Download and install
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Verify
helm version
```

**Helm Concepts:**
- **Chart**: Package of Kubernetes resources
- **Release**: Instance of a chart
- **Repository**: Collection of charts

**Using Helm Charts:**

```bash
# Add repository
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo add stable https://charts.helm.sh/stable
helm repo update

# Search charts
helm search repo nginx
helm search repo wordpress

# Install chart
helm install my-nginx bitnami/nginx

# Install with custom values
helm install my-nginx bitnami/nginx \
  --set service.type=LoadBalancer \
  --set replicaCount=3

# Install with values file
helm install my-nginx bitnami/nginx -f values.yaml

# List releases
helm list

# Get release status
helm status my-nginx

# Upgrade release
helm upgrade my-nginx bitnami/nginx --set replicaCount=5

# Rollback release
helm rollback my-nginx 1

# Uninstall release
helm uninstall my-nginx

# View chart values
helm show values bitnami/nginx
```

**Creating Custom Helm Chart:**

```bash
# Create chart
helm create myapp

# Chart structure:
myapp/
├── Chart.yaml          # Chart metadata
├── values.yaml         # Default values
├── templates/          # Kubernetes manifests
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   └── _helpers.tpl
└── charts/            # Dependencies
```

**Chart.yaml:**

```yaml
apiVersion: v2
name: myapp
description: My application Helm chart
type: application
version: 1.0.0
appVersion: "1.0"
```

**values.yaml:**

```yaml
replicaCount: 3

image:
  repository: myapp
  tag: "1.0"
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: true
  className: nginx
  hosts:
    - host: myapp.example.com
      paths:
        - path: /
          pathType: Prefix

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 200m
    memory: 256Mi

autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 80
```

**templates/deployment.yaml:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "myapp.fullname" . }}
  labels:
    {{- include "myapp.labels" . | nindent 4 }}
spec:
  {{- if not .Values.autoscaling.enabled }}
  replicas: {{ .Values.replicaCount }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "myapp.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "myapp.selectorLabels" . | nindent 8 }}
    spec:
      containers:
      - name: {{ .Chart.Name }}
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
        imagePullPolicy: {{ .Values.image.pullPolicy }}
        ports:
        - name: http
          containerPort: 80
          protocol: TCP
        resources:
          {{- toYaml .Values.resources | nindent 12 }}
```

**Install Custom Chart:**

```bash
# Package chart
helm package myapp

# Install from local
helm install myrelease ./myapp

# Install from package
helm install myrelease myapp-1.0.0.tgz

# Lint chart
helm lint myapp

# Template (dry-run)
helm template myrelease myapp

# Debug
helm install myrelease myapp --dry-run --debug
```

---

<a name="phase-7"></a>
## 8. Phase 7: Production Kubernetes (Weeks 23-26)

### 8.1 Horizontal Pod Autoscaling (HPA)

**HPA** automatically scales pods based on metrics.

**Metrics Server Installation:**

```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

**CPU-based HPA:**

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

**Memory-based HPA:**

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 15
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
      - type: Pods
        value: 4
        periodSeconds: 15
      selectPolicy: Max
```

**Custom Metrics HPA:**

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: "1000"
```

**Commands:**

```bash
# Create HPA
kubectl apply -f hpa.yaml

# Create HPA imperatively
kubectl autoscale deployment web-app --cpu-percent=70 --min=2 --max=10

# Get HPAs
kubectl get hpa

# Describe HPA
kubectl describe hpa web-app-hpa

# Watch HPA
kubectl get hpa -w

# Delete HPA
kubectl delete hpa web-app-hpa
```

---

### 8.2 Vertical Pod Autoscaling (VPA)

**VPA** automatically adjusts CPU and memory requests/limits.

**Install VPA:**

```bash
git clone https://github.com/kubernetes/autoscaler.git
cd autoscaler/vertical-pod-autoscaler
./hack/vpa-up.sh
```

**VPA Configuration:**

```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: web-app-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-app
  updatePolicy:
    updateMode: "Auto"  # Auto, Recreate, Initial, Off
  resourcePolicy:
    containerPolicies:
    - containerName: app
      minAllowed:
        cpu: 100m
        memory: 128Mi
      maxAllowed:
        cpu: 2
        memory: 2Gi
      controlledResources:
      - cpu
      - memory
```

---

### 8.3 RBAC (Role-Based Access Control)

**RBAC** controls who can access what in Kubernetes.

**Components:**
- **Role**: Permissions within namespace
- **ClusterRole**: Cluster-wide permissions
- **RoleBinding**: Binds role to users/groups
- **ClusterRoleBinding**: Binds cluster role

**Role Example:**

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
  namespace: development
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "watch"]
- apiGroups: [""]
  resources: ["pods/log"]
  verbs: ["get"]
```

**RoleBinding:**

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods
  namespace: development
subjects:
- kind: User
  name: jane
  apiGroup: rbac.authorization.k8s.io
- kind: ServiceAccount
  name: app-sa
  namespace: development
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

**ClusterRole:**

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: cluster-admin-readonly
rules:
- apiGroups: ["*"]
  resources: ["*"]
  verbs: ["get", "list", "watch"]
```

**ServiceAccount:**

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: app-sa
  namespace: production
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: app-sa-binding
  namespace: production
subjects:
- kind: ServiceAccount
  name: app-sa
  namespace: production
roleRef:
  kind: Role
  name: app-role
  apiGroup: rbac.authorization.k8s.io
```

**Using ServiceAccount in Pod:**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app-pod
spec:
  serviceAccountName: app-sa
  containers:
  - name: app
    image: myapp:1.0
```

**Commands:**

```bash
# Create ServiceAccount
kubectl create serviceaccount app-sa

# Get ServiceAccounts
kubectl get serviceaccounts

# Create Role
kubectl create role pod-reader --verb=get,list,watch --resource=pods

# Create RoleBinding
kubectl create rolebinding read-pods --role=pod-reader --user=jane

# Check permissions
kubectl auth can-i get pods --as=jane
kubectl auth can-i delete pods --as=jane

# View role
kubectl get role pod-reader -o yaml
```

---

### 8.4 Network Policies

**Network Policies** control pod-to-pod communication.

**Default Deny All:**

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

**Allow from Specific Pods:**

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-network-policy
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: database
    ports:
    - protocol: TCP
      port: 5432
  - to:
    - namespaceSelector:
        matchLabels:
          name: monitoring
    ports:
    - protocol: TCP
      port: 9090
```

**Allow from Namespace:**

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-from-namespace
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes:
  - Ingress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          env: production
```

---

### 8.5 Monitoring with Prometheus & Grafana

**Install Prometheus Stack:**

```bash
# Add Helm repo
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Install
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace
```

**Access Services:**

```bash
# Prometheus
kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-prometheus 9090:9090

# Grafana
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80

# Get Grafana password
kubectl get secret -n monitoring prometheus-grafana -o jsonpath="{.data.admin-password}" | base64 --decode
```

**ServiceMonitor Example:**

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: app-metrics
  namespace: monitoring
spec:
  selector:
    matchLabels:
      app: myapp
  endpoints:
  - port: metrics
    interval: 30s
    path: /metrics
```

---

### 8.6 Logging with EFK Stack

**Install EFK (Elasticsearch, Fluentd, Kibana):**

```bash
# Elasticsearch
helm install elasticsearch elastic/elasticsearch \
  --set replicas=1 \
  --set minimumMasterNodes=1

# Fluentd
kubectl apply -f https://raw.githubusercontent.com/fluent/fluentd-kubernetes-daemonset/master/fluentd-daemonset-elasticsearch.yaml

# Kibana
helm install kibana elastic/kibana
```

---

<a name="projects"></a>
## 9. Real-World Projects

### Project 1: Microservices E-Commerce Platform

**Architecture:**
```
Users → Ingress → Frontend
                   ↓
          ┌────────┴────────┬───────────┬──────────┐
          ↓                 ↓           ↓          ↓
      Product API      Cart API    Order API   User API
          ↓                 ↓           ↓          ↓
      PostgreSQL         Redis      MongoDB   PostgreSQL
```

**Components:**
- Frontend (React/Vue)
- 4 Microservices (Node.js/Python)
- 3 Databases (PostgreSQL, MongoDB, Redis)
- Ingress for routing
- HPA for auto-scaling
- Prometheus monitoring

---

### Project 2: CI/CD Pipeline

**Tools:**
- GitLab/GitHub
- Jenkins/ArgoCD
- Docker
- Kubernetes
- Helm

**Pipeline:**
1. Code commit → Trigger build
2. Docker build → Push to registry
3. Deploy to staging → Run tests
4. Promote to production → Rolling update

---

### Project 3: Logging & Monitoring Stack

**Components:**
- Prometheus + Grafana
- EFK Stack
- Alert Manager
- Custom dashboards

---

<a name="best-practices"></a>
## 10. Best Practices & Security

### Docker Best Practices

1. **Use minimal base images**
2. **Multi-stage builds**
3. **Run as non-root**
4. **Scan for vulnerabilities**
5. **Don't store secrets in images**
6. **Use .dockerignore**
7. **One process per container**
8. **Use specific image tags**

### Kubernetes Best Practices

1. **Use namespaces**
2. **Set resource requests/limits**
3. **Implement health checks**
4. **Use RBAC**
5. **Enable network policies**
6. **Regular backups**
7. **GitOps workflow**
8. **Use Helm charts**

---

<a name="resources"></a>
## 12. Learning Resources

### Official Documentation
- Docker Docs: docs.docker.com
- Kubernetes Docs: kubernetes.io/docs

### Online Courses
- Udemy - Docker & Kubernetes (Stephen Grider)
- A Cloud Guru - Kubernetes Deep Dive
- KodeKloud - CKA/CKAD/CKS courses

### Practice
- Play with Docker: labs.play-with-docker.com
- Play with Kubernetes: labs.play-with-k8s.com
- Katacoda scenarios

### Books
- "Docker Deep Dive" by Nigel Poulton
- "Kubernetes in Action" by Marko Lukša
- "Kubernetes Patterns" by Bilgin Ibryam

### Communities
- Docker Community Forums
- Kubernetes Slack
- Reddit: r/docker, r/kubernetes
- Stack Overflow

---

**Quick Reference Commands:**

```bash
# Docker
docker build -t myapp:1.0 .
docker run -d -p 8080:80 myapp:1.0
docker-compose up -d

# Kubernetes
kubectl apply -f deployment.yaml
kubectl get pods
kubectl logs pod-name
kubectl exec -it pod-name -- sh
kubectl port-forward pod-name 8080:80

# Helm
helm install myapp ./chart
helm upgrade myapp ./chart
helm rollback myapp 1
```