"""
Event Cleaning and Deduplication for CogniStream using Polars.
Ensures stable deduplication, schema conformity, and chronological ordering.
"""

from typing import List, Dict, Any
import json
import logging

logger = logging.getLogger("cognistream.transforms.clean")

try:
    import polars as pl
    POLARS_AVAILABLE = True
except ImportError:
    POLARS_AVAILABLE = False
    logger.warning("Polars not yet loaded; using fallback cleaner.")

def clean_and_deduplicate(events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Deduplicates events by event_id, validates essential fields,
    and sorts chronologically.
    """
    if not events:
        return []

    if POLARS_AVAILABLE:
        try:
            # Load into Polars DataFrame
            df = pl.DataFrame(events)
            
            # Deduplicate by event_id keeping last
            if "event_id" in df.columns:
                df = df.unique(subset=["event_id"], keep="last")
            
            # Filter non-null timestamps
            if "timestamp" in df.columns:
                df = df.filter(pl.col("timestamp").is_not_null())
                df = df.sort("timestamp")
            
            return df.to_dicts()
        except Exception as e:
            logger.warning(f"Polars cleaning encountered issue: {e}. Falling back to standard deduplication.")

    # Pure Python robust fallback
    seen = set()
    cleaned = []
    for ev in events:
        eid = ev.get("event_id")
        ts = ev.get("timestamp")
        if not eid or not ts:
            continue
        if eid in seen:
            continue
        seen.add(eid)
        cleaned.append(ev)

    cleaned.sort(key=lambda x: str(x.get("timestamp", "")))
    return cleaned
