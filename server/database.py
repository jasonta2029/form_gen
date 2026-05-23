"""
database.py — SQLAlchemy async engine, session factory, and declarative Base.

Usage in route handlers::

    @router.get("/")
    async def list_items(db: AsyncSession = Depends(get_db)):
        ...
"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from config import settings

# ── Engine ────────────────────────────────────────────────────
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    future=True,
)

# ── Session factory ───────────────────────────────────────────
async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# ── Declarative Base ─────────────────────────────────────────
class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""
    pass


# ── Dependency ────────────────────────────────────────────────
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that yields a database session and ensures cleanup."""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# ── Lifecycle helpers ─────────────────────────────────────────
async def init_db() -> None:
    """Create all tables (useful for dev / first-run)."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """Dispose of the engine's connection pool."""
    await engine.dispose()
