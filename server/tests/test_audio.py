"""
test_audio.py — Audio upload endpoint tests.
"""

import pytest
import io
from pathlib import Path


@pytest.fixture(scope="module")
def audio_project_id(client):
    """Create a shared project for audio tests."""
    resp = client.post("/api/projects/", json={"name": "Audio Test Project", "num_dancers": 2})
    assert resp.status_code == 201
    return resp.json()["id"]


def test_upload_audio_track_mp3(client, audio_project_id):
    """Test uploading a valid MP3 file."""
    # Create a fake MP3 file
    file_content = b"id3\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"  # Minimal ID3 header
    files = {"file": ("test.mp3", io.BytesIO(file_content), "audio/mpeg")}

    response = client.post(
        f"/api/projects/{audio_project_id}/music/upload",
        files=files
    )
    assert response.status_code == 200
    data = response.json()
    assert "file_path" in data
    assert "filename" in data
    assert data["filename"] == "test.mp3"
    assert "project_" + str(audio_project_id) in data["file_path"]


def test_upload_audio_track_wav(client, audio_project_id):
    """Test uploading a valid WAV file."""
    # Create a fake WAV file
    file_content = b"RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x40\x1f\x00\x00\x40\x1f\x00\x00\x01\x00\x08\x00data\x00\x00\x00\x00"
    files = {"file": ("test.wav", io.BytesIO(file_content), "audio/wav")}

    response = client.post(
        f"/api/projects/{audio_project_id}/music/upload",
        files=files
    )
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "test.wav"


def test_upload_audio_track_invalid_format(client, audio_project_id):
    """Test uploading an invalid audio format."""
    files = {"file": ("test.txt", io.BytesIO(b"not audio"), "text/plain")}

    response = client.post(
        f"/api/projects/{audio_project_id}/music/upload",
        files=files
    )
    assert response.status_code == 400
    assert "Unsupported audio format" in response.json()["detail"]


def test_upload_audio_track_no_file(client, audio_project_id):
    """Test uploading without a file."""
    response = client.post(
        f"/api/projects/{audio_project_id}/music/upload"
    )
    assert response.status_code == 422  # Validation error


def test_upload_audio_track_nonexistent_project(client):
    """Test uploading to a nonexistent project."""
    files = {"file": ("test.mp3", io.BytesIO(b"id3"), "audio/mpeg")}

    response = client.post(
        "/api/projects/999999/music/upload",
        files=files
    )
    assert response.status_code == 404