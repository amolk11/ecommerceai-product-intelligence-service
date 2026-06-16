from sqlalchemy import func
from sqlalchemy.orm import Session

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
    "health": ProductIntelligence.global_health_score,
}


class SQLAlchemyProductIntelligenceRepository(
    ProductIntelligenceRepository
):
    def __init__(
        self,
        db: Session,
    ) -> None:
        self.db = db

    def get_product_profile(
        self,
        product_id: int,
    ) -> ProductIntelligence | None:

        return (
            self.db.query(ProductIntelligence)
            .filter(
                ProductIntelligence.product_id == product_id
            )
            .first()
        )

    def get_product_insights(
        self,
        product_id: int,
    ) -> ProductIntelligence | None:

        return (
            self.db.query(ProductIntelligence)
            .filter(
                ProductIntelligence.product_id == product_id
            )
            .first()
        )

    def get_products(
        self,
        limit: int,
        offset: int,
        department: str | None = None,
        aisle: str | None = None,
        health_segment: str | None = None,
    ) -> tuple[list[ProductIntelligence], int]:

        query = self.db.query(
            ProductIntelligence
        )

        if department:
            query = query.filter(
                ProductIntelligence.department
                == department
            )

        if aisle:
            query = query.filter(
                ProductIntelligence.aisle
                == aisle
            )

        if health_segment:
            query = query.filter(
                ProductIntelligence.health_segment
                == health_segment
            )

        total = query.with_entities(
            func.count(
                ProductIntelligence.product_id
            )
        ).scalar()

        products = (
            query.order_by(
                ProductIntelligence.global_health_score.desc()
            )
            .offset(offset)
            .limit(limit)
            .all()
        )

        return products, total

    def get_top_products(
        self,
        metric: str,
        limit: int,
    ) -> list[ProductIntelligence]:

        score_column = METRIC_COLUMN_MAP.get(
            metric
        )

        if score_column is None:
            raise ValueError(
                f"Unsupported metric: {metric}"
            )

        return (
            self.db.query(ProductIntelligence)
            .order_by(score_column.desc())
            .limit(limit)
            .all()
        )
        