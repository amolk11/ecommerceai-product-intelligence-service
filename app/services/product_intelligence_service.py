from app.core.logger import get_logger
from app.repositories.interfaces.product_intelligence_repository import (
    ProductIntelligenceRepository,
)

from app.cache.cache_manager import CacheManager
from app.cache.cache_key import (
    PROFILE_TTL_SECONDS,
    product_profile_key,
    TOP_PRODUCTS_TTL_SECONDS,
    top_products_key,
)

from app.schemas.requests import RankingMetric
from app.schemas.responses import (
    DepartmentScores,
    GlobalScores,
    ProductFacts,
    ProductIdentity,
    ProductInsights,
    ProductListItem,
    ProductListResponse,
    ProductProfileResponse,
    ProductSegments,
    TopProductItem,
    TopProductsResponse,
)


logger = get_logger(
    log_name="product_intelligence",
    log_folder="services",
)


class ProductIntelligenceService:
    def __init__(
        self,
        repository: ProductIntelligenceRepository,
        cache_manager: CacheManager,
    ) -> None:
        self.repository = repository
        self.cache_manager = cache_manager

    def get_product_profile(
        self,
        product_id: int,
    ) -> ProductProfileResponse | None:

        logger.debug(
            "Fetching product profile product_id=%s",
            product_id,
        )

        cache_key = product_profile_key(
            product_id=product_id,
        )

        cached = self.cache_manager.get(
            cache_key,
        )

        if cached is not None:
            logger.info("Product profile cache hit product_id=%s", product_id)

            return ProductProfileResponse.model_validate(
                cached,
            )

        logger.info("Product profile cache miss product_id=%s", product_id)

        record = self.repository.get_product_profile(
            product_id=product_id,
        )

        if record is None:
            logger.info("Product profile missing product_id=%s", product_id)
            return None

        logger.debug("Mapping product profile product_id=%s", product_id)

        response = ProductProfileResponse(
            identity=ProductIdentity(
                product_id=record.product_id,
                product_name=record.product_name,
                department=record.department,
                aisle=record.aisle,
            ),
            facts=ProductFacts(
                purchase_count=record.purchase_count,
                unique_customers=record.unique_customers,
                unique_orders=record.unique_orders,
                relationship_count=record.relationship_count,
                avg_confidence=record.avg_confidence,
            ),
            global_scores=GlobalScores(
                popularity_score=record.global_popularity_score,
                loyalty_score=record.global_loyalty_score,
                reach_score=record.global_reach_score,
                basket_influence_score=record.global_basket_influence_score,
                purchase_intent_score=record.global_purchase_intent_score,
                performance_score=record.global_health_score,
            ),
            department_scores=DepartmentScores(
                popularity_score=record.department_popularity_score,
                loyalty_score=record.department_loyalty_score,
                reach_score=record.department_reach_score,
                basket_influence_score=record.department_basket_influence_score,
                purchase_intent_score=record.department_purchase_intent_score,
                performance_score=record.department_health_score,
            ),
            segments=ProductSegments(
                popularity=record.popularity_segment,
                loyalty=record.loyalty_segment,
                reach=record.reach_segment,
                basket_influence=record.basket_segment,
                purchase_intent=record.purchase_intent_segment,
                performance=record.health_segment,
            ),
            insights=ProductInsights(
                primary_strength=record.primary_strength,
                primary_weakness=record.primary_weakness,
            ),
        )

        self.cache_manager.set(
            key=cache_key,
            value=response.model_dump(),
            ttl=PROFILE_TTL_SECONDS,
        )

        logger.info(
            "Cached product profile product_id=%s ttl=%s",
            product_id,
            PROFILE_TTL_SECONDS,
        )

        return response

    def get_products(
        self,
        limit: int,
        offset: int,
        department: str | None = None,
        aisle: str | None = None,
        performance_segment: str | None = None,
    ) -> ProductListResponse:

        logger.debug(
            (
                "Fetching products limit=%s offset=%s department=%s "
                "aisle=%s performance_segment=%s"
            ),
            limit,
            offset,
            department,
            aisle,
            performance_segment,
        )

        rows, total = self.repository.get_products(
            limit=limit,
            offset=offset,
            department=department,
            aisle=aisle,
            performance_segment=performance_segment,
        )

        items = [
            ProductListItem(
                product_id=row.product_id,
                product_name=row.product_name,
                department=row.department,
                aisle=row.aisle,
                performance_score=row.global_health_score,
                performance_segment=row.health_segment,
            )
            for row in rows
        ]

        logger.debug(
            "Mapped products count=%s total=%s",
            len(items),
            total,
        )

        return ProductListResponse(
            items=items,
            total=total,
            limit=limit,
            offset=offset,
        )

    def get_top_products(
        self,
        metric: RankingMetric,
        limit: int,
    ) -> TopProductsResponse:

        cache_key = top_products_key(metric=metric.value, limit=limit)

        cached = self.cache_manager.get(cache_key)

        if cached:
            logger.info(
                "Top products cache hit metric=%s limit=%s",
                metric.value,
                limit,
            )
            return TopProductsResponse.model_validate_json(cached)

        logger.info(
            "Top products cache miss metric=%s limit=%s",
            metric.value,
            limit,
        )

        rows = self.repository.get_top_products(
            metric=metric.value,
            limit=limit,
        )

        score_field_map = {
            RankingMetric.POPULARITY: "global_popularity_score",
            RankingMetric.LOYALTY: "global_loyalty_score",
            RankingMetric.REACH: "global_reach_score",
            RankingMetric.BASKET_INFLUENCE: "global_basket_influence_score",
            RankingMetric.PURCHASE_INTENT: "global_purchase_intent_score",
            RankingMetric.PERFORMANCE: "global_health_score",
        }

        score_field = score_field_map[metric]

        products = [
            TopProductItem(
                rank=index + 1,
                product_id=row.product_id,
                product_name=row.product_name,
                score=getattr(row, score_field),
            )
            for index, row in enumerate(rows)
        ]

        response = TopProductsResponse(
            metric=metric,
            products=products,
        )

        self.cache_manager.set(
            key=cache_key,
            value=response.model_dump_json(),
            ttl=TOP_PRODUCTS_TTL_SECONDS,
        )

        logger.info(
            "Cached top products metric=%s limit=%s ttl=%s",
            metric.value,
            limit,
            3600,
        )

        return response
