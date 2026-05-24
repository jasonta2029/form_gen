"""
test_export.py — Export endpoint tests.
"""

import pytest
import io
from zipfile import ZipFile


@pytest.fixture(scope="module")
def export_project_id(client):
    """Create a shared project for export tests."""
    resp = client.post("/api/projects/", json={"name": "Export Test Project", "num_dancers": 2})
    assert resp.status_code == 201
    return resp.json()["id"]


@pytest.fixture(scope="module")
def export_dancer_ids(client, export_project_id):
    """Create 2 dancers in the project."""
    ids = []
    for i in range(1, 3):
        resp = client.post(
            f"/api/projects/{export_project_id}/dancers/",
            json={"number": i, "name": f"Dancer {i}"},
        )
        assert resp.status_code == 201
        ids.append(resp.json()["id"])
    return ids


@pytest.fixture(scope="module")
def export_formation_ids(client, export_project_id, export_dancer_ids):
    """Create 2 formations with positions."""
    formation_ids = []
    for i in range(2):
        # Create formation
        form_resp = client.post(
            f"/api/projects/{export_project_id}/formations/",
            json={"name": f"Formation {i}", "order_index": i}
        )
        assert form_resp.status_code == 201
        formation = form_resp.json()
        fid = formation["id"]

        # Add positions to formation
        positions = [
            {"dancer_id": export_dancer_ids[0], "x": 0.0, "y": 0.0},
            {"dancer_id": export_dancer_ids[1], "x": 5.0, "y": 0.0},
        ]
        pos_resp = client.put(
            f"/api/projects/{export_project_id}/formations/{fid}/positions/",
            json=positions
        )
        assert pos_resp.status_code == 200

        formation_ids.append(fid)

    return formation_ids


def test_export_formation_image(client, export_project_id, export_formation_ids):
    """Test exporting a single formation as PNG."""
    response = client.post(
        f"/api/projects/{export_project_id}/export/image",
        json={
            "formation_id": export_formation_ids[0],
            "width": 800,
            "height": 600,
            "format": "png",
            "show_labels": True,
            "show_grid": True,
            "background_color": "#000000"
        }
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    assert "attachment" in response.headers["content-disposition"]
    assert len(response.content) > 0  # Should have actual image data


def test_export_formation_image_jpeg(client, export_project_id, export_formation_ids):
    """Test exporting a single formation as JPEG."""
    response = client.post(
        f"/api/projects/{export_project_id}/export/image",
        json={
            "formation_id": export_formation_ids[0],
            "width": 800,
            "height": 600,
            "format": "jpeg",
            "show_labels": False,
            "show_grid": False,
            "background_color": "#ffffff"
        }
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/jpeg"
    assert len(response.content) > 0


def test_export_formation_image_not_found(client, export_project_id):
    """Test exporting a non-existent formation."""
    response = client.post(
        f"/api/projects/{export_project_id}/export/image",
        json={
            "formation_id": 999999,
            "width": 800,
            "height": 600,
            "format": "png"
        }
    )
    assert response.status_code == 404


def test_export_show_pdf(client, export_project_id, export_formation_ids):
    """Test exporting formations as PDF."""
    response = client.post(
        f"/api/projects/{export_project_id}/export/pdf",
        json={
            "formation_ids": export_formation_ids,
            "page_size": "LETTER",
            "show_labels": True
        }
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert "attachment" in response.headers["content-disposition"]
    assert len(response.content) > 0


def test_export_show_pdf_all_formations(client, export_project_id, export_formation_ids):
    """Test exporting all formations as PDF (no specific IDs)."""
    response = client.post(
        f"/api/projects/{export_project_id}/export/pdf",
        json={
            "page_size": "A4",
            "show_labels": False
        }
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert len(response.content) > 0


def test_export_show_pdf_no_formations(client):
    """Test exporting PDF when no formations exist."""
    # Create a project with no formations
    resp = client.post("/api/projects/", json={"name": "Empty Project", "num_dancers": 1})
    assert resp.status_code == 201
    project_id = resp.json()["id"]

    response = client.post(
        f"/api/projects/{project_id}/export/pdf",
        json={"page_size": "LETTER"}
    )
    assert response.status_code == 400
    assert "No formations to export" in response.json()["detail"]


def test_export_all_as_zip(client, export_project_id, export_formation_ids):
    """Test exporting all formations as ZIP."""
    response = client.post(f"/api/projects/{export_project_id}/export/all")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/zip"
    assert "attachment" in response.headers["content-disposition"]

    # Verify ZIP contents
    zip_bytes = io.BytesIO(response.content)
    with ZipFile(zip_bytes) as zf:
        namelist = zf.namelist()
        assert len(namelist) == 2  # Two formations
        # Check that files are named correctly
        for name in namelist:
            assert name.endswith(".png")
            assert "_" in name  # Has index and name


def test_export_all_as_zip_no_formations(client):
    """Test exporting ZIP when no formations exist."""
    resp = client.post("/api/projects/", json={"name": "Empty Project", "num_dancers": 1})
    assert resp.status_code == 201
    project_id = resp.json()["id"]

    response = client.post(f"/api/projects/{project_id}/export/all")
    assert response.status_code == 400
    assert "No formations to export" in response.json()["detail"]