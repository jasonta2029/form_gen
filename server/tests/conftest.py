"""
conftest.py — Async-compatible test setup.

Uses an in-memory SQLite async engine so every test gets a clean database.
TestClient from Starlette handles async FastAPI routes transparently via anyio.
"""

import asyncio
import pytest
from starlette.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from database import Base, get_db
from main import app

_TEST_DB_URL = "sqlite+aiosqlite:///./test_formflow.db"
_engine = create_async_engine(_TEST_DB_URL, echo=False)
_factory = async_sessionmaker(bind=_engine, class_=AsyncSession, expire_on_commit=False)


async def _create_tables() -> None:
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


asyncio.run(_create_tables())


async def _override_get_db():
    """Async dependency override — yields a real AsyncSession against the test DB."""
    async with _factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


app.dependency_overrides[get_db] = _override_get_db


@pytest.fixture(scope="module")
def client():
    """Sync TestClient wrapping the async FastAPI app."""
    with TestClient(app) as c:
        yield c
