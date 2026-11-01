"""
Interruption Analytics Endpoints.
"""

from fastapi import APIRouter, Query
from typing import Optional
from backend.app.services.analytics_service import analytics_service

router = APIRouter(prefix="/interruptions", tags=["Interruptions"])

@router.get("/breakdown")
def get_interruption_breakdown(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    team_id: Optional[str] = Query(None)
):
    breakdown = analytics_service.get_interruption_breakdown(start_date, end_date, team_id)
    return {"breakdown": breakdown}

@router.get("/timeline")
def get_interruption_timeline(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    team_id: Optional[str] = Query(None)
):
    timeline = analytics_service.get_interruption_timeline(start_date, end_date, team_id)
    return {"timeline": timeline}