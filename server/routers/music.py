"""
music.py — FastAPI router for audio track uploads and sync marker timeline configurations.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session

from database import get_db
from schemas.music_marker import MarkerCreate, MarkerUpdate, MarkerResponse

router = APIRouter(prefix="/api/projects/{project_id}/music", tags=["music"])

@router.post("/upload", response_model=dict, status_code=status.HTTP_200_OK)
async def upload_audio_track(project_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Uploads track audio stream file and bounds it to project metadata."""
    if not file.filename.endswith((".mp3", ".wav", ".aac", ".m4a")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported audio file format extension."
        )
    # Placeholder return
    return {"file_path": f"uploads/project_{project_id}_{file.filename}", "duration": 180.0}

@router.get("/markers", response_model=List[MarkerResponse])
async def list_timeline_markers(project_id: int, db: Session = Depends(get_db)):
    """Retrieves all timestamp markers registered under a project timeline."""
    return []

@router.post("/markers", response_model=MarkerResponse, status_code=status.HTTP_201_CREATED)
async def add_timeline_marker(project_id: int, marker: MarkerCreate, db: Session = Depends(get_db)):
    """Creates a timing marker bookmark pinned to a second timestamp."""
    return {
        "id": 1,
        "project_id": project_id,
        "name": marker.name,
        "timestamp": marker.timestamp,
        "formation_id": marker.formation_id
    }

@router.put("/markers/{marker_id}", response_model=MarkerResponse)
async def update_timeline_marker(project_id: int, marker_id: int, marker: MarkerUpdate, db: Session = Depends(get_db)):
    """Updates Timing Marker details."""
    return {
        "id": marker_id,
        "project_id": project_id,
        "name": marker.name or "Updated",
        "timestamp": marker.timestamp or 0.0,
        "formation_id": marker.formation_id
    }

@router.delete("/markers/{marker_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_timeline_marker(project_id: int, marker_id: int, db: Session = Depends(get_db)):
    """Removes a timeline timing marker."""
    return None
