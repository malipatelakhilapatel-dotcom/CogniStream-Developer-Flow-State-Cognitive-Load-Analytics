"""
Generate Deterministic Demo Developer Activity Data for CogniStream.
Outputs events to JSON file for ingestion.
"""

import os
import sys
import json
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from ingestion.generators.generate_mock_events import MockEventGenerator

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("cognistream.scripts.generate")

def main():
    seed = int(os.getenv("RANDOM_SEED", "42"))
    days = int(os.getenv("SYNTHETIC_DATA_DAYS", "30"))

    logger.info(f"Generating synthetic developer telemetry (seed={seed}, days={days})...")
    generator = MockEventGenerator(seed=seed, days=days)
    events = generator.generate_events()

    output_dir = os.path.join(BASE_DIR, "data_fallback")
    os.makedirs(output_dir, exist_ok=True)
    out_file = os.path.join(output_dir, "raw_developer_events.json")

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(events, f, indent=2)

    logger.info(f"Successfully generated {len(events)} events and saved to {out_file}")

if __name__ == "__main__":
    main()
