"""
export.py — FastAPI router delivering PDF booklet catalogs and high-res image sheets files.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import io

from database import get_db
from schemas.export import ExportImageRequest, ExportPDFRequest

router = APIRouter(prefix="/api/projects/{project_id}/export", tags=["export"])

@router.post("/image", response_class=StreamingResponse)
async def export_formation_image(project_id: int, request: ExportImageRequest, db: Session = Depends(get_db)):
    """Generates and returns PNG raw binary sheet representation of a single snapshot."""
    # Mocking binary response stream
    dummy_img = io.BytesIO(b"dummy png data")
    return StreamingResponse(dummy_img, media_type="image/png")

@router.post("/pdf", response_class=StreamingResponse)
async def export_show_pdf_booklet(project_id: int, request: ExportPDFRequest, db: Session = Depends(get_db)):
    """Compiles and builds multi-page PDF catalog showing snapshots sequence timelines."""
    dummy_pdf = io.BytesIO(b"dummy pdf data")
    return StreamingResponse(dummy_pdf, media_type="application/pdf")

@router.post("/all", response_class=StreamingResponse)
async def export_all_formations_zip(project_id: int, db: Session = Depends(get_db)):
    """Exports all snapshots as png files packed inside a zip archive."""
    dummy_zip = io.BytesIO(b"dummy zip data")
    return StreamingResponse(dummy_zip, media_type="application/zip")
