# Smoke Test Report (v1)

**Service:** CommerceAI Product Intelligence Service  
**Test Type:** Smoke Test  
**Environment:** Local Development  
**Date:** 30 June 2026  
**Status:** ✅ Passed

---

# 1. Objective

The objective of this smoke test was to verify that the Product Intelligence Service is operational and capable of handling a light production-like workload before executing more intensive performance benchmarks.

The test validates:

- API availability
- Authentication
- Database connectivity
- Redis connectivity
- Endpoint accessibility
- Basic response latency
- Request success rate

This test is **not intended to evaluate system limits**.

---

# 2. Test Environment

| Component | Value |
|-----------|-------|
| Environment | Local |
| Host | http://localhost:8000 |
| Load Testing Tool | Locust |
| Database | PostgreSQL |
| Cache | Redis |
| Monitoring | Prometheus + Grafana |

---

# 3. Workload Configuration

| Parameter | Value |
|-----------|-------|
| Concurrent Users | 5 |
| Spawn Rate | 1 user/sec |
| Test Duration | 2 minutes |
| Wait Time | 1–3 seconds |

---

# 4. Endpoint Distribution

| Endpoint | Weight |
|----------|--------|
| GET /api/v1/products | 40% |
| GET /api/v1/products/{product_id}/profile | 45% |
| GET /api/v1/products/top | 15% |

---

# 5. Test Results

## Overall Summary

| Metric | Value |
|---------|------:|
| Total Requests | 286 |
| Failed Requests | 0 |
| Failure Rate | **0%** |
| Average Response Time | **77.54 ms** |
| Median Response Time | **46 ms** |
| 95th Percentile | **210 ms** |
| 99th Percentile | **290 ms** |
| Maximum Response Time | **304 ms** |
| Average Throughput | **2.39 Requests/sec** |

---

## Endpoint Performance

| Endpoint | Requests | Avg (ms) | Median (ms) | P95 (ms) | Max (ms) |
|----------|---------:|---------:|------------:|----------:|---------:|
| GET /products | 119 | 134.96 | 120 | 270 | 304 |
| GET /products/{product_id}/profile | 126 | 33.51 | 28 | 94 | 154 |
| GET /products/top | 41 | 46.18 | 29 | 150 | 171 |

---

# 6. Observations

### Authentication

The initial execution failed due to missing API authentication headers (HTTP 401 Unauthorized). After configuring Locust to load the API key from the environment and include the `X-API-Key` header, the smoke test completed successfully with zero failures.

### API Stability

- No HTTP 5xx errors observed.
- No request failures.
- All endpoints remained available throughout the test.

### Response Time

The Product Profile endpoint demonstrated the lowest average latency, while the Product Listing endpoint exhibited comparatively higher response times due to pagination and the larger response payload.

### Reliability

The service remained stable during the entire execution with no crashes or connectivity issues.

---

# 7. Assessment

| Validation | Result |
|------------|--------|
| API Reachable | ✅ |
| Authentication Working | ✅ |
| PostgreSQL Connectivity | ✅ |
| Redis Connectivity | ✅ |
| Zero Request Failures | ✅ |
| Stable Response Times | ✅ |

---

# 8. Conclusion

The Product Intelligence Service successfully passed the smoke test under a light production-like workload.

The service demonstrated:

- Correct authentication handling
- Stable API availability
- Reliable request processing
- Zero request failures
- Consistent response times

With the service health verified, it is ready to proceed to baseline performance benchmarking under increased load.

---

# 9. Next Test

**Baseline Performance Test (v1)**

Objective:

Evaluate the steady-state performance of the Product Intelligence Service under normal expected production traffic and establish baseline latency, throughput, and reliability metrics for future optimization and regression testing.
