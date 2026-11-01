"""
Health Check Endpoint.
"""

from fastapi import APIRouter
from backend.app.repositories.event_repository import event_repo

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("")
def get_health_status():
    return event_repo.get_health()