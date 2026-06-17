import pytest

from app.repositories.sqlalchemy_product_intelligence_repository import (
    SQLAlchemyProductIntelligenceRepository,
)


pytestmark = pytest.mark.integration


def test_repository_filters_by_performance_segment(db_session):
    repository = SQLAlchemyProductIntelligenceRepository(db=db_session)

    products, total = repository.get_products(
        limit=10,
        offset=0,
        performance_segment="Star Product",
    )

    assert total == 1
    assert products[0].product_id == 101
    assert products[0].health_segment == "Star Product"


def test_repository_filters_by_department_and_paginates(db_session):
    repository = SQLAlchemyProductIntelligenceRepository(db=db_session)

    products, total = repository.get_products(
        limit=1,
        offset=0,
        department="produce",
    )

    assert total == 2
    assert len(products) == 1
    assert products[0].global_health_score >= 72.0


def test_repository_sorts_top_products_by_performance(db_session):
    repository = SQLAlchemyProductIntelligenceRepository(db=db_session)

    products = repository.get_top_products(
        metric="performance",
        limit=2,
    )

    assert [product.product_id for product in products] == [101, 102]
