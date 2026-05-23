"""
ai_service.py — AI-assisted coordinates generator implementing trigonometric preset layouts.
Supports V-shape, Arcs, Splits, Circles, and incorporates OpenAI templates advice handlers.
"""

import math
from typing import List, Dict, Any
from utils.stage import STAGE_WIDTH, STAGE_HEIGHT, is_on_stage

class AIService:
    @staticmethod
    def generate_formation_placements(num_dancers: int, style: str, density: float, symmetry: bool) -> List[Dict[str, float]]:
        """Generates random or symmetric coordinates placements using density constraints."""
        positions = []
        spacing = 3.0 * density
        
        for i in range(num_dancers):
            if symmetry:
                # Mirroring placements
                step = (i // 2) + 1
                sign = -1.0 if (i % 2 == 0) else 1.0
                x = sign * (step * spacing)
                y = 0.0
            else:
                x = (i - (num_dancers - 1) / 2) * spacing
                y = math.sin(i) * 2.0
            
            # Keep within border constraints
            x = max(-25.0, min(x, 25.0))
            y = max(-15.0, min(y, 15.0))
            
            positions.append({"dancer_id": i + 1, "x": x, "y": y})
            
        return positions

    @staticmethod
    def apply_geometry_preset(template_name: str, num_dancers: int, params: Dict[str, Any] = None) -> List[Dict[str, float]]:
        """Calculates exact mathematical placement patterns (V_SHAPE, ARC, SPLIT, CIRCLE, DIAGONAL)."""
        positions = []
        params = params or {}
        density = params.get("density", 0.5)
        spacing = 4.0 * density

        if template_name == "V_SHAPE":
            for i in range(num_dancers):
                if i == 0:
                    x, y = 0.0, -4.0
                elif i % 2 == 1:
                    step = (i // 2) + 1
                    x = -step * spacing
                    y = -4.0 + step * (spacing * 0.7)
                else:
                    step = i // 2
                    x = step * spacing
                    y = -4.0 + step * (spacing * 0.7)
                positions.append({"dancer_id": i + 1, "x": x, "y": y})

        elif template_name == "ARC":
            start_angle = math.pi * 0.2
            end_angle = math.pi * 0.8
            angle_step = (end_angle - start_angle) / max(1, num_dancers - 1)
            radius = 12.0
            
            for i in range(num_dancers):
                angle = start_angle + i * angle_step
                x = radius * math.cos(angle)
                y = radius * math.sin(angle) - 4.0
                positions.append({"dancer_id": i + 1, "x": x, "y": y})

        elif template_name == "SPLIT":
            half = math.ceil(num_dancers / 2)
            separation = 12.0
            
            for i in range(num_dancers):
                is_left = i < half
                team_idx = i if is_left else i - half
                team_size = half if is_left else num_dancers - half
                
                x = -separation / 2.0 if is_left else separation / 2.0
                y_step = 2.5
                start_y = -((team_size - 1) * y_step) / 2.0
                y = start_y + team_idx * y_step
                
                positions.append({"dancer_id": i + 1, "x": x, "y": y})

        else: # Default scattered circular ring
            for i in range(num_dancers):
                angle = (2.0 * math.pi * i) / num_dancers
                x = 8.0 * math.cos(angle)
                y = 8.0 * math.sin(angle)
                positions.append({"dancer_id": i + 1, "x": x, "y": y})

        return positions
