"""
schemas/project.py — Pydantic schemas for Project CRUD operations.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    """Request body for creating a new project."""
    name: str = Field(..., min_length=1, max_length=255, examples=["Spring Showcase 2026"])
    description: Optional[str] = Field(None, max_length=2000)
    num_dancers: int = Field(..., ge=1, le=200, examples=[12])


class ProjectUpdate(BaseModel):
    """Request body for updating an existing project (all fields optional)."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    num_dancers: Optional[int] = Field(None, ge=1, le=200)
    audio_file_path: Optional[str] = None


class ProjectResponse(BaseModel):
    """Single project returned from the API."""
    id: int
    name: str
    description: Optional[str]
    num_dancers: int
    audio_file_path: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ProjectListResponse(BaseModel):
    """Paginated list of projects."""
    items: List[ProjectResponse]
    total: int
