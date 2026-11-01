"""
CogniStream Database Connection Manager.
Handles ClickHouse connectivity with automated query abstraction,
lightning-fast socket probing, and fallback storage caching.
"""

import os
import json
import socket
import time
import logging
from typing import List, Dict, Any, Optional
from backend.app.config import settings

logger = logging.getLogger("cognistream.database")

try:
    import clickhouse_connect
    CLICKHOUSE_AVAILABLE = True
except ImportError:
    CLICKHOUSE_AVAILABLE = False

class DatabaseManager:
    def __init__(self):
        self.client = None
        self._is_connected = False
        self._last_probe = 0.0
        self._probe_ttl = 5.0 # Check port availability at most once every 5 seconds
        self._fallback_cache: Dict[str, List[Dict[str, Any]]] = {}
        self.fallback_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "data_fallback"
        )

    def _is_port_open(self, host: str, port: int, timeout: float = 0.05) -> bool:
        try:
            with socket.create_connection((host, port), timeout=timeout):
                return True
        except (socket.timeout, ConnectionRefusedError, OSError):
            return False

    def connect(self) -> bool:
        now = time.time()
        # If we recently checked and it was offline, return fast
        if not self._is_connected and (now - self._last_probe) < self._probe_ttl:
            return False

        self._last_probe = now

        if not CLICKHOUSE_AVAILABLE:
            self._is_connected = False
            return False

        # Rapid socket check before calling driver
        if not self._is_port_open(settings.CLICKHOUSE_HOST, settings.CLICKHOUSE_PORT):
            self._is_connected = False
            return False

        try:
            self.client = clickhouse_connect.get_client(
                host=settings.CLICKHOUSE_HOST,
                port=settings.CLICKHOUSE_PORT,
                database=settings.CLICKHOUSE_DB,
                username=settings.CLICKHOUSE_USER,
                password=settings.CLICKHOUSE_PASSWORD,
                secure=settings.CLICKHOUSE_SECURE,
                connect_timeout=1
            )
            self.client.command("SELECT 1")
            self._is_connected = True
            logger.info("Successfully connected to ClickHouse database.")
            return True
        except Exception as e:
            logger.warning(f"ClickHouse connect failed: {e}")
            self.client = None
            self._is_connected = False
            return False

    @property
    def is_connected(self) -> bool:
        return self._is_connected

    def get_fallback_data(self, filename: str) -> List[Dict[str, Any]]:
        if filename in self._fallback_cache:
            return self._fallback_cache[filename]

        file_path = os.path.join(self.fallback_dir, filename)
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._fallback_cache[filename] = data
                    return data
            except Exception as e:
                logger.error(f"Error reading fallback {filename}: {e}")
                return []
        return []

db_manager = DatabaseManager()