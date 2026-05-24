"""
test_ai.py — AI service unit tests and template endpoint tests.
"""

import pytest
from services.ai_service import AIService


# ── Pure unit tests (no DB, no HTTP) ─────────────────────────

class TestTemplateShapes:
    def setup_method(self):
        self.service = AIService()

    def test_v_shape_count(self):
        pos = self.service.apply_template("V_SHAPE", 12)
        assert len(pos) == 12

    def test_v_shape_lead_at_center(self):
        pos = self.service.apply_template("V_SHAPE", 6)
        assert pos[0]["x"] == 0.0

    def test_arc_count(self):
        pos = self.service.apply_template("ARC", 8)
        assert len(pos) == 8

    def test_circle_count(self):
        pos = self.service.apply_template("CIRCLE", 10)
        assert len(pos) == 10

    def test_split_count(self):
        pos = self.service.apply_template("SPLIT", 7)
        assert len(pos) == 7

    def test_line_count(self):
        pos = self.service.apply_template("LINE", 5)
        assert len(pos) == 5

    def test_diagonal_count(self):
        pos = self.service.apply_template("DIAGONAL", 9)
        assert len(pos) == 9

    def test_diamond_count(self):
        pos = self.service.apply_template("DIAMOND", 8)
        assert len(pos) == 8

    def test_cluster_count(self):
        pos = self.service.apply_template("CLUSTER", 6)
        assert len(pos) == 6

    def test_positions_within_stage_bounds(self):
        """All generated positions must stay within [-25,25] x [-15,15]."""
        for shape in ["V_SHAPE", "ARC", "CIRCLE", "SPLIT", "LINE", "DIAGONAL", "DIAMOND", "CLUSTER"]:
            pos = self.service.apply_template(shape, 12)
            for p in pos:
                assert -25.0 <= p["x"] <= 25.0, f"{shape}: x={p['x']} out of bounds"
                assert -15.0 <= p["y"] <= 15.0, f"{shape}: y={p['y']} out of bounds"

    def test_dancer_ids_sequential(self):
        pos = self.service.apply_template("CIRCLE", 6)
        ids = [p["dancer_id"] for p in pos]
        assert ids == list(range(1, 7))

    def test_scale_expands_positions(self):
        pos_1x = self.service.apply_template("CIRCLE", 6, scale=1.0)
        pos_2x = self.service.apply_template("CIRCLE", 6, scale=2.0)
        import math
        dist_1x = math.sqrt(pos_1x[0]["x"] ** 2 + pos_1x[0]["y"] ** 2)
        dist_2x = math.sqrt(pos_2x[0]["x"] ** 2 + pos_2x[0]["y"] ** 2)
        assert dist_2x > dist_1x

    def test_rotation_changes_positions(self):
        pos_0 = self.service.apply_template("LINE", 4, rotation_deg=0)
        pos_90 = self.service.apply_template("LINE", 4, rotation_deg=90)
        assert pos_0[0]["x"] != pytest.approx(pos_90[0]["x"], abs=0.1)

    def test_unknown_shape_falls_back_to_circle(self):
        pos = self.service.apply_template("UNKNOWN_SHAPE", 6)
        assert len(pos) == 6


# ── HTTP endpoint tests ───────────────────────────────────────

@pytest.fixture(scope="module")
def ai_project_id(client):
    resp = client.post("/api/projects/", json={"name": "AI Test Project", "num_dancers": 8})
    return resp.json()["id"]


def test_template_endpoint_v_shape(client, ai_project_id):
    response = client.post(
        f"/api/projects/{ai_project_id}/ai/template",
        json={"shape": "V_SHAPE", "num_dancers": 8, "scale": 1.0, "rotation_deg": 0},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 8
    assert "x" in data[0] and "y" in data[0]


def test_template_endpoint_all_shapes(client, ai_project_id):
    shapes = ["V_SHAPE", "ARC", "CIRCLE", "SPLIT", "LINE", "DIAGONAL", "DIAMOND", "CLUSTER"]
    for shape in shapes:
        response = client.post(
            f"/api/projects/{ai_project_id}/ai/template",
            json={"shape": shape, "num_dancers": 6, "scale": 1.0, "rotation_deg": 0},
        )
        assert response.status_code == 200, f"{shape} failed"
        assert len(response.json()) == 6


def test_generate_formation_endpoint_fallback(client, ai_project_id):
    """Without a real OpenAI key, should fall back to geometric and return 200."""
    response = client.post(
        f"/api/projects/{ai_project_id}/ai/generate",
        json={"prompt": "V shape with leads in front", "num_dancers": 6},
    )
    assert response.status_code == 200
    data = response.json()
    assert "positions" in data
    assert "reasoning" in data
