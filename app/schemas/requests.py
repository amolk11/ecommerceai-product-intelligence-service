from enum import Enum


class RankingMetric(str, Enum):
    POPULARITY = "popularity"
    LOYALTY = "loyalty"
    REACH = "reach"
    BASKET_INFLUENCE = "basket_influence"
    PURCHASE_INTENT = "purchase_intent"
    PERFORMANCE = "performance"
    
