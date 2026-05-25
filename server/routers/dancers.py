"""
routers/dancers.py — CRUD endpoints for dancers within a project.

Prefix: /api/projects/{project_id}/dancers
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models.dancer import Dancer
from models.project import Project
from schemas.dancer import DancerCreate, DancerUpdate, DancerResponse

router = APIRouter(
    prefix="/api/projects/{project_id}/dancers",
    tags=["dancers"],
)


async def _get_project_or_404(project_id: int, db: AsyncSession) -> Project:
    """Helper: fetch a project or raise 404."""
    project = await db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project


@router.get("/", response_model=List[DancerResponse])
async def list_dancers(
    project_id: int,
    db: AsyncSession = Depends(get_db),
) -> List[DancerResponse]:
    """List all dancers in a project, ordered by number."""
    await _get_project_or_404(project_id, db)
    result = await db.execute(
        select(Dancer)
        .where(Dancer.project_id == project_id)
        .order_by(Dancer.number)
    )
    dancers = result.scalars().all()
    return [DancerResponse.model_validate(d) for d in dancers]


@router.get("/{dancer_id}", response_model=DancerResponse)
async def get_dancer(
    project_id: int,
    dancer_id: int,
    db: AsyncSession = Depends(get_db),
) -> DancerResponse:
    """Get a single dancer by ID."""
    dancer = await db.get(Dancer, dancer_id)
    if not dancer or dancer.project_id != project_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dancer not found")
    return DancerResponse.model_validate(dancer)


@router.post("/", response_model=DancerResponse, status_code=status.HTTP_201_CREATED)
async def create_dancer(
    project_id: int,
    body: DancerCreate,
    db: AsyncSession = Depends(get_db),
) -> DancerResponse:
    """Add a new dancer to the project."""
    await _get_project_or_404(project_id, db)
    dancer = Dancer(project_id=project_id, **body.model_dump())
    db.add(dancer)
    await db.flush()
    await db.refresh(dancer)
    return DancerResponse.model_validate(dancer)


@router.put("/{dancer_id}", response_model=DancerResponse)
async def update_dancer(
    project_id: int,
    dancer_id: int,
    body: DancerUpdate,
    db: AsyncSession = Depends(get_db),
) -> DancerResponse:
    """Update a dancer's info."""
    dancer = await db.get(Dancer, dancer_id)
    if not dancer or dancer.project_id != project_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dancer not found")

    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(dancer, field, value)

    await db.flush()
    await db.refresh(dancer)
    return DancerResponse.model_validate(dancer)


@router.delete("/bulk", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dancers_bulk(
    project_id: int,
    dancer_ids: List[int],
    db: AsyncSession = Depends(get_db),
) -> None:
    """Remove multiple dancers from the project at once."""
    await _get_project_or_404(project_id, db)

    result = await db.execute(
        select(Dancer.id).where(
            Dancer.project_id == project_id,
            Dancer.id.in_(dancer_ids)
        )
    )
    valid_dancer_ids = {row[0] for row in result.fetchall()}

    invalid_ids = set(dancer_ids) - valid_dancer_ids
    if invalid_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The following dancer IDs do not belong to project {project_id}: {list(invalid_ids)}"
        )

    await db.execute(
        delete(Dancer).where(
            Dancer.project_id == project_id,
            Dancer.id.in_(dancer_ids)
        )
    )


@router.delete("/{dancer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dancer(
    project_id: int,
    dancer_id: int,
    db: AsyncSession = Depends(get_db),
) -> None:
    """Remove a dancer from the project."""
    dancer = await db.get(Dancer, dancer_id)
    if not dancer or dancer.project_id != project_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dancer not found")
    await db.delete(dancer)
