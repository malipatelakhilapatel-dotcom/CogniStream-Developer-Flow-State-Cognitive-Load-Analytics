# CogniStream Data Dictionary

## 1. Table: `raw_developer_events`
Stores untouched telemetry events directly extracted from mock or live source APIs.

| Field | Type | Description |
|---|---|---|
| `event_id` | String | Unique event identifier |
| `event_timestamp` | DateTime64(3, 'UTC') | Source event generation timestamp |
| `source` | LowCardinality(String) | Origin system (`github`, `slack`, `jira`, `ide`) |
| `event_type` | LowCardinality(String) | Source event name |
| `actor_id` | LowCardinality(String) | Developer identifier (e.g. `dev-maya`) |
| `team_id` | LowCardinality(String) | Engineering team (`team-platform`, `team-product`, `team-data`) |
| `raw_payload` | String | Raw JSON payload from source |
| `ingestion_timestamp` | DateTime64(3, 'UTC') | Pipeline ingestion timestamp |

---

## 2. Table: `developer_events`
Normalized and categorized events with validated timestamps and schema conformance.

| Field | Type | Description |
|---|---|---|
| `event_id` | String | Primary deduplication key |
| `timestamp` | DateTime64(3, 'UTC') | Standardized UTC timestamp |
| `source` | LowCardinality(String) | Source system |
| `event_type` | LowCardinality(String) | Standardized event type |
| `actor_id` | LowCardinality(String) | Pseudonymized developer ID |
| `team_id` | LowCardinality(String) | Organizational team |
| `session_id` | Nullable(String) | Reconstructed editor session ID |
| `project_id` | Nullable(String) | Target repository or service |
| `interruption_category` | LowCardinality(String) | Classified trigger category |
| `is_potential_interruption` | UInt8 | 1 if interruption trigger; 0 otherwise |
| `normalized_metadata` | String | JSON formatted metadata |
| `ingestion_timestamp` | DateTime64(3, 'UTC') | Database insert timestamp |

---

## 3. Table: `focus_blocks`
Reconstructed continuous IDE activity intervals.

| Field | Type | Description |
|---|---|---|
| `focus_block_id` | String | Focus block identifier (e.g. `fb-dev-chen-1`) |
| `actor_id` | LowCardinality(String) | Developer ID |
| `team_id` | LowCardinality(String) | Team ID |
| `project_id` | Nullable(String) | Active project |
| `start_timestamp` | DateTime64(3, 'UTC') | Session start time |
| `end_timestamp` | DateTime64(3, 'UTC') | Session end time |
| `duration_minutes` | Float64 | Reconstructed duration in minutes |
| `interruption_count` | UInt32 | Number of potential interruptions during block |
| `is_qualifying` | UInt8 | 1 if duration &ge; 90 min threshold; 0 otherwise |
| `qualification_status` | LowCardinality(String) | `qualifying` or `non_qualifying` |
| `calculation_version` | LowCardinality(String) | Engine version (e.g. `v1.0.0`) |

---

## 4. Table: `daily_team_metrics`
Aggregated daily metrics per engineering team.

| Field | Type | Description |
|---|---|---|
| `date` | Date | Partition date |
| `team_id` | LowCardinality(String) | Team ID |
| `active_developer_count` | UInt32 | Distinct active engineers |
| `observed_ide_minutes` | Float64 | Total observed IDE activity time |
| `qualifying_focus_minutes` | Float64 | Focus minutes from blocks &ge; 90m |
| `focus_block_count` | UInt32 | Total number of reconstructed blocks |
| `qualifying_block_count` | UInt32 | Number of qualifying blocks |
| `avg_focus_block_duration_minutes` | Float64 | Average block length in minutes |
| `interruption_count` | UInt32 | Total potential interruption events |
| `context_switch_count` | UInt32 | Cross-project or task switch count |
| `estimated_interruption_loss_minutes` | Float64 | Non-overlapping estimated lost focus time |
| `context_switching_tax_pct` | Float64 | Estimated Context-Switching Tax % |
| `source_event_counts` | String | JSON event counts by source |

---

## 5. Table: `interruption_metrics`
Aggregated interruption counts and loss by category.

| Field | Type | Description |
|---|---|---|
| `period_start` | DateTime64(3, 'UTC') | Aggregation start |
| `period_end` | DateTime64(3, 'UTC') | Aggregation end |
| `period_type` | LowCardinality(String) | `daily`, `weekly`, or `hourly` |
| `team_id` | LowCardinality(String) | Team ID |
| `interruption_category` | LowCardinality(String) | Categorized trigger |
| `event_count` | UInt32 | Frequency of events |
| `affected_sessions_count` | UInt32 | Number of focus sessions overlapped |
| `estimated_associated_focus_loss_minutes` | Float64 | Recovery estimate in minutes |
