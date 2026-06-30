"""
Spike Performance Test

Purpose:
    Evaluate the Product Intelligence Service's ability to
    absorb sudden bursts of traffic and recover gracefully.

Workload:
    - 500 concurrent users
    - Spawn rate: 100 users/sec
    - Duration: 5 minutes
    - Wait time: 1–2 seconds

Endpoint Distribution:
    - GET /api/v1/products                  -> 40%
    - GET /api/v1/products/{id}/profile     -> 45%
    - GET /api/v1/products/top              -> 15%
"""

from pathlib import Path
import sys
from random import choice

from locust import HttpUser
from locust import between
from locust import task

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config import API_KEY
from test_data import (
    API_PRODUCTS,
    API_PRODUCT_PROFILE,
    API_TOP_PRODUCTS,
    DEFAULT_PAGE,
    DEFAULT_PAGE_SIZE,
    PRODUCT_IDS,
    TOP_PRODUCTS_LIMIT,
    TOP_PRODUCTS_METRIC,
)


class SpikeUser(HttpUser):
    """
    Simulates a sudden burst of traffic to evaluate
    application resilience and recovery.
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
            f"{API_PRODUCTS}?page={DEFAULT_PAGE}&page_size={DEFAULT_PAGE_SIZE}",
            name="GET /products",
        )

    @task(45)
    def product_profile(self):
        self.client.get(
            API_PRODUCT_PROFILE.format(
                product_id=choice(PRODUCT_IDS),
            ),
            name="GET /products/{id}/profile",
        )

    @task(15)
    def top_products(self):
        self.client.get(
            f"{API_TOP_PRODUCTS}?metric={TOP_PRODUCTS_METRIC}&limit={TOP_PRODUCTS_LIMIT}",
            name="GET /products/top",
        )
