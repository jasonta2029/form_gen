"""
test_formations.py — Formation and position endpoint tests.
"""

import pytest


@pytest.fixture(scope="module")
def project_id(client):
    """Create a shared project for formation tests."""
    resp = client.post("/api/projects/", json={"name": "Formation Test Project", "num_dancers": 4})
    assert resp.status_code == 201
    return resp.json()["id"]


@pytest.fixture(scope="module")
def dancer_ids(client, project_id):
    """Create 4 dancers in the project."""
    ids = []
    for i in range(1, 5):
        resp = client.post(
            f"/api/projects/{project_id}/dancers/",
            json={"number": i, "name": f"Dancer {i}"},
        )
        assert resp.status_code == 201
        ids.append(resp.json()["id"])
    return ids


def test_list_formations_empty(client, project_id):
    response = client.get(f"/api/projects/{project_id}/formations/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_formation(client, project_id):
    payload = {"name": "Intro", "order_index": 0, "timestamp_start": 0.0, "timestamp_end": 8.0}
    response = client.post(f"/api/projects/{project_id}/formations/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Intro"
    assert data["order_index"] == 0
    assert data["timestamp_start"] == 0.0


def test_list_formations_after_create(client, project_id):
    client.post(f"/api/projects/{project_id}/formations/", json={"name": "Verse", "order_index": 1})
    response = client.get(f"/api/projects/{project_id}/formations/")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_update_formation(client, project_id):
    create = client.post(
        f"/api/projects/{project_id}/formations/",
        json={"name": "Original", "order_index": 5},
    )
    fid = create.json()["id"]

    response = client.put(
        f"/api/projects/{project_id}/formations/{fid}",
        json={"name": "Renamed"},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Renamed"


def test_delete_formation(client, project_id):
    create = client.post(
        f"/api/projects/{project_id}/formations/",
        json={"name": "Temporary", "order_index": 99},
    )
    fid = create.json()["id"]
    assert client.delete(f"/api/projects/{project_id}/formations/{fid}").status_code == 204


def test_batch_set_positions(client, project_id, dancer_ids):
    form = client.post(
        f"/api/projects/{project_id}/formations/",
        json={"name": "Position Test", "order_index": 10},
    ).json()
    fid = form["id"]

    positions = [
        {"dancer_id": dancer_ids[0], "x": 0.0, "y": 0.0},
        {"dancer_id": dancer_ids[1], "x": 5.0, "y": 0.0},
        {"dancer_id": dancer_ids[2], "x": -5.0, "y": 0.0},
        {"dancer_id": dancer_ids[3], "x": 0.0, "y": 5.0},
    ]
    response = client.put(
        f"/api/projects/{project_id}/formations/{fid}/positions/", json=positions
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 4
    xs = {p["dancer_id"]: p["x"] for p in data}
    assert xs[dancer_ids[1]] == 5.0


def test_positions_idempotent_replace(client, project_id, dancer_ids):
    """PUT positions should replace all existing positions cleanly."""
    form = client.post(
        f"/api/projects/{project_id}/formations/",
        json={"name": "Idempotent Test", "order_index": 20},
    ).json()
    fid = form["id"]

    first = [{"dancer_id": dancer_ids[0], "x": 1.0, "y": 1.0}]
    client.put(f"/api/projects/{project_id}/formations/{fid}/positions/", json=first)

    second = [{"dancer_id": dancer_ids[1], "x": 9.0, "y": 9.0}]
    response = client.put(
        f"/api/projects/{project_id}/formations/{fid}/positions/", json=second
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["dancer_id"] == dancer_ids[1]


def test_formation_not_found(client, project_id):
    assert client.get(f"/api/projects/{project_id}/formations/999999").status_code == 404
