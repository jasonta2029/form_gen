"""
routers/projects.py — CRUD endpoints for choreography projects.

Prefix: /api/projects
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models.project import Project
from schemas.project import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    ProjectListResponse,
)

router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.get("/", response_model=ProjectListResponse)
async def list_projects(
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
) -> ProjectListResponse:
    """Return a paginated list of all projects."""
    total_q = await db.execute(select(func.count(Project.id)))
    total = total_q.scalar_one()

    result = await db.execute(
        select(Project).order_by(Project.updated_at.desc()).offset(skip).limit(limit)
    )
    projects = result.scalars().all()
    return ProjectListResponse(
        items=[ProjectResponse.model_validate(p) for p in projects],
        total=total,
    )


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
) -> ProjectResponse:
    """Return a single project by ID."""
    project = await db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return ProjectResponse.model_validate(project)


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    body: ProjectCreate,
    db: AsyncSession = Depends(get_db),
) -> ProjectResponse:
    """Create a new choreography project."""
    project = Project(**body.model_dump())
    db.add(project)
    await db.flush()
    await db.refresh(project)
    return ProjectResponse.model_validate(project)


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    body: ProjectUpdate,
    db: AsyncSession = Depends(get_db),
) -> ProjectResponse:
    """Update an existing project's metadata."""
    project = await db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)

    await db.flush()
    await db.refresh(project)
    return ProjectResponse.model_validate(project)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete a project and all related data (cascade)."""
    project = await db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    await db.delete(project)
