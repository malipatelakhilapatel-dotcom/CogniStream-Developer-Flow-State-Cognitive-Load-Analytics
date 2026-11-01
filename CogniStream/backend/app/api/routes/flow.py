"""
Flow Analytics Endpoints.
"""

from fastapi import APIRouter, Query
from typing import Optional
from backend.app.services.analytics_service import analytics_service
from backend.app.repositories.event_repository import event_repo

router = APIRouter(prefix="/flow", tags=["Flow"])

@router.get("/blocks")
def get_focus_blocks(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    team_id: Optional[str] = Query(None),
    project_id: Optional[str] = Query(None),
    is_qualifying: Optional[int] = Query(None)
):
    blocks = event_repo.get_focus_blocks(start_date, end_date, team_id, project_id, is_qualifying)
    # Calculate duration buckets for distribution chart
    buckets = {"< 30m": 0, "30-60m": 0, "60-90m": 0, "90-120m": 0, "120m+": 0}
    for b in blocks:
        d = float(b.get("duration_minutes", 0.0))
        if d < 30:
            buckets["< 30m"] += 1
        elif d < 60:
            buckets["30-60m"] += 1
        elif d < 90:
            buckets["60-90m"] += 1
        elif d < 120:
            buckets["90-120m"] += 1
        else:
            buckets["120m+"] += 1

    duration_distribution = [{"bucket": k, "count": v} for k, v in buckets.items()]

    return {
        "total_blocks": len(blocks),
        "duration_distribution": duration_distribution,
        "blocks": blocks[:100] # Return top 100 for display
    }

@router.get("/trends")
def get_flow_trends(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    team_id: Optional[str] = Query(None)
):
    trends = analytics_service.get_flow_trends(start_date, end_date, team_id)
    return {"trends": trends}