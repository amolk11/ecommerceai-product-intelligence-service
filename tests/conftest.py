import os
from collections.abc import Generator
from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import get_session
from app.dependencies.product_intelligence import (
    get_product_intelligence_service,
)
from app.main import app
from app.models.base import Base
from app.schemas.requests import RankingMetric
from app.schemas.responses import (
    ProductInsights,
    ProductInsightsResponse,
    ProductListItem,
    ProductListResponse,
    ProductProfileResponse,
    TopProductItem,
    TopProductsResponse,
)
from app.services.product_intelligence_service import (
    ProductIntelligenceService,
)
from tests.fixtures.database import prepare_database
from tests.fixtures.database import seed_products
from tests.fixtures.products import product_record


@pytest.fixture
def repository_mock() -> Mock:
    return Mock()


@pytest.fixture
def product_service(repository_mock: Mock) -> ProductIntelligenceService:
    return ProductIntelligenceService(repository=repository_mock)


@pytest.fixture
def sample_product():
    return product_record()


@pytest.fixture
def mock_product_service() -> Mock:
    service = Mock(spec=ProductIntelligenceService)
    service.get_products.return_value = ProductListResponse(
        items=[
            ProductListItem(
                product_id=101,
                product_name="Organic Bananas",
                department="produce",
                aisle="fresh fruits",
                performance_score=97.2,
                performance_segment="Star Product",
            )
        ],
        total=1,
        limit=20,
        offset=0,
    )
    service.get_product_profile.return_value = ProductProfileResponse(
        identity={
            "product_id": 101,
            "product_name": "Organic Bananas",
            "department": "produce",
            "aisle": "fresh fruits",
        },
        facts={
            "purchase_count": 1200,
            "unique_customers": 820,
            "unique_orders": 1040,
            "relationship_count": 310,
            "avg_confidence": 0.87,
        },
        global_scores={
            "popularity_score": 98.1,
            "loyalty_score": 91.4,
            "reach_score": 88.2,
            "basket_influence_score": 93.7,
            "purchase_intent_score": 95.5,
            "performance_score": 97.2,
        },
        department_scores={
            "popularity_score": 96.2,
            "loyalty_score": 90.1,
            "reach_score": 84.5,
            "basket_influence_score": 92.3,
            "purchase_intent_score": 94.4,
            "performance_score": 91.6,
        },
        segments={
            "popularity": "High Demand",
            "loyalty": "Repeat Driver",
            "reach": "Broad Reach",
            "basket_influence": "Basket Builder",
            "purchase_intent": "High Intent",
            "performance": "Star Product",
        },
        insights={
            "primary_strength": "High repeat purchase behavior",
            "primary_weakness": "Limited cross-category reach",
            "recommended_action": "Increase premium placement",
        },
    )
    service.get_product_insights.return_value = ProductInsightsResponse(
        product_id=101,
        insights=ProductInsights(
            primary_strength="High repeat purchase behavior",
            primary_weakness="Limited cross-category reach",
            recommended_action="Increase premium placement",
        ),
    )
    service.get_top_products.return_value = TopProductsResponse(
        metric=RankingMetric.PERFORMANCE,
        products=[
            TopProductItem(
                rank=1,
                product_id=101,
                product_name="Organic Bananas",
                score=97.2,
            )
        ],
    )
    return service


@pytest.fixture
def client(mock_product_service: Mock) -> Generator[TestClient, None, None]:
    app.dependency_overrides[get_product_intelligence_service] = (
        lambda: mock_product_service
    )

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture(scope="session")
def test_engine():
    test_db_url = os.getenv("TEST_DB_URL")

    if not test_db_url:
        pytest.skip("TEST_DB_URL is required for database-backed tests")

    engine = create_engine(test_db_url, pool_pre_ping=True)
    prepare_database(engine)
    yield engine
    engine.dispose()


@pytest.fixture
def db_session(test_engine):
    session_factory = sessionmaker(
        bind=test_engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )

    session = session_factory()
    seed_products(session)

    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def db_client(db_session) -> Generator[TestClient, None, None]:
    def override_get_session():
        yield db_session

    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture(scope="session")
def sqlite_test_engine():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    @event.listens_for(engine, "connect")
    def attach_serving_schema(dbapi_connection, _connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("ATTACH DATABASE ':memory:' AS serving")
        cursor.close()

    Base.metadata.create_all(bind=engine)
    yield engine
    engine.dispose()


@pytest.fixture
def sqlite_db_session(sqlite_test_engine):
    session_factory = sessionmaker(
        bind=sqlite_test_engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )

    session = session_factory()
    seed_products(session)

    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def sqlite_db_client(sqlite_db_session) -> Generator[TestClient, None, None]:
    def override_get_session():
        yield sqlite_db_session

    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
