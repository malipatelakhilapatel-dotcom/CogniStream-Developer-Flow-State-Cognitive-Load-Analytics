"""
Filters Metadata Endpoint.
"""

from fastapi import APIRouter
from backend.app.repositories.event_repository import event_repo

router = APIRouter(prefix="/filters", tags=["Filters"])

@router.get("")
def get_filter_options():
    return event_repo.get_filter_options()