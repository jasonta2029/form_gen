"""
schemas/dancer.py — Pydantic schemas for Dancer CRUD operations.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DancerCreate(BaseModel):
    """Request body for adding a dancer to a project."""
    number: int = Field(..., ge=1, examples=[1])
    name: Optional[str] = Field(None, max_length=255, examples=["Alice"])
    color: Optional[str] = Field(
        "#3B82F6", pattern=r"^#[0-9A-Fa-f]{6}$", examples=["#FF5733"]
    )
    group: Optional[str] = Field(None, max_length=100, examples=["Front Row"])


class DancerUpdate(BaseModel):
    """Request body for updating a dancer (all fields optional)."""
    number: Optional[int] = Field(None, ge=1)
    name: Optional[str] = Field(None, max_length=255)
    color: Optional[str] = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")
    group: Optional[str] = Field(None, max_length=100)


class DancerResponse(BaseModel):
    """Dancer returned from the API."""
    id: int
    project_id: int
    number: int
    name: Optional[str]
    color: Optional[str]
    group: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}
