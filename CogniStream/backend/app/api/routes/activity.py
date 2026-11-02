"""
Activity Explorer and Event Log Endpoints.
"""

from fastapi import APIRouter, Query
from typing import Optional
from backend.app.repositories.event_repository import event_repo

router = APIRouter(prefix="/activity", tags=["Activity"])

@router.get("/recent")
def get_recent_activity(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    team_id: Optional[str] = Query(None),
    source: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=1, le=100)
):
    offset = (page - 1) * page_size
    events, total = event_repo.get_events(
        start_date=start_date,
        end_date=end_date,
        team_id=team_id,
        source=source,
        category=category,
        search=search,
        offset=offset,
        limit=page_size
    )

    # Sanitize and minimize payload
    sanitized = []
    for ev in events:
        sanitized.append({
            "event_id": ev.get("event_id"),
            "timestamp": ev.get("timestamp"),
            "source": ev.get("source"),
            "event_type": ev.get("event_type"),
            "actor_id": ev.get("actor_id"),
            "team_id": ev.get("team_id"),
            "project_id": ev.get("project_id"),
            "interruption_category": ev.get("interruption_category"),
            "is_potential_interruption": ev.get("is_potential_interruption", 0),
        })

    return {
        "page": page,
        "page_size": page_size,
        "total_events": total,
        "total_pages": (total + page_size - 1) // page_size if total > 0 else 1,
        "events": sanitized
    }