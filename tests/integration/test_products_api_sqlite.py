import pytest


pytestmark = pytest.mark.integration


def test_get_products_returns_database_backed_success_response(
    sqlite_db_client,
):
    response = sqlite_db_client.get("/api/v1/products?limit=2&offset=0")

    assert response.status_code == 200
    payload = response.json()
    assert payload["total"] == 3
    assert payload["limit"] == 2
    assert payload["offset"] == 0
    assert [item["product_id"] for item in payload["items"]] == [101, 102]
    assert payload["items"][0]["performance_score"] == 97.2
    assert payload["items"][0]["performance_segment"] == "Star Product"


def test_get_products_filters_by_aisle_in_success_response(sqlite_db_client):
    response = sqlite_db_client.get("/api/v1/products?aisle=fresh%20vegetables")

    assert response.status_code == 200
    payload = response.json()
    assert payload["total"] == 1
    assert payload["items"][0]["product_id"] == 103
    assert payload["items"][0]["aisle"] == "fresh vegetables"


def test_get_top_products_returns_ranked_database_results(sqlite_db_client):
    response = sqlite_db_client.get("/api/v1/products/top?metric=performance&limit=2")

    assert response.status_code == 200
    payload = response.json()
    assert payload["metric"] == "performance"
    assert [item["rank"] for item in payload["products"]] == [1, 2]
    assert [item["product_id"] for item in payload["products"]] == [101, 102]
    assert [item["score"] for item in payload["products"]] == [97.2, 83.4]


def test_get_product_profile_returns_database_backed_payload(
    sqlite_db_client,
):
    response = sqlite_db_client.get("/api/v1/products/101/profile")

    assert response.status_code == 200
    payload = response.json()
    assert payload["identity"]["product_id"] == 101
    assert payload["identity"]["product_name"] == "Organic Bananas"
    assert payload["facts"]["purchase_count"] == 1200
    assert payload["global_scores"]["performance_score"] == 97.2
    assert payload["segments"]["performance"] == "Star Product"


def test_get_product_profile_returns_404_detail_for_missing_product(
    sqlite_db_client,
):
    response = sqlite_db_client.get("/api/v1/products/999/profile")

    assert response.status_code == 404
    assert response.json() == {"detail": "Product 999 not found"}


def test_get_product_insights_returns_database_backed_payload(
    sqlite_db_client,
):
    response = sqlite_db_client.get("/api/v1/products/101/insights")

    assert response.status_code == 200
    payload = response.json()
    assert payload["product_id"] == 101
    assert payload["insights"] == {
        "primary_strength": "High repeat purchase behavior",
        "primary_weakness": "Limited cross-category reach",
        "recommended_action": "Increase premium placement",
    }


def test_get_product_insights_returns_404_detail_for_missing_product(
    sqlite_db_client,
):
    response = sqlite_db_client.get("/api/v1/products/999/insights")

    assert response.status_code == 404
    assert response.json() == {"detail": "Product 999 not found"}


@pytest.mark.parametrize(
    "path",
    [
        "/api/v1/products?limit=0",
        "/api/v1/products?offset=-1",
        "/api/v1/products/top?metric=health",
        "/api/v1/products/top?metric=performance&limit=101",
        "/api/v1/products/not-an-int/profile",
    ],
)
def test_products_endpoints_return_validation_errors(path, sqlite_db_client):
    response = sqlite_db_client.get(path)

    assert response.status_code == 422
    assert response.json()["detail"]
