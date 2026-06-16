from pydantic import BaseModel

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
    health_score: float


class DepartmentScores(BaseModel):
    popularity_score: float
    loyalty_score: float
    reach_score: float
    basket_influence_score: float
    purchase_intent_score: float
    health_score: float


class ProductSegments(BaseModel):
    popularity: str
    loyalty: str
    reach: str
    basket_influence: str
    purchase_intent: str
    health: str


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
    health_score: float
    health_segment: str


class ProductListResponse(BaseModel):
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
    