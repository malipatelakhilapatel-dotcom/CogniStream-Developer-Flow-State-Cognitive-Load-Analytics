"""
CogniStream Flow Analytics DAG (DAG B).
Calculates focus blocks, interruption metrics, Context-Switching Tax,
and team-level daily aggregates, then persists them to ClickHouse.
"""

from datetime import datetime, timedelta, timezone
import json
import logging
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from ingestion.transforms.clean_events import clean_and_deduplicate
from backend.app.analytics.engine import FlowAnalyticsEngine
from ingestion.loaders.clickhouse_loader import ClickHouseLoader

logger = logging.getLogger("airflow.cognistream.analytics")

def get_engine():
    inactivity = float(os.getenv("SESSION_INACTIVITY_THRESHOLD_MINUTES", "15.0"))
    qualification = float(os.getenv("FOCUS_QUALIFICATION_THRESHOLD_MINUTES", "90.0"))
    return FlowAnalyticsEngine(
        inactivity_threshold_minutes=inactivity,
        qualification_threshold_minutes=qualification
    )

def read_and_clean_events(**context):
    logger.info("Reading normalized events from storage...")
    loader = ClickHouseLoader()

    events = []
    # If ClickHouse connected, query developer_events
    if loader.connect() and loader.client:
        result = loader.client.query("SELECT * FROM cognistream.developer_events ORDER BY timestamp ASC")
        cols = result.column_names
        for row in result.result_rows:
            events.append(dict(zip(cols, row)))
    else:
        # Fallback reading
        fb_path = os.path.join(BASE_DIR, "data_fallback", "developer_events.json")
        if os.path.exists(fb_path):
            with open(fb_path, "r", encoding="utf-8") as f:
                events = json.load(f)

    logger.info(f"Loaded {len(events)} raw normalized events. Executing Polars deduplication...")
    cleaned = clean_and_deduplicate(events)
    logger.info(f"Cleaned dataset contains {len(cleaned)} unique events.")
    return cleaned

def compute_and_load_analytics(**context):
    logger.info("Computing focus blocks, interruption metrics, and daily aggregates...")
    cleaned_events = read_and_clean_events()
    if not cleaned_events:
        logger.warning("No events available to compute analytics.")
        return {"status": "no_data"}

    engine = get_engine()

    # 1. Reconstruct Focus Blocks
    focus_blocks = engine.reconstruct_focus_blocks(cleaned_events)
    logger.info(f"Reconstructed {len(focus_blocks)} focus blocks.")

    # 2. Interruption Loss
    loss_metrics = engine.calculate_estimated_focus_loss(cleaned_events, focus_blocks)
    logger.info(f"Estimated interruption loss: {loss_metrics['total_estimated_loss_minutes']} mins.")

    # 3. Daily Aggregations
    daily_records = engine.aggregate_daily_metrics(cleaned_events, focus_blocks)
    logger.info(f"Generated {len(daily_records)} daily team aggregate records.")

    # 4. Detailed Interruption Category Metrics
    interruption_records = []
    # Build daily interruption breakdown records
    by_day_cat: dict = {}
    for ev in cleaned_events:
        if ev.get("is_potential_interruption") == 1:
            day = ev["timestamp"][:10]
            tm = ev.get("team_id", "unknown")
            cat = ev.get("interruption_category", "default")
            key = (day, tm, cat)
            by_day_cat[key] = by_day_cat.get(key, 0) + 1

    for (day_str, tm, cat), count in by_day_cat.items():
        recovery_per_event = engine.recovery_minutes.get(cat, 10.0)
        est_loss = count * recovery_per_event
        interruption_records.append({
            "period_start": f"{day_str}T00:00:00",
            "period_end": f"{day_str}T23:59:59",
            "period_type": "daily",
            "team_id": tm,
            "interruption_category": cat,
            "event_count": count,
            "affected_sessions_count": max(1, count // 2),
            "estimated_associated_focus_loss_minutes": est_loss,
            "calculation_version": engine.calculation_version
        })

    # 5. Persist via Loader
    loader = ClickHouseLoader()
    fb_inserted = loader.insert_focus_blocks(focus_blocks)
    daily_inserted = loader.insert_daily_metrics(daily_records)
    intr_inserted = loader.insert_interruption_metrics(interruption_records)

    logger.info(f"Analytics successfully written to storage: FocusBlocks={fb_inserted}, DailyMetrics={daily_inserted}, InterruptionMetrics={intr_inserted}")
    return {
        "focus_blocks_count": fb_inserted,
        "daily_metrics_count": daily_inserted,
        "interruption_metrics_count": intr_inserted
    }

# Airflow DAG definition
try:
    from airflow import DAG
    from airflow.operators.python import PythonOperator

    default_args = {
        "owner": "cognistream",
        "depends_on_past": False,
        "start_date": datetime(2026, 1, 1),
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 2,
        "retry_delay": timedelta(minutes=5),
    }

    dag = DAG(
        "cognistream_analytics_dag",
        default_args=default_args,
        description="Calculates developer flow state, focus blocks, and interruption metrics",
        schedule_interval="30 1 * * *", # Daily at 01:30 UTC after ingestion
        catchup=False,
        max_active_runs=1,
    )

    t1 = PythonOperator(
        task_id="compute_and_load_analytics",
        python_callable=compute_and_load_analytics,
        dag=dag,
    )

except ImportError:
    pass

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("Executing CogniStream Analytics Pipeline standalone...")
    res = compute_and_load_analytics()
    print(f"Analytics Pipeline Complete: {res}")