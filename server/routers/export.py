"""
routers/export.py — Image and PDF export endpoints.

Prefix: /api/projects/{project_id}/export
"""

import io
import zipfile
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database import get_db
from models.dancer import Dancer
from models.formation import Formation
from models.position import DancerPosition
from models.project import Project
from schemas.export import ExportImageRequest, ExportPDFRequest
from services.export_service import render_formation_image, build_pdf_booklet

router = APIRouter(prefix="/api/projects/{project_id}/export", tags=["export"])


async def _get_project_or_404(project_id: int, db: AsyncSession) -> Project:
    project = await db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project


async def _load_dancers(project_id: int, db: AsyncSession) -> List[dict]:
    result = await db.execute(select(Dancer).where(Dancer.project_id == project_id))
    return [
        {"id": d.id, "name": d.name, "number": d.number, "color": d.color}
        for d in result.scalars().all()
    ]


async def _load_formation_with_positions(formation_id: int, db: AsyncSession) -> dict:
    result = await db.execute(
        select(Formation)
        .options(selectinload(Formation.positions))
        .where(Formation.id == formation_id)
    )
    f = result.scalar_one_or_none()
    if not f:
        return None
    return {
        "id": f.id,
        "name": f.name,
        "order_index": f.order_index,
        "timestamp_start": f.timestamp_start,
        "timestamp_end": f.timestamp_end,
        "positions": [{"dancer_id": p.dancer_id, "x": p.x, "y": p.y} for p in f.positions],
    }


async def _load_all_formations(project_id: int, db: AsyncSession) -> List[dict]:
    result = await db.execute(
        select(Formation)
        .options(selectinload(Formation.positions))
        .where(Formation.project_id == project_id)
        .order_by(Formation.order_index)
    )
    formations = []
    for f in result.scalars().all():
        formations.append({
            "id": f.id,
            "name": f.name,
            "order_index": f.order_index,
            "timestamp_start": f.timestamp_start,
            "timestamp_end": f.timestamp_end,
            "positions": [{"dancer_id": p.dancer_id, "x": p.x, "y": p.y} for p in f.positions],
        })
    return formations


# ── Endpoints ─────────────────────────────────────────────────

@router.post("/image")
async def export_formation_image(
    project_id: int,
    request: ExportImageRequest,
    db: AsyncSession = Depends(get_db),
) -> StreamingResponse:
    """Render a single formation snapshot as a PNG or JPEG image."""
    await _get_project_or_404(project_id, db)

    formation = await _load_formation_with_positions(request.formation_id, db)
    if not formation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Formation not found")

    dancers = await _load_dancers(project_id, db)

    png_bytes = render_formation_image(
        formation_name=formation["name"],
        positions=formation["positions"],
        dancers=dancers,
        width=request.width,
        height=request.height,
        show_labels=request.show_labels,
        show_grid=request.show_grid,
        background_color=request.background_color,
    )

    fmt = request.format.value
    media_type = "image/png" if fmt == "png" else "image/jpeg"
    filename = f"formation_{request.formation_id}.{fmt}"

    return StreamingResponse(
        io.BytesIO(png_bytes),
        media_type=media_type,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.post("/pdf")
async def export_show_pdf(
    project_id: int,
    request: ExportPDFRequest,
    db: AsyncSession = Depends(get_db),
) -> StreamingResponse:
    """Compile selected (or all) formations into a multi-page PDF booklet."""
    project = await _get_project_or_404(project_id, db)
    dancers = await _load_dancers(project_id, db)
    all_formations = await _load_all_formations(project_id, db)

    if request.formation_ids:
        id_set = set(request.formation_ids)
        formations = [f for f in all_formations if f["id"] in id_set]
    else:
        formations = all_formations

    if not formations:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No formations to export")

    pdf_bytes = build_pdf_booklet(
        project_name=project.name,
        formations=formations,
        dancers=dancers,
        page_size=request.page_size,
        show_labels=request.show_labels,
    )

    filename = f"{project.name.replace(' ', '_')}_formations.pdf"
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.post("/all")
async def export_all_as_zip(
    project_id: int,
    db: AsyncSession = Depends(get_db),
) -> StreamingResponse:
    """Export every formation as a PNG inside a single ZIP archive."""
    project = await _get_project_or_404(project_id, db)
    dancers = await _load_dancers(project_id, db)
    formations = await _load_all_formations(project_id, db)

    if not formations:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No formations to export")

    zip_buf = io.BytesIO()
    with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for formation in formations:
            png_bytes = render_formation_image(
                formation_name=formation["name"],
                positions=formation["positions"],
                dancers=dancers,
            )
            safe_name = formation["name"].replace(" ", "_").replace("/", "-")
            zf.writestr(f"{formation['order_index']:03d}_{safe_name}.png", png_bytes)

    zip_buf.seek(0)
    filename = f"{project.name.replace(' ', '_')}_all_formations.zip"
    return StreamingResponse(
        zip_buf,
        media_type="application/zip",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
