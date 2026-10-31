"""
GitHub Event Extractor for CogniStream.
Implements REST API extraction pattern with support for synthetic mock data.
"""

from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
import requests
import json
import logging

logger = logging.getLogger("cognistream.extractors.github")

class GitHubExtractor:
    def __init__(self, api_token: Optional[str] = None, base_url: str = "https://api.github.com"):
        self.api_token = api_token
        self.base_url = base_url.rstrip("/")
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "CogniStream-Analytics-Agent/1.0"
        }
        if api_token:
            self.headers["Authorization"] = f"token {api_token}"

    def extract_events(
        self,
        repo_or_project: str,
        since: Optional[datetime] = None,
        mock_events: Optional[List[Dict[str, Any]]] = None
    ) -> List[Dict[str, Any]]:
        """
        Extracts GitHub events. If mock_events are provided or no live credentials are set,
        filters and returns standardized mock events.
        """
        if mock_events is not None or not self.api_token:
            logger.info("Using mock/deterministic extractor for GitHub events")
            if not mock_events:
                return []
            
            filtered = []
            for ev in mock_events:
                if ev.get("source") == "github":
                    if since:
                        ev_dt = datetime.fromisoformat(ev["timestamp"].replace("Z", "+00:00"))
                        if ev_dt < since:
                            continue
                    filtered.append(ev)
            return filtered

        # Live GitHub REST API extraction
        url = f"{self.base_url}/repos/{repo_or_project}/events"
        params = {"per_page": 100}
        response = requests.get(url, headers=self.headers, params=params, timeout=10)
        response.raise_for_status()
        raw_events = response.json()

        standardized = []
        for r in raw_events:
            event_type = r.get("type", "").replace("Event", "").lower()
            ev_id = f"gh-{r.get('id')}"
            ts = r.get("created_at")
            standardized.append({
                "event_id": ev_id,
                "timestamp": ts,
                "source": "github",
                "event_type": event_type,
                "actor_id": r.get("actor", {}).get("login", "unknown"),
                "team_id": "team-platform", # default or mapped from org
                "session_id": None,
                "project_id": repo_or_project,
                "metadata": {
                    "repo": r.get("repo", {}).get("name"),
                    "payload_action": r.get("payload", {}).get("action"),
                },
                "ingestion_timestamp": datetime.now(timezone.utc).isoformat()
            })
        return standardized
