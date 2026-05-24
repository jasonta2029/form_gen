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


def test_duplicate_formation(client, project_id, dancer_ids):
    """Test duplicating a formation with all its positions."""
    # Create a formation with positions
    form_resp = client.post(
        f"/api/projects/{project_id}/formations/",
        json={"name": "Original Formation", "order_index": 0}
    )
    assert form_resp.status_code == 201
    formation = form_resp.json()
    fid = formation["id"]

    # Add positions to the formation
    positions = [
        {"dancer_id": dancer_ids[0], "x": 0.0, "y": 0.0},
        {"dancer_id": dancer_ids[1], "x": 5.0, "y": 0.0},
    ]
    pos_resp = client.put(
        f"/api/projects/{project_id}/formations/{fid}/positions/",
        json=positions
    )
    assert pos_resp.status_code == 200

    # Duplicate the formation
    dup_resp = client.post(
        f"/api/projects/{project_id}/formations/{fid}/duplicate"
    )
    assert dup_resp.status_code == 201
    duplicate = dup_resp.json()

    # Verify duplicate properties
    assert duplicate["name"] == "Original Formation (Copy)"
    assert duplicate["order_index"] == 1  # Should be after original
    assert duplicate["timestamp_start"] == formation["timestamp_start"]
    assert duplicate["timestamp_end"] == formation["timestamp_end"]
    assert duplicate["id"] != fid  # Different ID

    # Verify positions were duplicated
    dup_positions_resp = client.get(
        f"/api/projects/{project_id}/formations/{duplicate['id']}/positions/"
    )
    assert dup_positions_resp.status_code == 200
    dup_positions = dup_positions_resp.json()
    assert len(dup_positions) == 2

    # Check that positions match original
    dup_xs = {p["dancer_id"]: p["x"] for p in dup_positions}
    assert dup_xs[dancer_ids[0]] == 0.0
    assert dup_xs[dancer_ids[1]] == 5.0


def test_reorder_formations(client, project_id):
    """Test reordering formations."""
    # Create three formations
    formation_ids = []
    for i in range(3):
        resp = client.post(
            f"/api/projects/{project_id}/formations/",
            json={"name": f"Formation {i}", "order_index": i}
        )
        assert resp.status_code == 201
        formation_ids.append(resp.json()["id"])

    # Verify initial order
    resp = client.get(f"/api/projects/{project_id}/formations/")
    assert resp.status_code == 200
    formations = resp.json()
    assert len(formations) == 3
    assert [f["id"] for f in formations] == formation_ids
    assert [f["order_index"] for f in formations] == [0, 1, 2]

    # Reorder: put formation 2 first, then 0, then 1
    new_order = [formation_ids[2], formation_ids[0], formation_ids[1]]
    resp = client.put(
        f"/api/projects/{project_id}/formations/reorder",
        json={"formation_ids": new_order}
    )
    assert resp.status_code == 200
    reordered = resp.json()

    # Verify new order
    assert len(reordered) == 3
    assert [f["id"] for f in reordered] == new_order
    assert [f["order_index"] for f in reordered] == [0, 1, 2]

    # Verify persistence by getting formations again
    resp = client.get(f"/api/projects/{project_id}/formations/")
    assert resp.status_code == 200
    formations = resp.json()
    assert [f["id"] for f in formations] == new_order
    assert [f["order_index"] for f in formations] == [0, 1, 2]


def test_reorder_formations_invalid_id(client, project_id):
    """Test reordering with invalid formation ID."""
    # Create one formation
    resp = client.post(
        f"/api/projects/{project_id}/formations/",
        json={"name": "Formation 0", "order_index": 0}
    )
    assert resp.status_code == 201
    formation = resp.json()
    fid = formation["id"]

    # Try to reorder with invalid ID
    resp = client.put(
        f"/api/projects/{project_id}/formations/reorder",
        json={"formation_ids": [fid, 999999]}  # 999999 doesn't exist
    )
    assert resp.status_code == 400
    assert "not found in project" in resp.json()["detail"]
