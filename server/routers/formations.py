"""
routers/formations.py — CRUD + reorder endpoints for formations.

Prefix: /api/projects/{project_id}/formations
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models.formation import Formation
from models.project import Project
from schemas.formation import (
    FormationCreate,
    FormationUpdate,
    FormationResponse,
    FormationWithPositions,
    ReorderRequest,
)

router = APIRouter(
    prefix="/api/projects/{project_id}/formations",
    tags=["formations"],
)


async def _get_project_or_404(project_id: int, db: AsyncSession) -> Project:
    project = await db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project


@router.get("/", response_model=List[FormationResponse])
async def list_formations(
    project_id: int,
    db: AsyncSession = Depends(get_db),
) -> List[FormationResponse]:
    """List formations for a project in timeline order."""
    await _get_project_or_404(project_id, db)
    result = await db.execute(
        select(Formation)
        .where(Formation.project_id == project_id)
        .order_by(Formation.order_index)
    )
    return [FormationResponse.model_validate(f) for f in result.scalars().all()]


@router.get("/{formation_id}", response_model=FormationWithPositions)
async def get_formation(
    project_id: int,
    formation_id: int,
    db: AsyncSession = Depends(get_db),
) -> FormationWithPositions:
    """Get a single formation with all dancer positions."""
    formation = await db.get(Formation, formation_id)
    if not formation or formation.project_id != project_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Formation not found")
    # TODO: eager-load positions via selectinload for efficiency
    return FormationWithPositions.model_validate(formation)


@router.post("/", response_model=FormationResponse, status_code=status.HTTP_201_CREATED)
async def create_formation(
    project_id: int,
    body: FormationCreate,
    db: AsyncSession = Depends(get_db),
) -> FormationResponse:
    """Create a new formation in the project timeline."""
    await _get_project_or_404(project_id, db)
    formation = Formation(project_id=project_id, **body.model_dump())
    db.add(formation)
    await db.flush()
    await db.refresh(formation)
    return FormationResponse.model_validate(formation)


@router.put("/{formation_id}", response_model=FormationResponse)
async def update_formation(
    project_id: int,
    formation_id: int,
    body: FormationUpdate,
    db: AsyncSession = Depends(get_db),
) -> FormationResponse:
    """Update a formation's name, timing, or order."""
    formation = await db.get(Formation, formation_id)
    if not formation or formation.project_id != project_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Formation not found")

    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(formation, field, value)

    await db.flush()
    await db.refresh(formation)
    return FormationResponse.model_validate(formation)


@router.delete("/{formation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_formation(
    project_id: int,
    formation_id: int,
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete a formation and its positions."""
    formation = await db.get(Formation, formation_id)
    if not formation or formation.project_id != project_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Formation not found")
    await db.delete(formation)


@router.post("/{formation_id}/duplicate", response_model=FormationResponse, status_code=status.HTTP_201_CREATED)
async def duplicate_formation(
    project_id: int,
    formation_id: int,
    db: AsyncSession = Depends(get_db),
) -> FormationResponse:
    """Duplicate a formation with all its positions."""
    await _get_project_or_404(project_id, db)

    formation = await db.get(Formation, formation_id)
    if not formation or formation.project_id != project_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Formation not found")

    # Get the highest order_index to place the duplicate at the end
    result = await db.execute(
        select(Formation.order_index)
        .where(Formation.project_id == project_id)
        .order_by(Formation.order_index.desc())
        .limit(1)
    )
    max_order = result.scalar_one_or_none() or -1

    # Create duplicate formation
    duplicate = Formation(
        project_id=project_id,
        name=f"{formation.name} (Copy)",
        order_index=max_order + 1,
        timestamp_start=formation.timestamp_start,
        timestamp_end=formation.timestamp_end
    )
    db.add(duplicate)
    await db.flush()
    await db.refresh(formation)  # Get the formation with ID

    # Import here to avoid circular imports
    from models.position import DancerPosition

    # Duplicate all positions
    result = await db.execute(
        select(DancerPosition).where(DancerPosition.formation_id == formation_id)
    )
    positions = result.scalars().all()

    for pos in positions:
        duplicate_pos = DancerPosition(
            formation_id=duplicate.id,
            dancer_id=pos.dancer_id,
            x=pos.x,
            y=pos.y
        )
        db.add(duplicate_pos)

    await db.flush()
    await db.refresh(duplicate)

    return FormationResponse.model_validate(duplicate)


@router.put("/reorder", response_model=List[FormationResponse])
async def reorder_formations(
    project_id: int,
    body: ReorderRequest,
    db: AsyncSession = Depends(get_db),
) -> List[FormationResponse]:
    """Bulk-reorder formations by providing an ordered list of IDs."""
    await _get_project_or_404(project_id, db)

    result = await db.execute(
        select(Formation).where(Formation.project_id == project_id)
    )
    formations_by_id = {f.id: f for f in result.scalars().all()}

    for new_index, fid in enumerate(body.formation_ids):
        if fid not in formations_by_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Formation {fid} not found in project {project_id}",
            )
        formations_by_id[fid].order_index = new_index

    await db.flush()

    ordered = sorted(formations_by_id.values(), key=lambda f: f.order_index)
    return [FormationResponse.model_validate(f) for f in ordered]
