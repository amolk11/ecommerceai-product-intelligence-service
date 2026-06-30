# Spike Performance Test Report (v1)

**Service:** CommerceAI Product Intelligence Service  
**Test Type:** Spike Test  
**Environment:** Local (Docker Compose)  
**Date:** 30 June 2026  
**Status:** ✅ Completed (Service Saturation Observed)

---

# 1. Objective

The objective of the spike test was to evaluate the Product Intelligence Service's ability to withstand an abrupt and substantial increase in traffic.

The benchmark simulates sudden real-world traffic bursts such as:

- Flash sales
- Marketing campaigns
- Viral product launches
- Push notification events

The primary focus is to observe service resilience, latency behaviour, and failure characteristics during a rapid traffic surge.

---

# 2. Test Environment

| Component | Value |
|-----------|-------|
| Environment | Local (Docker Compose) |
| Application Server | FastAPI + Uvicorn |
| Uvicorn Workers | 1 |
| Database | PostgreSQL |
| Cache | Redis |
| Monitoring | Prometheus + Grafana |
| Load Testing Tool | Locust |

---

# 3. Workload Configuration

| Parameter | Value |
|-----------|-------|
| Concurrent Users | 500 |
| Spawn Rate | 100 users/sec |
| Duration | 5 Minutes |
| Wait Time | 1–2 Seconds |

---

# 4. Endpoint Distribution

| Endpoint | Weight |
|----------|--------|
| GET /api/v1/products | 40% |
| GET /api/v1/products/{product_id}/profile | 45% |
| GET /api/v1/products/top | 15% |

---

# 5. Overall Results

| Metric | Value |
|---------|------:|
| Total Requests | **3,155** |
| Failed Requests | **248** |
| Failure Rate | **7.86%** |
| Average Response Time | **39,006.43 ms** |
| Median Response Time | **33,000 ms** |
| 95th Percentile | **94,000 ms** |
| 99th Percentile | **94,000 ms** |
| Maximum Response Time | **94,509 ms** |

---

# 6. Endpoint Performance

| Endpoint | Requests | Failures | Avg (ms) | P95 (ms) | Max (ms) |
|----------|---------:|---------:|---------:|---------:|---------:|
| GET /products | 1,284 | 248 | 39,104.31 | 94,000 | 94,509 |
| GET /products/{product_id}/profile | 1,399 | 0 | 38,907.23 | 94,000 | 94,408 |
| GET /products/top | 472 | 0 | 39,034.20 | 94,000 | 94,384 |

---

# 7. Performance Analysis

## Reliability

The Product Intelligence Service remained operational throughout the traffic spike and did not crash.

However, the sudden increase in concurrent requests exceeded the processing capacity of the current deployment, resulting in request queuing and a measurable failure rate.

Overall request failure rate reached **7.86%**.

---

## Response Time

Latency increased dramatically immediately after the traffic surge.

| Test | Average Latency |
|------|----------------:|
| Baseline | 26.62 ms |
| Load | 31.21 ms |
| Stress | 1,177.94 ms |
| Spike | 39,006.43 ms |

The median response time reached **33 seconds**, while the slowest requests required approximately **94 seconds** to complete.

These values indicate that the application became saturated almost immediately after the spike occurred.

---

## Endpoint Behaviour

All endpoints experienced similar latency characteristics, suggesting that the bottleneck occurred within shared infrastructure rather than endpoint-specific business logic.

The Product Listing endpoint experienced **248 failed requests**, while the remaining endpoints continued processing requests successfully, although with extremely high response times.

---

## Burst Handling

The benchmark demonstrates that the service remained available during the spike but was unable to absorb the sudden workload without significant request queuing.

The system prioritised completing queued requests rather than rejecting connections, resulting in very high response times.

---

# 8. Comparison with Previous Tests

| Metric | Baseline | Load | Stress | Spike |
|---------|---------:|-----:|-------:|------:|
| Users | 20 | 100 | 250 | 500 |
| Requests | 3,902 | 38,812 | 83,219 | 3,155 |
| Failure Rate | 0% | 0% | 0% | 7.86% |
| Average Latency | 26.62 ms | 31.21 ms | 1,177.94 ms | 39,006.43 ms |

---

# 9. Key Findings

- ✅ Service remained operational throughout the benchmark.
- ✅ No application crash observed.
- ⚠ Sudden traffic surge caused immediate request queuing.
- ⚠ Average response time increased to approximately 39 seconds.
- ⚠ Product Listing endpoint experienced request failures.
- ⚠ Current deployment configuration cannot absorb a burst of 500 concurrent users while maintaining acceptable latency.

---

# 10. Conclusion

The Product Intelligence Service successfully survived an extreme traffic spike without experiencing a complete service outage.

The benchmark clearly identifies the burst-handling limit of the current deployment. While the application continued processing requests, the abrupt increase in concurrency caused extensive request queuing, substantial latency growth, and a moderate request failure rate.

These results indicate that the current single-worker deployment is appropriate for expected production traffic but would require additional optimization or horizontal scaling to efficiently handle sudden large-scale traffic bursts.

---

# 11. Next Test

## Soak Test (v1)

**Objective**

Evaluate the long-term stability of the Product Intelligence Service under sustained production-level traffic by monitoring response latency, throughput, error rates, and resource utilization over an extended execution period.
