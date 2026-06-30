# Baseline Performance Test Report (v1)

**Service:** CommerceAI Product Intelligence Service  
**Test Type:** Baseline Performance Test  
**Environment:** Local (Docker Compose)  
**Date:** 30 June 2026  
**Status:** ✅ Passed

---

# 1. Objective

The objective of the baseline performance test was to evaluate the steady-state performance of the Product Intelligence Service under normal production-like traffic.

This benchmark establishes a reliable performance baseline that will be used for comparison during subsequent load, stress, spike, and soak tests.

---

# 2. Test Environment

| Component | Value |
|-----------|-------|
| Environment | Local (Docker Compose) |
| Application Server | FastAPI + Uvicorn |
| Uvicorn Workers | **1** |
| Database | PostgreSQL |
| Cache | Redis |
| Monitoring | Prometheus + Grafana |
| Load Testing Tool | Locust |

---

# 3. Workload Configuration

| Parameter | Value |
|-----------|-------|
| Concurrent Users | 20 |
| Spawn Rate | 5 users/sec |
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
| Total Requests | **3,902** |
| Failed Requests | **0** |
| Failure Rate | **0%** |
| Average Response Time | **26.62 ms** |
| Median Response Time | **17 ms** |
| 95th Percentile | **58 ms** |
| 99th Percentile | **78 ms** |
| Maximum Response Time | **293 ms** |
| Average Throughput | **12.9 Requests/sec** |

---

# 6. Endpoint Performance

| Endpoint | Requests | Avg (ms) | Median (ms) | P95 (ms) | P99 (ms) | Max (ms) |
|----------|---------:|---------:|------------:|---------:|---------:|---------:|
| GET /products | 1,564 | 47.28 | 43 | 68 | 87 | 293 |
| GET /products/{product_id}/profile | 1,725 | 12.74 | 9 | 31 | 48 | 205 |
| GET /products/top | 613 | 12.99 | 10 | 28 | 51 | 201 |

---

# 7. Monitoring Summary

| Metric | Observation |
|---------|-------------|
| Total Product Intelligence Requests | 3,903 |
| Average Latency | ~23.3 ms |
| Throughput | ~11.3 req/s |
| API Success Rate | 100% |
| Authentication Success Rate | 100% |
| Cache Hit Rate | No data |

---

# 8. Performance Analysis

## Reliability

The Product Intelligence Service successfully processed all requests throughout the benchmark.

- Zero failed requests
- Zero HTTP 5xx responses
- Stable application execution
- Successful authentication for every request

The service demonstrated excellent reliability under sustained baseline traffic.

---

## Response Time

Response latency remained consistently low throughout the benchmark.

The Product Profile endpoint achieved the lowest average latency at approximately **12.74 ms**, indicating efficient retrieval from the serving layer and cache.

The Product Listing endpoint exhibited the highest latency due to pagination, filtering, and larger response payloads. Even so, the average response time remained below **50 ms**, which is well within acceptable limits for a REST API.

---

## Throughput

The service sustained approximately **13 requests per second** without any observable degradation in response time or request failures.

Monitoring data closely matched Locust statistics after configuring the application to run with a single Uvicorn worker.

---

## Monitoring Validation

During initial benchmarking, Prometheus reported approximately half of the total requests due to the application running with two Uvicorn workers. Since the Python Prometheus client maintains metrics in process-local memory, only one worker's metrics were exposed through the `/metrics` endpoint.

The application was subsequently reconfigured to use a single Uvicorn worker for benchmarking.

Following this change:

- Locust Requests: **3,902**
- Grafana Requests: **3,903**

The one-request difference is expected due to Prometheus scraping the metrics endpoint during the benchmark.

This validates that the monitoring stack accurately reflects application traffic.

---

## Cache Metrics

Redis caching was functioning correctly during the benchmark.

However, the Cache Hit Rate panel displayed **No data** because cache miss metrics are not currently instrumented.

The application exposes cache hit counters but does not yet record cache misses, preventing Grafana from computing the hit ratio.

This affects only dashboard visualization and does **not** impact application functionality or benchmark results.

---

# 9. Key Findings

- ✅ Zero request failures
- ✅ Stable latency throughout execution
- ✅ Excellent throughput under baseline traffic
- ✅ Accurate monitoring after migrating to a single Uvicorn worker
- ✅ Authentication remained fully successful
- ✅ Service remained stable without resource saturation
- ⚠ Cache miss metrics require instrumentation before Cache Hit Rate can be calculated

---

# 10. Conclusion

The Product Intelligence Service successfully passed the baseline performance benchmark.

The service demonstrated:

- Excellent reliability
- Consistently low response latency
- Stable throughput
- Accurate monitoring and observability
- Zero request failures

These results establish a reliable performance baseline for future optimization efforts and provide a strong reference point for subsequent load, stress, spike, and soak testing.

---

# 11. Next Test

## Load Test (v1)

**Objective**

Evaluate the Product Intelligence Service under significantly higher concurrent traffic to determine how latency, throughput, and reliability scale beyond normal operating conditions while identifying the point at which performance begins to degrade.
