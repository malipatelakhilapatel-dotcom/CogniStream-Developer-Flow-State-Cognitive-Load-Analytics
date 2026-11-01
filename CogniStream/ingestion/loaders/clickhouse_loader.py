"""
ClickHouse Ingestion and Persistence Loader for CogniStream.
Loads raw and transformed events into ClickHouse MergeTree tables,
with local fallback store if ClickHouse connection is temporarily offline.
"""

import os
import json
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger("cognistream.loaders.clickhouse")

try:
    import clickhouse_connect
    CLICKHOUSE_CONNECT_AVAILABLE = True
except ImportError:
    CLICKHOUSE_CONNECT_AVAILABLE = False

class ClickHouseLoader:
    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        database: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        secure: bool = False
    ):
        self.host = host or os.getenv("CLICKHOUSE_HOST", "localhost")
        self.port = int(port or os.getenv("CLICKHOUSE_PORT", "8123"))
        self.database = database or os.getenv("CLICKHOUSE_DB", "cognistream")
        self.username = username or os.getenv("CLICKHOUSE_USER", "default")
        self.password = password or os.getenv("CLICKHOUSE_PASSWORD", "")
        self.secure = secure or (os.getenv("CLICKHOUSE_SECURE", "false").lower() == "true")
        self.client = None
        self._connected = False
        self._fallback_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data_fallback")
        os.makedirs(self._fallback_dir, exist_ok=True)

    def connect(self) -> bool:
        """Attempts to connect to ClickHouse. Returns True if connected, False otherwise."""
        if not CLICKHOUSE_CONNECT_AVAILABLE:
            logger.warning("clickhouse-connect is not installed.")
            self._connected = False
            return False

        try:
            self.client = clickhouse_connect.get_client(
                host=self.host,
                port=self.port,
                database=self.database,
                username=self.username,
                password=self.password,
                secure=self.secure,
                connect_timeout=3
            )
            self._connected = True
            logger.info(f"Connected to ClickHouse at {self.host}:{self.port}/{self.database}")
            return True
        except Exception as e:
            logger.warning(f"ClickHouse connection failed ({self.host}:{self.port}): {e}. Using fallback storage.")
            self.client = None
            self._connected = False
            return False

    @property
    def is_connected(self) -> bool:
        return self._connected

    def insert_raw_events(self, events: List[Dict[str, Any]]) -> int:
        if not events:
            return 0
        if not self._connected:
            self.connect()

        if self._connected and self.client:
            rows = []
            for ev in events:
                rows.append([
                    str(ev["event_id"]),
                    str(ev["timestamp"]).replace("T", " ")[:23],
                    str(ev.get("source", "unknown")),
                    str(ev.get("event_type", "unknown")),
                    str(ev.get("actor_id", "unknown")),
                    str(ev.get("team_id", "unknown")),
                    json.dumps(ev.get("metadata", {})),
                    str(ev.get("ingestion_timestamp", "")).replace("T", " ")[:23]
                ])
            self.client.insert(
                "raw_developer_events",
                rows,
                column_names=[
                    "event_id", "event_timestamp", "source", "event_type",
                    "actor_id", "team_id", "raw_payload", "ingestion_timestamp"
                ]
            )
            return len(rows)
        else:
            # Fallback JSON persistence
            self._save_fallback("raw_developer_events.json", events)
            return len(events)

    def insert_developer_events(self, events: List[Dict[str, Any]]) -> int:
        if not events:
            return 0
        if not self._connected:
            self.connect()

        if self._connected and self.client:
            rows = []
            for ev in events:
                rows.append([
                    str(ev["event_id"]),
                    str(ev["timestamp"]).replace("T", " ")[:23],
                    str(ev.get("source", "unknown")),
                    str(ev.get("event_type", "unknown")),
                    str(ev.get("actor_id", "unknown")),
                    str(ev.get("team_id", "unknown")),
                    ev.get("session_id"),
                    ev.get("project_id"),
                    str(ev.get("interruption_category", "none")),
                    int(ev.get("is_potential_interruption", 0)),
                    str(ev.get("normalized_metadata", "{}")),
                    str(ev.get("ingestion_timestamp", "")).replace("T", " ")[:23]
                ])
            self.client.insert(
                "developer_events",
                rows,
                column_names=[
                    "event_id", "timestamp", "source", "event_type",
                    "actor_id", "team_id", "session_id", "project_id",
                    "interruption_category", "is_potential_interruption",
                    "normalized_metadata", "ingestion_timestamp"
                ]
            )
            return len(rows)
        else:
            self._save_fallback("developer_events.json", events)
            return len(events)

    def insert_focus_blocks(self, blocks: List[Dict[str, Any]]) -> int:
        if not blocks:
            return 0
        if not self._connected:
            self.connect()

        if self._connected and self.client:
            rows = []
            for b in blocks:
                rows.append([
                    str(b["focus_block_id"]),
                    str(b["actor_id"]),
                    str(b["team_id"]),
                    b.get("project_id"),
                    str(b["start_timestamp"]).replace("T", " ")[:23],
                    str(b["end_timestamp"]).replace("T", " ")[:23],
                    float(b.get("duration_minutes", 0.0)),
                    int(b.get("interruption_count", 0)),
                    int(b.get("is_qualifying", 0)),
                    str(b.get("qualification_status", "non_qualifying")),
                    str(b.get("calculation_version", "v1.0.0")),
                ])
            self.client.insert(
                "focus_blocks",
                rows,
                column_names=[
                    "focus_block_id", "actor_id", "team_id", "project_id",
                    "start_timestamp", "end_timestamp", "duration_minutes",
                    "interruption_count", "is_qualifying", "qualification_status",
                    "calculation_version"
                ]
            )
            return len(rows)
        else:
            self._save_fallback("focus_blocks.json", blocks)
            return len(blocks)

    def insert_daily_metrics(self, metrics: List[Dict[str, Any]]) -> int:
        if not metrics:
            return 0
        if not self._connected:
            self.connect()

        if self._connected and self.client:
            rows = []
            for m in metrics:
                rows.append([
                    str(m["date"]),
                    str(m["team_id"]),
                    int(m.get("active_developer_count", 0)),
                    float(m.get("observed_ide_minutes", 0.0)),
                    float(m.get("qualifying_focus_minutes", 0.0)),
                    float(m.get("total_focus_minutes", 0.0)),
                    int(m.get("focus_block_count", 0)),
                    int(m.get("qualifying_block_count", 0)),
                    float(m.get("avg_focus_block_duration_minutes", 0.0)),
                    int(m.get("interruption_count", 0)),
                    int(m.get("context_switch_count", 0)),
                    float(m.get("estimated_interruption_loss_minutes", 0.0)),
                    float(m.get("context_switching_tax_pct", 0.0)),
                    json.dumps(m.get("source_event_counts", {})),
                    str(m.get("calculation_version", "v1.0.0"))
                ])
            self.client.insert(
                "daily_team_metrics",
                rows,
                column_names=[
                    "date", "team_id", "active_developer_count", "observed_ide_minutes",
                    "qualifying_focus_minutes", "total_focus_minutes", "focus_block_count",
                    "qualifying_block_count", "avg_focus_block_duration_minutes",
                    "interruption_count", "context_switch_count", "estimated_interruption_loss_minutes",
                    "context_switching_tax_pct", "source_event_counts", "calculation_version"
                ]
            )
            return len(rows)
        else:
            self._save_fallback("daily_team_metrics.json", metrics)
            return len(metrics)

    def insert_interruption_metrics(self, metrics: List[Dict[str, Any]]) -> int:
        if not metrics:
            return 0
        if not self._connected:
            self.connect()

        if self._connected and self.client:
            rows = []
            for m in metrics:
                rows.append([
                    str(m["period_start"]).replace("T", " ")[:23],
                    str(m["period_end"]).replace("T", " ")[:23],
                    str(m.get("period_type", "daily")),
                    str(m["team_id"]),
                    str(m["interruption_category"]),
                    int(m.get("event_count", 0)),
                    int(m.get("affected_sessions_count", 0)),
                    float(m.get("estimated_associated_focus_loss_minutes", 0.0)),
                    str(m.get("calculation_version", "v1.0.0"))
                ])
            self.client.insert(
                "interruption_metrics",
                rows,
                column_names=[
                    "period_start", "period_end", "period_type", "team_id",
                    "interruption_category", "event_count", "affected_sessions_count",
                    "estimated_associated_focus_loss_minutes", "calculation_version"
                ]
            )
            return len(rows)
        else:
            self._save_fallback("interruption_metrics.json", metrics)
            return len(metrics)

    def _save_fallback(self, filename: str, data: List[Dict[str, Any]]):
        path = os.path.join(self._fallback_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        logger.info(f"Saved {len(data)} records to fallback storage {path}")
