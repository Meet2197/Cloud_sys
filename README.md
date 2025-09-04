# Cloud UI & File Explorer (Nuxt + FastAPI + SQLite)

Run with Docker:

```bash
docker compose up --build
```

- Frontend: http://localhost:3000
- Backend: http://localhost:8000/docs


## Tests

Run backend tests:

```
cd backend
pytest -q
```

## Seed data

To populate example data for local development:

```
cd backend
python seed.py
```

## Kubernetes (minimal)

Manifests are in `k8s/minimal`. Update image names, hostnames and apply:

```bash
kubectl apply -f k8s/minimal/namespace.yaml
kubectl apply -f k8s/minimal/pvc.yaml
kubectl apply -f k8s/minimal/backend-deployment.yaml
kubectl apply -f k8s/minimal/backend-service.yaml
kubectl apply -f k8s/minimal/frontend-deployment.yaml
kubectl apply -f k8s/minimal/frontend-service.yaml
kubectl apply -f k8s/minimal/ingress.yaml
```
