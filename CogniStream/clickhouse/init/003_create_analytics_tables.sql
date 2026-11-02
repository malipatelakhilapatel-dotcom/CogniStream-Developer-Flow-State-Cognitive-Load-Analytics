-- 003_create_analytics_tables.sql
-- CogniStream Analytics Tables

-- 1. Focus Blocks: Reconstructed focus intervals
CREATE TABLE IF NOT EXISTS cognistream.focus_blocks
(
    focus_block_id String,
    actor_id LowCardinality(String),
    team_id LowCardinality(String),
    project_id Nullable(String),
    start_timestamp DateTime64(3, 'UTC'),
    end_timestamp DateTime64(3, 'UTC'),
    duration_minutes Float64,
    interruption_count UInt32 DEFAULT 0,
    is_qualifying UInt8 DEFAULT 0,
    qualification_status LowCardinality(String) DEFAULT 'non_qualifying',
    calculation_version LowCardinality(String) DEFAULT 'v1.0.0',
    created_at DateTime64(3, 'UTC') DEFAULT now64(3)
)
ENGINE = ReplacingMergeTree(created_at)
PARTITION BY toYYYYMM(start_timestamp)
ORDER BY (team_id, actor_id, start_timestamp, focus_block_id)
SETTINGS index_granularity = 8192;

-- 2. Daily Team Metrics: Pre-aggregated daily metrics per team
CREATE TABLE IF NOT EXISTS cognistream.daily_team_metrics
(
    date Date,
    team_id LowCardinality(String),
    active_developer_count UInt32 DEFAULT 0,
    observed_ide_minutes Float64 DEFAULT 0.0,
    qualifying_focus_minutes Float64 DEFAULT 0.0,
    total_focus_minutes Float64 DEFAULT 0.0,
    focus_block_count UInt32 DEFAULT 0,
    qualifying_block_count UInt32 DEFAULT 0,
    avg_focus_block_duration_minutes Float64 DEFAULT 0.0,
    interruption_count UInt32 DEFAULT 0,
    context_switch_count UInt32 DEFAULT 0,
    estimated_interruption_loss_minutes Float64 DEFAULT 0.0,
    context_switching_tax_pct Float64 DEFAULT 0.0,
    source_event_counts String DEFAULT '{}',
    calculation_version LowCardinality(String) DEFAULT 'v1.0.0',
    updated_at DateTime64(3, 'UTC') DEFAULT now64(3)
)
ENGINE = ReplacingMergeTree(updated_at)
PARTITION BY toYYYYMM(date)
ORDER BY (team_id, date)
SETTINGS index_granularity = 8192;

-- 3. Interruption Metrics: Aggregated interruption statistics by category
CREATE TABLE IF NOT EXISTS cognistream.interruption_metrics
(
    period_start DateTime64(3, 'UTC'),
    period_end DateTime64(3, 'UTC'),
    period_type LowCardinality(String) DEFAULT 'daily',
    team_id LowCardinality(String),
    interruption_category LowCardinality(String),
    event_count UInt32 DEFAULT 0,
    affected_sessions_count UInt32 DEFAULT 0,
    estimated_associated_focus_loss_minutes Float64 DEFAULT 0.0,
    calculation_version LowCardinality(String) DEFAULT 'v1.0.0',
    updated_at DateTime64(3, 'UTC') DEFAULT now64(3)
)
ENGINE = ReplacingMergeTree(updated_at)
PARTITION BY toYYYYMM(period_start)
ORDER BY (team_id, interruption_category, period_start)
SETTINGS index_granularity = 8192;
