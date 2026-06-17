import pytest


pytestmark = pytest.mark.integration


def test_get_product_insights_returns_insight_fields(db_client):
    response = db_client.get("/api/v1/products/101/insights")

    assert response.status_code == 200
    payload = response.json()
    assert payload["product_id"] == 101
    assert payload["insights"]["primary_strength"] == ("High repeat purchase behavior")
    assert payload["insights"]["recommended_action"] == ("Increase premium placement")


def test_get_product_insights_returns_404_for_missing_product(db_client):
    response = db_client.get("/api/v1/products/999/insights")

    assert response.status_code == 404
