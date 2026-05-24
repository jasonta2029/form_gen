"""
routers/music.py — Audio upload and music marker CRUD.

Prefix: /api/projects/{project_id}/music
"""

import shutil
from pathlib import Path
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from database import get_db
from models.music_marker import MusicMarker
from models.project import Project
from schemas.music_marker import MarkerCreate, MarkerResponse, MarkerUpdate

router = APIRouter(prefix="/api/projects/{project_id}/music", tags=["music"])

ALLOWED_AUDIO = {".mp3", ".wav", ".aac", ".m4a", ".ogg"}


async def _get_project_or_404(project_id: int, db: AsyncSession) -> Project:
    project = await db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project


# ── Audio upload ──────────────────────────────────────────────

@router.post("/upload", status_code=status.HTTP_200_OK)
async def upload_audio_track(
    project_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Save an audio file to disk and attach it to the project."""
    project = await _get_project_or_404(project_id, db)

    suffix = Path(file.filename).suffix.lower()
    if suffix not in ALLOWED_AUDIO:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported audio format '{suffix}'. Allowed: {', '.join(ALLOWED_AUDIO)}",
        )

    dest_dir = settings.upload_dir / f"project_{project_id}"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / file.filename

    with dest.open("wb") as f:
        shutil.copyfileobj(file.file, f)

    relative_path = str(dest)
    project.audio_file_path = relative_path
    await db.flush()
    await db.refresh(project)

    return {"file_path": relative_path, "filename": file.filename}


# ── Markers ───────────────────────────────────────────────────

@router.get("/markers", response_model=List[MarkerResponse])
async def list_markers(
    project_id: int,
    db: AsyncSession = Depends(get_db),
) -> List[MarkerResponse]:
    """Return all music markers for this project ordered by timestamp."""
    await _get_project_or_404(project_id, db)
    result = await db.execute(
        select(MusicMarker)
        .where(MusicMarker.project_id == project_id)
        .order_by(MusicMarker.timestamp)
    )
    return [MarkerResponse.model_validate(m) for m in result.scalars().all()]


@router.post("/markers", response_model=MarkerResponse, status_code=status.HTTP_201_CREATED)
async def create_marker(
    project_id: int,
    body: MarkerCreate,
    db: AsyncSession = Depends(get_db),
) -> MarkerResponse:
    """Add a new timestamp marker to the project's audio timeline."""
    await _get_project_or_404(project_id, db)
    marker = MusicMarker(project_id=project_id, **body.model_dump())
    db.add(marker)
    await db.flush()
    await db.refresh(marker)
    return MarkerResponse.model_validate(marker)


@router.put("/markers/{marker_id}", response_model=MarkerResponse)
async def update_marker(
    project_id: int,
    marker_id: int,
    body: MarkerUpdate,
    db: AsyncSession = Depends(get_db),
) -> MarkerResponse:
    """Update an existing music marker."""
    marker = await db.get(MusicMarker, marker_id)
    if not marker or marker.project_id != project_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Marker not found")

    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(marker, field, value)

    await db.flush()
    await db.refresh(marker)
    return MarkerResponse.model_validate(marker)


@router.delete("/markers/{marker_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_marker(
    project_id: int,
    marker_id: int,
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete a music marker."""
    marker = await db.get(MusicMarker, marker_id)
    if not marker or marker.project_id != project_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Marker not found")
    await db.delete(marker)
