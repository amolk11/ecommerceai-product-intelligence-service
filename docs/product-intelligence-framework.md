# CommerceAI Product Intelligence Scoring Framework

## Overview

The **Product Intelligence Service** answers a critical business question:

> **Tell me everything CommerceAI knows about this product.**

Rather than exposing raw analytics, this service converts historical customer behavior into business-friendly intelligence scores that describe how a product performs across multiple dimensions.

### Service Consumers

- Business Users
- Business Copilot
- Customer Copilot
- Recommendation Service
- Future Search & Ranking Services
- Future Customer Intelligence Service

### Output

A comprehensive **Product Knowledge Object** containing:
- Product facts
- Intelligence scores
- Segments
- Relationships
- Insights

---

## Design Philosophy

### The Problem

Traditional analytics systems report metrics like:
- Purchase Count
- Reorder Rate
- Customer Count

While useful, these metrics require interpretation and don't directly answer business questions.

### The Solution

CommerceAI converts raw metrics into **explainable intelligence dimensions**:

| Dimension | Question Answered |
|-----------|-------------------|
| **Popularity** | How much demand does this product have? |
| **Loyalty** | Do customers come back and buy it again? |
| **Reach** | How many unique customers does it touch? |
| **Basket Influence** | How much does it influence basket composition? |
| **Purchase Intent** | How intentionally do customers buy it? |
| **Health Score** | How strong is this product overall? |

---

## Data Sources

### `features.product_features`

Primary source of product behavioral signals.

**Contains:**
- `purchase_count`
- `unique_customers`
- `unique_orders`
- `reorder_rate`
- `total_reorders`
- `avg_cart_position`
- `std_cart_position`
- `avg_purchase_hour`

### `analytics.product_affinity_features`

Derived from association rule mining and basket analysis.

**Contains:**
- `product_id_a` / `product_id_b`
- `co_purchase_count`
- `support`
- `confidence`
- `lift`

**Purpose:** Understand product relationships and basket influence.

---

## Intelligence Dimensions

### 1. Global Popularity Score

**Business Meaning:** Measures overall product demand across the entire catalog.

**Question:** How popular is this product compared to all products?

#### Challenge

Purchase counts follow a long-tail distribution. Without adjustment, metrics heavily favor top products.

**Example:**
| Product | Purchase Count |
|---------|-----------------|
| Banana | 472,565 |
| Average Product | 653 |
| Thousands of Products | < 20 |

#### Solution

Apply logarithmic transformation to normalize the distribution:

```
log_purchase_count = log1p(purchase_count)
```

#### Formula

```
Popularity Score = 50% Percentile(Log Purchase Count) 
                  + 50% Percentile(Purchase Count)
```

**Range:** 0 - 100

**Examples:**
| Product | Score |
|---------|-------|
| Banana | 100 |
| Organic Strawberries | 99.9 |
| Average Product | ~50 |
| Rare Product | <10 |

---

### 2. Global Loyalty Score

**Business Meaning:** Measures customer retention and repeat purchasing behavior.

**Question:** Do customers repeatedly come back to buy this product?

#### Challenge

Products with few purchases can produce misleading reorder rates.

**Example:**
| Product | Purchases | Reorders | Reorder Rate |
|---------|-----------|----------|--------------|
| Product A | 10 | 9 | 90% |
| Banana | 472,565 | 398,609 | 84% |

Without adjustment, low-volume products appear artificially loyal.

#### Solution

Apply **Bayesian Smoothing** to shrink reorder rates toward the catalog average for low-volume products.

**Bayesian Parameters:**
- `m = 100`
- `global_reorder_rate = 0.5896974667922161`

#### Components

**Loyalty Efficiency**
- Measures how efficiently a product converts purchases into repeat purchases
- Uses: `smoothed_reorder_rate`

**Loyalty Volume**
- Measures how many repeat purchases exist
- Uses: `log(total_reorders)`

