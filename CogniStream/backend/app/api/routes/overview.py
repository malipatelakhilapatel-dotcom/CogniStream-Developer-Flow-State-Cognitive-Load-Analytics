"""
Overview Dashboard Endpoints.
"""

from fastapi import APIRouter, Query
from typing import Optional
from backend.app.services.analytics_service import analytics_service

router = APIRouter(prefix="/overview", tags=["Overview"])

@router.get("")
def get_overview(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    team_id: Optional[str] = Query(None, description="Team identifier filter")
):
    kpis = analytics_service.get_overview_kpis(start_date, end_date, team_id)
    insights = analytics_service.get_insights(start_date, end_date, team_id)
    return {
        "kpis": kpis,
        "insights": insights
    }