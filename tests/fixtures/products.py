from types import SimpleNamespace

from app.models.product_intelligence import ProductIntelligence


def product_record(**overrides):
    values = {
        "product_id": 101,
        "product_name": "Organic Bananas",
        "department": "produce",
        "aisle": "fresh fruits",
        "purchase_count": 1200,
        "unique_customers": 820,
        "unique_orders": 1040,
        "relationship_count": 310,
        "avg_confidence": 0.87,
        "global_popularity_score": 98.1,
        "global_loyalty_score": 91.4,
        "global_reach_score": 88.2,
        "global_basket_influence_score": 93.7,
        "global_purchase_intent_score": 95.5,
        "global_health_score": 97.2,
        "department_popularity_score": 96.2,
        "department_loyalty_score": 90.1,
        "department_reach_score": 84.5,
        "department_basket_influence_score": 92.3,
        "department_purchase_intent_score": 94.4,
        "department_health_score": 91.6,
        "popularity_segment": "High Demand",
        "loyalty_segment": "Repeat Driver",
        "reach_segment": "Broad Reach",
        "basket_segment": "Basket Builder",
        "purchase_intent_segment": "High Intent",
        "health_segment": "Star Product",
        "primary_strength": "High repeat purchase behavior",
        "primary_weakness": "Limited cross-category reach",
        "recommended_action": "Increase premium placement",
    }
    values.update(overrides)
    return SimpleNamespace(**values)


def product_model(**overrides):
    return ProductIntelligence(
        **product_record(**overrides).__dict__,
    )


def product_catalog():
    return [
        product_model(
            product_id=101,
            product_name="Organic Bananas",
            department="produce",
            aisle="fresh fruits",
            global_health_score=97.2,
            health_segment="Star Product",
        ),
        product_model(
            product_id=102,
            product_name="Whole Milk",
            department="dairy eggs",
            aisle="milk",
            global_health_score=83.4,
            health_segment="Core Performer",
        ),
        product_model(
            product_id=103,
            product_name="Spinach",
            department="produce",
            aisle="fresh vegetables",
            global_health_score=72.0,
            health_segment="Core Performer",
        ),
    ]
