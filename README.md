# CogniStream — Developer Flow-State & Cognitive Load Analytics Platform

[![Python](https://img.shields.io/badge/Python-3.11%20--%203.15-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-1.0.0-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg)](https://react.dev/)
[![ClickHouse](https://img.shields.io/badge/ClickHouse-MergeTree-FFCC01.svg)](https://clickhouse.com/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind-CSS-38B2AC.svg)](https://tailwindcss.com/)

> **CogniStream** is an engineering analytics platform that analyzes developer activity telemetry to identify workflow friction, context switching, and notification noise—helping engineering organizations understand where focus time is lost without surveillance or invasive psychological claims.

---

## 1. Quick Launch (One Command)

From the project root:

```bash
python start_dashboard.py
```
*Or double click `start.bat` on Windows.*

### Active Localhost URLs:
- **Dashboard UI:** [http://localhost:5173](http://localhost:5173)
- **FastAPI Documentation & Swagger:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **API Health Check:** [http://127.0.0.1:8000/api/health](http://127.0.0.1:8000/api/health)
- **Overview Analytics:** [http://127.0.0.1:8000/api/overview](http://127.0.0.1:8000/api/overview)

---

## 2. Platform Architecture

```
Mock Developer Telemetry (GitHub, Slack, Jira, IDE Heartbeats)
                           |
                           v
              Python Source Extractors
                           |
                           v
           Apache Airflow Orchestration DAGs
                           |
                           v
        Polars Cleaning & Event Deduplication
                           |
                           v
            ClickHouse Event Storage Engine
             (with Embedded Fallback Engine)
                           |
                           v
          Flow-State Analytics & Union Engine
                           |
                           v
             FastAPI Analytical REST API
                           |
                           v
              React 18 + Vite Dashboard
```

---

## 3. Directory Structure

```
CogniStream-Developer-Flow-State-Cognitive-Load-Analytics/
|-- start_dashboard.py                 # Unified launcher for Backend & Frontend
|-- start.bat                          # One-click Windows launcher
|-- render.yaml                        # Cloud deployment blueprint (Render)
|-- .env                               # Environment configuration
|-- .gitignore                         # Project-wide ignore patterns
|-- README.md                          # Primary repository documentation
|
|-- CogniStream/
    |-- backend/                       # FastAPI application & API routers
    |   |-- app/
    |   |   |-- main.py                # FastAPI entrypoint
    |   |   |-- config.py              # Settings & thresholds
    |   |   |-- database.py            # ClickHouse & fallback engine
    |   |   |-- api/routes/            # REST API endpoints
    |   |   |-- analytics/engine.py    # Focus block & interval union engine
    |   |   |-- repositories/          # Event query repositories
    |   |   |-- services/              # Metric calculations
    |   |-- tests/                     # Backend API & Engine test suites
    |   |-- requirements.txt           # Python dependencies
    |
    |-- frontend/                      # React 18 + TypeScript + Vite UI
    |   |-- src/
    |   |   |-- components/            # Header, Sidebar, KpiCard, InsightCard
    |   |   |-- pages/                 # Overview, Flow, Interruptions, Teams, Explorer
    |   |   |-- services/api.ts        # Typed API client
    |   |   |-- types/api.ts           # Schema interfaces
    |   |-- dist/                      # Pre-built production distribution
    |   |-- package.json
    |
    |-- ingestion/                     # Ingestion & generation pipelines
    |   |-- extractors/                # GitHub, Slack, Jira, IDE telemetry
    |   |-- generators/                # Deterministic synthetic generator
    |   |-- transforms/                # Polars deduplication & normalization
    |   |-- loaders/                   # Persistence loader
    |   |-- tests/                     # Pipeline tests
    |
    |-- airflow/                       # Airflow DAGs (Ingestion & Analytics)
    |-- clickhouse/                    # ClickHouse SQL schema definitions
    |-- data_fallback/                 # Verified fallback datasets (20,589 events)
    |-- docs/                          # In-depth architectural & methodology docs
    |-- scripts/                       # Bootstrap, verification & pipeline runners
        |-- bootstrap.py
        |-- run_pipeline.py
        |-- verify_setup.py
```

---

## 4. Running Tests

Run the full automated test suite (20 tests covering analytics formulas, endpoints, and ingestion pipelines):

```bash
cd CogniStream
python -m pytest backend/tests/ ingestion/tests/ -v
```

---

## 5. Analytics Methodology Highlights

- **Focus Qualification Threshold:** Continuous IDE sessions $\ge 90$ minutes qualify as deep focus.
- **Inactivity Session Gap:** An inactivity gap $> 15$ minutes splits IDE activity into new sessions.
- **Interval Union Interruption Model:** Multiple notifications arriving within overlapping recovery windows are merged via union math to guarantee zero double-counting.
- **Context-Switching Tax Formula:**
  $$\text{Tax } (\%) = \frac{\text{Interruption-Associated Focus Loss (mins)}}{\text{Total Observed IDE Active Time (mins)}} \times 100$$

