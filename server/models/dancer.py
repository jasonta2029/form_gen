"""
models/dancer.py — Dancer ORM model.

Each dancer belongs to a project and is referenced by DancerPosition entries
to indicate where the dancer stands in each formation.
"""

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

if TYPE_CHECKING:
    from models.project import Project


class Dancer(Base):
    """A single performer in a choreography project."""

    __tablename__ = "dancers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    number: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    color: Mapped[Optional[str]] = mapped_column(
        String(7), nullable=True, default="#3B82F6",
        comment="Hex colour used for the dancer's dot on stage, e.g. '#FF5733'",
    )
    group: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True,
        comment="Optional grouping label, e.g. 'Front Row', 'Leads'",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # ── Relationships ────────────────────────────────────────
    project: Mapped["Project"] = relationship("Project", back_populates="dancers")

    def __repr__(self) -> str:
        return f"<Dancer id={self.id} number={self.number} name={self.name!r}>"
