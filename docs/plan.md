# CommerceAI Product Intelligence Service - Architecture Plan

## Objective

The Product Intelligence Service should answer:

> "Tell me everything CommerceAI knows about this product."

The service is not a CRUD API and not a simple analytics API.

Its responsibility is to assemble product facts, intelligence, relationships, and insights into a unified Product Knowledge Object consumable by:

* Business Users
* Business Copilot
* Customer Copilot
* Recommendation Service
* Future Customer Intelligence Service
* Future Search and Ranking Services

---

# Product Intelligence Philosophy

The Product Intelligence Service acts as the Product Knowledge Layer of CommerceAI.

It combines:

* Product Facts
* Product Intelligence
* Product Relationships
* Product Insights

into a single product profile.

The service should answer:

### What happened?

Facts

### What does it mean?

Intelligence

### What is this product connected to?

Relationships

### What should I know?

Insights

---

# Data Sources

## features.product_features

Contains factual product behavior.

Columns:

* product_id
* product_name
* department
* aisle
* purchase_count
* unique_customers
* unique_orders
* reorder_rate
* total_reorders
* avg_cart_position
* std_cart_position
* avg_purchase_hour

Purpose:

Answer:

> What happened historically?

---

## serving.product_intelligence

Contains derived intelligence artifacts.

Purpose:

Answer:

> What does CommerceAI think about this product?

---

## analytics.product_affinity_features

Contains product relationship data.

Columns:

* product_id_a
* product_id_b
* co_purchase_count
* support
* confidence
* lift

Purpose:

Answer:

> What products are related to this product?

---

# Why We Are NOT Using serving.product_recommendations

Current coverage:

```text
Products in feature store       : 49,677
Products with recommendations   : 17,773
```

Approximately 64% of products have no recommendation records.

Recommendation tables are optimized for recommendation serving and filtered candidate generation.

They are not a complete product relationship graph.

Decision:

Product Intelligence relationships will use:

```text
analytics.product_affinity_features
```

instead of:

```text
serving.product_recommendations
serving.product_recommendations_top20
```

This ensures full product coverage.

---

# serving.product_intelligence Schema

| Column                             |
| ---------------------------------- |
| product_id                         |
| global_popularity_score            |
| global_loyalty_score               |
| global_reach_score                 |
| global_basket_influence_score      |
| global_purchase_intent_score       |
| global_health_score                |
| department_popularity_score        |
| department_loyalty_score           |
| department_reach_score             |
| department_basket_influence_score  |
| department_purchase_intent_score   |
| department_health_score            |
| global_popularity_segment          |
| global_loyalty_segment             |
| global_reach_segment               |
| global_basket_segment              |
| global_purchase_intent_segment     |
| global_health_segment              |
| department_popularity_segment      |
| department_loyalty_segment         |
| department_reach_segment           |
| department_basket_segment          |
| department_purchase_intent_segment |
| department_health_segment          |
| scoring_version                    |
| generated_at                       |

---

# Why We Are NOT Copying Facts

Rejected Design:

```text
serving.product_intelligence
    +
purchase_count
unique_customers
reorder_rate
...
```

Reason for Rejection:

* Creates duplication
* Multiple sources of truth
* Harder maintenance
* Violates existing CommerceAI architecture
* Inconsistent with Recommendation Service design

Decision:

Facts remain in:

```text
features.product_features
```

Intelligence remains in:

```text
serving.product_intelligence
```

This creates clear ownership boundaries.

---

# Why We Are Creating serving.product_intelligence

Alternative Considered:

Calculate intelligence scores during every API request.

Example:

```text
GET /product-profiles/{id}
```

↓

Read features

↓

Calculate scores

↓

Return profile

Reason for Rejection:

* Business logic scattered across service layer
* Recalculation on every request
* Harder testing
* Harder reproducibility
* Difficult future ML integration
* Difficult score versioning

Decision:

Precompute intelligence using a dedicated pipeline.

Store intelligence artifacts in:

```text
serving.product_intelligence
```

This makes intelligence a first-class domain asset.

---

# Intelligence Dimensions

## Popularity

Question:

> How popular is this product?

Based on:

* purchase_count
* unique_orders

Outputs:

* Global Popularity Score
* Department Popularity Score
* Popularity Segment

---

## Loyalty

Question:

> Do customers come back?

Based on:

* reorder_rate
* total_reorders

Outputs:

* Global Loyalty Score
* Department Loyalty Score
* Loyalty Segment

---

## Reach

Question:

> How many customers does this product touch?

Based on:

* unique_customers
* customer_penetration

Outputs:

* Global Reach Score
* Department Reach Score
* Reach Segment

---

## Basket Influence

Question:

> How important is this product inside baskets?

Based on:

* co_purchase_count
* support
* confidence
* lift

Outputs:

* Global Basket Influence Score
* Department Basket Influence Score
* Basket Segment

---

## Purchase Intent

Question:

> Is this product a planned purchase or an impulse purchase?

Based on:

* avg_cart_position
* std_cart_position

Outputs:

* Global Purchase Intent Score
* Department Purchase Intent Score
* Purchase Intent Segment

---

## Health

Question:

> How strong is this product overall?

Based on:

* Popularity
* Loyalty
* Reach
* Basket Influence
* Purchase Intent

Outputs:

* Global Health Score
* Department Health Score
* Health Segment

---

# Why We Are Using Global Scores

Global scores compare products against the entire catalog.

Example:

```text
Bananas vs 49,677 products
```

Benefits:

* Executive-friendly
* Cross-category comparison
* Portfolio-wide ranking
* Business-wide product assessment

---

# Why We Are Using Department Scores

Department scores compare products only within their department.

Example:

```text
Bananas vs Produce
```

Benefits:

* Fair category comparison
* Reduced department bias
* Better category-level insights

---

# Why We Chose BOTH

Rejected:

Global Only

Problem:

High-volume departments dominate rankings.

Rejected:

Department Only

Problem:

Cross-category comparison becomes impossible.

Decision:

Store both.

Benefits:

* Executive View
* Category Manager View
* Better Copilot Explanations
* More complete intelligence

---

# Why We Are Using Percentile-Based Scoring

Rejected:

```text
reorder_rate > 0.7
```

Problem:

Dataset-specific thresholds.

Decision:

```text
Log Scaling
+
Percentile Ranking
```

Benefits:

* Handles Instacart's long-tail distribution
* Dataset agnostic
* Explainable
* Robust

---

# Product Knowledge Object

Final API response should assemble:

```json
{
  "identity": {},
  "facts": {},
  "global_scores": {},
  "department_scores": {},
  "segments": {},
  "relationships": {},
  "insights": {},
  "metadata": {}
}
```

This becomes the canonical product profile across the CommerceAI ecosystem.

---

# Final Product Intelligence Architecture

```text
features.product_features
            ↓
          Facts

serving.product_intelligence
            ↓
       Intelligence

analytics.product_affinity_features
            ↓
      Relationships

            ↓

Product Intelligence Service

            ↓

Product Knowledge Object

            ↓

API
```

---

# Architectural Principles

The Product Intelligence Service follows:

```text
Facts
+
Intelligence
+
Relationships
+
Insights
=
Product Knowledge
```

Ownership:

```text
Features Layer      -> Facts

Serving Layer       -> Intelligence

Analytics Layer     -> Relationships

Service Layer       -> Knowledge Assembly

API Layer           -> Product Profile Delivery
```

This design is scalable, explainable, reusable, and fully aligned with the CommerceAI platform architecture.
