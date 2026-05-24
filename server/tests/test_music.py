"""
test_music.py — Music marker CRUD endpoint tests.
"""

import pytest


@pytest.fixture(scope="module")
def project_id(client):
    resp = client.post("/api/projects/", json={"name": "Music Test Project", "num_dancers": 4})
    return resp.json()["id"]


def test_list_markers_empty(client, project_id):
    response = client.get(f"/api/projects/{project_id}/music/markers")
    assert response.status_code == 200
    assert response.json() == []


def test_create_marker(client, project_id):
    response = client.post(
        f"/api/projects/{project_id}/music/markers",
        json={"name": "Drop", "timestamp": 32.5},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Drop"
    assert data["timestamp"] == 32.5
    assert data["project_id"] == project_id
    assert data["formation_id"] is None


def test_create_marker_linked_to_formation(client, project_id):
    form = client.post(
        f"/api/projects/{project_id}/formations/",
        json={"name": "Chorus", "order_index": 0},
    ).json()
    fid = form["id"]

    response = client.post(
        f"/api/projects/{project_id}/music/markers",
        json={"name": "Chorus Start", "timestamp": 64.0, "formation_id": fid},
    )
    assert response.status_code == 201
    assert response.json()["formation_id"] == fid


def test_list_markers_ordered_by_timestamp(client, project_id):
    client.post(f"/api/projects/{project_id}/music/markers", json={"name": "Late", "timestamp": 120.0})
    client.post(f"/api/projects/{project_id}/music/markers", json={"name": "Early", "timestamp": 5.0})

    response = client.get(f"/api/projects/{project_id}/music/markers")
    timestamps = [m["timestamp"] for m in response.json()]
    assert timestamps == sorted(timestamps)


def test_update_marker(client, project_id):
    create = client.post(
        f"/api/projects/{project_id}/music/markers",
        json={"name": "Old", "timestamp": 10.0},
    )
    marker_id = create.json()["id"]

    response = client.put(
        f"/api/projects/{project_id}/music/markers/{marker_id}",
        json={"name": "Updated", "timestamp": 15.0},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated"
    assert data["timestamp"] == 15.0


def test_delete_marker(client, project_id):
    create = client.post(
        f"/api/projects/{project_id}/music/markers",
        json={"name": "Delete Me", "timestamp": 99.0},
    )
    marker_id = create.json()["id"]

    assert client.delete(f"/api/projects/{project_id}/music/markers/{marker_id}").status_code == 204

    markers = client.get(f"/api/projects/{project_id}/music/markers").json()
    ids = [m["id"] for m in markers]
    assert marker_id not in ids


def test_marker_not_found(client, project_id):
    assert client.put(
        f"/api/projects/{project_id}/music/markers/999999",
        json={"name": "Ghost"},
    ).status_code == 404


def test_marker_negative_timestamp_rejected(client, project_id):
    response = client.post(
        f"/api/projects/{project_id}/music/markers",
        json={"name": "Bad", "timestamp": -1.0},
    )
    assert response.status_code == 422
