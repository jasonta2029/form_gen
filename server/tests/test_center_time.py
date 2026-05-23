"""
test_center_time.py — Pytest checking center time exposures calculations accuracy.
"""

from utils.geometry import distance
from services.center_time_service import CenterTimeService

def test_distance_check_formula():
    """Asserts Euclidean spacing metric handles coordinate offsets properly."""
    d = distance(0.0, 0.0, 3.0, 4.0)
    assert d == 5.0

def test_exposure_evaluation_calculation():
    """Verifies dancer proximity occupancy triggers correctly."""
    dancers = [{"id": 1, "name": "Patty"}]
    formations = [
        {
            "timestamp_start": 0.0,
            "timestamp_end": 10.0,
            "positions": [{"dancer_id": 1, "x": 0.0, "y": 0.0}] # Exactly at Red X center
        }
    ]
    res = CenterTimeService.calculate_residency_exposures(1, dancers, formations)
    assert res["stats"][0]["total_time_near_center"] == 10.0
    assert res["stats"][0]["percentage"] == 100.0
    assert res["stats"][0]["is_flagged"] == True # Highly overrepresented
