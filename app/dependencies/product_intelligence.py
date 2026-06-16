from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_session

from app.repositories.interfaces.product_intelligence_repository import (
    ProductIntelligenceRepository,
)

from app.repositories.sqlalchemy_product_intelligence_repository import (
    SQLAlchemyProductIntelligenceRepository,
)

from app.services.product_intelligence_service import (
    ProductIntelligenceService,
)


def get_product_intelligence_repository(
    db: Session = Depends(get_session),
) -> ProductIntelligenceRepository:

    return SQLAlchemyProductIntelligenceRepository(
        db=db,
    )


def get_product_intelligence_service(
    repository: ProductIntelligenceRepository = Depends(
        get_product_intelligence_repository
    ),
) -> ProductIntelligenceService:

    return ProductIntelligenceService(
        repository=repository,
    )
    