"""
test_center_time.py — Center-time calculation and rebalance endpoint tests.
"""

import pytest
from utils.geometry import distance
from utils.stage import CENTER_THRESHOLD_RADIUS


# ── Pure geometry unit tests ──────────────────────────────────

def test_distance_formula():
    assert distance(0.0, 0.0, 3.0, 4.0) == 5.0


def test_distance_zero():
    assert distance(2.0, 3.0, 2.0, 3.0) == 0.0


def test_dancer_at_center_within_threshold():
    d = distance(0.0, 0.0, 0.0, 0.0)
    assert d <= CENTER_THRESHOLD_RADIUS


def test_dancer_far_from_center_outside_threshold():
    d = distance(10.0, 10.0, 0.0, 0.0)
    assert d > CENTER_THRESHOLD_RADIUS


def test_dancer_on_threshold_boundary():
    """A dancer exactly at the threshold radius should be counted as center."""
    import math
    # Point exactly on the circle boundary
    x = CENTER_THRESHOLD_RADIUS
    y = 0.0
    d = distance(x, y, 0.0, 0.0)
    assert d <= CENTER_THRESHOLD_RADIUS


# ── HTTP endpoint tests ───────────────────────────────────────

@pytest.fixture(scope="module")
def ct_setup(client):
    """Create project with 3 dancers and 2 formations with known positions."""
    proj = client.post("/api/projects/", json={"name": "CenterTime Project", "num_dancers": 3}).json()
    pid = proj["id"]

    dancers = []
    for i in range(1, 4):
        d = client.post(f"/api/projects/{pid}/dancers/", json={"number": i, "name": f"D{i}"}).json()
        dancers.append(d["id"])

    # Formation 1: dancer 1 at center, others far out
    f1 = client.post(
        f"/api/projects/{pid}/formations/",
        json={"name": "F1", "order_index": 0, "timestamp_start": 0.0, "timestamp_end": 8.0},
    ).json()
    client.put(
        f"/api/projects/{pid}/formations/{f1['id']}/positions/",
        json=[
            {"dancer_id": dancers[0], "x": 0.0, "y": 0.0},   # at center
            {"dancer_id": dancers[1], "x": 15.0, "y": 0.0},  # far right
            {"dancer_id": dancers[2], "x": -15.0, "y": 0.0}, # far left
        ],
    )

    # Formation 2: dancer 2 at center, others far out
    f2 = client.post(
        f"/api/projects/{pid}/formations/",
        json={"name": "F2", "order_index": 1, "timestamp_start": 8.0, "timestamp_end": 16.0},
    ).json()
    client.put(
        f"/api/projects/{pid}/formations/{f2['id']}/positions/",
        json=[
            {"dancer_id": dancers[0], "x": 15.0, "y": 0.0},  # far
            {"dancer_id": dancers[1], "x": 0.0, "y": 0.0},   # at center
            {"dancer_id": dancers[2], "x": -15.0, "y": 0.0}, # far
        ],
    )

    return {"project_id": pid, "dancer_ids": dancers}


def test_center_time_stats_returns_all_dancers(client, ct_setup):
    pid = ct_setup["project_id"]
    response = client.get(f"/api/projects/{pid}/center-time/")
    assert response.status_code == 200
    data = response.json()
    assert data["project_id"] == pid
    assert len(data["dancers"]) == 3
    assert "ideal_percentage" in data


def test_center_time_dancer1_is_over(client, ct_setup):
    """Dancer 1 is center in formation 1 only — 50% of formations."""
    pid = ct_setup["project_id"]
    d1_id = ct_setup["dancer_ids"][0]
    response = client.get(f"/api/projects/{pid}/center-time/")
    dancers = {d["dancer_id"]: d for d in response.json()["dancers"]}
    d1 = dancers[d1_id]
    assert d1["center_formations"] == 1
    assert d1["total_formations"] == 2


def test_center_time_dancer3_never_center(client, ct_setup):
    """Dancer 3 (index 2) is never near center."""
    pid = ct_setup["project_id"]
    d3_id = ct_setup["dancer_ids"][2]
    response = client.get(f"/api/projects/{pid}/center-time/")
    dancers = {d["dancer_id"]: d for d in response.json()["dancers"]}
    d3 = dancers[d3_id]
    assert d3["center_formations"] == 0
    assert d3["status"] == "under"


def test_center_time_single_dancer_endpoint(client, ct_setup):
    pid = ct_setup["project_id"]
    d1_id = ct_setup["dancer_ids"][0]
    response = client.get(f"/api/projects/{pid}/center-time/{d1_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["dancer_id"] == d1_id


def test_center_time_single_dancer_not_found(client, ct_setup):
    pid = ct_setup["project_id"]
    response = client.get(f"/api/projects/{pid}/center-time/999999")
    assert response.status_code == 404


def test_rebalance_returns_before_and_after(client, ct_setup):
    pid = ct_setup["project_id"]
    response = client.post(
        f"/api/projects/{pid}/center-time/rebalance",
        json={"tolerance": 5.0},
    )
    assert response.status_code == 200
    data = response.json()
    assert "before" in data
    assert "after" in data
    assert "adjusted_formations" in data
    assert isinstance(data["adjusted_formations"], int)
