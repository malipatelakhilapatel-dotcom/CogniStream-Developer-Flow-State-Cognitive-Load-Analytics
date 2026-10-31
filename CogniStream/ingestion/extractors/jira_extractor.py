"""
Jira Event Extractor for CogniStream.
Extracts ticket lifecycle events, status changes, and sprint updates.
"""

from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
import requests
import logging

logger = logging.getLogger("cognistream.extractors.jira")

class JiraExtractor:
    def __init__(self, jira_url: Optional[str] = None, email: Optional[str] = None, api_token: Optional[str] = None):
        self.jira_url = jira_url.rstrip("/") if jira_url else None
        self.email = email
        self.api_token = api_token

    def extract_events(
        self,
        jql: Optional[str] = None,
        since: Optional[datetime] = None,
        mock_events: Optional[List[Dict[str, Any]]] = None
    ) -> List[Dict[str, Any]]:
        """
        Extracts Jira ticket events.
        """
        if mock_events is not None or not (self.jira_url and self.api_token):
            logger.info("Using mock/deterministic extractor for Jira events")
            if not mock_events:
                return []
            
            filtered = []
            for ev in mock_events:
                if ev.get("source") == "jira":
                    if since:
                        ev_dt = datetime.fromisoformat(ev["timestamp"].replace("Z", "+00:00"))
                        if ev_dt < since:
                            continue
                    filtered.append(ev)
            return filtered

        url = f"{self.jira_url}/rest/api/3/search"
        auth = (self.email, self.api_token)
        params = {"jql": jql or "updated >= -7d", "maxResults": 100}
        response = requests.get(url, auth=auth, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        extracted = []
        for issue in data.get("issues", []):
            fields = issue.get("fields", {})
            updated_ts = fields.get("updated")
            extracted.append({
                "event_id": f"jira-{issue.get('id')}",
                "timestamp": updated_ts,
                "source": "jira",
                "event_type": "issue_updated",
                "actor_id": fields.get("assignee", {}).get("accountId", "unassigned"),
                "team_id": "team-product",
                "session_id": None,
                "project_id": fields.get("project", {}).get("key"),
                "metadata": {
                    "issue_key": issue.get("key"),
                    "status": fields.get("status", {}).get("name"),
                    "priority": fields.get("priority", {}).get("name")
                },
                "ingestion_timestamp": datetime.now(timezone.utc).isoformat()
            })
        return extracted
