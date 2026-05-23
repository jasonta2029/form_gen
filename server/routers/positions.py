"""
routers/positions.py — Batch position management for a formation.

Prefix: /api/projects/{project_id}/formations/{formation_id}/positions
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models.formation import Formation
from models.position import DancerPosition
from schemas.position import PositionCreate, PositionUpdate, PositionResponse

router = APIRouter(
    prefix="/api/projects/{project_id}/formations/{formation_id}/positions",
    tags=["positions"],
)


async def _get_formation_or_404(
    project_id: int, formation_id: int, db: AsyncSession
) -> Formation:
    formation = await db.get(Formation, formation_id)
    if not formation or formation.project_id != project_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Formation not found"
        )
    return formation


@router.get("/", response_model=List[PositionResponse])
async def list_positions(
    project_id: int,
    formation_id: int,
    db: AsyncSession = Depends(get_db),
) -> List[PositionResponse]:
    """Get all dancer positions in a formation."""
    await _get_formation_or_404(project_id, formation_id, db)
    result = await db.execute(
        select(DancerPosition).where(DancerPosition.formation_id == formation_id)
    )
    return [PositionResponse.model_validate(p) for p in result.scalars().all()]


@router.put("/", response_model=List[PositionResponse])
async def batch_update_positions(
    project_id: int,
    formation_id: int,
    positions: List[PositionCreate],
    db: AsyncSession = Depends(get_db),
) -> List[PositionResponse]:
    """
    Replace all positions in a formation with the provided set.

    This is an idempotent "set positions" operation:
    1. Delete existing positions for this formation.
    2. Insert the new positions.
    """
    await _get_formation_or_404(project_id, formation_id, db)

    # Clear existing
    await db.execute(
        delete(DancerPosition).where(DancerPosition.formation_id == formation_id)
    )

    # Insert new
    new_positions: List[DancerPosition] = []
    for pos in positions:
        dp = DancerPosition(
            formation_id=formation_id,
            dancer_id=pos.dancer_id,
            x=pos.x,
            y=pos.y,
        )
        db.add(dp)
        new_positions.append(dp)

    await db.flush()
    for dp in new_positions:
        await db.refresh(dp)

    return [PositionResponse.model_validate(dp) for dp in new_positions]


@router.patch("/{position_id}", response_model=PositionResponse)
async def update_single_position(
    project_id: int,
    formation_id: int,
    position_id: int,
    body: PositionUpdate,
    db: AsyncSession = Depends(get_db),
) -> PositionResponse:
    """Move a single dancer within a formation."""
    await _get_formation_or_404(project_id, formation_id, db)

    position = await db.get(DancerPosition, position_id)
    if not position or position.formation_id != formation_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Position not found"
        )

    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(position, field, value)

    await db.flush()
    await db.refresh(position)
    return PositionResponse.model_validate(position)
