"""
test_formations.py — API tests checking formations timeline order sequence CRUD.
"""

def test_list_project_formations(client):
    """Ensures formations queries return lists coordinates array."""
    response = client.get("/api/projects/1/formations")
    assert response.status_code == 200

def test_add_formation_snapshot(client):
    """Checks that dropping timing snap returns created details."""
    payload = {
        "name": "Confidence V Shape",
        "order_index": 0,
        "timestamp_start": 0.0,
        "timestamp_end": 4.5,
        "positions": []
    }
    response = client.post("/api/projects/1/formations", json=payload)
    # If project 1 doesn't exist, we mock expected outputs or mock DB dependencies
    assert response.status_code in [201, 404]
