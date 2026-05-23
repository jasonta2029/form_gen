"""
test_ai.py — Unit test validating AI geometric shape calculators.
"""

from services.ai_service import AIService

def test_v_shape_placements_count():
    """Asserts that V_SHAPE layout preset builds coordinates for exactly matching roster count."""
    count = 12
    pos = AIService.apply_geometry_preset("V_SHAPE", count)
    assert len(pos) == count
    # Peak of V is centered at focal X
    assert pos[0]["x"] == 0.0

def test_arc_placements_count():
    """Checks that Arc presetter coordinates matches the requested group sizes."""
    count = 8
    pos = AIService.apply_geometry_preset("ARC", count)
    assert len(pos) == count
