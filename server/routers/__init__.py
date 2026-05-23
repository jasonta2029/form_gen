"""
routers — FastAPI router instances for every resource.
"""

from routers.projects import router as projects_router
from routers.dancers import router as dancers_router
from routers.formations import router as formations_router
from routers.positions import router as positions_router
from routers.ai import router as ai_router
from routers.center_time import router as center_time_router
from routers.music import router as music_router
from routers.export import router as export_router

__all__ = [
    "projects_router",
    "dancers_router",
    "formations_router",
    "positions_router",
    "ai_router",
    "center_time_router",
    "music_router",
    "export_router",
]
