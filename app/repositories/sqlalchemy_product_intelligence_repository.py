from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.logger import get_logger
from app.models.product_intelligence import (
    ProductIntelligence,
)

from app.repositories.interfaces.product_intelligence_repository import (
    ProductIntelligenceRepository,
)


METRIC_COLUMN_MAP = {
    "popularity": ProductIntelligence.global_popularity_score,
    "loyalty": ProductIntelligence.global_loyalty_score,
    "reach": ProductIntelligence.global_reach_score,
    "basket_influence": ProductIntelligence.global_basket_influence_score,
    "purchase_intent": ProductIntelligence.global_purchase_intent_score,
    "performance": ProductIntelligence.global_health_score,
}


logger = get_logger(
    log_name="product_intelligence",
    log_folder="repositories",
)


class SQLAlchemyProductIntelligenceRepository(ProductIntelligenceRepository):
    def __init__(
        self,
        db: Session,
    ) -> None:
        self.db = db

    def get_product_profile(
        self,
        product_id: int,
    ) -> ProductIntelligence | None:

        logger.debug(
            "Querying product profile product_id=%s",
            product_id,
        )

        product = (
            self.db.query(ProductIntelligence)
            .filter(ProductIntelligence.product_id == product_id)
            .first()
        )

        logger.debug(
            "Queried product profile product_id=%s found=%s",
            product_id,
            product is not None,
        )

        return product

    def get_product_insights(
        self,
        product_id: int,
    ) -> ProductIntelligence | None:

        logger.debug(
            "Querying product insights product_id=%s",
            product_id,
        )

        product = (
            self.db.query(ProductIntelligence)
            .filter(ProductIntelligence.product_id == product_id)
            .first()
        )

        logger.debug(
            "Queried product insights product_id=%s found=%s",
            product_id,
            product is not None,
        )

        return product

    def get_products(
        self,
        limit: int,
        offset: int,
        department: str | None = None,
        aisle: str | None = None,
        performance_segment: str | None = None,
    ) -> tuple[list[ProductIntelligence], int]:

        logger.debug(
            (
                "Querying products limit=%s offset=%s department=%s "
                "aisle=%s performance_segment=%s"
            ),
            limit,
            offset,
            department,
            aisle,
            performance_segment,
        )

        query = self.db.query(ProductIntelligence)

        if department:
            query = query.filter(ProductIntelligence.department == department)

        if aisle:
            query = query.filter(ProductIntelligence.aisle == aisle)

        if performance_segment:
            query = query.filter(
                ProductIntelligence.health_segment == performance_segment
            )

        total = query.with_entities(func.count(ProductIntelligence.product_id)).scalar()

        products = (
            query.order_by(ProductIntelligence.global_health_score.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

        logger.debug(
            "Queried products count=%s total=%s",
            len(products),
            total,
        )

        return products, total

    def get_top_products(
        self,
        metric: str,
        limit: int,
    ) -> list[ProductIntelligence]:

        score_column = METRIC_COLUMN_MAP.get(metric)

        if score_column is None:
            logger.warning(
                "Unsupported product ranking metric metric=%s",
                metric,
            )
            raise ValueError(f"Unsupported metric: {metric}")

        logger.debug(
            "Querying top products metric=%s limit=%s",
            metric,
            limit,
        )

        products = (
            self.db.query(ProductIntelligence)
            .order_by(score_column.desc())
            .limit(limit)
            .all()
        )

        logger.debug(
            "Queried top products metric=%s count=%s",
            metric,
            len(products),
        )

        return products
