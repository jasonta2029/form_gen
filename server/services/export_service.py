"""
export_service.py — Renders formation snapshots as PNG images and PDF booklets.

Uses Pillow for raster images and ReportLab for PDF generation.
Stage coordinate space: x ∈ [-25, 25], y ∈ [-15, 15], center = (0, 0).
"""

import io
import math
from typing import List, Optional, Tuple

from PIL import Image, ImageDraw, ImageFont

from utils.stage import STAGE_WIDTH, STAGE_HEIGHT


# ── Colour helpers ────────────────────────────────────────────

_DANCER_PALETTE = [
    "#FF5733", "#3B82F6", "#10B981", "#F59E0B", "#8B5CF6",
    "#EC4899", "#14B8A6", "#F97316", "#6366F1", "#84CC16",
    "#EF4444", "#06B6D4", "#A855F7", "#22C55E", "#EAB308",
    "#3B82F6", "#F43F5E", "#0EA5E9", "#D946EF", "#4ADE80",
]

def _hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


# ── Coordinate mapping ────────────────────────────────────────

def _stage_to_pixel(
    sx: float, sy: float, img_w: int, img_h: int, margin: int = 60
) -> Tuple[int, int]:
    """Convert stage coordinates to pixel coordinates."""
    usable_w = img_w - 2 * margin
    usable_h = img_h - 2 * margin
    px = margin + (sx + STAGE_WIDTH / 2) / STAGE_WIDTH * usable_w
    # Stage y: positive = backstage (up on screen = smaller pixel y)
    py = margin + (1 - (sy + STAGE_HEIGHT / 2) / STAGE_HEIGHT) * usable_h
    return int(px), int(py)


# ── Image renderer ────────────────────────────────────────────

def render_formation_image(
    formation_name: str,
    positions: List[dict],
    dancers: List[dict],
    width: int = 1200,
    height: int = 800,
    show_labels: bool = True,
    show_grid: bool = False,
    background_color: str = "#1a1a24",
) -> bytes:
    """
    Render a single formation as a PNG image.

    positions — list of {dancer_id, x, y}
    dancers   — list of {id, name, number, color}
    """
    bg = _hex_to_rgb(background_color)
    img = Image.new("RGB", (width, height), bg)
    draw = ImageDraw.Draw(img)

    margin = 60
    cx_px = width // 2
    cy_px = height // 2

    # Grid lines
    if show_grid:
        grid_color = (50, 50, 70)
        for gx in range(-24, 25, 4):
            px, _ = _stage_to_pixel(gx, 0, width, height, margin)
            draw.line([(px, margin), (px, height - margin)], fill=grid_color, width=1)
        for gy in range(-14, 15, 4):
            _, py = _stage_to_pixel(0, gy, width, height, margin)
            draw.line([(margin, py), (width - margin, py)], fill=grid_color, width=1)

    # Stage border
    border_color = (255, 42, 127)
    draw.rounded_rectangle(
        [margin, margin, width - margin, height - margin],
        radius=16, outline=border_color, width=3
    )

    # Center X marker
    cx, cy = _stage_to_pixel(0, 0, width, height, margin)
    marker_size = 14
    draw.line([(cx - marker_size, cy - marker_size), (cx + marker_size, cy + marker_size)],
              fill=(220, 50, 50), width=3)
    draw.line([(cx - marker_size, cy + marker_size), (cx + marker_size, cy - marker_size)],
              fill=(220, 50, 50), width=3)

    # Direction labels
    label_color = (120, 120, 150)
    draw.text((cx, margin - 20), "BACKSTAGE", fill=label_color, anchor="mm")
    draw.text((cx, height - margin + 20), "AUDIENCE", fill=label_color, anchor="mm")

    # Build dancer lookup
    dancer_map = {d["id"]: d for d in dancers}

    dot_radius = max(12, min(24, 400 // max(1, len(positions))))

    for i, pos in enumerate(positions):
        dancer = dancer_map.get(pos["dancer_id"], {})
        color_hex = dancer.get("color") or _DANCER_PALETTE[i % len(_DANCER_PALETTE)]
        color_rgb = _hex_to_rgb(color_hex)

        px, py = _stage_to_pixel(pos["x"], pos["y"], width, height, margin)

        # Shadow
        draw.ellipse(
            [px - dot_radius + 2, py - dot_radius + 2, px + dot_radius + 2, py + dot_radius + 2],
            fill=(20, 20, 30)
        )
        # Fill
        draw.ellipse(
            [px - dot_radius, py - dot_radius, px + dot_radius, py + dot_radius],
            fill=color_rgb
        )
        # Border
        draw.ellipse(
            [px - dot_radius, py - dot_radius, px + dot_radius, py + dot_radius],
            outline=(255, 255, 255), width=2
        )

        if show_labels:
            label = dancer.get("name") or str(dancer.get("number", i + 1))
            draw.text((px, py), label[:3], fill=(255, 255, 255), anchor="mm")

    # Formation name
    draw.text((width // 2, margin // 2), formation_name, fill=(220, 220, 240), anchor="mm")

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


# ── PDF builder ───────────────────────────────────────────────

def build_pdf_booklet(
    project_name: str,
    formations: List[dict],
    dancers: List[dict],
    page_size: str = "letter",
    show_labels: bool = True,
) -> bytes:
    """
    Compile all formations into a multi-page PDF.

    formations — list of {id, name, order_index, timestamp_start, timestamp_end, positions: [...]}
    dancers    — list of {id, name, number, color}
    """
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.pdfgen import canvas as rl_canvas
    from reportlab.lib.utils import ImageReader

    page = letter if page_size == "letter" else A4
    pw, ph = page

    buf = io.BytesIO()
    c = rl_canvas.Canvas(buf, pagesize=page)

    img_w, img_h = 800, 480

    for formation in formations:
        png_bytes = render_formation_image(
            formation_name=formation.get("name", "Untitled"),
            positions=formation.get("positions", []),
            dancers=dancers,
            width=img_w,
            height=img_h,
            show_labels=show_labels,
            background_color="#1a1a24",
        )
        img_buf = io.BytesIO(png_bytes)
        img_reader = ImageReader(img_buf)

        # Scale image to fit page with margins
        margin = 40
        available_w = pw - 2 * margin
        available_h = ph - 2 * margin - 60  # leave room for header
        scale = min(available_w / img_w, available_h / img_h)
        draw_w = img_w * scale
        draw_h = img_h * scale
        draw_x = (pw - draw_w) / 2
        draw_y = margin

        # Dark background
        c.setFillColorRGB(0.1, 0.1, 0.14)
        c.rect(0, 0, pw, ph, fill=1, stroke=0)

        # Header
        c.setFont("Helvetica-Bold", 14)
        c.setFillColorRGB(0.85, 0.85, 0.95)
        c.drawCentredString(pw / 2, ph - margin - 20, f"{project_name}  —  {formation.get('name', '')}")

        ts = formation.get("timestamp_start")
        te = formation.get("timestamp_end")
        if ts is not None and te is not None:
            c.setFont("Helvetica", 10)
            c.setFillColorRGB(0.6, 0.6, 0.7)
            c.drawCentredString(pw / 2, ph - margin - 38, f"{ts:.1f}s — {te:.1f}s")

        c.drawImage(img_reader, draw_x, draw_y, width=draw_w, height=draw_h)
        c.showPage()

    c.save()
    return buf.getvalue()
