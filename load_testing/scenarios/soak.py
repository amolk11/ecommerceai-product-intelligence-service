"""
Soak Test Scenario

Purpose:
    Evaluate the long-term stability of the Product Intelligence Service
    under sustained production-like traffic.

This test is designed to identify:
    - Memory leaks
    - CPU growth
    - Database connection leaks
    - Redis stability
    - Throughput degradation
    - Latency drift

Workload:
    - 100 concurrent users
    - Spawn rate: 10 users/sec
    - Duration: 60 minutes
    - Wait time: 1–2 seconds

Endpoint Distribution:
    - GET /api/v1/products                  -> 40%
    - GET /api/v1/products/{id}/profile     -> 45%
    - GET /api/v1/products/top              -> 15%
"""

from random import choice

from locust import HttpUser, between, task

from config import API_KEY

PRODUCT_IDS = [
    1,
    10,
    25,
    50,
    99,
    100,
    250,
    500,
    1000,
    2500,
    5000,
]


class SoakTestUser(HttpUser):
    """
    Simulates sustained production traffic.
    """

    wait_time = between(1, 2)

    def on_start(self):
        self.client.headers.update(
            {
                "X-API-Key": API_KEY,
                "Accept": "application/json",
            }
        )

    @task(40)
    def list_products(self):
        self.client.get(
            "/api/v1/products?page=1&page_size=20",
            name="GET /products",
        )

    @task(45)
    def product_profile(self):
        product_id = choice(PRODUCT_IDS)

        self.client.get(
            f"/api/v1/products/{product_id}/profile",
            name="GET /products/{id}/profile",
        )

    @task(15)
    def top_products(self):
        self.client.get(
            "/api/v1/products/top?metric=performance&limit=20",
            name="GET /products/top",
        )
