"""
config.py — Application settings loaded from environment variables.

Uses pydantic-settings BaseSettings so values are automatically read
from a .env file (or real env vars) and validated at startup.
"""

from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration for the FormFlow server."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # ── Server ───────────────────────────────────────────────
    port: int = 5000
    debug: bool = False

    # ── Database ─────────────────────────────────────────────
    database_url: str = "sqlite+aiosqlite:///./formflow.db"

    # ── OpenAI ───────────────────────────────────────────────
    openai_api_key: str = "your-key-here"
    openai_model: str = "gpt-4"

    # ── CORS ─────────────────────────────────────────────────
    cors_origins: str = "http://localhost:3000"

    # ── File Storage ─────────────────────────────────────────
    upload_dir: Path = Path("uploads")

    @property
    def cors_origin_list(self) -> List[str]:
        """Parse the comma-separated CORS_ORIGINS string into a list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]


# Singleton settings instance — import this wherever config is needed.
settings = Settings()
