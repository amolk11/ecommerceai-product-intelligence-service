import pytest


pytestmark = pytest.mark.e2e


def test_product_listing_flow_returns_ranked_business_performance(db_client):
    response = db_client.get("/api/v1/products?limit=2")

    assert response.status_code == 200
    payload = response.json()
    assert payload["total"] == 3
    assert len(payload["items"]) == 2
    assert payload["items"][0]["performance_score"] >= (
        payload["items"][1]["performance_score"]
    )
