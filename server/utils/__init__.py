"""
utils — Helper geometry algorithms and standard coordinates grids limits constants.
"""

from utils.stage import (
  STAGE_WIDTH,
  STAGE_HEIGHT,
  CENTER_X,
  CENTER_Y,
  CENTER_THRESHOLD_RADIUS,
  GRID_SPACING,
  is_on_stage,
  snap_to_grid
)

from utils.geometry import (
  distance,
  midpoint,
  rotate_point,
  mirror_point,
  calculate_centroid
)
