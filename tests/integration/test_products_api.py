import pytest


pytestmark = pytest.mark.integration


def test_get_products_returns_performance_contract(db_client):
    response = db_client.get("/api/v1/products")

    assert response.status_code == 200
    payload = response.json()
    assert payload["total"] == 3
    assert payload["items"][0]["performance_score"] == 97.2
    assert payload["items"][0]["performance_segment"] == "Star Product"
    assert "health_score" not in payload["items"][0]
    assert "health_segment" not in payload["items"][0]


def test_get_products_filters_by_department(db_client):
    response = db_client.get("/api/v1/products?department=produce")

    assert response.status_code == 200
    payload = response.json()
    assert payload["total"] == 2
    assert all(item["department"] == "produce" for item in payload["items"])


def test_get_products_filters_by_performance_segment(db_client):
    response = db_client.get("/api/v1/products?performance_segment=Star Product")

    assert response.status_code == 200
    payload = response.json()
    assert payload["total"] == 1
    assert payload["items"][0]["performance_segment"] == "Star Product"


def test_get_top_products_uses_performance_metric(db_client):
    response = db_client.get("/api/v1/products/top?metric=performance&limit=2")

    assert response.status_code == 200
    payload = response.json()
    assert payload["metric"] == "performance"
    assert [item["product_id"] for item in payload["products"]] == [101, 102]