#### Formula

```
Loyalty Score = 50% Percentile(Smoothed Reorder Rate)
               + 50% Percentile(Log Total Reorders)
```

---

### 3. Global Reach Score

**Business Meaning:** Measures customer penetration.

**Question:** How many unique customers purchased this product?

#### Challenge

Reach is highly correlated with popularity (correlation ≈ 0.98).

#### Decision

Reach is retained for explainability and reporting but **excluded from Health Score** calculations to avoid double-counting demand.

#### Formula

```
Reach Score = Percentile(Unique Customers)
```

**Range:** 0 - 100

---

### 4. Global Basket Influence Score

**Business Meaning:** Measures how strongly a product influences basket composition.

**Question:** How important is this product within the shopping basket ecosystem?

#### Basket Intelligence Construction

For every product, aggregate both sides of the affinity graph:
- `product_id_a` relationships
- `product_id_b` relationships

**Produces:**
- `relationship_count`
- `total_co_purchase_count`
- `avg_confidence`
- `avg_lift`
- `p95_lift`

#### Components

**Basket Breadth**
- Measures how many products are connected to this product
- Uses: `relationship_count`

**Basket Strength**
- Measures how strongly this product predicts other products
- Uses: `avg_confidence`

#### Rejected Metrics

**Lift**
- Reason: Extremely unstable, sensitive to rare products
- Observed: max lift > 167,000

**Total Co-Purchase Count**
- Reason: Highly correlated with relationship count (0.82)

#### Formula

```
Basket Influence = 70% Percentile(Relationship Count)
                  + 30% Percentile(Average Confidence)
```

**Range:** 0 - 100

---

### 5. Global Purchase Intent Score

**Business Meaning:** Measures how intentionally customers buy a product.

**Question:** Is this a planned purchase or an impulse purchase?

#### Signals Used

**Average Cart Position**
- Measures how early the product is added to the basket
- Lower is better (earlier = more intentional)

**Cart Position Consistency**
- Measures how consistently the product is purchased
- Lower standard deviation is better

#### Challenge

Products purchased only once generate unrealistic rankings.

**Example:**
- Purchase Count = 1
- Cart Position = 1
- Result: Appears as a perfect product

#### Solution

Apply **Bayesian smoothing** to both `avg_cart_position` and `std_cart_position` using purchase count as confidence.

**Bayesian Parameters:**
- `m = 100`
- `global_avg_cart_position = 9.09756808901078`
- `global_std_position = 7.2688253370464055`

#### Components

**Priority Score**
- Based on: Smoothed Average Cart Position
- Lower is better

**Consistency Score**
- Based on: Smoothed Standard Deviation
- Lower is better

#### Formula

```
Purchase Intent = 50% Inverse Percentile(Smoothed Avg Cart Position)
                 + 50% Inverse Percentile(Smoothed Std Position)
```

**Range:** 0 - 100

---

### 6. Global Health Score

**Business Meaning:** Measures overall product quality and performance.

**Question:** How healthy is this product across all intelligence dimensions?

#### Included Dimensions

- Popularity
- Loyalty
- Basket Influence
- Purchase Intent

#### Excluded Dimension

**Reach**
- Reason: Reach ≈ Popularity (0.98 correlation)
- Impact: Including Reach would double-count demand

#### Formula

```
Health Score = (Popularity + Loyalty + Basket Influence + Purchase Intent) / 4
```

**Range:** 0 - 100

---

## Department Scores

Global scores compare products against the **entire catalog**.

Department scores compare products only against **products in the same department**.

### Why Both?

| Score Type | Question |
|-----------|----------|
| **Global** | How important is this product overall? |
| **Department** | How important is this product within its category? |

Both perspectives provide valuable business insights.

---

## Product Intelligence Serving Layer

The serving layer converts intelligence scores into business-friendly product knowledge.

**Source:** `analytics.product_intelligence_base`

