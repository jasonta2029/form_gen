"""
center_time_service.py — Center-time analysis and rebalancing.

Calculates how much time each dancer spends near stage center (0, 0)
across all formations and can redistribute that time by swapping positions.
"""

import math
from typing import Dict, List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.dancer import Dancer
from models.formation import Formation
from models.position import DancerPosition
from schemas.center_time import CenterTimeStats, DancerCenterTime, RebalanceResponse
from utils.stage import CENTER_THRESHOLD_RADIUS


class CenterTimeService:

    async def calculate_center_time(
        self, project_id: int, db: AsyncSession
    ) -> CenterTimeStats:
        """Return center-time stats for every dancer in the project."""
        dancers = (
            await db.execute(select(Dancer).where(Dancer.project_id == project_id).order_by(Dancer.number))
        ).scalars().all()

        formations = (
            await db.execute(select(Formation).where(Formation.project_id == project_id))
        ).scalars().all()

        if not dancers:
            return CenterTimeStats(project_id=project_id, dancers=[], ideal_percentage=0.0)

        ideal = 100.0 / len(dancers)

        dancer_stats: List[DancerCenterTime] = []
        for dancer in dancers:
            total_f = 0
            center_f = 0
            total_dist = 0.0

            for formation in formations:
                pos = (
                    await db.execute(
                        select(DancerPosition).where(
                            DancerPosition.formation_id == formation.id,
                            DancerPosition.dancer_id == dancer.id,
                        )
                    )
                ).scalar_one_or_none()

                if pos is None:
                    continue
                total_f += 1
                dist = math.sqrt(pos.x ** 2 + pos.y ** 2)
                total_dist += dist
                if dist <= CENTER_THRESHOLD_RADIUS:
                    center_f += 1

            pct = (center_f / max(1, total_f)) * 100.0
            avg_dist = total_dist / max(1, total_f)

            if pct > ideal + 5:
                status = "over"
            elif pct < ideal - 5:
                status = "under"
            else:
                status = "balanced"

            dancer_stats.append(
                DancerCenterTime(
                    dancer_id=dancer.id,
                    dancer_name=dancer.name,
                    total_formations=total_f,
                    center_formations=center_f,
                    center_percentage=round(pct, 2),
                    avg_distance_to_center=round(avg_dist, 3),
                    status=status,
                )
            )

        return CenterTimeStats(
            project_id=project_id,
            dancers=dancer_stats,
            ideal_percentage=round(ideal, 2),
        )

    async def calculate_for_dancer(
        self, project_id: int, dancer_id: int, db: AsyncSession
    ) -> Optional[DancerCenterTime]:
        """Return center-time stats for a single dancer, or None if not found."""
        dancer = await db.get(Dancer, dancer_id)
        if not dancer or dancer.project_id != project_id:
            return None

        stats = await self.calculate_center_time(project_id, db)
        for entry in stats.dancers:
            if entry.dancer_id == dancer_id:
                return entry
        return None

    async def rebalance_formations(
        self,
        project_id: int,
        db: AsyncSession,
        target_weights: Optional[Dict[int, float]],
        tolerance: float,
    ) -> RebalanceResponse:
        """
        Swap dancer positions across formations to distribute center time more fairly.

        Strategy: For each formation, find dancers in center slots who are over-represented
        and swap their (x, y) with dancers in outer slots who are under-represented.
        """
        before = await self.calculate_center_time(project_id, db)

        # Identify over/under dancers by id
        over_ids = {d.dancer_id for d in before.dancers if d.status == "over"}
        under_ids = {d.dancer_id for d in before.dancers if d.status == "under"}

        if not over_ids or not under_ids:
            return RebalanceResponse(adjusted_formations=0, before=before, after=before)

        formations = (
            await db.execute(select(Formation).where(Formation.project_id == project_id))
        ).scalars().all()

        adjusted = 0
        for formation in formations:
            positions = (
                await db.execute(
                    select(DancerPosition).where(DancerPosition.formation_id == formation.id)
                )
            ).scalars().all()

            # Separate into center and outer slots
            center_slots = [
                p for p in positions
                if math.sqrt(p.x ** 2 + p.y ** 2) <= CENTER_THRESHOLD_RADIUS
                and p.dancer_id in over_ids
            ]
            outer_slots = [
                p for p in positions
                if math.sqrt(p.x ** 2 + p.y ** 2) > CENTER_THRESHOLD_RADIUS
                and p.dancer_id in under_ids
            ]

            swapped = False
            for over_pos, under_pos in zip(center_slots, outer_slots):
                over_pos.x, under_pos.x = under_pos.x, over_pos.x
                over_pos.y, under_pos.y = under_pos.y, over_pos.y
                swapped = True

            if swapped:
                adjusted += 1

        await db.flush()
        after = await self.calculate_center_time(project_id, db)
        return RebalanceResponse(adjusted_formations=adjusted, before=before, after=after)
