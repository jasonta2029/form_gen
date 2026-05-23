"""
schemas/ai.py — Pydantic schemas for AI formation generation endpoints.
"""

from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from schemas.position import PositionResponse


class TemplateShape(str, Enum):
    """Pre-defined geometric template names."""
    V_SHAPE = "V_SHAPE"
    ARC = "ARC"
    CLUSTER = "CLUSTER"
    SPLIT = "SPLIT"
    DIAGONAL = "DIAGONAL"
    LINE = "LINE"
    CIRCLE = "CIRCLE"
    DIAMOND = "DIAMOND"
    SCATTER = "SCATTER"


class GenerationRequest(BaseModel):
    """Request body for AI-powered formation generation."""
    prompt: str = Field(
        ..., min_length=1, max_length=1000,
        examples=["Create a dynamic opening formation with two groups converging"],
    )
    num_dancers: int = Field(..., ge=1, le=200)
    style: Optional[str] = Field(None, examples=["contemporary", "hip-hop", "ballet"])
    constraints: Optional[Dict[str, object]] = Field(
        None,
        description="Extra constraints, e.g. {'avoid_edges': true, 'symmetry': 'bilateral'}",
    )


class GenerationResponse(BaseModel):
    """Response containing AI-generated positions."""
    positions: List[PositionResponse]
    reasoning: str = Field(
        ..., description="Short explanation of why the AI chose this arrangement"
    )


class TransitionRequest(BaseModel):
    """Request body for suggesting transitions between two formations."""
    from_formation_id: int
    to_formation_id: int
    num_intermediate_steps: int = Field(1, ge=1, le=10)


class TransitionResponse(BaseModel):
    """Response containing suggested intermediate formations."""
    steps: List[List[PositionResponse]]
    total_distance: float = Field(..., description="Sum of all dancer travel distances")
    crossing_count: int = Field(..., description="Number of path crossings detected")


class TemplateRequest(BaseModel):
    """Request body for applying a geometric template."""
    shape: TemplateShape
    num_dancers: int = Field(..., ge=1, le=200)
    scale: float = Field(1.0, gt=0.0, le=5.0, description="Scale factor for the shape")
    rotation_deg: float = Field(0.0, ge=0.0, lt=360.0, description="Rotation in degrees")
