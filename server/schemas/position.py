"""
schemas/position.py — Pydantic schemas for DancerPosition CRUD.
"""

from pydantic import BaseModel, Field
from typing import Optional


class PositionCreate(BaseModel):
    """Body for placing a dancer in a formation."""
    dancer_id: int
    x: float = Field(..., description="Horizontal stage coordinate")
    y: float = Field(..., description="Vertical stage coordinate")


class PositionUpdate(BaseModel):
    """Body for moving a dancer within a formation."""
    x: Optional[float] = None
    y: Optional[float] = None


class PositionResponse(BaseModel):
    """Dancer position returned from the API."""
    id: int
    formation_id: int
    dancer_id: int
    x: float
    y: float

    model_config = {"from_attributes": True}
