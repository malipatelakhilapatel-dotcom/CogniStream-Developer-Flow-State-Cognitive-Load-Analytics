"""
Slack Event Extractor for CogniStream.
Extracts communication, mention, and CI/CD bot events.
"""

from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
import requests
import logging

logger = logging.getLogger("cognistream.extractors.slack")

class SlackExtractor:
    def __init__(self, bot_token: Optional[str] = None):
        self.bot_token = bot_token
        self.base_url = "https://slack.com/api"

    def extract_events(
        self,
        channels: Optional[List[str]] = None,
        since: Optional[datetime] = None,
        mock_events: Optional[List[Dict[str, Any]]] = None
    ) -> List[Dict[str, Any]]:
        """
        Extracts Slack events. If mock_events are provided or no live credentials are set,
        filters and returns standardized mock events.
        """
        if mock_events is not None or not self.bot_token:
            logger.info("Using mock/deterministic extractor for Slack events")
            if not mock_events:
                return []
            
            filtered = []
            for ev in mock_events:
                if ev.get("source") == "slack":
                    if since:
                        ev_dt = datetime.fromisoformat(ev["timestamp"].replace("Z", "+00:00"))
                        if ev_dt < since:
                            continue
                    filtered.append(ev)
            return filtered

        headers = {"Authorization": f"Bearer {self.bot_token}"}
        extracted = []
        for channel in (channels or []):
            url = f"{self.base_url}/conversations.history"
            params = {"channel": channel, "limit": 100}
            if since:
                params["oldest"] = str(since.timestamp())
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            for msg in data.get("messages", []):
                bot_id = msg.get("bot_id")
                subtype = msg.get("subtype")
                is_cicd = bool(bot_id or subtype == "bot_message")
                event_type = "ci_cd_notification" if is_cicd else "message_received"
                extracted.append({
                    "event_id": f"slack-{msg.get('ts')}",
                    "timestamp": datetime.fromtimestamp(float(msg.get("ts", 0)), tz=timezone.utc).isoformat(),
                    "source": "slack",
                    "event_type": event_type,
                    "actor_id": msg.get("user", "bot"),
                    "team_id": "team-platform",
                    "session_id": None,
                    "project_id": None,
                    "metadata": {
                        "channel": channel,
                        "is_bot": is_cicd,
                        "text_snippet": msg.get("text", "")[:50]
                    },
                    "ingestion_timestamp": datetime.now(timezone.utc).isoformat()
                })
        return extracted
