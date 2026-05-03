# 🏥 URL Health Monitor

> A containerized API that automatically monitors websites and tracks their uptime history.  
> Built with Flask, PostgreSQL, Docker, and Kubernetes.

🌐 **Live Demo:** [url-health-monitor-1.onrender.com](https://url-health-monitor-1.onrender.com)

---

## 📌 What It Does

- Automatically checks if websites are **UP** or **DOWN** every 30 seconds
- Stores full health check history in **PostgreSQL**
- Exposes a clean **REST API** to query results
- Runs as a fully containerized, **Kubernetes-orchestrated** application with 3 replicas

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│              Kubernetes Cluster          │
│                                         │
│  ┌─────────────┐    ┌────────────────┐  │
│  │  Flask API  │    │   monitor.py   │  │
│  │ (3 replicas)│    │ (checks every  │  │
│  │             │    │   30 seconds)  │  │
│  └──────┬──────┘    └───────┬────────┘  │
│         │                   │           │
│         └─────────┬─────────┘           │
│                   ▼                     │
│          ┌────────────────┐             │
│          │   PostgreSQL   │             │
│          │  (StatefulSet  │             │
│          │  + PVC 1Gi)    │             │
│          └────────────────┘             │
└─────────────────────────────────────────┘
         ▲
         │
   GitHub Actions
   (build & push
    on every commit)
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| **Flask** | REST API server |
| **PostgreSQL** | Persistent health check storage |
| **Docker** | Containerization |
| **Kubernetes** | Orchestration — 3 replicas, rolling updates |
| **Minikube** | Local Kubernetes cluster |
| **GitHub Actions** | CI/CD — auto build & push to Docker Hub |
| **Render** | Live cloud deployment |

---

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page — shows which pod is serving |
| `/health` | GET | Last 20 health check results from DB |
| `/health/<url>` | GET | Check a specific URL on demand |

**Example responses:**

```bash
# GET /health
[
  {
    "url": "google.com",
    "status": "UP",
    "last_checked": "2025-01-15T10:30:00"
  },
  {
    "url": "reddit.com",
    "status": "DOWN",
    "last_checked": "2025-01-15T10:29:30"
  }
]

# GET /health/github.com
{
  "url": "github.com",
  "status": "UP"
}
```

---

## 🚀 Quick Start

### Option 1 — Docker Compose (easiest)

```bash
# Clone the repo
git clone https://github.com/Ritika-ui/url-health-monitor.git
cd url-health-monitor

# Start everything (Flask + PostgreSQL)
docker-compose up --build

# Test the API
curl http://localhost:5000/
curl http://localhost:5000/health
curl http://localhost:5000/health/google.com
```

### Option 2 — Kubernetes (Minikube)

**Prerequisites:** Docker, Minikube, kubectl

```bash
# Start Minikube
minikube start

# Build and load image into Minikube
docker build -t sunfloweryyy/health-monitor:latest .
minikube image load sunfloweryyy/health-monitor:latest

# Deploy PostgreSQL first and wait for it to be ready
kubectl apply -f k8s/postgres.yml
kubectl wait --for=condition=ready pod -l app=postgres --timeout=60s

# Deploy the app
kubectl apply -f k8s/deployment.yml

# Open in browser
minikube service health-monitor-service
```

**Verify everything is running:**
```bash
kubectl get pods           # 3 health-monitor pods + 1 postgres pod
kubectl get services       # health-monitor-service + postgres-service
kubectl logs -l app=health-monitor    # view live logs
```

---

## 📁 Project Structure

```
url-health-monitor/
├── app/
│   ├── app.py              # Flask API — routes and endpoints
│   ├── monitor.py          # Background worker — checks URLs every 30s
│   ├── database.py         # Shared DB connection (used by both)
│   └── requirements.txt    # Python dependencies
├── k8s/
│   ├── deployment.yml      # App Deployment + Service + Secret
│   └── postgres.yml        # PostgreSQL StatefulSet + ConfigMap + Secret
├── .github/
│   └── workflows/
│       └── health.yml      # CI/CD pipeline
├── Dockerfile
├── docker-compose.yml
├── run.sh                  # Starts Flask + monitor in one container
└── README.md
```

---

## ⚙️ CI/CD Pipeline

Every push to `main` automatically triggers:

```
Push to main
     │
     ▼
GitHub Actions
     │
     ├── 1. Checkout code
     ├── 2. Set up Docker Buildx
     ├── 3. Login to Docker Hub (via GitHub Secrets)
     └── 4. Build & push sunfloweryyy/health-monitor:latest ✅
```

**Required GitHub Secrets:**

| Secret | Description |
|--------|-------------|
| `DOCKER_USERNAME` | Your Docker Hub username |
| `DOCKER_PASSWORD` | Your Docker Hub access token |

---

## 🗄️ Database Schema

```sql
CREATE TABLE health_checks (
    id           SERIAL PRIMARY KEY,
    url          TEXT NOT NULL,
    status       TEXT NOT NULL,         -- 'UP' or 'DOWN'
    last_checked TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🔒 Security

| What | How |
|------|-----|
| Database password | Stored in Kubernetes `Secret` — never hardcoded |
| Docker Hub credentials | Stored in GitHub Secrets — never in YAML files |
| PostgreSQL access | ClusterIP only — not exposed outside the cluster |

---

## 🧹 Cleanup

```bash
# Stop Docker Compose
docker-compose down

# Remove Kubernetes deployment
kubectl delete -f k8s/

# Stop Minikube
minikube stop
```

---

## 👩‍💻 Author

**Ritika Khadka**  

