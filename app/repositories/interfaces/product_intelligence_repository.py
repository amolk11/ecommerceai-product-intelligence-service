from abc import ABC
from abc import abstractmethod

from app.models.product_intelligence import (
    ProductIntelligence,
)


class ProductIntelligenceRepository(ABC):

    @abstractmethod
    def get_product_profile(
        self,
        product_id: int,
    ) -> ProductIntelligence | None:
        raise NotImplementedError

    @abstractmethod
    def get_product_insights(
        self,
        product_id: int,
    ) -> ProductIntelligence | None:
        raise NotImplementedError

    @abstractmethod
    def get_products(
        self,
        limit: int,
        offset: int,
        department: str | None = None,
        aisle: str | None = None,
        health_segment: str | None = None,
    ) -> tuple[list[ProductIntelligence], int]:
        raise NotImplementedError

    @abstractmethod
    def get_top_products(
        self,
        metric: str,
        limit: int,
    ) -> list[ProductIntelligence]:
        raise NotImplementedError
    