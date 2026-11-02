# CogniStream Troubleshooting Guide

## Common Issues and Resolutions

### 1. ClickHouse Offline / Connection Refused
**Symptom:**
```
ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it
```
**Cause:**
ClickHouse is not running locally or Docker Desktop is stopped.
**Resolution:**
CogniStream has built-in auto-discovery and resilience:
- When ClickHouse is active, it writes and queries ClickHouse MergeTree tables.
- When ClickHouse is offline, CogniStream automatically routes queries to its verified embedded local data engine (`data_fallback/`).
- The dashboard top header displays an active badge indicating storage status (`ClickHouse MergeTree` vs `Embedded Local Engine`).
- To start ClickHouse: `docker-compose up clickhouse`

---

### 2. Frontend Cannot Reach Backend
**Symptom:**
`Failed to connect to CogniStream backend service` banner on the dashboard.
**Resolution:**
1. Ensure the FastAPI backend is running on `http://localhost:8000`.
2. Check `frontend/.env` or `VITE_API_BASE_URL` in root `.env` points to `http://localhost:8000/api`.
3. Verify CORS origins in `.env` include `http://localhost:5173`.

---

### 3. Node.js Not Recognized on Windows
**Symptom:**
`'node' is not recognized as an internal or external command`
**Resolution:**
CogniStream includes a standalone portable Node.js tool runner in `tools/node`. Prepend it to your PowerShell PATH:
```powershell
$env:PATH = "C:\Users\malip\congniiiiiii\tools\node;" + $env:PATH
npm run dev
```

---

### 4. Airflow DAG Loading in Local Python
**Symptom:**
`ModuleNotFoundError: No module named 'airflow'`
**Resolution:**
Airflow is an orchestration engine designed for Docker deployment. The DAG files in `airflow/dags/` contain dual-execution capabilities:
- When running inside the Airflow container, they execute standard `DAG` and `PythonOperator` definitions.
- When run locally via `python scripts/run_pipeline.py`, they execute standalone pipelines using native Python and Polars.
