import pytest


pytestmark = pytest.mark.e2e


def test_top_products_flow_returns_ranked_products(db_client):
    response = db_client.get(
        "/api/v1/products/top?metric=performance&limit=3"
    )

    assert response.status_code == 200
    payload = response.json()
    scores = [item["score"] for item in payload["products"]]

    assert payload["metric"] == "performance"
    assert scores == sorted(scores, reverse=True)
