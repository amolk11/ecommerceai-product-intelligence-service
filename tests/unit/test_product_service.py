import pytest

from app.schemas.requests import RankingMetric

pytestmark = pytest.mark.unit


def test_get_products_maps_warehouse_health_fields_to_performance_contract(
    product_service, repository_mock, sample_product
):

    repository_mock.get_products.return_value = ([sample_product], 1)

    response = product_service.get_products(
        limit=20,
        offset=0,
        department="produce",
        performance_segment="Star Product",
    )

    item = response.items[0]
    assert item.performance_score == sample_product.global_health_score
    assert item.performance_segment == sample_product.health_segment
    assert "health_score" not in item.model_dump()
    assert "health_segment" not in item.model_dump()

    repository_mock.get_products.assert_called_once_with(
        limit=20,
        offset=0,
        department="produce",
        aisle=None,
        performance_segment="Star Product",
    )


def test_get_product_profile_maps_performance_scores_and_segments(
    product_service, repository_mock, sample_product
):

    repository_mock.get_product_profile.return_value = sample_product

    response = product_service.get_product_profile(product_id=101)

    assert response.global_scores.performance_score == 97.2
    assert response.department_scores.performance_score == 91.6
    assert response.segments.performance == "Star Product"
    assert "health_score" not in response.model_dump()["global_scores"]
    assert "health" not in response.model_dump()["segments"]


def test_get_top_products_uses_performance_metric_for_warehouse_score(
    product_service, repository_mock, sample_product
):
    repository_mock.get_top_products.return_value = [sample_product]

    response = product_service.get_top_products(
        metric=RankingMetric.PERFORMANCE,
        limit=10,
    )

    assert response.metric == RankingMetric.PERFORMANCE
    assert response.products[0].score == sample_product.global_health_score
    repository_mock.get_top_products.assert_called_once_with(
        metric="performance",
        limit=10,
    )


def test_get_product_profile_uses_cache_after_first_request(
    product_service, repository_mock, sample_product
):

    repository_mock.get_product_profile.return_value = sample_product

    first_response = product_service.get_product_profile(product_id=101)

    second_response = product_service.get_product_profile(product_id=101)

    assert first_response == second_response

    repository_mock.get_product_profile.assert_called_once_with(product_id=101)
