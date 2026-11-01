"""
Unit tests for CogniStream Flow-State Analytics Engine.
"""

import pytest
from datetime import datetime, timezone, timedelta
from backend.app.analytics.engine import (
    FlowAnalyticsEngine,
    merge_intervals,
    parse_iso
)

def test_parse_iso():
    dt = parse_iso("2026-10-25T14:30:00Z")
    assert dt.year == 2026
    assert dt.hour == 14
    assert dt.tzinfo == timezone.utc

def test_merge_intervals_non_overlapping():
    t0 = datetime(2026, 10, 25, 10, 0, tzinfo=timezone.utc)
    t1 = t0 + timedelta(minutes=10)
    t2 = t0 + timedelta(minutes=20)
    t3 = t0 + timedelta(minutes=30)
    
    intervals = [(t0, t1), (t2, t3)]
    merged = merge_intervals(intervals)
    assert len(merged) == 2
    assert merged[0] == (t0, t1)
    assert merged[1] == (t2, t3)

def test_merge_intervals_overlapping():
    t0 = datetime(2026, 10, 25, 10, 0, tzinfo=timezone.utc)
    t1 = t0 + timedelta(minutes=15)
    t2 = t0 + timedelta(minutes=10)
    t3 = t0 + timedelta(minutes=25)
    
    # [10:00, 10:15] and [10:10, 10:25]
    intervals = [(t0, t1), (t2, t3)]
    merged = merge_intervals(intervals)
    assert len(merged) == 1
    assert merged[0] == (t0, t3)
    # Total merged duration is 25 minutes, not 15 + 15 = 30 minutes!

def test_reconstruct_focus_blocks_heartbeats():
    engine = FlowAnalyticsEngine(inactivity_threshold_minutes=15.0, qualification_threshold_minutes=90.0)
    base_time = datetime(2026, 10, 25, 9, 0, tzinfo=timezone.utc)

    # 30 heartbeats every 3 minutes = 90 minutes
    events = []
    for i in range(31):
        ts = base_time + timedelta(minutes=i * 3)
        events.append({
            "event_id": f"hb-{i}",
            "timestamp": ts.isoformat(),
            "source": "ide",
            "event_type": "ide_heartbeat",
            "actor_id": "dev-chen",
            "team_id": "team-platform",
            "session_id": "sess-1",
            "project_id": "proj-infra",
            "is_potential_interruption": 0
        })

    blocks = engine.reconstruct_focus_blocks(events)
    assert len(blocks) == 1
    b = blocks[0]
    assert b["actor_id"] == "dev-chen"
    assert b["duration_minutes"] == 90.0
    assert b["is_qualifying"] == 1
    assert b["qualification_status"] == "qualifying"

def test_session_split_on_long_inactivity():
    engine = FlowAnalyticsEngine(inactivity_threshold_minutes=15.0, qualification_threshold_minutes=90.0)
    base_time = datetime(2026, 10, 25, 9, 0, tzinfo=timezone.utc)

    # 3 heartbeats, then a 30-minute lunch gap, then 3 heartbeats
    events = [
        {"event_id": "1", "timestamp": (base_time).isoformat(), "source": "ide", "event_type": "ide_heartbeat", "actor_id": "dev-maya", "team_id": "team-platform"},
        {"event_id": "2", "timestamp": (base_time + timedelta(minutes=3)).isoformat(), "source": "ide", "event_type": "ide_heartbeat", "actor_id": "dev-maya", "team_id": "team-platform"},
        {"event_id": "3", "timestamp": (base_time + timedelta(minutes=6)).isoformat(), "source": "ide", "event_type": "ide_heartbeat", "actor_id": "dev-maya", "team_id": "team-platform"},
        # 30 minute gap > 15m threshold!
        {"event_id": "4", "timestamp": (base_time + timedelta(minutes=36)).isoformat(), "source": "ide", "event_type": "ide_heartbeat", "actor_id": "dev-maya", "team_id": "team-platform"},
        {"event_id": "5", "timestamp": (base_time + timedelta(minutes=39)).isoformat(), "source": "ide", "event_type": "ide_heartbeat", "actor_id": "dev-maya", "team_id": "team-platform"},
    ]

    blocks = engine.reconstruct_focus_blocks(events)
    assert len(blocks) == 2
    assert blocks[0]["actor_id"] == "dev-maya"
    assert blocks[1]["actor_id"] == "dev-maya"
    # Neither is >= 90 mins
    assert blocks[0]["is_qualifying"] == 0
    assert blocks[1]["is_qualifying"] == 0

def test_context_switching_tax_formula():
    engine = FlowAnalyticsEngine()
    
    # 60 mins loss / 200 mins observed = 30%
    tax = engine.compute_context_switching_tax(observed_ide_minutes=200.0, estimated_loss_minutes=60.0)
    assert tax == 30.0

    # Zero denominator
    assert engine.compute_context_switching_tax(observed_ide_minutes=0.0, estimated_loss_minutes=50.0) == 0.0

def test_empty_dataset_handling():
    engine = FlowAnalyticsEngine()
    assert engine.reconstruct_focus_blocks([]) == []
    loss = engine.calculate_estimated_focus_loss([], [])
    assert loss["total_estimated_loss_minutes"] == 0.0
    assert engine.aggregate_daily_metrics([], []) == []
    insights = engine.generate_deterministic_insights([], [], [])
    assert len(insights) == 1
    assert insights[0]["title"] == "Insufficient Data"