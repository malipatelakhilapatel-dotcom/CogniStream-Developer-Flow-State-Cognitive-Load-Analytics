"""
Event and Analytics Repository for CogniStream.
Implements parameterized data access patterns with query filtering.
"""

from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from backend.app.database import db_manager
import logging

logger = logging.getLogger("cognistream.repository")

def filter_by_date_and_team(
    items: List[Dict[str, Any]],
    date_field: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    team_id: Optional[str] = None
) -> List[Dict[str, Any]]:
    filtered = items
    if start_date:
        filtered = [x for x in filtered if str(x.get(date_field, ""))[:10] >= start_date[:10]]
    if end_date:
        filtered = [x for x in filtered if str(x.get(date_field, ""))[:10] <= end_date[:10]]
    if team_id and team_id != "all":
        filtered = [x for x in filtered if x.get("team_id") == team_id]
    return filtered

class EventRepository:
    def __init__(self):
        self.db = db_manager

    def get_health(self) -> Dict[str, Any]:
        connected = self.db.connect()
        counts = {}
        if connected and self.db.client:
            try:
                counts["raw_events"] = self.db.client.command("SELECT count() FROM cognistream.raw_developer_events")
                counts["developer_events"] = self.db.client.command("SELECT count() FROM cognistream.developer_events")
                counts["focus_blocks"] = self.db.client.command("SELECT count() FROM cognistream.focus_blocks")
                counts["daily_metrics"] = self.db.client.command("SELECT count() FROM cognistream.daily_team_metrics")
            except Exception as e:
                logger.error(f"Error querying ClickHouse health counts: {e}")
                connected = False

        if not connected:
            # Fallback counts
            counts["developer_events"] = len(self.db.get_fallback_data("developer_events.json"))
            counts["focus_blocks"] = len(self.db.get_fallback_data("focus_blocks.json"))
            counts["daily_metrics"] = len(self.db.get_fallback_data("daily_team_metrics.json"))
            counts["interruption_metrics"] = len(self.db.get_fallback_data("interruption_metrics.json"))

        return {
            "status": "healthy",
            "database_connected": connected,
            "engine": "ClickHouse MergeTree" if connected else "Embedded Local Data Engine",
            "table_counts": counts,
            "mode": "synthetic_demo"
        }

    def get_events(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        team_id: Optional[str] = None,
        source: Optional[str] = None,
        category: Optional[str] = None,
        search: Optional[str] = None,
        offset: int = 0,
        limit: int = 50
    ) -> Tuple[List[Dict[str, Any]], int]:
        all_events = []
        if self.db.connect() and self.db.client:
            conditions = ["1=1"]
            params = {}
            if start_date:
                conditions.append("toDate(timestamp) >= %(start_date)s")
                params["start_date"] = start_date[:10]
            if end_date:
                conditions.append("toDate(timestamp) <= %(end_date)s")
                params["end_date"] = end_date[:10]
            if team_id and team_id != "all":
                conditions.append("team_id = %(team_id)s")
                params["team_id"] = team_id
            if source and source != "all":
                conditions.append("source = %(source)s")
                params["source"] = source
            if category and category != "all":
                conditions.append("interruption_category = %(category)s")
                params["category"] = category

            where_clause = " AND ".join(conditions)
            total = self.db.client.command(f"SELECT count() FROM cognistream.developer_events WHERE {where_clause}", parameters=params)
            query = f"SELECT * FROM cognistream.developer_events WHERE {where_clause} ORDER BY timestamp DESC LIMIT {limit} OFFSET {offset}"
            res = self.db.client.query(query, parameters=params)
            cols = res.column_names
            for r in res.result_rows:
                all_events.append(dict(zip(cols, r)))
            return all_events, total

        # Fallback
        raw_events = self.db.get_fallback_data("developer_events.json")
        filtered = filter_by_date_and_team(raw_events, "timestamp", start_date, end_date, team_id)
        if source and source != "all":
            filtered = [x for x in filtered if x.get("source") == source]
        if category and category != "all":
            filtered = [x for x in filtered if x.get("interruption_category") == category]
        if search:
            s = search.lower()
            filtered = [
                x for x in filtered
                if s in str(x.get("event_id", "")).lower()
                or s in str(x.get("actor_id", "")).lower()
                or s in str(x.get("project_id", "")).lower()
                or s in str(x.get("event_type", "")).lower()
            ]

        # Sort descending by timestamp
        filtered.sort(key=lambda x: str(x.get("timestamp", "")), reverse=True)
        total = len(filtered)
        paginated = filtered[offset: offset + limit]
        return paginated, total

    def get_focus_blocks(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        team_id: Optional[str] = None,
        project_id: Optional[str] = None,
        is_qualifying: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        if self.db.connect() and self.db.client:
            conditions = ["1=1"]
            params = {}
            if start_date:
                conditions.append("toDate(start_timestamp) >= %(start_date)s")
                params["start_date"] = start_date[:10]
            if end_date:
                conditions.append("toDate(start_timestamp) <= %(end_date)s")
                params["end_date"] = end_date[:10]
            if team_id and team_id != "all":
                conditions.append("team_id = %(team_id)s")
                params["team_id"] = team_id
            if project_id and project_id != "all":
                conditions.append("project_id = %(project_id)s")
                params["project_id"] = project_id
            if is_qualifying is not None:
                conditions.append("is_qualifying = %(is_qualifying)s")
                params["is_qualifying"] = is_qualifying

            where_clause = " AND ".join(conditions)
            query = f"SELECT * FROM cognistream.focus_blocks WHERE {where_clause} ORDER BY start_timestamp ASC"
            res = self.db.client.query(query, parameters=params)
            cols = res.column_names
            return [dict(zip(cols, r)) for r in res.result_rows]

        # Fallback
        blocks = self.db.get_fallback_data("focus_blocks.json")
        filtered = filter_by_date_and_team(blocks, "start_timestamp", start_date, end_date, team_id)
        if project_id and project_id != "all":
            filtered = [x for x in filtered if x.get("project_id") == project_id]
        if is_qualifying is not None:
            filtered = [x for x in filtered if x.get("is_qualifying") == is_qualifying]
        return filtered

    def get_daily_metrics(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        team_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        if self.db.connect() and self.db.client:
            conditions = ["1=1"]
            params = {}
            if start_date:
                conditions.append("date >= %(start_date)s")
                params["start_date"] = start_date[:10]
            if end_date:
                conditions.append("date <= %(end_date)s")
                params["end_date"] = end_date[:10]
            if team_id and team_id != "all":
                conditions.append("team_id = %(team_id)s")
                params["team_id"] = team_id

            where_clause = " AND ".join(conditions)
            query = f"SELECT * FROM cognistream.daily_team_metrics WHERE {where_clause} ORDER BY date ASC"
            res = self.db.client.query(query, parameters=params)
            cols = res.column_names
            return [dict(zip(cols, r)) for r in res.result_rows]

        metrics = self.db.get_fallback_data("daily_team_metrics.json")
        return filter_by_date_and_team(metrics, "date", start_date, end_date, team_id)

    def get_interruption_metrics(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        team_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        if self.db.connect() and self.db.client:
            conditions = ["1=1"]
            params = {}
            if start_date:
                conditions.append("toDate(period_start) >= %(start_date)s")
                params["start_date"] = start_date[:10]
            if end_date:
                conditions.append("toDate(period_start) <= %(end_date)s")
                params["end_date"] = end_date[:10]
            if team_id and team_id != "all":
                conditions.append("team_id = %(team_id)s")
                params["team_id"] = team_id

            where_clause = " AND ".join(conditions)
            query = f"SELECT * FROM cognistream.interruption_metrics WHERE {where_clause} ORDER BY period_start ASC"
            res = self.db.client.query(query, parameters=params)
            cols = res.column_names
            return [dict(zip(cols, r)) for r in res.result_rows]

        metrics = self.db.get_fallback_data("interruption_metrics.json")
        return filter_by_date_and_team(metrics, "period_start", start_date, end_date, team_id)

    def get_filter_options(self) -> Dict[str, Any]:
        return {
            "teams": [
                {"id": "all", "name": "All Teams"},
                {"id": "team-platform", "name": "Platform Engineering"},
                {"id": "team-product", "name": "Product Engineering"},
                {"id": "team-data", "name": "Data Engineering"},
            ],
            "projects": [
                {"id": "all", "name": "All Projects"},
                {"id": "proj-k8s-infra", "name": "Kubernetes Infrastructure"},
                {"id": "proj-service-mesh", "name": "Service Mesh"},
                {"id": "proj-auth-v2", "name": "Auth V2 Platform"},
                {"id": "proj-billing-portal", "name": "Billing Portal"},
                {"id": "proj-customer-dashboard", "name": "Customer Dashboard"},
                {"id": "proj-checkout-flow", "name": "Checkout Flow"},
                {"id": "proj-stream-pipeline", "name": "Streaming Pipeline"},
                {"id": "proj-lakehouse-etl", "name": "Lakehouse ETL"},
                {"id": "proj-dbt-models", "name": "dbt Data Models"}
            ],
            "sources": [
                {"id": "all", "name": "All Sources"},
                {"id": "ide", "name": "IDE Activity"},
                {"id": "slack", "name": "Slack"},
                {"id": "github", "name": "GitHub"},
                {"id": "jira", "name": "Jira"}
            ],
            "categories": [
                {"id": "all", "name": "All Categories"},
                {"id": "ci_cd_notification", "name": "CI/CD Notifications"},
                {"id": "direct_message", "name": "Direct Messages"},
                {"id": "mention", "name": "Mentions"},
                {"id": "project_switch", "name": "Project Switches"},
                {"id": "task_switch", "name": "Task Transitions"},
                {"id": "code_review", "name": "Code Reviews"},
                {"id": "ide_activity", "name": "IDE Activity"},
                {"id": "channel_message", "name": "Channel Messages"}
            ],
            "date_range": {
                "default_start": "2026-09-25",
                "default_end": "2026-10-25"
            }
        }

event_repo = EventRepository()