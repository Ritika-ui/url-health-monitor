# 🏥 URL Health Monitor

A containerized API that checks if websites are up or down. Built with Flask, PostgreSQL, and Kubernetes.

🌐 Live Demo: https://url-health-monitor-1.onrender.com

## Features

- ✅ Real-time website health checks (UP/DOWN)
- 📊 REST API for health data
- 🗄️ PostgreSQL for storing history
- 🐳 Docker & ☸️ Kubernetes ready

## Tech Stack

| Tool | Purpose |
|------|---------|
| Flask | API server |
| PostgreSQL | Database |
| Docker | Containerization |
| Kubernetes | Orchestration |
| Minikube | Local K8s cluster |

## Quick Start (Docker Compose)

```bash
# Clone and run
git clone https://github.com/Ritika-ui/url-health-monitor.git
cd url-health-monitor
docker-compose up --build

# Test API
curl http://localhost:5000/health

API Endpoints
Endpoint	                What it does
-> GET /	                Welcome page
-> GET /health	                List recent health checks
-> GET /health/google.com	Check single URL

Deploy to Kubernetes

# Start Minikube
minikube start

# Load image
docker build -t sunfloweryyy/health-monitor:latest .
minikube image load sunfloweryyy/health-monitor:latest

# Deploy
kubectl apply -f k8s/postgres.yml
kubectl wait --for=condition=ready pod -l app=postgres --timeout=60s
kubectl apply -f k8s/deployment.yml

# Access
minikube service health-monitor-service


Cleanup

docker-compose down           # Stop Docker Compose
kubectl delete -f k8s/        # Stop Kubernetes deployment
minikube stop                 # Stop Minikube



Author
Ritika Khadka
