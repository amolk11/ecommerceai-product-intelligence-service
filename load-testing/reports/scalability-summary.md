# Scalability Summary

## Objective

Summarize the scalability characteristics of the Product Intelligence Service.

---

# Benchmark Results

| Test | Users | Avg Latency | Failure Rate |
|------|------:|------------:|-------------:|
| Baseline | 20 | 26 ms | 0% |
| Load | 100 | 31 ms | 0% |
| Stress | 250 | 1178 ms | 0% |
| Spike | 500 | 39006 ms | 7.86% |

---

# Scalability Regions

## Region A

20–100 users

Characteristics

- Excellent performance
- Low latency
- Zero failures

Recommended Production Region

✅

---

## Region B

100–250 users

Characteristics

- Throughput increases.
- Latency increases.

Still Stable

✅

---

## Region C

500 users

Characteristics

- Queueing
- Saturation
- Failures

Recommended

❌

---

# Capacity Curve

Excellent

↓

Scalable

↓

Saturation

↓

Failure

---

# Recommendation

Current deployment

Ideal

≈100 concurrent users

Maximum sustainable

≈250 concurrent users

Extreme spike

500 users (degraded)
