from unittest.mock import MagicMock
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "product-intelligence-service",
        "version": "0.1.0",
    }


@patch("app.api.v1.health.get_redis_client")
@patch("app.api.v1.health.get_engine")
def test_ready_success(
    mock_get_engine,
    mock_get_redis_client,
) -> None:
    mock_connection = MagicMock()
    mock_engine = MagicMock()

    mock_engine.connect.return_value.__enter__.return_value = (
        mock_connection
    )

    mock_get_engine.return_value = mock_engine

    mock_redis = MagicMock()
    mock_redis.ping.return_value = True
    mock_get_redis_client.return_value = mock_redis

    response = client.get("/api/v1/ready")

    assert response.status_code == 200

    assert response.json() == {
        "status": "ready",
        "database": "up",
        "cache": "up",
    }


@patch("app.api.v1.health.get_redis_client")
@patch("app.api.v1.health.get_engine")
def test_ready_database_failure(
    mock_get_engine,
    mock_get_redis_client,
) -> None:
    mock_get_engine.side_effect = Exception("db down")

    mock_redis = MagicMock()
    mock_redis.ping.return_value = True
    mock_get_redis_client.return_value = mock_redis

    response = client.get("/api/v1/ready")

    assert response.status_code == 503

    assert response.json() == {
        "detail": {
            "status": "not_ready",
            "database": "down",
            "cache": "up",
        }
    }


@patch("app.api.v1.health.get_redis_client")
@patch("app.api.v1.health.get_engine")
def test_ready_redis_failure(
    mock_get_engine,
    mock_get_redis_client,
) -> None:
    mock_connection = MagicMock()
    mock_engine = MagicMock()

    mock_engine.connect.return_value.__enter__.return_value = (
        mock_connection
    )

    mock_get_engine.return_value = mock_engine

    mock_redis = MagicMock()
    mock_redis.ping.side_effect = Exception("redis down")
    mock_get_redis_client.return_value = mock_redis

    response = client.get("/api/v1/ready")

    assert response.status_code == 503

    assert response.json() == {
        "detail": {
            "status": "not_ready",
            "database": "up",
            "cache": "down",
        }
    }
    