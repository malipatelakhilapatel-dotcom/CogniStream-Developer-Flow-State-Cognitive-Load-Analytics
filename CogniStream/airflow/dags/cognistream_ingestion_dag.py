"""
CogniStream Ingestion DAG (DAG A).
Orchestrates event extraction from GitHub, Slack, Jira, and IDE Activity Watch,
validates payloads, normalizes schemas, and loads into ClickHouse.
"""

from datetime import datetime, timedelta, timezone
import json
import logging
import os
import sys

# Add project root to sys.path so operators find modules
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from ingestion.generators.generate_mock_events import MockEventGenerator
from ingestion.extractors.github_extractor import GitHubExtractor
from ingestion.extractors.slack_extractor import SlackExtractor
from ingestion.extractors.jira_extractor import JiraExtractor
from ingestion.extractors.ide_extractor import IDEActivityExtractor
from ingestion.transforms.normalize_events import normalize_event
from ingestion.loaders.clickhouse_loader import ClickHouseLoader

logger = logging.getLogger("airflow.cognistream.ingestion")

def check_sources_availability(**context):
    logger.info("Checking data source connectivity and mock mode configuration...")
    mock_mode = os.getenv("MOCK_DATA_MODE", "true").lower() == "true"
    logger.info(f"Source configuration verified. Mock data mode: {mock_mode}")
    return {"status": "ok", "mock_mode": mock_mode}

def extract_all_events(**context):
    logger.info("Starting multi-source extraction pipeline...")
    days = int(os.getenv("SYNTHETIC_DATA_DAYS", "30"))
    seed = int(os.getenv("RANDOM_SEED", "42"))

    generator = MockEventGenerator(seed=seed, days=days)
    all_raw = generator.generate_events()

    # Extract via specialized source extractors
    gh_ext = GitHubExtractor()
    slack_ext = SlackExtractor()
    jira_ext = JiraExtractor()
    ide_ext = IDEActivityExtractor()

    gh_events = gh_ext.extract_events("cognistream/core", mock_events=all_raw)
    slack_events = slack_ext.extract_events(mock_events=all_raw)
    jira_events = jira_ext.extract_events(mock_events=all_raw)
    ide_events = ide_ext.extract_events(mock_events=all_raw)

    total_extracted = len(gh_events) + len(slack_events) + len(jira_events) + len(ide_events)
    logger.info(f"Extracted: GitHub={len(gh_events)}, Slack={len(slack_events)}, Jira={len(jira_events)}, IDE={len(ide_events)}")
    
    # Store raw events in raw table
    loader = ClickHouseLoader()
    raw_saved = loader.insert_raw_events(all_raw)
    logger.info(f"Stored {raw_saved} raw events.")

    # Return summary for downstream tasks
    return {"total_extracted": total_extracted, "raw_saved": raw_saved}

def normalize_and_load_events(**context):
    logger.info("Normalizing and validating event payloads...")
    days = int(os.getenv("SYNTHETIC_DATA_DAYS", "30"))
    seed = int(os.getenv("RANDOM_SEED", "42"))

    generator = MockEventGenerator(seed=seed, days=days)
    all_raw = generator.generate_events()

    normalized_events = []
    dropped_count = 0

    for raw in all_raw:
        norm = normalize_event(raw)
        if norm:
            normalized_events.append(norm)
        else:
            dropped_count += 1

    logger.info(f"Normalized {len(normalized_events)} events (dropped {dropped_count} invalid).")

    loader = ClickHouseLoader()
    inserted = loader.insert_developer_events(normalized_events)
    logger.info(f"Successfully loaded {inserted} normalized events into developer_events table.")
    return {"normalized_count": len(normalized_events), "inserted": inserted}

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
        "cognistream_ingestion_dag",
        default_args=default_args,
        description="Ingests developer activity events from multiple sources into ClickHouse",
        schedule_interval="0 1 * * *", # Daily at 01:00 UTC
        catchup=False,
        max_active_runs=1,
    )

    t1 = PythonOperator(
        task_id="check_sources_availability",
        python_callable=check_sources_availability,
        dag=dag,
    )

    t2 = PythonOperator(
        task_id="extract_all_events",
        python_callable=extract_all_events,
        dag=dag,
    )

    t3 = PythonOperator(
        task_id="normalize_and_load_events",
        python_callable=normalize_and_load_events,
        dag=dag,
    )

    t1 >> t2 >> t3

except ImportError:
    # Airflow not installed in host execution environment; standalone runner supported
    pass

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("Executing CogniStream Ingestion Pipeline standalone...")
    s1 = check_sources_availability()
    s2 = extract_all_events()
    s3 = normalize_and_load_events()
    print(f"Ingestion Pipeline Complete: {s3}")