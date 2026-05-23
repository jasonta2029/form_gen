"""
stage.py — Shared relative coordinate definitions mapping limits matching frontends.
"""

STAGE_WIDTH = 50.0   # Left [-25.0] to Right [+25.0]
STAGE_HEIGHT = 30.0  # Down/Audience [-15.0] to Up/Backstage [+15.0]

CENTER_X = 0.0
CENTER_Y = 0.0
CENTER_THRESHOLD_RADIUS = 2.5  # Exposure Focal Radius limits definition around center red X

GRID_SPACING = 1.0  # Meter interval guides

def is_on_stage(x: float, y: float) -> bool:
    """Verifies coordinates exist within limits of stage borders."""
    return -25.0 <= x <= 25.0 and -15.0 <= y <= 15.0

def snap_to_grid(x: float, y: float, interval: float = 0.5) -> tuple:
    """Aligns positions to clean fractions spacing intervals (e.g. nearest 0.5)."""
    snapped_x = round(x / interval) * interval
    snapped_y = round(y / interval) * interval
    
    # Keep snapped node inside borders
    snapped_x = max(-25.0, min(snapped_x, 25.0))
    snapped_y = max(-15.0, min(snapped_y, 15.0))
    return snapped_x, snapped_y
