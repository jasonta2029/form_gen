"""
models/formation.py — Formation ORM model.

A *Formation* is a snapshot of the stage at a particular moment in time.
It belongs to a project and contains many DancerPosition rows.
"""

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Integer, String, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

if TYPE_CHECKING:
    from models.project import Project
    from models.position import DancerPosition


class Formation(Base):
    """A named stage arrangement within a project timeline."""

    __tablename__ = "formations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False, default="Untitled")
    order_index: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0,
        comment="Zero-based ordering of formations in the timeline",
    )

    timestamp_start: Mapped[Optional[float]] = mapped_column(
        Float, nullable=True, comment="Start time in seconds relative to audio track"
    )
    timestamp_end: Mapped[Optional[float]] = mapped_column(
        Float, nullable=True, comment="End time in seconds relative to audio track"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # ── Relationships ────────────────────────────────────────
    project: Mapped["Project"] = relationship("Project", back_populates="formations")
    positions: Mapped[List["DancerPosition"]] = relationship(
        "DancerPosition", back_populates="formation", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Formation id={self.id} name={self.name!r} order={self.order_index}>"
