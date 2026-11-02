-- 002_create_event_tables.sql
-- CogniStream Event Tables

-- 1. Raw source events table
CREATE TABLE IF NOT EXISTS cognistream.raw_developer_events
(
    event_id String,
    event_timestamp DateTime64(3, 'UTC'),
    source LowCardinality(String),
    event_type LowCardinality(String),
    actor_id LowCardinality(String),
    team_id LowCardinality(String),
    raw_payload String,
    ingestion_timestamp DateTime64(3, 'UTC') DEFAULT now64(3)
)
ENGINE = ReplacingMergeTree(ingestion_timestamp)
PARTITION BY toYYYYMM(event_timestamp)
ORDER BY (team_id, source, event_type, actor_id, event_timestamp, event_id)
SETTINGS index_granularity = 8192;

-- 2. Cleaned and normalized developer events table
CREATE TABLE IF NOT EXISTS cognistream.developer_events
(
    event_id String,
    timestamp DateTime64(3, 'UTC'),
    source LowCardinality(String),
    event_type LowCardinality(String),
    actor_id LowCardinality(String),
    team_id LowCardinality(String),
    session_id Nullable(String),
    project_id Nullable(String),
    interruption_category LowCardinality(String),
    is_potential_interruption UInt8 DEFAULT 0,
    normalized_metadata String,
    ingestion_timestamp DateTime64(3, 'UTC') DEFAULT now64(3)
)
ENGINE = ReplacingMergeTree(ingestion_timestamp)
PARTITION BY toYYYYMM(timestamp)
ORDER BY (team_id, actor_id, timestamp, event_id)
SETTINGS index_granularity = 8192;
