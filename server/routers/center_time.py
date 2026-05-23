"""
routers/center_time.py — Center-time analysis & rebalancing endpoints.

Prefix: /api/projects/{project_id}/center-time
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models.project import Project
from schemas.center_time import (
    CenterTimeStats,
    DancerCenterTime,
    RebalanceRequest,
    RebalanceResponse,
)
from services.center_time_service import CenterTimeService

router = APIRouter(
    prefix="/api/projects/{project_id}/center-time",
    tags=["center-time"],
)


async def _get_project_or_404(project_id: int, db: AsyncSession) -> Project:
    project = await db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project


@router.get("/", response_model=CenterTimeStats)
async def get_center_time_stats(
    project_id: int,
    db: AsyncSession = Depends(get_db),
) -> CenterTimeStats:
    """
    Return center-time statistics for every dancer in the project.

    Each dancer's result includes the percentage of formations in which
    they fall within the "center zone" and a status flag (over / under / balanced).
    """
    await _get_project_or_404(project_id, db)
    service = CenterTimeService()
    return await service.calculate_center_time(project_id, db)


@router.get("/{dancer_id}", response_model=DancerCenterTime)
async def get_dancer_center_time(
    project_id: int,
    dancer_id: int,
    db: AsyncSession = Depends(get_db),
) -> DancerCenterTime:
    """Return center-time statistics for a single dancer."""
    await _get_project_or_404(project_id, db)
    service = CenterTimeService()
    result = await service.calculate_for_dancer(project_id, dancer_id, db)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Dancer not found in project"
        )
    return result


@router.post("/rebalance", response_model=RebalanceResponse)
async def rebalance_center_time(
    project_id: int,
    body: RebalanceRequest,
    db: AsyncSession = Depends(get_db),
) -> RebalanceResponse:
    """
    Automatically adjust dancer positions across formations so that
    center-time is distributed according to the requested weights.
    """
    await _get_project_or_404(project_id, db)
    service = CenterTimeService()
    return await service.rebalance_formations(
        project_id=project_id,
        db=db,
        target_weights=body.target_weights,
        tolerance=body.tolerance,
    )
