# Stress Performance Test Report (v1)

**Service:** CommerceAI Product Intelligence Service  
**Test Type:** Stress Test  
**Environment:** Local (Docker Compose)  
**Date:** 30 June 2026  
**Status:** ✅ Completed Successfully

---

# 1. Objective

The objective of the stress test was to push the Product Intelligence Service beyond its expected production workload in order to identify its performance limits, measure scalability under heavy traffic, and observe system behaviour as resources approach saturation.

Unlike the load test, this benchmark intentionally exceeds normal operating conditions to identify bottlenecks and degradation characteristics.

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
| Concurrent Users | 250 |
| Spawn Rate | 20 users/sec |
| Duration | 15 Minutes |
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
| Total Requests | **83,219** |
| Failed Requests | **0** |
| Failure Rate | **0%** |
| Average Response Time | **1,177.94 ms** |
| Median Response Time | **1,200 ms** |
| 95th Percentile | **1,700 ms** |
| 99th Percentile | **1,900 ms** |
| Maximum Response Time | **2,500 ms** |
| Average Throughput | **88.5 Requests/sec** |

---

# 6. Endpoint Performance

| Endpoint | Requests | Avg (ms) | Median (ms) | P95 (ms) | P99 (ms) | Max (ms) |
|----------|---------:|---------:|------------:|---------:|---------:|---------:|
| GET /products | 33,546 | 1,248.35 | 1,300 | 1,800 | 2,000 | 2,500 |
| GET /products/{product_id}/profile | 37,093 | 1,131.48 | 1,200 | 1,600 | 1,800 | 2,152 |
| GET /products/top | 12,580 | 1,127.18 | 1,200 | 1,600 | 1,800 | 2,204 |

---

# 7. Performance Analysis

## Reliability

Despite operating well beyond normal production load, the Product Intelligence Service maintained complete functional reliability.

- Zero failed requests
- Zero HTTP 5xx responses
- Zero authentication failures
- No service crashes

The application continued serving requests throughout the entire benchmark.

---

## Throughput

The service achieved an average throughput of approximately **88.5 requests per second**, representing the highest throughput observed during testing.

Compared with previous benchmarks:

| Test | Throughput |
|------|-----------:|
| Baseline | 12.9 req/s |
| Load | 65.6 req/s |
| Stress | 88.5 req/s |

Although throughput continued to increase, the improvement was significantly smaller than the increase in workload, indicating diminishing returns.

---

## Response Time

Latency increased dramatically under stress.

| Test | Average Latency |
|------|----------------:|
| Baseline | 26.62 ms |
| Load | 31.21 ms |
| Stress | 1,177.94 ms |

The average response time increased by nearly **38×** compared to the load test.

Median response time stabilized around **1.2 seconds**, indicating that request queuing and resource contention had become significant.

---

## Endpoint Behaviour

All endpoints exhibited similar latency characteristics under stress.

This suggests that the bottleneck was **shared infrastructure** (application server, database connection pool, CPU scheduling, or I/O) rather than endpoint-specific business logic.

The Product Listing endpoint remained the slowest endpoint, but the difference between endpoints became relatively small under heavy load.

---

## Scalability

The system continued scaling in terms of throughput, but latency increased disproportionately.

This behaviour indicates that the application reached its efficient operating limit somewhere between the Load Test and the Stress Test.

Beyond this point:

- Requests continued to complete successfully.
- Response times increased substantially.
- User experience would begin to degrade.
- Additional concurrency yielded diminishing performance gains.

---

# 8. Comparison with Previous Tests

| Metric | Baseline | Load | Stress |
|---------|---------:|-----:|-------:|
| Users | 20 | 100 | 250 |
| Requests | 3,902 | 38,812 | 83,219 |
| Failures | 0 | 0 | 0 |
| Average Latency | 26.62 ms | 31.21 ms | 1,177.94 ms |
| P95 | 58 ms | 69 ms | 1,700 ms |
| Throughput | 12.9 req/s | 65.6 req/s | 88.5 req/s |

---

# 9. Bottleneck Assessment

The benchmark indicates that the Product Intelligence Service remained stable under stress but entered a latency-dominated operating region.

Observed characteristics:

- No functional failures
- Stable throughput
- High request completion rate
- Significant increase in response latency
- Evidence of request queuing

Potential limiting resources include:

- CPU availability
- Database connection pool
- PostgreSQL query execution
- Application worker capacity
- Redis request serialization

Further infrastructure monitoring would be required to identify the primary bottleneck.

---

# 10. Key Findings

- ✅ 83,219 successful requests processed
- ✅ Zero request failures
- ✅ Stable application behaviour
- ✅ Highest throughput achieved during testing
- ⚠ Average latency exceeded one second
- ⚠ System reached its practical operating limit under sustained stress

---

# 11. Conclusion

The Product Intelligence Service successfully survived sustained stress without experiencing application failures.

The benchmark demonstrates excellent stability and fault tolerance.

However, the significant increase in response latency indicates that the service reached resource saturation under this workload. While throughput continued to increase, the associated latency would likely impact end-user experience.

Based on current results, the service's optimal operating region lies closer to the Load Test workload, while the Stress Test identifies the upper boundary of acceptable scalability for the current deployment configuration.

---

# 12. Next Test

## Spike Test (v1)

**Objective**

Evaluate the Product Intelligence Service's ability to handle sudden, short-duration traffic spikes and observe how quickly it absorbs and recovers from abrupt workload changes.