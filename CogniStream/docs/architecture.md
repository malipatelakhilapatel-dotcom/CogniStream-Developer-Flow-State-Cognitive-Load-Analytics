# CogniStream Architecture & Technical Design

## 1. High-Level Architecture

CogniStream is an end-to-end engineering flow-state and cognitive load analytics platform designed to quantify developer workflow friction, context switching, and uninterrupted focus periods without performing invasive mental surveillance.

```
+-----------------------------------------------------------------------+
|                       MOCK SOURCE EVENT GENERATOR                     |
|        GitHub API       Slack Events       Jira API       IDE Watches |
|     (Commits, PRs)    (CI/CD, DMs, @)    (Tasks, Bugs)   (Heartbeats) |
+-----------------------------------+-----------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
|                 APACHE AIRFLOW ORCHESTRATION LAYER                     |
|                                                                       |
|   [DAG A: Ingestion]                  [DAG B: Analytics Engine]        |
|   1. Verify Source Connectors         1. Read Normalized Events       |
|   2. Extract Multi-Source Payloads    2. Deduplicate (Polars)         |
|   3. Validate Event Schemas           3. Reconstruct Sessions         |
|   4. Categorize Interruption Triggers 4. Interval-Union Recovery Model|
|   5. Ingest Raw Table                 5. Context-Switching Tax Calc   |
|                                       6. Aggregate Team Daily Metrics |
+-----------------------------------+-----------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
|                    CLICKHOUSE ANALYTICAL STORAGE                      |
|                                                                       |
|   - raw_developer_events   (ReplacingMergeTree, Partition: toYYYYMM)  |
|   - developer_events       (ReplacingMergeTree, Partition: toYYYYMM)  |
|   - focus_blocks           (ReplacingMergeTree, Partition: toYYYYMM)  |
|   - daily_team_metrics     (ReplacingMergeTree, Partition: toYYYYMM)  |
|   - interruption_metrics   (ReplacingMergeTree, Partition: toYYYYMM)  |
+-----------------------------------+-----------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
|                       FASTAPI BACKEND REST API                        |
|                                                                       |
|   - Health & Engine Discovery       /api/health                       |
|   - Executive Overview & Insights   /api/overview                     |
|   - Flow Blocks & Trends            /api/flow/blocks, /api/flow/trends|
|   - Interruption Breakdown          /api/interruptions/breakdown      |
|   - Team Normalized Comparison      /api/teams/comparison             |
|   - Activity Explorer Log           /api/activity/recent              |
+-----------------------------------+-----------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
|               REACT + TAILWIND EDITORIAL DASHBOARD                    |
|                                                                       |
|   - Restrained human designer typography & neutral light palette      |
|   - 6 Core Views: Overview, Flow, Interruptions, Teams, Logs, Theory  |
|   - Zero-overlap interval visualization & deterministic observations  |
+-----------------------------------------------------------------------+
```

## 2. Component Design

### 2.1 Event Normalization & Categorization
Raw payloads from GitHub, Slack, Jira, and IDE Activity are parsed into a uniform schema:
- `event_id`: Unique identifier (deduplication key).
- `timestamp`: UTC ISO-8601 timestamp.
- `source`: Telemetry origin (`github`, `slack`, `jira`, `ide`).
- `event_type`: Event primitive.
- `actor_id`: Pseudonymized engineer identifier.
- `team_id`: Engineering group.
- `session_id`: Associated active editor session.
- `project_id`: Target repository or service.
- `interruption_category`: Classified category.
- `is_potential_interruption`: Boolean flag (1 if potential disruption trigger, 0 if background).

### 2.2 Deduplication Strategy
ClickHouse uses `ReplacingMergeTree(ingestion_timestamp)` engine ordered by `(team_id, actor_id, timestamp, event_id)`.
In the transformation pipeline, Polars executes in-memory deduplication `df.unique(subset=["event_id"], keep="last")` prior to database writes, ensuring idempotent execution across retries.

### 2.3 Non-Overlapping Recovery Interval Union
Cognitive research indicates that interruptions incur context recovery latency. When bursts of interruptions occur (e.g. 5 Slack alerts in 10 minutes), naive summation creates unrealistic numbers exceeding total clock time.
CogniStream uses the mathematical **Interval Union Algorithm**:
1. For each interruption $i$ at $T_i$ with nominal recovery $R_i$, create interval $[T_i, T_i + R_i]$.
2. Sort intervals by start time.
3. Merge overlapping and contiguous intervals into $[S_k, E_k]$.
4. Total loss is $\sum (E_k - S_k)$, strictly guaranteeing zero double-counting.
