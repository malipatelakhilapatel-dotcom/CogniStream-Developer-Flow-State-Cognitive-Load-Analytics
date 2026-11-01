"""
CogniStream Application Configuration.
Loads environment variables and validates configuration at startup.
"""

import os
from typing import List
from dotenv import load_dotenv

load_dotenv()

class Settings:
    COGNISTREAM_ENV: str = os.getenv("COGNISTREAM_ENV", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-cognistream-platform-change-in-production")

    CLICKHOUSE_HOST: str = os.getenv("CLICKHOUSE_HOST", "localhost")
    CLICKHOUSE_PORT: int = int(os.getenv("CLICKHOUSE_PORT", "8123"))
    CLICKHOUSE_DB: str = os.getenv("CLICKHOUSE_DB", "cognistream")
    CLICKHOUSE_USER: str = os.getenv("CLICKHOUSE_USER", "default")
    CLICKHOUSE_PASSWORD: str = os.getenv("CLICKHOUSE_PASSWORD", "")
    CLICKHOUSE_SECURE: bool = os.getenv("CLICKHOUSE_SECURE", "false").lower() == "true"

    FOCUS_QUALIFICATION_THRESHOLD_MINUTES: float = float(os.getenv("FOCUS_QUALIFICATION_THRESHOLD_MINUTES", "90.0"))
    SESSION_INACTIVITY_THRESHOLD_MINUTES: float = float(os.getenv("SESSION_INACTIVITY_THRESHOLD_MINUTES", "15.0"))

    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173,http://127.0.0.1:3000")

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

settings = Settings()