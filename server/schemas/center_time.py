"""
schemas/center_time.py — Pydantic schemas for center-time analysis.

"Center time" measures how much time each dancer spends near the
center of the stage across all formations, helping choreographers
distribute spotlight time fairly.
"""

from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class DancerCenterTime(BaseModel):
    """Center-time stats for a single dancer."""
    dancer_id: int
    dancer_name: Optional[str]
    total_formations: int = Field(..., description="Number of formations the dancer appears in")
    center_formations: int = Field(
        ..., description="Number of formations where the dancer is inside the center zone"
    )
    center_percentage: float = Field(
        ..., ge=0.0, le=100.0,
        description="Percentage of formations spent in the center zone",
    )
    avg_distance_to_center: float = Field(
        ..., description="Average Euclidean distance to stage center across formations"
    )
    status: str = Field(
        ..., description="'over' | 'under' | 'balanced'",
        examples=["balanced"],
    )


class CenterTimeStats(BaseModel):
    """Aggregated center-time statistics for an entire project."""
    project_id: int
    dancers: List[DancerCenterTime]
    ideal_percentage: float = Field(
        ..., description="Target center-time percentage if evenly distributed"
    )


class RebalanceRequest(BaseModel):
    """Request to automatically rebalance center time across formations."""
    target_weights: Optional[Dict[int, float]] = Field(
        None,
        description=(
            "Optional per-dancer weight map (dancer_id → relative weight). "
            "Omit for equal distribution."
        ),
    )
    tolerance: float = Field(
        5.0, ge=0.0, le=50.0,
        description="Acceptable deviation (%) from ideal center-time",
    )


class RebalanceResponse(BaseModel):
    """Result of a rebalance operation."""
    adjusted_formations: int = Field(..., description="Number of formations that were modified")
    before: CenterTimeStats
    after: CenterTimeStats
