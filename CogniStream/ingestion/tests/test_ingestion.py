"""
Unit tests for data generation, normalization, and deduplication.
"""

import pytest
from datetime import datetime, timezone
from ingestion.generators.generate_mock_events import MockEventGenerator
from ingestion.transforms.normalize_events import normalize_event
from ingestion.transforms.clean_events import clean_and_deduplicate

def test_mock_event_generator_deterministic():
    gen1 = MockEventGenerator(seed=42, days=2)
    evts1 = gen1.generate_events()

    gen2 = MockEventGenerator(seed=42, days=2)
    evts2 = gen2.generate_events()

    assert len(evts1) > 0
    assert len(evts1) == len(evts2)
    assert evts1[0]["event_id"] == evts2[0]["event_id"]
    assert evts1[0]["timestamp"] == evts2[0]["timestamp"]

def test_normalize_event_interruption_categorization():
    raw_cicd = {
        "event_id": "evt-101",
        "timestamp": "2026-10-25T10:00:00Z",
        "source": "slack",
        "event_type": "ci_cd_notification",
        "actor_id": "dev-maya",
        "team_id": "team-platform",
        "metadata": {"build_status": "FAILED"}
    }
    norm = normalize_event(raw_cicd)
    assert norm is not None
    assert norm["interruption_category"] == "ci_cd_notification"
    assert norm["is_potential_interruption"] == 1

    # Standard heartbeat should not be an interruption
    raw_hb = {
        "event_id": "evt-102",
        "timestamp": "2026-10-25T10:05:00Z",
        "source": "ide",
        "event_type": "ide_heartbeat",
        "actor_id": "dev-chen",
        "team_id": "team-platform"
    }
    norm_hb = normalize_event(raw_hb)
    assert norm_hb["interruption_category"] == "ide_activity"
    assert norm_hb["is_potential_interruption"] == 0

def test_clean_and_deduplicate():
    evts = [
        {"event_id": "dup-1", "timestamp": "2026-10-25T10:00:00Z", "source": "ide"},
        {"event_id": "dup-1", "timestamp": "2026-10-25T10:00:00Z", "source": "ide"},
        {"event_id": "unique-2", "timestamp": "2026-10-25T10:02:00Z", "source": "slack"},
    ]
    cleaned = clean_and_deduplicate(evts)
    assert len(cleaned) == 2
    ids = [e["event_id"] for e in cleaned]
    assert "dup-1" in ids
    assert "unique-2" in ids
