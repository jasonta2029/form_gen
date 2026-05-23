"""
schemas/export.py — Pydantic schemas for image/PDF export endpoints.
"""

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class ImageFormat(str, Enum):
    """Supported raster image formats."""
    PNG = "png"
    JPEG = "jpeg"


class ExportImageRequest(BaseModel):
    """Request body for exporting a single formation as an image."""
    formation_id: int
    width: int = Field(1200, ge=100, le=4000)
    height: int = Field(800, ge=100, le=4000)
    format: ImageFormat = ImageFormat.PNG
    show_labels: bool = Field(True, description="Render dancer numbers/names on dots")
    show_grid: bool = Field(False, description="Overlay a reference grid")
    background_color: str = Field("#FFFFFF", pattern=r"^#[0-9A-Fa-f]{6}$")


class ExportPDFRequest(BaseModel):
    """Request body for exporting all formations as a PDF document."""
    formation_ids: Optional[List[int]] = Field(
        None, description="Subset of formation IDs to include; None = all"
    )
    page_size: str = Field("letter", description="'letter' or 'a4'")
    include_timeline: bool = Field(True, description="Append a timeline overview page")
    show_labels: bool = True


class ExportResponse(BaseModel):
    """Response after a successful export."""
    file_url: str = Field(..., description="Relative URL to download the generated file")
    file_size_bytes: int
    format: str
