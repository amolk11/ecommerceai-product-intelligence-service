from app.dependencies.product_intelligence import (
    get_product_intelligence_repository,
    get_product_intelligence_service,
)
from app.repositories.sqlalchemy_product_intelligence_repository import (
    SQLAlchemyProductIntelligenceRepository,
)
from app.services.product_intelligence_service import ProductIntelligenceService


def test_get_product_intelligence_repository_builds_sqlalchemy_repository():
    db_session = object()

    repository = get_product_intelligence_repository(db=db_session)

    assert isinstance(repository, SQLAlchemyProductIntelligenceRepository)
    assert repository.db is db_session


def test_get_product_intelligence_service_uses_injected_repository():
    repository = object()

    service = get_product_intelligence_service(repository=repository)

    assert isinstance(service, ProductIntelligenceService)
    assert service.repository is repository
