"""
ai_service.py — AI-assisted formation generator.

Provides:
  - apply_template()        — pure geometry, no API call needed
  - generate_formation()    — OpenAI natural-language prompt with geometric fallback
  - suggest_transitions()   — linear interpolation between two saved formations
"""

import math
import json
from typing import List, Dict, Any, Optional

from utils.geometry import rotate_point
from utils.stage import CENTER_THRESHOLD_RADIUS


class AIService:

    # ── Public async methods (called by routers) ──────────────

    def apply_template(
        self,
        shape: str,
        num_dancers: int,
        scale: float = 1.0,
        rotation_deg: float = 0.0,
    ) -> List[Dict]:
        """
        Calculate (x, y) positions for num_dancers in the requested geometric shape.
        Returns dicts compatible with PositionResponse (id=0, formation_id=0 as placeholders).
        """
        raw = self._shape(shape.upper(), num_dancers)
        rotation_rad = math.radians(rotation_deg)

        result = []
        for i, pos in enumerate(raw):
            x, y = pos["x"] * scale, pos["y"] * scale
            if rotation_deg != 0.0:
                x, y = rotate_point(x, y, rotation_rad)
            x = max(-25.0, min(25.0, x))
            y = max(-15.0, min(15.0, y))
            result.append({"id": 0, "formation_id": 0, "dancer_id": i + 1, "x": x, "y": y})
        return result

    async def generate_formation(
        self,
        prompt: str,
        num_dancers: int,
        style: Optional[str],
        constraints: Optional[Dict],
    ) -> Dict:
        """
        Ask OpenAI to generate a formation from a natural-language prompt.
        Falls back to a geometric SCATTER if no API key is configured.
        """
        try:
            from config import settings
            if settings.openai_api_key in ("your-key-here", "", None):
                raise ValueError("OpenAI key not set")

            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=settings.openai_api_key)

            system = (
                "You are a choreography assistant. "
                "Generate precise dancer positions on a rectangular stage. "
                "Stage: x ∈ [-25, 25] (left → right), y ∈ [-15, 15] (audience → backstage). "
                "Center is (0, 0). "
                "Respond ONLY with valid JSON: "
                '{"positions": [{"dancer_id": 1, "x": 0.0, "y": 0.0}, ...], "reasoning": "..."}'
            )
            user = (
                f"Formation prompt: {prompt}\n"
                f"Number of dancers: {num_dancers}\n"
                f"Style: {style or 'not specified'}\n"
                f"Constraints: {json.dumps(constraints or {})}"
            )

            resp = await client.chat.completions.create(
                model=settings.openai_model,
                messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
                temperature=0.7,
                response_format={"type": "json_object"},
            )
            data = json.loads(resp.choices[0].message.content)
            positions = data.get("positions", [])

            # Normalise to PositionResponse shape and clamp to stage
            normalised = []
            for i, p in enumerate(positions[:num_dancers]):
                normalised.append({
                    "id": 0,
                    "formation_id": 0,
                    "dancer_id": p.get("dancer_id", i + 1),
                    "x": max(-25.0, min(25.0, float(p.get("x", 0)))),
                    "y": max(-15.0, min(15.0, float(p.get("y", 0)))),
                })
            return {"positions": normalised, "reasoning": data.get("reasoning", "")}

        except Exception as exc:
            positions = self.apply_template("SCATTER", num_dancers)
            return {
                "positions": positions,
                "reasoning": f"Geometric fallback (OpenAI unavailable: {exc})",
            }

    async def suggest_transitions(
        self,
        db,
        from_formation_id: int,
        to_formation_id: int,
        num_steps: int,
    ) -> Dict:
        """
        Compute linearly-interpolated intermediate positions between two saved formations.
        Returns num_steps evenly-spaced snapshots plus total travel distance.
        """
        from sqlalchemy import select
        from models.position import DancerPosition

        from_rows = (
            await db.execute(
                select(DancerPosition).where(DancerPosition.formation_id == from_formation_id)
            )
        ).scalars().all()
        to_rows = (
            await db.execute(
                select(DancerPosition).where(DancerPosition.formation_id == to_formation_id)
            )
        ).scalars().all()

        from_map = {p.dancer_id: p for p in from_rows}
        to_map = {p.dancer_id: p for p in to_rows}

        total_distance = 0.0
        for did, fp in from_map.items():
            tp = to_map.get(did)
            if tp:
                total_distance += math.sqrt((tp.x - fp.x) ** 2 + (tp.y - fp.y) ** 2)

        steps = []
        for step in range(1, num_steps + 1):
            t = step / (num_steps + 1)
            step_positions = []
            for did, fp in from_map.items():
                tp = to_map.get(did)
                if tp:
                    step_positions.append({
                        "id": 0,
                        "formation_id": 0,
                        "dancer_id": did,
                        "x": fp.x + (tp.x - fp.x) * t,
                        "y": fp.y + (tp.y - fp.y) * t,
                    })
            steps.append(step_positions)

        return {
            "steps": steps,
            "total_distance": round(total_distance, 3),
            "crossing_count": 0,
        }

    # ── Shape calculators ─────────────────────────────────────

    def _shape(self, name: str, n: int) -> List[Dict]:
        dispatch = {
            "V_SHAPE": self._v_shape,
            "ARC": self._arc,
            "CIRCLE": self._circle,
            "SPLIT": self._split,
            "LINE": self._line,
            "DIAGONAL": self._diagonal,
            "DIAMOND": self._diamond,
            "CLUSTER": self._cluster,
            "SCATTER": self._circle,
        }
        fn = dispatch.get(name, self._circle)
        return fn(n)

    def _v_shape(self, n: int) -> List[Dict]:
        positions = []
        spacing = 3.0
        for i in range(n):
            if i == 0:
                x, y = 0.0, -4.0
            elif i % 2 == 1:
                step = (i // 2) + 1
                x = -step * spacing
                y = -4.0 + step * spacing * 0.7
            else:
                step = i // 2
                x = step * spacing
                y = -4.0 + step * spacing * 0.7
            positions.append({"x": x, "y": y})
        return positions

    def _arc(self, n: int) -> List[Dict]:
        radius = 12.0
        start, end = math.pi * 0.15, math.pi * 0.85
        step = (end - start) / max(1, n - 1)
        return [
            {"x": radius * math.cos(start + i * step), "y": radius * math.sin(start + i * step) - 3.0}
            for i in range(n)
        ]

    def _circle(self, n: int) -> List[Dict]:
        r = min(10.0, 2.0 * n)
        return [
            {"x": r * math.cos(2 * math.pi * i / n), "y": r * math.sin(2 * math.pi * i / n)}
            for i in range(n)
        ]

    def _split(self, n: int) -> List[Dict]:
        half = math.ceil(n / 2)
        sep = 10.0
        result = []
        for i in range(n):
            is_left = i < half
            idx = i if is_left else i - half
            size = half if is_left else n - half
            x = -sep / 2 if is_left else sep / 2
            y = -((size - 1) * 2.5) / 2 + idx * 2.5
            result.append({"x": x, "y": y})
        return result

    def _line(self, n: int) -> List[Dict]:
        spacing = min(4.0, 48.0 / max(1, n - 1))
        start_x = -(n - 1) * spacing / 2
        return [{"x": start_x + i * spacing, "y": 0.0} for i in range(n)]

    def _diagonal(self, n: int) -> List[Dict]:
        step = min(3.0, 40.0 / max(1, n - 1))
        start_x = -(n - 1) * step / 2
        start_y = -(n - 1) * step * 0.5 / 2
        return [{"x": start_x + i * step, "y": start_y + i * step * 0.5} for i in range(n)]

    def _diamond(self, n: int) -> List[Dict]:
        sides = 4
        per_side = max(1, n // sides)
        radius = 8.0
        positions = []
        for s in range(sides):
            angle_start = math.pi / 4 + s * math.pi / 2
            angle_end = math.pi / 4 + (s + 1) * math.pi / 2
            for j in range(per_side):
                t = j / max(1, per_side)
                angle = angle_start + t * (angle_end - angle_start)
                positions.append({"x": radius * math.cos(angle), "y": radius * math.sin(angle)})
                if len(positions) >= n:
                    return positions
        while len(positions) < n:
            positions.append({"x": 0.0, "y": 0.0})
        return positions

    def _cluster(self, n: int) -> List[Dict]:
        """Tight cluster around center with slight random-looking offsets."""
        positions = []
        rings = [1, 6, 12, 18]
        radii = [0.0, 2.5, 5.0, 7.5]
        placed = 0
        for ring_idx, (count, r) in enumerate(zip(rings, radii)):
            for j in range(count):
                if placed >= n:
                    break
                if r == 0.0:
                    positions.append({"x": 0.0, "y": 0.0})
                else:
                    angle = 2 * math.pi * j / count
                    positions.append({"x": r * math.cos(angle), "y": r * math.sin(angle)})
                placed += 1
            if placed >= n:
                break
        return positions
