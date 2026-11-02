"""
Integration tests for FastAPI endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert data["service"] == "CogniStream Analytics Platform"

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "table_counts" in data

def test_filters_endpoint():
    response = client.get("/api/filters")
    assert response.status_code == 200
    data = response.json()
    assert "teams" in data
    assert "projects" in data
    assert "categories" in data
    assert len(data["teams"]) >= 3

def test_overview_endpoint():
    response = client.get("/api/overview")
    assert response.status_code == 200
    data = response.json()
    assert "kpis" in data
    assert "insights" in data
    kpis = data["kpis"]
    assert "observed_ide_hours" in kpis
    assert "qualifying_focus_hours" in kpis
    assert "estimated_context_switching_tax_pct" in kpis
    assert kpis["active_developers"] > 0

def test_flow_blocks_endpoint():
    response = client.get("/api/flow/blocks")
    assert response.status_code == 200
    data = response.json()
    assert "total_blocks" in data
    assert "duration_distribution" in data
    assert "blocks" in data
    assert data["total_blocks"] > 0

def test_flow_trends_endpoint():
    response = client.get("/api/flow/trends")
    assert response.status_code == 200
    data = response.json()
    assert "trends" in data
    assert len(data["trends"]) > 0

def test_interruption_breakdown_endpoint():
    response = client.get("/api/interruptions/breakdown")
    assert response.status_code == 200
    data = response.json()
    assert "breakdown" in data
    assert len(data["breakdown"]) > 0
    # Ensure CI/CD is present in breakdown
    cats = [c["category"] for c in data["breakdown"]]
    assert "ci_cd_notification" in cats

def test_interruption_timeline_endpoint():
    response = client.get("/api/interruptions/timeline")
    assert response.status_code == 200
    data = response.json()
    assert "timeline" in data
    assert len(data["timeline"]) > 0

def test_teams_comparison_endpoint():
    response = client.get("/api/teams/comparison")
    assert response.status_code == 200
    data = response.json()
    assert "teams" in data
    assert len(data["teams"]) >= 3
    for tm in data["teams"]:
        assert "qualifying_hours_per_dev" in tm
        assert "avg_focus_block_minutes" in tm
        assert "context_switching_tax_pct" in tm

def test_activity_recent_endpoint():
    response = client.get("/api/activity/recent?page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 1
    assert data["page_size"] == 10
    assert "events" in data
    assert len(data["events"]) == 10
    assert "total_events" in data
    assert data["total_events"] > 100