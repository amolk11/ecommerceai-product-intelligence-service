import pytest

from app.schemas.requests import RankingMetric

pytestmark = pytest.mark.unit


def test_performance_metric_replaces_public_health_metric():
    values = {metric.value for metric in RankingMetric}

    assert "performance" in values
    assert "health" not in values


def test_performance_segment_is_translated_from_internal_warehouse_segment(
    product_service,
    repository_mock,
    sample_product,
):
    repository_mock.get_product_profile.return_value = sample_product

    profile = product_service.get_product_profile(product_id=101)

    assert profile.segments.performance == sample_product.health_segment
