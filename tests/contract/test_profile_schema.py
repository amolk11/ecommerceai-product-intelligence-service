import pytest


pytestmark = pytest.mark.contract


def test_profile_contract_exposes_performance_shape(client):
    response = client.get("/api/v1/products/101/profile")

    assert response.status_code == 200
    payload = response.json()

    assert "performance_score" in payload["global_scores"]
    assert "performance_score" in payload["department_scores"]
    assert "performance" in payload["segments"]
    assert "health_score" not in payload["global_scores"]
    assert "health" not in payload["segments"]


def test_profile_contract_contains_expected_sections(client):
    response = client.get("/api/v1/products/101/profile")

    assert response.status_code == 200
    assert set(response.json()) == {
        "identity",
        "facts",
        "global_scores",
        "department_scores",
        "segments",
        "insights",
    }
