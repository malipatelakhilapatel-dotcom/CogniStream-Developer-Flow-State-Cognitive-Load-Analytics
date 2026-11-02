# CogniStream Setup & Installation Guide

This guide details running CogniStream either locally in development mode or as a containerized stack using Docker Compose.

---

## 1. Prerequisites

### Local Development:
- **Python**: 3.11+ (Python 3.14 verified)
- **Node.js**: 18+ (Node.js v20.18.0 included in `tools/node` if needed)
- **Git**

### Containerized Deployment:
- **Docker**: 24.0+
- **Docker Compose**: v2.20+
- Recommended resources: 4 CPU cores, 6GB RAM (if running ClickHouse + Airflow together)

---

## 2. Quickstart: Local Development

### Step 1: Configure Environment
Copy the example environment file:
```bash
cp .env.example .env
```

### Step 2: Install Python Dependencies
```bash
pip install -r backend/requirements.txt
```

### Step 3: Run Data Generation & Pipeline
Execute the full ingestion and flow analytics pipeline:
```bash
python scripts/run_pipeline.py
```
This generates 30 days of realistic developer telemetry across GitHub, Slack, Jira, and IDE Activity, categorizes interruptions, reconstructs focus blocks, and aggregates metrics.

### Step 4: Verify Pipeline
```bash
python scripts/verify_setup.py
```

### Step 5: Start Backend API
```bash
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```
The FastAPI documentation will be available at: `http://localhost:8000/docs`

### Step 6: Start Frontend Dashboard
In a separate terminal:
```bash
cd frontend
npm install
npm run dev
```
Open your browser at: `http://localhost:5173`

---

## 3. Containerized Setup: Docker Compose

To start ClickHouse, FastAPI, React Frontend, and Airflow together:

```bash
docker-compose up --build
```

### Service Endpoints:
- **Dashboard UI**: `http://localhost:5173`
- **FastAPI Documentation**: `http://localhost:8000/docs`
- **ClickHouse HTTP**: `http://localhost:8123`
- **Airflow Webserver**: `http://localhost:8080` (credentials: `airflow` / `airflow`)
