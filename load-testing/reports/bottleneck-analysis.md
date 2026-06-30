# Bottleneck Analysis

## Objective

Identify the primary performance bottlenecks observed during benchmarking.

---

# Benchmark Summary

| Test | Result |
|------|--------|
| Smoke | Healthy |
| Baseline | Excellent |
| Load | Excellent |
| Stress | High latency |
| Spike | Saturation |
| Soak | Stable |

---

# Bottleneck 1 — Application Worker Capacity

Observations

- Stable until approximately 100 concurrent users.
- Latency increased significantly beyond 250 users.
- Queueing became dominant during spike testing.

Impact

- High request waiting time.
- Reduced responsiveness.

Recommendation

- Increase worker count.
- Horizontal scaling.

---

# Bottleneck 2 — Database Layer

Observations

- Product Listing endpoint consistently slower.
- Larger payloads increased response time.

Possible Causes

- Pagination
- Query execution
- Serialization

Recommendations

- Additional indexes
- Query optimization
- Materialized views

---

# Bottleneck 3 — Request Queueing

Evidence

Stress Test

Average latency

31 ms

↓

1178 ms

↓

39006 ms (Spike)

Interpretation

Incoming requests exceeded processing capacity.

---

# Bottleneck 4 — CPU

Observed Behaviour

- All endpoints slowed similarly.

Interpretation

Shared infrastructure bottleneck.

---

# Bottleneck 5 — Redis

Observations

Redis continued functioning.

No evidence that Redis became the primary bottleneck.

---

# Overall Findings

Primary

- Worker saturation
- Request queueing

Secondary

- PostgreSQL
- CPU

Minor

- Redis