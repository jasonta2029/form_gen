"""
center_time_service.py — Evaluates dancer occupancy times around central Red X coordinates.
Supports automatic layouts adjustments to satisfy priority weights constraints.
"""

from typing import List, Dict, Any
import math
from utils.geometry import distance
from utils.stage import CENTER_X, CENTER_Y, CENTER_THRESHOLD_RADIUS

class CenterTimeService:
    @staticmethod
    def calculate_residency_exposures(project_id: int, dancers: List[dict], formations: List[dict]) -> dict:
        """Calculates cumulative seconds that each dancer spends near coordinates (0, 0)."""
        stats = []
        total_show_duration = 0.0
        
        # Initialize seconds accumulator map
        residency_map = {d["id"]: 0.0 for d in dancers}
        
        for form in formations:
            duration = max(0.0, form.get("timestamp_end", 0.0) - form.get("timestamp_start", 0.0))
            total_show_duration += duration
            
            positions = form.get("positions", [])
            for pos in positions:
                d_id = pos["dancer_id"]
                if d_id in residency_map:
                    # Calculate proximity radius to Red X centerstage (0,0)
                    dist = distance(pos["x"], pos["y"], CENTER_X, CENTER_Y)
                    if dist <= CENTER_THRESHOLD_RADIUS:
                        residency_map[d_id] += duration

        # Formulate metrics summaries list
        target_share = 100.0 / max(1, len(dancers))
        
        for d in dancers:
            total_time = residency_map[d["id"]]
            percent = (total_time / max(0.1, total_show_duration)) * 100.0
            deviation = percent - target_share
            
            # Flag dancer if deviation is severe (e.g. over 15% discrepancy)
            is_flagged = abs(deviation) > 15.0
            
            stats.append({
                "dancer_id": d["id"],
                "dancer_name": d["name"],
                "total_time_near_center": total_time,
                "percentage": percent,
                "target_percentage": target_share,
                "deviation": deviation,
                "is_flagged": is_flagged
            })

        return {
            "center_point": {"x": CENTER_X, "y": CENTER_Y},
            "threshold_radius": CENTER_THRESHOLD_RADIUS,
            "stats": stats
        }

    @staticmethod
    def balance_layout_weights(project_id: int, target_weights: Dict[int, float], strategy: str) -> List[dict]:
        """Calculates recommended layout offsets tweaks to satisfying prioritizations."""
        # Simple recommendation mock
        return []
