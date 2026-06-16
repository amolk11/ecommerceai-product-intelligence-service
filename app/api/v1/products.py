from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Query

from app.dependencies.product_intelligence import (
    get_product_intelligence_service,
)

from app.schemas.requests import RankingMetric

from app.schemas.responses import (
    ProductInsightsResponse,
    ProductListResponse,
    ProductProfileResponse,
    TopProductsResponse,
)

from app.services.product_intelligence_service import (
    ProductIntelligenceService,
)

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.get(
    "",
    response_model=ProductListResponse,
    summary="Get Products",
)
def get_products(
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    offset: int = Query(
        default=0,
        ge=0,
    ),
    department: str | None = None,
    aisle: str | None = None,
    health_segment: str | None = None,
    service: ProductIntelligenceService = Depends(
        get_product_intelligence_service,
    ),
) -> ProductListResponse:
    """
    Retrieve paginated products.
    """

    return service.get_products(
        limit=limit,
        offset=offset,
        department=department,
        aisle=aisle,
        health_segment=health_segment,
    )


@router.get(
    "/top",
    response_model=TopProductsResponse,
    summary="Get Top Products",
)
def get_top_products(
    metric: RankingMetric,
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
    ),
    service: ProductIntelligenceService = Depends(
        get_product_intelligence_service,
    ),
) -> TopProductsResponse:
    """
    Retrieve top-ranked products for a metric.
    """

    return service.get_top_products(
        metric=metric,
        limit=limit,
    )


@router.get(
    "/{product_id}/profile",
    response_model=ProductProfileResponse,
    summary="Get Product Profile",
)
def get_product_profile(
    product_id: int,
    service: ProductIntelligenceService = Depends(
        get_product_intelligence_service,
    ),
) -> ProductProfileResponse:
    """
    Retrieve a complete product profile.
    """

    product = service.get_product_profile(
        product_id=product_id,
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail=f"Product {product_id} not found",
        )

    return product


@router.get(
    "/{product_id}/insights",
    response_model=ProductInsightsResponse,
    summary="Get Product Insights",
)
def get_product_insights(
    product_id: int,
    service: ProductIntelligenceService = Depends(
        get_product_intelligence_service,
    ),
) -> ProductInsightsResponse:
    """
    Retrieve product insights.
    """

    insights = service.get_product_insights(
        product_id=product_id,
    )

    if insights is None:
        raise HTTPException(
            status_code=404,
            detail=f"Product {product_id} not found",
        )

    return insights
