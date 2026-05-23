"""
models/project.py — Project ORM model.

A *Project* is the top-level entity that groups dancers, formations, and
music markers for a single choreography piece.
"""

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Integer, String, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

if TYPE_CHECKING:
    from models.dancer import Dancer
    from models.formation import Formation
    from models.music_marker import MusicMarker


class Project(Base):
    """Represents a single choreography project."""

    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    num_dancers: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    audio_file_path: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # ── Relationships ────────────────────────────────────────
    dancers: Mapped[List["Dancer"]] = relationship(
        "Dancer", back_populates="project", cascade="all, delete-orphan"
    )
    formations: Mapped[List["Formation"]] = relationship(
        "Formation",
        back_populates="project",
        cascade="all, delete-orphan",
        order_by="Formation.order_index",
    )
    music_markers: Mapped[List["MusicMarker"]] = relationship(
        "MusicMarker", back_populates="project", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Project id={self.id} name={self.name!r}>"
