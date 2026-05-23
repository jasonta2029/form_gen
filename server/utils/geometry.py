"""
geometry.py — Coordinates math equations mapping centroid structures and rotations.
"""

import math
from typing import List, Tuple

def distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """Standard Euclidean distance formula."""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def midpoint(x1: float, y1: float, x2: float, y2: float) -> Tuple[float, float]:
    """Calculates linear center midpoint between two points."""
    return (x1 + x2) / 2.0, (y1 + y2) / 2.0

def rotate_point(x: float, y: float, angle_rad: float, cx: float = 0.0, cy: float = 0.0) -> Tuple[float, float]:
    """Rotates a point (x, y) by an angle (in radians) around a central point (cx, cy)."""
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)
    
    # Translate to origin
    tx = x - cx
    ty = y - cy
    
    # Rotate coordinates
    rx = tx * cos_a - ty * sin_a
    ry = tx * sin_a + ty * cos_a
    
    # Translate back to center
    return rx + cx, ry + cy

def mirror_point(x: float, y: float, axis: str = "y", cx: float = 0.0, cy: float = 0.0) -> Tuple[float, float]:
    """Mirrors a coordinate over either horizontal axis (x) or vertical axis (y) center boundaries."""
    if axis == "y":
        return cx - (x - cx), y
    elif axis == "x":
        return x, cy - (y - cy)
    return x, y

def calculate_centroid(points: List[Tuple[float, float]]) -> Tuple[float, float]:
    """Computes coordinate centroid (geometric mean coordinate center point) of a set of dancers."""
    if not points:
        return 0.0, 0.0
    sum_x = sum(p[0] for p in points)
    sum_y = sum(p[1] for p in points)
    return sum_x / len(points), sum_y / len(points)
