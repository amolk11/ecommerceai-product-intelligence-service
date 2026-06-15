# CommerceAI Product Intelligence Scoring Framework

## Overview

The goal of the Product Intelligence Service is to answer a simple but powerful question:

> Tell me everything CommerceAI knows about this product.

Rather than exposing raw analytics, the service converts historical customer behavior into business-friendly intelligence scores that describe how a product performs across multiple dimensions.

The Product Intelligence Service is designed to serve:

* Business Users
* Business Copilot
* Customer Copilot
* Recommendation Service
* Future Search & Ranking Services
* Future Customer Intelligence Service

The output is a Product Knowledge Object containing product facts, intelligence scores, segments, relationships, and insights.

---

# Design Philosophy

Most analytics systems stop at reporting metrics such as:

* Purchase Count
* Reorder Rate
* Customer Count

While useful, these metrics require interpretation.

CommerceAI converts raw metrics into explainable intelligence dimensions:

| Dimension        | Question Answered                              |
| ---------------- | ---------------------------------------------- |
| Popularity       | How much demand does this product have?        |
| Loyalty          | Do customers come back and buy it again?       |
| Reach            | How many unique customers does it touch?       |
| Basket Influence | How much does it influence basket composition? |
| Purchase Intent  | How intentionally do customers buy it?         |
| Health Score     | How strong is this product overall?            |

---

# Data Sources

## features.product_features

Primary source of product behavioral signals.

Contains:

* purchase_count
* unique_customers
* unique_orders
* reorder_rate
* total_reorders
* avg_cart_position
* std_cart_position
* avg_purchase_hour

---

## Analytics Basket Intelligence

Derived from product affinity analysis.

Contains:

* co_purchase_count
* support
* confidence
* lift

Used to understand product relationships and basket influence.

---

# Global Popularity Score

## Business Meaning

Measures overall product demand across the entire catalog.

Answers:

> How popular is this product compared to all products?

---

## Challenge

Purchase counts follow a long-tail distribution.

Example:

| Product               | Purchase Count |
| --------------------- | -------------: |
| Banana                |        472,565 |
| Average Product       |            653 |
| Thousands of Products |           < 20 |

Raw purchase counts heavily favor top products.

---

## Solution

Apply logarithmic transformation:

```python
log_purchase_count = log1p(purchase_count)
```

Then percentile ranking:

```python
global_popularity_score
```

Range:

```text
0 - 100
```

---

## Example

| Product              | Popularity Score |
| -------------------- | ---------------: |
| Banana               |              100 |
| Organic Strawberries |             99.9 |
| Average Product      |              ~50 |
| Rare Product         |              <10 |

---

# Global Loyalty Score

## Business Meaning

Measures customer retention.

Answers:

> Do customers repeatedly come back to buy this product?

---

## Challenge

Products with few purchases can produce misleading reorder rates.

Example:

| Product   | Purchases | Reorders | Reorder Rate |
| --------- | --------: | -------: | -----------: |
| Product A |        10 |        9 |          90% |
| Banana    |   472,565 |  398,609 |          84% |

Without adjustment, Product A appears more loyal than Banana.

---

## Solution

Bayesian Smoothing

The reorder rate is shrunk toward the catalog average for low-volume products.

Result:

```text
smoothed_reorder_rate
```

---

## Final Components

### Loyalty Efficiency

Measures:

> How efficiently a product converts purchases into repeat purchases.

Uses:

```text
smoothed_reorder_rate
```

---

### Loyalty Volume

Measures:

> How many total repeat purchases exist.

Uses:

```text
log(total_reorders)
```

---

## Final Formula

```text
Global Loyalty Score
=
50% Loyalty Efficiency
+
50% Loyalty Volume
```

---

# Global Reach Score

## Business Meaning

Measures customer penetration.

Answers:

> How many unique customers purchased this product?

---

## Challenge

Reach is highly correlated with popularity.

Observed correlation:

```text
Popularity vs Reach ≈ 0.98
```

---

## Decision

Reach is retained for explainability and reporting but excluded from Health Score calculations.

---

## Example

| Product       | Reach Meaning                             |
| ------------- | ----------------------------------------- |
| Banana        | Purchased by a large portion of customers |
| Niche Product | Purchased by few customers                |

---

# Global Basket Influence Score

## Business Meaning

Measures how strongly a product influences basket composition.

Answers:

> How important is this product within the shopping basket ecosystem?

---

# Basket Analysis Process

Affinity analysis generated:

* Confidence
* Lift
* Co-Purchase Count

for millions of product relationships.

---

# Discovery

Basket influence naturally separates into two dimensions.

---

## Basket Breadth

Measures:

> How many products are connected to this product?

Uses:

```text
relationship_count
```

Example:

| Product       | Relationship Count |
| ------------- | -----------------: |
| Banana        |             23,516 |
| Niche Product |                 15 |

---

## Basket Strength

Measures:

> How strongly does this product predict other products?

Uses:

```text
avg_confidence
```

---

## Rejected Metrics

### Lift

Rejected because:

* Extremely unstable
* Sensitive to rare products
* Produced unrealistic outliers

Observed:

```text
max lift > 167,000
```

