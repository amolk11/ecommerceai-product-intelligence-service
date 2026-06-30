# CommerceAI Product Intelligence Service - Load Testing

This directory contains the complete performance testing suite for the CommerceAI Product Intelligence Service.

The objective of this suite is to validate the service under different workload patterns and evaluate its:

- Performance
- Reliability
- Scalability
- Stability
- Burst handling capability
- Long-running operational behavior

The benchmarks were executed using **Locust** while application metrics were collected using **Prometheus** and visualized in **Grafana**.

---

# Directory Structure

```
load-testing/
│
├── locustfile.py
├── config.py
├── test-data.py
├── requirements.txt
├── README.md
│
├── scenarios/
│   ├── smoke.py
│   ├── baseline.py
│   ├── load.py
│   ├── stress.py
│   ├── spike.py
│   └── soak.py
│
├── reports/
│   ├── bottleneck-analysis.md
│   ├── optimization-summary.md
│   ├── scalability-summary.md
│   ├── performance-report.md
│   └── final-conclusion.md
│
└── results/
    ├── aws/
    └── local/
        ├── smoke-v1.md
        ├── baseline-v1.md
        ├── load-v1.md
        ├── stress-v1.md
        ├── spike-v1.md
        └── soak-v1.md
```

---

# Performance Test Matrix

| Test | Purpose |
|-------|---------|
| Smoke | Verify service availability and correctness |
| Baseline | Establish normal operating performance |
| Load | Validate expected production workload |
| Stress | Identify maximum sustainable capacity |
| Spike | Evaluate resilience to sudden traffic bursts |
| Soak | Validate long-term stability |

---

# Test Environment

| Component | Value |
|----------|-------|
| Framework | FastAPI |
| Server | Uvicorn |
| Workers | 1 |
| Database | PostgreSQL |
| Cache | Redis |
| Monitoring | Prometheus + Grafana |
| Load Generator | Locust |

---

# Installation

```bash
pip install -r requirements.txt
```

---

# Running Tests

Start the Product Intelligence Service.

```bash
docker compose up -d
```

Navigate to the load testing directory.

```bash
cd load-testing
```

Start Locust.

```bash
locust -f scenarios/baseline.py --host=http://localhost:8000
```

Open

```
http://localhost:8089
```

Configure the desired workload and start the benchmark.

---

# Available Scenarios

## Smoke Test

```bash
locust -f scenarios/smoke.py --host=http://localhost:8000
```

---

## Baseline Test

```bash
locust -f scenarios/baseline.py --host=http://localhost:8000
```

---

## Load Test

```bash
locust -f scenarios/load.py --host=http://localhost:8000
```

---

## Stress Test

```bash
locust -f scenarios/stress.py --host=http://localhost:8000
```

---

## Spike Test

```bash
locust -f scenarios/spike.py --host=http://localhost:8000
```

---

## Soak Test

```bash
locust -f scenarios/soak.py --host=http://localhost:8000
```

---

# Monitoring

Performance metrics are collected using Prometheus and visualized using Grafana.

Useful dashboards include:

- Request Throughput
- Average Latency
- API Success Rate
- Authentication Success Rate
- Cache Hit Rate
- CPU Utilization
- Memory Utilization

---

# Benchmark Results

Detailed benchmark reports are available under:

```
results/local/
```

Engineering analysis is available under:

```
reports/
```

---

# Summary

The Product Intelligence Service was successfully evaluated under multiple workload patterns.

The benchmark suite established:

- Expected production performance
- Maximum sustainable throughput
- Burst handling capability
- Long-term operational stability
- Current scalability limits

These benchmarks provide the performance baseline for future versions of the Product Intelligence Service.