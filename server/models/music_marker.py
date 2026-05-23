"""
models/music_marker.py — MusicMarker ORM model.

Music markers are user-placed timestamps on the audio track that can
optionally be linked to a formation to sync the choreography timeline.
"""

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Integer, String, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

if TYPE_CHECKING:
    from models.project import Project
    from models.formation import Formation


class MusicMarker(Base):
    """A labelled timestamp on the project's audio track."""

    __tablename__ = "music_markers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False, default="Marker")
    timestamp: Mapped[float] = mapped_column(
        Float, nullable=False, comment="Position in seconds from audio start"
    )

    # Optional link to a formation (nullable FK)
    formation_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("formations.id", ondelete="SET NULL"), nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # ── Relationships ────────────────────────────────────────
    project: Mapped["Project"] = relationship("Project", back_populates="music_markers")
    formation: Mapped[Optional["Formation"]] = relationship("Formation", lazy="joined")

    def __repr__(self) -> str:
        return f"<MusicMarker id={self.id} name={self.name!r} t={self.timestamp}>"
