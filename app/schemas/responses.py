from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

from app.schemas.requests import RankingMetric


class ProductIdentity(BaseModel):
    product_id: int
    product_name: str
    department: str
    aisle: str


class ProductFacts(BaseModel):
    purchase_count: int
    unique_customers: int
    unique_orders: int
    relationship_count: int
    avg_confidence: float


class GlobalScores(BaseModel):
    popularity_score: float
    loyalty_score: float
    reach_score: float
    basket_influence_score: float
    purchase_intent_score: float
    performance_score: float = Field(
        examples=[97.2],
        description=(
            "Overall business performance score derived from commercial "
            "strength signals."
        ),
    )


class DepartmentScores(BaseModel):
    popularity_score: float
    loyalty_score: float
    reach_score: float
    basket_influence_score: float
    purchase_intent_score: float
    performance_score: float = Field(
        examples=[91.6],
        description="Department-relative business performance score.",
    )


class ProductSegments(BaseModel):
    popularity: str
    loyalty: str
    reach: str
    basket_influence: str
    purchase_intent: str
    performance: str = Field(
        examples=["Star Product"],
        description="Business performance segment for the product.",
    )


class ProductInsights(BaseModel):
    primary_strength: str
    primary_weakness: str
    recommended_action: str


class ProductProfileResponse(BaseModel):
    identity: ProductIdentity
    facts: ProductFacts
    global_scores: GlobalScores
    department_scores: DepartmentScores
    segments: ProductSegments
    insights: ProductInsights


class ProductListItem(BaseModel):
    product_id: int
    product_name: str
    department: str
    aisle: str
    performance_score: float = Field(
        examples=[97.2],
        description="Overall business performance score.",
    )
    performance_segment: str = Field(
        examples=["Star Product"],
        description="Business performance segment.",
    )


class ProductListResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "items": [
                        {
                            "product_id": 101,
                            "product_name": "Organic Bananas",
                            "department": "produce",
                            "aisle": "fresh fruits",
                            "performance_score": 97.2,
                            "performance_segment": "Star Product",
                        }
                    ],
                    "total": 1,
                    "limit": 20,
                    "offset": 0,
                }
            ]
        }
    )

    items: list[ProductListItem]
    total: int
    limit: int
    offset: int


class TopProductItem(BaseModel):
    rank: int
    product_id: int
    product_name: str
    score: float


class TopProductsResponse(BaseModel):
    metric: RankingMetric
    products: list[TopProductItem]


class ProductInsightsResponse(BaseModel):
    product_id: int
    insights: ProductInsights
    
