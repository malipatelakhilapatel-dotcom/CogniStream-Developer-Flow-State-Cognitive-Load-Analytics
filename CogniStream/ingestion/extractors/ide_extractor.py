"""
IDE Activity Extractor for CogniStream.
Extracts IDE heartbeat, editor focus, file switch, and project switch events.
"""

from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger("cognistream.extractors.ide")

class IDEActivityExtractor:
    def __init__(self, endpoint_url: Optional[str] = None):
        self.endpoint_url = endpoint_url

    def extract_events(
        self,
        since: Optional[datetime] = None,
        mock_events: Optional[List[Dict[str, Any]]] = None
    ) -> List[Dict[str, Any]]:
        """
        Extracts IDE activity events.
        """
        if mock_events is not None or not self.endpoint_url:
            logger.info("Using mock/deterministic extractor for IDE activity events")
            if not mock_events:
                return []
            
            filtered = []
            for ev in mock_events:
                if ev.get("source") == "ide":
                    if since:
                        ev_dt = datetime.fromisoformat(ev["timestamp"].replace("Z", "+00:00"))
                        if ev_dt < since:
                            continue
                    filtered.append(ev)
            return filtered

        # If live telemetry endpoint configured:
        return []
