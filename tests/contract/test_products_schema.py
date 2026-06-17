import pytest


pytestmark = pytest.mark.contract


def test_products_contract_exposes_performance_fields(client):
    response = client.get("/api/v1/products")

    assert response.status_code == 200
    item = response.json()["items"][0]

    assert "performance_score" in item
    assert "performance_segment" in item
    assert "health_score" not in item
    assert "health_segment" not in item


def test_products_openapi_contract_uses_performance_terms(client):
    response = client.get("/openapi.json")

    assert response.status_code == 200
    schema_text = response.text

    assert "performance_score" in schema_text
    assert "performance_segment" in schema_text
    assert "health_score" not in schema_text
    assert "health_segment" not in schema_text
