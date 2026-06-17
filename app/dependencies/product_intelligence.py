from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.core.logger import get_logger

from app.repositories.interfaces.product_intelligence_repository import (
    ProductIntelligenceRepository,
)

from app.repositories.sqlalchemy_product_intelligence_repository import (
    SQLAlchemyProductIntelligenceRepository,
)

from app.services.product_intelligence_service import (
    ProductIntelligenceService,
)


logger = get_logger(
    log_name="product_intelligence",
    log_folder="dependencies",
)


def get_product_intelligence_repository(
    db: Session = Depends(get_session),
) -> ProductIntelligenceRepository:

    logger.debug("Creating product intelligence repository")

    return SQLAlchemyProductIntelligenceRepository(
        db=db,
    )


def get_product_intelligence_service(
    repository: ProductIntelligenceRepository = Depends(
        get_product_intelligence_repository
    ),
) -> ProductIntelligenceService:

    logger.debug("Creating product intelligence service")

    return ProductIntelligenceService(
        repository=repository,
    )