**Output:** `serving.product_intelligence`

### Generated Segments

#### Popularity Segment
- 90+ → **Top Seller**
- 70-89 → **Popular**
- 40-69 → **Average**
- <40 → **Niche**

#### Loyalty Segment
- 90+ → **Highly Loyal**
- 70-89 → **Loyal**
- 40-69 → **Moderate**
- <40 → **Low Loyalty**

#### Reach Segment
- 90+ → **Mass Market**
- 70-89 → **Broad Reach**
- 40-69 → **Focused Audience**
- <40 → **Specialized Product**

#### Basket Segment
- 90+ → **Basket Driver**
- 70-89 → **Basket Builder**
- 40-69 → **Companion Product**
- <40 → **Standalone Product**

#### Purchase Intent Segment
- 90+ → **Essential Purchase**
- 70-89 → **Planned Purchase**
- 40-69 → **Mixed Intent**
- <40 → **Impulse Product**

#### Health Segment
- 90+ → **Star Product**
- 75-89 → **Strong Product**
- 50-74 → **Stable Product**
- <50 → **Weak Product**

### Business Insights

The serving layer generates three key insights for each product:

1. **Primary Strength** - Top-performing dimension(s)
2. **Primary Weakness** - Lowest-performing dimension(s)
3. **Recommended Action** - Specific business strategy

#### Possible Strengths
- High Demand
- Customer Loyalty
- Broad Customer Reach
- Basket Influence
- Purchase Intent

#### Possible Recommended Actions
- Maintain performance and protect market position
- Promote to a broader customer audience
- Improve cross-sell opportunities
- Focus on customer retention

---

## Product Knowledge Object

The Product Intelligence Service assembles a comprehensive product profile:

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

This becomes the **canonical product profile** across the CommerceAI ecosystem.

---

## Validation Results

The framework was validated across the complete Instacart catalog.

### Dataset Coverage

**Products Evaluated:** 49,677

### Health Score Distribution

| Metric | Value |
|--------|-------|
| Minimum Health Score | 10.67 |
| Average Health Score | 47.45 |
| Maximum Health Score | 99.02 |

### Health Segments

| Segment | Count |
|---------|-------|
| Star Product (90+) | 1,083 |
| Strong Product (75-89) | 4,702 |
| Stable Product (50-74) | 16,702 |
| Weak Product (<50) | 27,190 |

### Top Ranked Products

1. Banana
2. Bag of Organic Bananas
3. Organic Hass Avocado
4. Organic Avocado
5. Organic Whole Milk
6. Organic Strawberries
7. Organic Baby Spinach
8. 2% Reduced Fat Milk
9. Soda
10. Organic Raspberries

These align with known high-volume and highly reordered products in the Instacart dataset, validating that the framework captures real customer purchasing behavior.

---

## Known Dataset Limitations

### No True Timestamps

**Unavailable:**
- Exact order date
- Exact order time
- Calendar history

**As a result, no support for:**
- Seasonality modeling
- Demand forecasting
- Trend analysis

### No Pricing Data

**Unavailable:**
- Product prices
- Discounts
- Promotions
- Revenue
- Profit

**As a result, no support for:**
- Revenue analytics
- Profit analytics
- Price elasticity

### No Inventory Data

**Unavailable:**
- Inventory levels
- Stockouts
- Warehouse information

**As a result, no support for:**
- Inventory optimization
- Supply chain analytics

### No Customer Demographics

**Unavailable:**
- Age
- Gender
- Income
- Location

**As a result:**
- Behavioral segmentation only (no demographic targeting)

---

## Final Architecture

```
staging.order_items
        ↓
        
features.product_features
    +
analytics.product_affinity_features
        ↓
        
analytics.product_intelligence_base
        ↓
        
serving.product_intelligence
        ↓
        
Product Intelligence Service
        ↓
        
├─ Business Copilot
├─ Customer Copilot
├─ Recommendation Service
├─ Future Search & Ranking Services
└─ Future Customer Intelligence Service
```

