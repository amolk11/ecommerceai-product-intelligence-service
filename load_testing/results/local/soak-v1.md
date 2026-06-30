# Soak Performance Test Report (v1)

**Service:** CommerceAI Product Intelligence Service  
**Test Type:** Soak Test  
**Environment:** Local (Docker Compose)  
**Date:** 30 June 2026  
**Duration:** 30 Minutes  
**Status:** ✅ Passed

---

# 1. Objective

The objective of the soak test was to evaluate the long-term stability of the Product Intelligence Service under sustained production-like traffic.

Unlike stress or spike testing, a soak test focuses on identifying:

- Memory leaks
- Resource exhaustion
- Connection pool exhaustion
- Throughput degradation over time
- Response time drift
- Overall application stability

The goal is to verify that the application can continuously process requests over an extended period without performance degradation.

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
| Concurrent Users | 100 |
| Spawn Rate | 10 users/sec |
| Duration | 30 Minutes |
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
| Total Requests | **116,772** |
| Failed Requests | **0** |
| Failure Rate | **0%** |
| Average Response Time | **33.52 ms** |
| Median Response Time | **20 ms** |
| 95th Percentile | **71 ms** |
| 99th Percentile | **150 ms** |
| Maximum Response Time | **1,869 ms** |
| Average Throughput | **66 Requests/sec** |

---

# 6. Endpoint Performance

| Endpoint | Requests | Avg (ms) | Median (ms) | P95 (ms) | P99 (ms) | Max (ms) |
|----------|---------:|---------:|------------:|---------:|---------:|---------:|
| GET /products | 46,661 | 57.37 | 49 | 84 | 200 | 1,869 |
| GET /products/{product_id}/profile | 52,517 | 17.58 | 12 | 34 | 110 | 1,292 |
| GET /products/top | 17,594 | 17.82 | 12 | 35 | 120 | 1,294 |

---

# 7. Performance Analysis

## Reliability

The Product Intelligence Service remained completely stable throughout the benchmark.

The application successfully processed every request without failures.

Observed during the test:

- Zero failed requests
- Zero HTTP 5xx responses
- Stable authentication
- Stable Redis connectivity
- Stable PostgreSQL connectivity
- No application restarts

The benchmark demonstrates excellent operational reliability.

---

## Response Time Stability

Average response latency remained remarkably stable during the entire 30-minute execution.

| Metric | Value |
|---------|------:|
| Average | 33.52 ms |
| Median | 20 ms |
| P95 | 71 ms |
| P99 | 150 ms |

No noticeable latency drift was observed during the benchmark.

This indicates that the application maintained consistent processing performance over time.

---

## Throughput

The service maintained an average throughput of approximately **66 requests per second** throughout the benchmark.

Unlike stress or spike testing, throughput remained nearly constant during the entire execution.

This demonstrates that the application is capable of sustaining continuous production traffic without throughput degradation.

---

## Endpoint Behaviour

The Product Profile endpoint continued to provide the fastest responses, averaging approximately **18 ms**.

The Product Ranking endpoint also maintained excellent response times.

The Product Listing endpoint remained the slowest endpoint because of pagination and larger response payloads, yet still averaged less than **60 ms**.

No endpoint exhibited progressive slowdown.

---

## Long-Term Stability

One of the primary objectives of a soak test is to identify gradual degradation.

During this benchmark, no evidence of the following issues was observed:

- Memory leaks
- CPU degradation
- Increasing response latency
- Connection pool exhaustion
- Redis instability
- Database instability

The application maintained consistent behaviour throughout the full 30-minute execution.

---

# 8. Comparison with Previous Tests

| Test | Users | Requests | Failure Rate | Avg Latency | Throughput |
|------|------:|---------:|-------------:|------------:|-----------:|
| Smoke | 5 | 286 | 0% | 77.54 ms | 2.39 req/s |
| Baseline | 20 | 3,902 | 0% | 26.62 ms | 12.9 req/s |
| Load | 100 | 38,812 | 0% | 31.21 ms | 65.6 req/s |
| Stress | 250 | 83,219 | 0% | 1,177.94 ms | 88.5 req/s |
| Spike | 500 | 3,155 | 7.86% | 39,006.43 ms | Saturated |
| **Soak (30 min)** | **100** | **116,772** | **0%** | **33.52 ms** | **66 req/s** |

---

# 9. Key Findings

- ✅ 116,772 successful requests processed
- ✅ Zero request failures
- ✅ Stable throughput throughout the benchmark
- ✅ Stable response latency
- ✅ No observable performance degradation
- ✅ No memory leak symptoms
- ✅ No connection pool exhaustion
- ✅ No application instability

---

# 10. Conclusion

The Product Intelligence Service successfully passed the 30-minute soak test.

The benchmark demonstrates that the application can continuously sustain production-level traffic while maintaining:

- Excellent reliability
- Stable throughput
- Low response latency
- Zero request failures
- Consistent endpoint performance

Unlike the stress and spike tests, which intentionally exceeded the application's capacity, the soak test validates that the service remains stable under realistic production workloads for an extended duration.

No evidence of gradual performance degradation or resource exhaustion was observed.

---

# 11. Overall Performance Assessment

The complete performance evaluation identifies three distinct operating regions.

| Operating Region | Observation |
|------------------|-------------|
| **Normal Operation (20–100 Users)** | Excellent performance with low latency and zero failures. |
| **Heavy Load (~250 Users)** | Stable operation with increased latency but no request failures. |
| **Extreme Burst (500 Users)** | Service remains operational but experiences significant request queuing, high latency, and request failures. |

The soak test confirms that the **recommended operating region** (100 concurrent users) can be sustained continuously without observable degradation.

---

# 12. Next Steps

The performance evaluation indicates that the current deployment is suitable for expected production workloads.

Future optimization efforts may include:

- Increasing Uvicorn workers (with Prometheus multiprocess support)
- Database query optimization
- Additional Redis caching
- Connection pool tuning
- Horizontal scaling using multiple application instances
- Load balancing across application replicas

These optimizations would further improve scalability and increase the service's capacity under heavy and burst traffic while preserving the excellent stability demonstrated during the soak benchmark.
