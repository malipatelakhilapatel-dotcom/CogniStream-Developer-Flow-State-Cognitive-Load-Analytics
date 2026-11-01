"""
Team Comparison Endpoints.
"""

from fastapi import APIRouter, Query
from typing import Optional
from backend.app.services.analytics_service import analytics_service

router = APIRouter(prefix="/teams", tags=["Teams"])

@router.get("/comparison")
def get_team_comparison(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None)
):
    comparison = analytics_service.get_team_comparison(start_date, end_date)
    return {"teams": comparison}