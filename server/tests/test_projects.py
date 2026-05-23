"""
test_projects.py — REST API validation tests checking project addition and edit methods.
"""

def test_list_all_projects_endpoint(client):
    """Checks that projects API returns a lists array of registered shows."""
    response = client.get("/api/projects")
    assert response.status_code == 200
    assert "projects" in response.json()

def test_create_new_project_endpoint(client):
    """Verifies creating project details satisfies boundary contracts."""
    payload = {
        "name": "Confidence Tour Showcase",
        "description": "Choreographies with 21 dancers",
        "num_dancers": 21
    }
    response = client.post("/api/projects", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Confidence Tour Showcase"
    assert data["num_dancers"] == 21
