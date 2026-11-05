# CogniStream — Developer Flow-State & Cognitive Load Analytics Platform

[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.14-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-1.0.0-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg)](https://react.dev/)
[![ClickHouse](https://img.shields.io/badge/ClickHouse-MergeTree-FFCC01.svg)](https://clickhouse.com/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind-CSS-38B2AC.svg)](https://tailwindcss.com/)

> **CogniStream** is an engineering analytics platform that analyzes developer activity telemetry to identify workflow friction, context switching, and notification noise—helping engineering organizations understand where focus time is lost without surveillance or invasive psychological claims.

---

## 1. Problem Statement

Traditional engineering productivity metrics (lines of code, PR counts, tickets closed) fail to measure developer focus capacity. Developers frequently lose concentration due to interruptions from automated CI/CD notifications, direct Slack messages, context-switching between disparate repositories, and meetings.

Instead of measuring simplistic output or claiming to read a developer's mind, CogniStream:
* Reconstructs continuous focus sessions from observable IDE telemetry.
* Quantifies **Qualifying Focus Blocks** (sessions &ge; 90 minutes).
* Categorizes potential interruption triggers (CI/CD alerts, DMs, mentions, project switches).
* Calculates the **Context-Switching Tax (%)** using non-overlapping recovery window interval union.
* Generates **deterministic, data-grounded insights** into team workflow friction.

---

## 2. Key Features

- **Multi-Source Extraction:** Ingests events from GitHub, Slack, Jira, and IDE Activity Watch.
- **Deterministic Mock Data:** Produces 30 days of realistic developer activity (20,000+ events) with varied behavioral profiles (deep focus, interrupted, context switchers).
- **Session Reconstruction Heuristics:** Automatically merges heartbeats within 15 minutes of inactivity; detects explicit session boundaries.
- **Interval Union Recovery Engine:** Mathematically guarantees zero double-counting of overlapping interruption recovery windows.
- **FastAPI Analytics Backend:** REST API with parameterized queries, input validation, health checks, and responsive caching.
- **Editorial Human-Designed UI:** Restrained, developer-focused aesthetic using warm off-white, dark charcoal typography, subtle borders, and zero tacky neon gradients.
- **Transparent Methodology:** Every calculation, assumption, and limitation is fully documented and accessible directly from the dashboard navigation.

---

## 3. Architecture

```
Mock Developer Event Sources (GitHub, Slack, Jira, IDE)
                      |
                      v
          Python Source Extractors
                      |
                      v
      Apache Airflow DAGs (Ingestion & Analytics)
                      |
                      v
   Polars Cleaning, Deduplication & Normalization
                      |
                      v
        ClickHouse Event & Analytics Tables
                      |
                      v
          Flow-State Analytics Engine
                      |
                      v
           FastAPI Analytical REST API
                      |
                      v
        React + TypeScript Dashboard
```

---

## 4. Technology Stack

- **Data Ingestion & Orchestration:** Python 3.11+, Apache Airflow 2.8.2, Polars.
- **Analytical Storage:** ClickHouse (ReplacingMergeTree tables partitioned by `toYYYYMM`).
- **Analytics Engine:** Python, Polars, Interval Union Algorithm.
- **Backend API:** FastAPI, Pydantic, ClickHouse-Connect, Uvicorn.
- **Frontend Dashboard:** React 18, TypeScript, Vite, Tailwind CSS, Recharts, Lucide Icons.
- **Testing:** Pytest, HTTPX TestClient.

---

## 5. Repository Structure

```
cognistream/
|-- backend/
|   |-- app/
|   |   |-- main.py                    # FastAPI application entrypoint
|   |   |-- config.py                  # Environment settings & validation
|   |   |-- database.py                # ClickHouse connection manager with fallback
|   |   |-- api/routes/
|   |   |   |-- health.py              # Health check & storage status
|   |   |   |-- overview.py            # Overview KPIs & dynamic insights
|   |   |   |-- flow.py                # Focus blocks & trends
|   |   |   |-- interruptions.py       # Interruption breakdown & timeline
|   |   |   |-- teams.py               # Normalized team comparisons
|   |   |   |-- activity.py            # Paginated event explorer
|   |   |   |-- filters.py             # Filter metadata options
|   |   |-- analytics/
|   |   |   |-- engine.py              # Session reconstruction & interval union engine
|   |   |-- repositories/
|   |   |   |-- event_repository.py    # Query filters & database access
|   |   |-- services/
|   |   |   |-- analytics_service.py   # Aggregation & metric calculations
|   |-- tests/
|   |   |-- test_analytics_engine.py   # 7 unit tests for analytics formulas
|   |   |-- test_api_endpoints.py      # 10 integration tests for FastAPI routes
|   |-- requirements.txt
|   |-- Dockerfile
|
|-- frontend/
|   |-- src/
|   |   |-- components/
|   |   |   |-- Header.tsx             # Top bar with team & date filters
|   |   |   |-- Sidebar.tsx            # Left navigation bar
|   |   |   |-- KpiCard.tsx            # Clean editorial KPI card
|   |   |   |-- InsightCard.tsx        # Grounded observation card
|   |   |   |-- Badge.tsx              # Reusable badge tag
|   |   |-- pages/
|   |   |   |-- OverviewPage.tsx       # Executive dashboard
|   |   |   |-- FlowAnalyticsPage.tsx  # Focus blocks & duration distribution
|   |   |   |-- InterruptionsPage.tsx  # Interruption sources & timeline
|   |   |   |-- TeamComparisonPage.tsx # Per-developer normalized comparisons
|   |   |   |-- ActivityExplorerPage.tsx# Searchable & filterable event log
|   |   |   |-- MethodologyPage.tsx    # Formulas, assumptions & bias guide
|   |   |-- services/api.ts            # Frontend API client
|   |   |-- types/api.ts               # Complete TypeScript types
|   |   |-- App.tsx                    # Root dashboard shell
|   |   |-- main.tsx                   # React DOM root
|   |-- package.json
|   |-- vite.config.ts
|   |-- tailwind.config.js
|   |-- Dockerfile
|
|-- ingestion/
|   |-- extractors/                    # Source extractors (GitHub, Slack, Jira, IDE)
|   |-- generators/                    # Deterministic mock event generator
|   |-- transforms/                    # Polars cleaning, deduplication & normalization
|   |-- loaders/                       # ClickHouse persistence loader
|   |-- tests/test_ingestion.py        # Ingestion pipeline tests
|
|-- airflow/
|   |-- dags/
|   |   |-- cognistream_ingestion_dag.py # DAG A: Ingestion pipeline
|   |   |-- cognistream_analytics_dag.py # DAG B: Analytics pipeline
|   |-- Dockerfile
|
|-- clickhouse/init/                   # SQL initialization scripts
|   |-- 001_create_database.sql
|   |-- 002_create_event_tables.sql
|   |-- 003_create_analytics_tables.sql
|
|-- scripts/
|   |-- bootstrap.py                   # Automated full-stack bootstrap
|   |-- generate_demo_data.py          # Standalone synthetic generator
|   |-- run_pipeline.py                # Standalone pipeline runner
|   |-- verify_setup.py                # System verification & integrity audit
|
|-- docs/                              # Technical documentation
|   |-- architecture.md
|   |-- data_dictionary.md
|   |-- analytics_methodology.md
|   |-- setup.md
|   |-- troubleshooting.md
|   |-- demo_guide.md
|
|-- .env.example
|-- docker-compose.yml
|-- Makefile
|-- README.md
```

---

## 6. Prerequisites

- Python 3.11+
- Node.js 18+ (Node.js v20.18.0 portable executable provided in `tools/node` if needed)
- Docker & Docker Compose (optional, for full containerized stack)

---

## 7. Quickstart (Local Development)

### 1. Environment Setup
```bash
cp .env.example .env
```

### 2. Install Dependencies
```bash
pip install -r backend/requirements.txt
cd frontend && npm install && cd ..
```

### 3. Run Pipeline (Ingestion + Analytics)
```bash
python scripts/run_pipeline.py
```
Outputs 20,589 normalized events, 514 reconstructed focus blocks, and 71 daily aggregates.

### 4. Verify System Setup
```bash
python scripts/verify_setup.py
```

### 5. Start Backend API
```bash
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```
* API Documentation: `http://localhost:8000/docs`

### 6. Start Frontend Dashboard
```bash
cd frontend
npm run dev
```
* Dashboard URL: `http://localhost:5173`

---

## 8. Docker Compose Deployment

To launch ClickHouse, FastAPI, React Frontend, and Airflow in containers:

```bash
docker-compose up --build
```

### Service URLs:
- **Dashboard UI:** `http://localhost:5173`
- **FastAPI Documentation:** `http://localhost:8000/docs`
- **ClickHouse HTTP:** `http://localhost:8123`
- **Airflow Webserver:** `http://localhost:8080` (credentials: `airflow` / `airflow`)

---

## 9. Running Automated Tests

Run the complete test suite across backend API, analytics engine, and data ingestion:

```bash
python -m pytest backend/tests/ ingestion/tests/ -v
```

All 20 test cases verify:
- Focus block reconstruction with 15-minute inactivity gaps.
- Non-overlapping interval union recovery calculations.
- Context-Switching Tax formula with zero-denominator safety.
- Schema validation and event categorization.
- Polars deduplication correctness.
- Complete FastAPI endpoint response schemas and pagination.

---

## 10. Analytics Engine Assumptions

- **Focus Qualification Threshold:** Focus blocks &ge; 90 minutes are classified as *Qualifying Focus*.
- **Inactivity Session Gap:** An inactivity gap &gt; 15 minutes splits continuous IDE heartbeats into new sessions.
- **Recovery Window Assumptions:**
  - `ci_cd_notification`: 12.0 minutes
  - `direct_message`: 15.0 minutes
  - `project_switch`: 18.0 minutes
  - `mention`: 10.0 minutes
  - `task_switch`: 10.0 minutes
- **Context-Switching Tax Formula:**
  $$\text{Tax } (\%) = \frac{\text{Estimated Interruption-Associated Focus Loss (mins)}}{\text{Total Observed IDE Active Time (mins)}} \times 100$$
- **Interval Union Guarantee:** Multiple interruptions arriving in close succession are merged into a single disjoint time span, eliminating double-counting of recovery periods.

---

## 11. Known Limitations & Future Improvements

- **Async Notifications:** Engineers may not notice every bot notification immediately. Current metrics model an upper bound on potential friction.
- **Calendar Integrations:** Future releases can integrate Google Calendar / Outlook APIs to explicitly account for scheduled meetings vs ad-hoc interruptions.
- **IDE Extensions:** Direct VS Code and JetBrains plugins can provide richer in-editor friction feedback directly to developers.

---

## 12. License

CogniStream is open-source software licensed under the MIT License.
