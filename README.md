# Cloud Storage & File Explorer

A modern, interactive cloud storage solution with advanced file management, previews, and analytics.

Supports standard file types, N-D chunked images, and JSON metadata, with KNN-based clustering and filtering.

---

## Features

### Frontend

* Minimalist, dark-themed, fully responsive design
* File Explorer with grid/list views
* Rich previews and metadata panel
* Drag-and-drop file uploads
* Real-time search and dynamic filtering
* Folder and file actions via context menus
* Upload/download manager

### Backend

* Python FastAPI backend
* REST API for file management and analytics
* SQLite for local development (PostgreSQL ready)
* KNN-based clustering of file metadata
* CRUD operations for files, folders, and metadata

### DevOps

* Docker and Docker Compose for local development
* Kubernetes manifests for production deployment
* Persistent storage support

---

## Tech Stack

| Layer         | Technology                        |
| ------------- | --------------------------------- |
| Frontend      | Nuxt.js 3, Tailwind               |
| Backend       | Python 3, FastAPI, SQLAlchemy     |
| Database      | SQLite3 (local), PostgreSQL ready |
| Container     | Docker                            |
| Orchestration | Kubernetes                        |

---

## Project Structure

```
Cloud_sys/
├─ backend/         # FastAPI backend
│  ├─ app/
│  │  ├─ main.py
│  │  ├─ models.py
│  │  ├─ crud.py
│  │  ├─ database.py
│  ├─ seed.py       # Example seed data
│  ├─ requirements.txt
│  └─ tests/        # Pytest tests
├─ frontend/        # Nuxt.js frontend
│  ├─ pages/
│  ├─ components/
│  ├─ nuxt.config.ts
│  └─ package.json
├─ data/            # SQLite DB + blobs
├─ k8s/minimal/     # Minimal Kubernetes manifests
└─ README.md
```

---

## Quick Start (Local Development)

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdir -p data/blobs
python seed.py   # populate example data
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API runs at: `http://localhost:8000`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

UI runs at: `http://localhost:3000`

Make sure the environment variable points to the backend API:

```bash
NUXT_PUBLIC_API_BASE=http://localhost:8000
```

---

## Docker Compose

```bash
docker compose up --build
```

Seed data can be added via:

```bash
docker compose exec backend python seed.py
```

---

## Kubernetes Deployment

Minimal manifests are under `k8s/minimal/`.
Steps:

```bash
kubectl apply -f k8s/minimal/namespace.yaml
kubectl apply -f k8s/minimal/pvc.yaml
kubectl apply -f k8s/minimal/backend-deployment.yaml
kubectl apply -f k8s/minimal/backend-service.yaml
kubectl apply -f k8s/minimal/frontend-deployment.yaml
kubectl apply -f k8s/minimal/frontend-service.yaml
kubectl apply -f k8s/minimal/ingress.yaml
```

Update `cloud.example.com` in ingress and Docker image names for your environment.

---

## Running Tests

Backend tests with **pytest**:

```bash
cd backend
pytest -q
```

---

## Seed Data

Populate example data:

```bash
cd backend
python seed.py
```

Creates:

* Sample folders: `Documents`, `Pictures`
* Sample files with metadata
* Sample blob files in `data/blobs/`

---

## Notes

* For production, switch SQLite → PostgreSQL.
* Configure persistent storage for uploads (`data/blobs/`) in Docker/Kubernetes.
* KNN clustering endpoint is available at `/analytics/recluster`.

---

## License

MIT License
