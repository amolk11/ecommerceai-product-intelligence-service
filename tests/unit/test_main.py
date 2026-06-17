import pytest
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response

from app.main import app
from app.main import lifespan
from app.main import log_requests


@pytest.mark.asyncio
async def test_lifespan_runs_startup_and_shutdown():
    async with lifespan(FastAPI()):
        assert True


def test_log_requests_adds_request_id_response_header(client):
    response = client.get(
        "/api/v1/products",
        headers={"x-request-id": "request-123"},
    )

    assert response.status_code == 200
    assert response.headers["x-request-id"] == "request-123"


@pytest.mark.asyncio
async def test_log_requests_propagates_handler_exceptions():
    request = Request(
        {
            "type": "http",
            "method": "GET",
            "path": "/boom",
            "headers": [],
            "client": ("testclient", 50000),
            "server": ("testserver", 80),
            "scheme": "http",
            "query_string": b"",
        }
    )

    async def failing_call_next(_request):
        raise RuntimeError("boom")

    with pytest.raises(RuntimeError, match="boom"):
        await log_requests(request, failing_call_next)


@pytest.mark.asyncio
async def test_log_requests_handles_request_without_client():
    request = Request(
        {
            "type": "http",
            "method": "GET",
            "path": "/health",
            "headers": [],
            "client": None,
            "server": ("testserver", 80),
            "scheme": "http",
            "query_string": b"",
        }
    )

    async def ok_call_next(_request):
        return Response(status_code=204)

    response = await log_requests(request, ok_call_next)

    assert response.status_code == 204
    assert "x-request-id" in response.headers


def test_app_registers_products_router():
    route_paths = {route.path for route in app.routes}

    assert "/api/v1/products" in route_paths
    assert "/api/v1/products/top" in route_paths
    assert "/api/v1/products/{product_id}/profile" in route_paths
    assert "/api/v1/products/{product_id}/insights" in route_paths
