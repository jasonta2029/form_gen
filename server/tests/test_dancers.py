"""
test_dancers.py — Dancer CRUD endpoint tests.
"""

import pytest


@pytest.fixture(scope="module")
def project_id(client):
    resp = client.post("/api/projects/", json={"name": "Dancer Test Project", "num_dancers": 10})
    return resp.json()["id"]


def test_list_dancers_empty(client, project_id):
    response = client.get(f"/api/projects/{project_id}/dancers/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_add_dancer(client, project_id):
    response = client.post(
        f"/api/projects/{project_id}/dancers/",
        json={"number": 1, "name": "Alice", "color": "#FF5733"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Alice"
    assert data["number"] == 1
    assert data["color"] == "#FF5733"
    assert data["project_id"] == project_id


def test_add_dancer_minimal(client, project_id):
    """Should work with only required field (number)."""
    response = client.post(
        f"/api/projects/{project_id}/dancers/",
        json={"number": 2},
    )
    assert response.status_code == 201
    assert response.json()["number"] == 2


def test_list_dancers_after_add(client, project_id):
    response = client.get(f"/api/projects/{project_id}/dancers/")
    assert response.status_code == 200
    assert len(response.json()) >= 2


def test_get_dancer(client, project_id):
    create = client.post(
        f"/api/projects/{project_id}/dancers/",
        json={"number": 5, "name": "Bob"},
    )
    dancer_id = create.json()["id"]
    response = client.get(f"/api/projects/{project_id}/dancers/{dancer_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Bob"


def test_update_dancer(client, project_id):
    create = client.post(
        f"/api/projects/{project_id}/dancers/",
        json={"number": 7, "name": "Old Name"},
    )
    dancer_id = create.json()["id"]

    response = client.put(
        f"/api/projects/{project_id}/dancers/{dancer_id}",
        json={"name": "New Name", "color": "#10B981"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "New Name"
    assert data["color"] == "#10B981"


def test_delete_dancer(client, project_id):
    create = client.post(
        f"/api/projects/{project_id}/dancers/",
        json={"number": 9, "name": "Temporary"},
    )
    dancer_id = create.json()["id"]

    assert client.delete(f"/api/projects/{project_id}/dancers/{dancer_id}").status_code == 204
    assert client.get(f"/api/projects/{project_id}/dancers/{dancer_id}").status_code == 404


def test_dancer_invalid_color(client, project_id):
    response = client.post(
        f"/api/projects/{project_id}/dancers/",
        json={"number": 10, "color": "not-a-hex"},
    )
    assert response.status_code == 422


def test_dancer_not_found(client, project_id):
    assert client.get(f"/api/projects/{project_id}/dancers/999999").status_code == 404


def test_dancer_belongs_to_correct_project(client):
    """Dancer from project A should not be visible under project B."""
    proj_a = client.post("/api/projects/", json={"name": "Project A", "num_dancers": 1}).json()["id"]
    proj_b = client.post("/api/projects/", json={"name": "Project B", "num_dancers": 1}).json()["id"]

    dancer = client.post(f"/api/projects/{proj_a}/dancers/", json={"number": 1, "name": "Cross"}).json()
    dancer_id = dancer["id"]

    assert client.get(f"/api/projects/{proj_b}/dancers/{dancer_id}").status_code == 404
