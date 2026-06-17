from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.models.base import Base


class ProductIntelligence(Base):
    __tablename__ = "product_intelligence"
    __table_args__ = {"schema": "serving"}

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------

    product_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    product_name: Mapped[str] = mapped_column(String)

    department: Mapped[str] = mapped_column(String)

    aisle: Mapped[str] = mapped_column(String)

    # ------------------------------------------------------------------
    # Facts
    # ------------------------------------------------------------------

    purchase_count: Mapped[int] = mapped_column(Integer)

    unique_customers: Mapped[int] = mapped_column(Integer)

    unique_orders: Mapped[int] = mapped_column(Integer)

    relationship_count: Mapped[int] = mapped_column(Integer)

    avg_confidence: Mapped[float] = mapped_column(Float)

    # ------------------------------------------------------------------
    # Global Scores
    # ------------------------------------------------------------------

    global_popularity_score: Mapped[float] = mapped_column(Float)

    global_loyalty_score: Mapped[float] = mapped_column(Float)

    global_reach_score: Mapped[float] = mapped_column(Float)

    global_basket_influence_score: Mapped[float] = mapped_column(Float)

    global_purchase_intent_score: Mapped[float] = mapped_column(Float)

    global_health_score: Mapped[float] = mapped_column(Float)

    # ------------------------------------------------------------------
    # Department Scores
    # ------------------------------------------------------------------

    department_popularity_score: Mapped[float] = mapped_column(Float)

    department_loyalty_score: Mapped[float] = mapped_column(Float)

    department_reach_score: Mapped[float] = mapped_column(Float)

    department_basket_influence_score: Mapped[float] = mapped_column(Float)

    department_purchase_intent_score: Mapped[float] = mapped_column(Float)

    department_health_score: Mapped[float] = mapped_column(Float)

    # ------------------------------------------------------------------
    # Segments
    # ------------------------------------------------------------------

    popularity_segment: Mapped[str] = mapped_column(String)

    loyalty_segment: Mapped[str] = mapped_column(String)

    reach_segment: Mapped[str] = mapped_column(String)

    basket_segment: Mapped[str] = mapped_column(String)

    purchase_intent_segment: Mapped[str] = mapped_column(String)

    health_segment: Mapped[str] = mapped_column(String)

    # ------------------------------------------------------------------
    # Insights
    # ------------------------------------------------------------------

    primary_strength: Mapped[str] = mapped_column(String)

    primary_weakness: Mapped[str] = mapped_column(String)

    recommended_action: Mapped[str] = mapped_column(String)
