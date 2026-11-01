"""
CogniStream FastAPI Application Entrypoint.
Exposes REST analytics endpoints connecting ClickHouse event storage to React dashboard.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from backend.app.config import settings
from backend.app.database import db_manager
from backend.app.api.routes import health, overview, flow, interruptions, teams, activity, filters

logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))
logger = logging.getLogger("cognistream.main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing CogniStream Analytics API...")
    connected = db_manager.connect()
    if connected:
        logger.info(f"Connected to ClickHouse at {settings.CLICKHOUSE_HOST}:{settings.CLICKHOUSE_PORT}")
    else:
        logger.warning("ClickHouse service offline. Utilizing verified embedded fallback engine.")
    yield
    logger.info("Shutting down CogniStream API.")

app = FastAPI(
    title="CogniStream API",
    description="Developer Flow-State & Cognitive Load Analytics Platform REST API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow local Vite/React dev origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(health.router, prefix="/api")
app.include_router(overview.router, prefix="/api")
app.include_router(flow.router, prefix="/api")
app.include_router(interruptions.router, prefix="/api")
app.include_router(teams.router, prefix="/api")
app.include_router(activity.router, prefix="/api")
app.include_router(filters.router, prefix="/api")

@app.get("/")
def root():
    return {
        "service": "CogniStream Analytics Platform",
        "version": "1.0.0",
        "status": "online",
        "docs_url": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host=settings.API_HOST, port=settings.API_PORT, reload=True)