"""
routers/ai.py — AI-powered formation generation endpoints.

Prefix: /api/projects/{project_id}/ai
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models.project import Project
from schemas.ai import (
    GenerationRequest,
    GenerationResponse,
    TransitionRequest,
    TransitionResponse,
    TemplateRequest,
)
from schemas.position import PositionResponse
from services.ai_service import AIService

router = APIRouter(
    prefix="/api/projects/{project_id}/ai",
    tags=["ai"],
)


async def _get_project_or_404(project_id: int, db: AsyncSession) -> Project:
    project = await db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project


@router.post("/generate", response_model=GenerationResponse)
async def generate_formation(
    project_id: int,
    body: GenerationRequest,
    db: AsyncSession = Depends(get_db),
) -> GenerationResponse:
    """
    Use AI to generate a new formation based on a natural-language prompt.

    The AI considers the number of dancers, style, and any constraints
    to produce an arrangement with an explanatory reasoning string.
    """
    await _get_project_or_404(project_id, db)
    service = AIService()
    result = await service.generate_formation(
        prompt=body.prompt,
        num_dancers=body.num_dancers,
        style=body.style,
        constraints=body.constraints,
    )
    return result


@router.post("/suggest-transitions", response_model=TransitionResponse)
async def suggest_transitions(
    project_id: int,
    body: TransitionRequest,
    db: AsyncSession = Depends(get_db),
) -> TransitionResponse:
    """
    Suggest smooth intermediate formations between two existing formations.

    Uses optimal assignment to minimise total travel distance and avoid
    path crossings.
    """
    await _get_project_or_404(project_id, db)
    service = AIService()
    result = await service.suggest_transitions(
        db=db,
        from_formation_id=body.from_formation_id,
        to_formation_id=body.to_formation_id,
        num_steps=body.num_intermediate_steps,
    )
    return result


@router.post("/template", response_model=list[PositionResponse])
async def apply_template(
    project_id: int,
    body: TemplateRequest,
    db: AsyncSession = Depends(get_db),
) -> list[PositionResponse]:
    """
    Generate positions from a geometric template (e.g. CIRCLE, V_SHAPE).

    Pure geometry — no AI call required.
    """
    await _get_project_or_404(project_id, db)
    service = AIService()
    positions = service.apply_template(
        shape=body.shape,
        num_dancers=body.num_dancers,
        scale=body.scale,
        rotation_deg=body.rotation_deg,
    )
    return positions