---

## Philosophy

CommerceAI does **not attempt to invent unsupported intelligence**.

Instead, it converts the signals that actually exist in the dataset into explainable, business-friendly intelligence.

### Platform Priorities

✅ **Supported Capabilities**
- Product Intelligence
- Customer Intelligence
- Recommendation Intelligence
- Explainable AI

❌ **Unsupported Capabilities**
- Demand forecasting
- Inventory optimization
- Revenue prediction
- Demographic targeting

The result is a **transparent, scalable, and realistic** intelligence platform built around the information available in the dataset.

---

## Project Status

| Component | Status |
|-----------|--------|
| Product Intelligence Research | ✅ Complete |
| Scoring Framework | ✅ Complete |
| Basket Intelligence Design | ✅ Complete |
| Bayesian Smoothing Design | ✅ Complete |
| `analytics.product_intelligence_base` | ✅ Complete |
| `serving.product_intelligence` | ✅ Complete |
| Validation & Testing | ✅ Complete |
| Product Intelligence Service | ⏳ Next Phase |

---

## Scoring Methodology

All CommerceAI Product Intelligence scores use a standardized **0–100 scale**.

Scores are generated using **percentile-based ranking** rather than raw metrics.

### Score Interpretation

| Score Range | Interpretation |
|-------------|-----------------|
| 90 – 100 | Exceptional |
| 70 – 89 | Strong |
| 50 – 69 | Average |
| 30 – 49 | Below Average |
| 0 – 29 | Weak |

### Why Percentile Ranking?

This approach ensures:
- ✅ Scores remain interpretable regardless of metric scale
- ✅ Prevents domination by extreme outliers
- ✅ Enables consistent comparison across dimensions
- ✅ Supports business-friendly communication

### Example

```
Popularity Score = 95
```

**Interpretation:** The product performs better than approximately 95% of products in the catalog for that dimension.

---

## Future Roadmap

The Product Intelligence framework serves as the foundation for future CommerceAI services.

### Phase 1: Intelligence Foundation (Completed)

```
Product Features
        +
Product Affinity Analysis
        ↓
Product Intelligence
```

**Status:** ✅ Production Validated

### Phase 2: Product Intelligence Service (Next)

```
GET /products/{product_id}
GET /products/{product_id}/scores
GET /products/{product_id}/insights
GET /products/{product_id}/relationships
```

**Capabilities:**
- Retrieve comprehensive product scores
- Access dimension-specific insights
- Explore product relationships and basket influence
- Query department-level comparisons

### Phase 3: Business Copilot

```
Product Intelligence Service
        ↓
Business Copilot
```

**Business users will ask:**
- Why is this product performing well?
- Which products are category leaders?
- Which products need attention?
- What actions should we take?

### Phase 4: Customer Intelligence Service

```
Product Intelligence
        +
Customer Behavior
        ↓
Customer Intelligence Service
```

Combines customer behavior patterns with product intelligence for deeper insights.

### Phase 5: Customer Copilot

```
Customer Intelligence Service
        ↓
Customer Copilot
```

**Capabilities:**
- Personalized product explanations
- Recommendation justifications
- Customer-specific product insights
- Behavioral predictions

---

## Framework Version

```
CommerceAI Product Intelligence Framework
Version: 1.0
Status: Production Validated
Date: June 2026
```

---

## Summary

The CommerceAI Product Intelligence Scoring Framework transforms raw e-commerce data into actionable business insights by:

1. **Normalizing** raw metrics through logarithmic and Bayesian techniques
2. **Combining** multiple signals into explainable dimensions
3. **Contextualizing** scores through segmentation and insights
4. **Validating** against real-world purchasing behavior
5. **Maintaining** transparency about data limitations

This approach enables business users, copilots, and recommendation engines to understand product performance without requiring deep technical knowledge of the underlying analytics.