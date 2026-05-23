"""
main.py — FastAPI application entry point for FormFlow.

Configures CORS, registers all routers, and manages startup/shutdown events.
Run with:  python main.py   (or)   uvicorn main:app --reload
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from database import init_db, close_db
from routers import (
    projects_router,
    dancers_router,
    formations_router,
    positions_router,
    ai_router,
    center_time_router,
    music_router,
    export_router,
)


# ── Lifespan ──────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Startup / shutdown lifecycle hook."""
    # Startup: ensure tables exist & upload dir is ready
    await init_db()
    settings.upload_dir.mkdir(parents=True, exist_ok=True)
    yield
    # Shutdown: close DB connections
    await close_db()


# ── App ───────────────────────────────────────────────────────
app = FastAPI(
    title="FormFlow API",
    description="REST API for AI-powered dance formation planning",
    version="0.1.0",
    lifespan=lifespan,
)

# ── CORS ──────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────
app.include_router(projects_router)
app.include_router(dancers_router)
app.include_router(formations_router)
app.include_router(positions_router)
app.include_router(ai_router)
app.include_router(center_time_router)
app.include_router(music_router)
app.include_router(export_router)


# ── Health check ──────────────────────────────────────────────
@app.get("/api/health", tags=["health"])
async def health_check() -> dict:
    """Simple health probe endpoint."""
    return {"status": "ok", "version": app.version}


# ── Entrypoint ────────────────────────────────────────────────
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.port,
        reload=settings.debug,
    )
