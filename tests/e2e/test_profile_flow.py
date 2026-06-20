import pytest


pytestmark = pytest.mark.e2e


def test_product_profile_flow_returns_complete_profile(db_client):
    response = db_client.get("/api/v1/products/101/profile")

    assert response.status_code == 200
    payload = response.json()
    assert payload["identity"]["product_id"] == 101
    assert payload["global_scores"]["performance_score"] == 97.2
