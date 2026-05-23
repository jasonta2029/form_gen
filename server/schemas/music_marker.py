"""
schemas/music_marker.py — Pydantic schemas for MusicMarker CRUD.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class MarkerCreate(BaseModel):
    """Request body for creating a music marker."""
    name: str = Field("Marker", max_length=255)
    timestamp: float = Field(..., ge=0.0, description="Seconds from audio start")
    formation_id: Optional[int] = Field(
        None, description="Optionally link this marker to a formation"
    )


class MarkerUpdate(BaseModel):
    """Request body for updating a music marker."""
    name: Optional[str] = Field(None, max_length=255)
    timestamp: Optional[float] = Field(None, ge=0.0)
    formation_id: Optional[int] = None


class MarkerResponse(BaseModel):
    """Music marker returned from the API."""
    id: int
    project_id: int
    name: str
    timestamp: float
    formation_id: Optional[int]
    created_at: datetime

    model_config = {"from_attributes": True}
