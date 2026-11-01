"""
Event Normalization and Interruption Classification for CogniStream.
Converts raw heterogenous payloads from GitHub, Slack, Jira, and IDE telemetry
into standard normalized schema with explicit interruption categories.
"""

from datetime import datetime, timezone
import json
from typing import Dict, Any, Optional

INTERRUPTION_CATEGORIES = {
    "ci_cd_notification": {"is_interruption": True, "category": "ci_cd_notification"},
    "direct_message_received": {"is_interruption": True, "category": "direct_message"},
    "mention_received": {"is_interruption": True, "category": "mention"},
    "message_received": {"is_interruption": False, "category": "channel_message"},
    "project_switch": {"is_interruption": True, "category": "project_switch"},
    "issue_started": {"is_interruption": True, "category": "task_switch"},
    "issue_updated": {"is_interruption": False, "category": "task_update"},
    "pull_request_reviewed": {"is_interruption": True, "category": "code_review"},
    "commit": {"is_interruption": False, "category": "git_commit"},
    "ide_heartbeat": {"is_interruption": False, "category": "ide_activity"},
    "ide_session_started": {"is_interruption": False, "category": "ide_activity"},
    "ide_session_ended": {"is_interruption": False, "category": "ide_activity"},
    "file_switch": {"is_interruption": False, "category": "file_switch"},
}

def parse_iso_timestamp(ts: Any) -> datetime:
    if isinstance(ts, datetime):
        if ts.tzinfo is None:
            return ts.replace(tzinfo=timezone.utc)
        return ts.astimezone(timezone.utc)
    if isinstance(ts, (int, float)):
        return datetime.fromtimestamp(ts, tz=timezone.utc)
    
    # String parsing
    ts_str = str(ts).replace("Z", "+00:00")
    dt = datetime.fromisoformat(ts_str)
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)

def normalize_event(raw: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Validates and normalizes raw event payload.
    Returns normalized dictionary or None if malformed.
    """
    if not isinstance(raw, dict):
        return None

    event_id = raw.get("event_id") or raw.get("id")
    raw_ts = raw.get("timestamp") or raw.get("created_at") or raw.get("ts")
    source = raw.get("source", "").lower()
    event_type = raw.get("event_type", "").lower()
    actor_id = raw.get("actor_id") or raw.get("user") or raw.get("actor")
    team_id = raw.get("team_id") or "team-platform"

    if not event_id or not raw_ts or not source or not event_type or not actor_id:
        return None

    try:
        dt = parse_iso_timestamp(raw_ts)
        norm_ts = dt.isoformat()
    except Exception:
        return None

    # Determine interruption category and potential flag
    mapping = INTERRUPTION_CATEGORIES.get(event_type, {"is_interruption": False, "category": "other"})
    category = mapping["category"]
    is_interruption = 1 if mapping["is_interruption"] else 0

    session_id = raw.get("session_id")
    project_id = raw.get("project_id")

    metadata = raw.get("metadata", {})
    if isinstance(metadata, str):
        try:
            metadata = json.loads(metadata)
        except Exception:
            metadata = {"raw": metadata}
    elif not isinstance(metadata, dict):
        metadata = {}

    ingestion_ts = raw.get("ingestion_timestamp") or datetime.now(timezone.utc).isoformat()

    return {
        "event_id": str(event_id),
        "timestamp": norm_ts,
        "source": str(source),
        "event_type": str(event_type),
        "actor_id": str(actor_id),
        "team_id": str(team_id),
        "session_id": str(session_id) if session_id else None,
        "project_id": str(project_id) if project_id else None,
        "interruption_category": str(category),
        "is_potential_interruption": int(is_interruption),
        "normalized_metadata": json.dumps(metadata),
        "ingestion_timestamp": ingestion_ts
    }