---

### Total Co-Purchase Count

Rejected because it was highly correlated with relationship count.

Observed correlation:

```text
0.82
```

---

## Final Formula

```text
Basket Influence
=
70% Breadth
+
30% Strength
```

---

# Global Purchase Intent Score

## Business Meaning

Measures how intentionally customers buy a product.

Answers:

> Is this a planned purchase or an impulse purchase?

---

# Signals Used

## Average Cart Position

Measures:

> How early is the product added to the basket?

Lower is better.

---

## Cart Position Consistency

Measures:

> How consistently is the product purchased?

Lower standard deviation is better.

---

# Challenge

Products purchased only once generated unrealistic rankings.

Example:

```text
Purchase Count = 1
Cart Position = 1
```

appeared as a perfect product.

---

# Solution

Bayesian smoothing was applied to:

* avg_cart_position
* std_cart_position

using purchase count as confidence.

---

## Components

### Priority Score

Based on:

```text
Smoothed Average Cart Position
```

---

### Consistency Score

Based on:

```text
Smoothed Standard Deviation
```

---

## Final Formula

```text
Purchase Intent
=
50% Priority
+
50% Consistency
```

---

# Department Scores

Global scores compare products against the entire catalog.

Department scores compare products only against products in the same department.

---

## Example

### Global View

| Product   | Global Popularity |
| --------- | ----------------: |
| Banana    |               100 |
| Olive Oil |                80 |

---

### Department View

| Product            | Department Popularity |
| ------------------ | --------------------: |
| Banana (Produce)   |                   100 |
| Olive Oil (Pantry) |                   100 |

Both are category leaders.

---

# Why Both Global and Department Scores?

Global Scores answer:

> How important is this product overall?

Department Scores answer:

> How important is this product within its category?

Both perspectives are valuable.

---

# Global Health Score

## Business Meaning

Measures overall product quality and performance.

Answers:

> How healthy is this product across all intelligence dimensions?

---

## Included Dimensions

* Popularity
* Loyalty
* Basket Influence
* Purchase Intent

---

## Excluded Dimension

Reach

Reason:

```text
Reach ≈ Popularity
```

Including Reach would double-count demand.

---

## Final Formula

```text
Health Score
=
Popularity
+
Loyalty
+
Basket Influence
+
Purchase Intent
--------------------------------
4
```

---

# Product Knowledge Object

The Product Intelligence Service ultimately assembles:

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

# Known Dataset Limitations and Design Decisions

The CommerceAI Product Intelligence framework is built on the Instacart dataset. While the dataset provides rich information about customer purchasing behavior, it also has several important limitations that influence system design.

## Missing Transaction Timestamps

The dataset does not contain actual order timestamps.

Available fields:

* order_number
* order_dow
* order_hour_of_day
* days_since_prior_order

Unavailable:

* exact order date
* exact order time
* calendar history

As a result, true time-series analysis, seasonality modeling, and production-grade demand forecasting are not possible.

### Design Decision

CommerceAI focuses on behavioral intelligence rather than forecasting future inventory demand.

---

## No Pricing Information

The dataset does not contain:

* product prices
* discounts
* promotions
* revenue

As a result, CommerceAI cannot calculate:

* product revenue
* profit contribution
* customer lifetime value
* price elasticity

### Design Decision

Product Health is based on customer behavior rather than financial performance.

---

## No Inventory Information

The dataset does not contain:

* inventory levels
* stockouts
* warehouse data
* replenishment information

### Design Decision

CommerceAI does not attempt inventory optimization or supply chain analytics.

---

## No Customer Demographics

The dataset does not contain:

* age
* gender
* income
* location
* household information

### Design Decision

Customer Intelligence focuses on behavioral segmentation rather than demographic segmentation.

---

## One Product Per Order Item Structure

Each row in the dataset represents a single product within an order.

As a result:

```text
purchase_count ≈ unique_orders
```

for most products.

This explains why purchase volume and order volume are nearly identical.

### Design Decision

Purchase Count is used as the primary popularity signal.

Unique Orders is not used separately because it provides little additional information.

---

## Basket Intelligence Coverage

Product affinity analysis generated basket relationships for approximately 57% of products.

Approximately 43% of products did not meet relationship thresholds and therefore have no meaningful basket connections.

### Design Decision

Products without basket relationships receive low Basket Influence scores rather than being excluded from Product Intelligence.

This preserves complete catalog coverage.

---

## Philosophy

Rather than treating these limitations as weaknesses, CommerceAI explicitly documents them and designs intelligence layers around the signals that are actually available.

The platform prioritizes:

* Product Intelligence
* Customer Intelligence
* Recommendation Intelligence
* Explainable AI

over unsupported capabilities such as inventory forecasting, revenue optimization, or demographic targeting.

This results in a system that is transparent, realistic, and aligned with the actual information available in the dataset.

# Final Architecture

```text
features.product_features
            +
basket_intelligence
            ↓

serving.product_intelligence
            ↓

Product Intelligence Service
            ↓

Product Knowledge Object
            ↓

API
```

The resulting system is scalable, explainable, business-friendly, and aligned with CommerceAI's architecture-first philosophy.
