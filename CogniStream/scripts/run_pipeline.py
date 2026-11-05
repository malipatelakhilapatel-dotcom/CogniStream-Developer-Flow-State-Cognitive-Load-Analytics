"""
Run Ingestion and Analytics Pipeline for CogniStream.
Executes DAG A (Extraction + Ingestion) followed by DAG B (Focus & Interruption Analytics).
"""

import os
import sys
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from airflow.dags.cognistream_ingestion_dag import (
    check_sources_availability,
    extract_all_events,
    normalize_and_load_events
)
from airflow.dags.cognistream_analytics_dag import compute_and_load_analytics

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("cognistream.scripts.pipeline")

def run():
    logger.info("=== STEP 1: RUNNING INGESTION PIPELINE ===")
    check_sources_availability()
    extract_all_events()
    ingest_result = normalize_and_load_events()
    logger.info(f"Ingestion Finished: {ingest_result}")

    logger.info("=== STEP 2: RUNNING ANALYTICS PIPELINE ===")
    analytics_result = compute_and_load_analytics()
    logger.info(f"Analytics Finished: {analytics_result}")

    logger.info("CogniStream Pipeline completed successfully!")

if __name__ == "__main__":
    run()
