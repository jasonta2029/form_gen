"""
test_projects.py — Project CRUD endpoint tests.
"""


def test_list_projects_empty(client):
    response = client.get("/api/projects/")
    assert response.status_code == 200
    body = response.json()
    assert "projects" in body
    assert isinstance(body["projects"], list)
    assert "total" in body


def test_create_project(client):
    payload = {"name": "Spring Showcase", "description": "21 dancers", "num_dancers": 21}
    response = client.post("/api/projects/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Spring Showcase"
    assert data["num_dancers"] == 21
    assert "id" in data
    assert "created_at" in data


def test_get_project_detail(client):
    create = client.post("/api/projects/", json={"name": "Detail Test", "num_dancers": 4})
    project_id = create.json()["id"]

    response = client.get(f"/api/projects/{project_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == project_id
    assert "dancers" in data
    assert "formations" in data


def test_get_project_not_found(client):
    response = client.get("/api/projects/999999")
    assert response.status_code == 404


def test_update_project(client):
    create = client.post("/api/projects/", json={"name": "Old Name", "num_dancers": 5})
    project_id = create.json()["id"]

    response = client.put(f"/api/projects/{project_id}", json={"name": "New Name"})
    assert response.status_code == 200
    assert response.json()["name"] == "New Name"


def test_delete_project(client):
    create = client.post("/api/projects/", json={"name": "To Delete", "num_dancers": 3})
    project_id = create.json()["id"]

    delete = client.delete(f"/api/projects/{project_id}")
    assert delete.status_code == 204

    get = client.get(f"/api/projects/{project_id}")
    assert get.status_code == 404


def test_create_project_validates_num_dancers(client):
    response = client.post("/api/projects/", json={"name": "Bad", "num_dancers": 0})
    assert response.status_code == 422

    response = client.post("/api/projects/", json={"name": "Bad", "num_dancers": 201})
    assert response.status_code == 422


def test_create_project_requires_name(client):
    response = client.post("/api/projects/", json={"num_dancers": 5})
    assert response.status_code == 422
