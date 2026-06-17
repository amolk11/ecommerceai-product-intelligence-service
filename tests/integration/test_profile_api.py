import pytest


pytestmark = pytest.mark.integration


def test_get_product_profile_returns_performance_schema(db_client):
    response = db_client.get("/api/v1/products/101/profile")

    assert response.status_code == 200
    payload = response.json()
    assert payload["global_scores"]["performance_score"] == 97.2
    assert payload["department_scores"]["performance_score"] == 91.6
    assert payload["segments"]["performance"] == "Star Product"
    assert "health_score" not in payload["global_scores"]
    assert "health" not in payload["segments"]


def test_get_product_profile_returns_404_for_missing_product(db_client):
    response = db_client.get("/api/v1/products/999/profile")

    assert response.status_code == 404
