import pytest

from app.repositories.sqlalchemy_product_intelligence_repository import (
    SQLAlchemyProductIntelligenceRepository,
)


pytestmark = pytest.mark.integration


@pytest.fixture
def repository(sqlite_db_session):
    return SQLAlchemyProductIntelligenceRepository(db=sqlite_db_session)


def test_repository_get_product_profile_returns_existing_product(repository):
    product = repository.get_product_profile(product_id=101)

    assert product is not None
    assert product.product_id == 101
    assert product.product_name == "Organic Bananas"
    assert product.department == "produce"
    assert product.health_segment == "Star Product"


def test_repository_get_product_profile_returns_none_for_missing_product(
    repository,
):
    product = repository.get_product_profile(product_id=999)

    assert product is None


def test_repository_get_product_insights_returns_existing_product(repository):
    product = repository.get_product_insights(product_id=101)

    assert product is not None
    assert product.product_id == 101
    assert product.primary_strength == "High repeat purchase behavior"
    assert product.recommended_action == "Increase premium placement"


def test_repository_get_product_insights_returns_none_for_missing_product(
    repository,
):
    product = repository.get_product_insights(product_id=999)

    assert product is None


def test_repository_get_products_without_filters_returns_total_and_sorted_rows(
    repository,
):
    products, total = repository.get_products(limit=10, offset=0)

    assert total == 3
    assert [product.product_id for product in products] == [101, 102, 103]
    assert [product.global_health_score for product in products] == sorted(
        [product.global_health_score for product in products],
        reverse=True,
    )


def test_repository_get_products_filters_by_department(repository):
    products, total = repository.get_products(
        limit=10,
        offset=0,
        department="produce",
    )

    assert total == 2
    assert [product.product_id for product in products] == [101, 103]
    assert {product.department for product in products} == {"produce"}


def test_repository_get_products_filters_by_aisle(repository):
    products, total = repository.get_products(
        limit=10,
        offset=0,
        aisle="fresh vegetables",
    )

    assert total == 1
    assert products[0].product_id == 103
    assert products[0].aisle == "fresh vegetables"


def test_repository_get_products_filters_by_performance_segment(repository):
    products, total = repository.get_products(
        limit=10,
        offset=0,
        performance_segment="Star Product",
    )

    assert total == 1
    assert products[0].product_id == 101
    assert products[0].health_segment == "Star Product"


def test_repository_get_products_applies_all_filters_together(repository):
    products, total = repository.get_products(
        limit=10,
        offset=0,
        department="produce",
        aisle="fresh fruits",
        performance_segment="Star Product",
    )

    assert total == 1
    assert products[0].product_id == 101
    assert products[0].department == "produce"
    assert products[0].aisle == "fresh fruits"
    assert products[0].health_segment == "Star Product"


def test_repository_get_products_paginates_without_changing_total(repository):
    products, total = repository.get_products(limit=1, offset=1)

    assert total == 3
    assert len(products) == 1
    assert products[0].product_id == 102


def test_repository_get_top_products_returns_valid_metric_results(repository):
    products = repository.get_top_products(metric="performance", limit=2)

    assert [product.product_id for product in products] == [101, 102]
    assert [product.global_health_score for product in products] == [97.2, 83.4]


def test_repository_get_top_products_raises_for_invalid_metric(repository):
    with pytest.raises(ValueError, match="Unsupported metric: health"):
        repository.get_top_products(metric="health", limit=2)
