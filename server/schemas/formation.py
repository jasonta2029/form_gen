"""
schemas/formation.py — Pydantic schemas for Formation CRUD & reordering.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from schemas.position import PositionResponse


class PositionInput(BaseModel):
    """Inline position entry used when creating a formation with initial positions."""
    dancer_id: int
    x: float = 0.0
    y: float = 0.0


class FormationCreate(BaseModel):
    """Request body for creating a new formation."""
    name: str = Field("Untitled", max_length=255)
    order_index: int = Field(0, ge=0)
    timestamp_start: Optional[float] = Field(None, ge=0.0)
    timestamp_end: Optional[float] = Field(None, ge=0.0)
    positions: Optional[List[PositionInput]] = Field(default=None)


class FormationUpdate(BaseModel):
    """Request body for updating a formation (all fields optional)."""
    name: Optional[str] = Field(None, max_length=255)
    order_index: Optional[int] = Field(None, ge=0)
    timestamp_start: Optional[float] = Field(None, ge=0.0)
    timestamp_end: Optional[float] = Field(None, ge=0.0)


class FormationResponse(BaseModel):
    """Formation returned from the API (without nested positions)."""
    id: int
    project_id: int
    name: str
    order_index: int
    timestamp_start: Optional[float]
    timestamp_end: Optional[float]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class FormationWithPositions(FormationResponse):
    """Formation with all dancer positions included."""
    positions: List[PositionResponse] = []


class ReorderRequest(BaseModel):
    """Request body for bulk-reordering formations."""
    formation_ids: List[int] = Field(
        ..., min_length=1,
        description="Ordered list of formation IDs representing the new sequence",
    )
