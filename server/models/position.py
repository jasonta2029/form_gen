"""
models/position.py — DancerPosition ORM model.

Each row records the (x, y) coordinate of a single dancer within a
single formation.  Together these rows describe the full stage picture
for a given formation.
"""

from typing import TYPE_CHECKING

from sqlalchemy import Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

if TYPE_CHECKING:
    from models.formation import Formation
    from models.dancer import Dancer


class DancerPosition(Base):
    """X/Y position of one dancer in one formation."""

    __tablename__ = "dancer_positions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    formation_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("formations.id", ondelete="CASCADE"), nullable=False
    )
    dancer_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("dancers.id", ondelete="CASCADE"), nullable=False
    )

    x: Mapped[float] = mapped_column(
        Float, nullable=False, default=0.0, comment="Horizontal stage position"
    )
    y: Mapped[float] = mapped_column(
        Float, nullable=False, default=0.0, comment="Vertical stage position"
    )

    # ── Relationships ────────────────────────────────────────
    formation: Mapped["Formation"] = relationship(
        "Formation", back_populates="positions"
    )
    dancer: Mapped["Dancer"] = relationship("Dancer", lazy="joined")

    def __repr__(self) -> str:
        return (
            f"<DancerPosition id={self.id} dancer={self.dancer_id} "
            f"formation={self.formation_id} x={self.x} y={self.y}>"
        )
