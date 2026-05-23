"""
music_service.py — Manages show audio markers timings and files listings metadata.
"""

from typing import List

class MusicService:
    @staticmethod
    def register_timing_marker(project_id: int, name: str, timestamp: float, formation_id: int = None) -> dict:
        """Registers aTiming Marker bound to timeline."""
        return {
            "id": 1,
            "project_id": project_id,
            "name": name,
            "timestamp": timestamp,
            "formation_id": formation_id
        }

    @staticmethod
    def list_project_markers(project_id: int) -> List[dict]:
        """Lists timing bookmarks registered under a show."""
        return []
