from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from fastapi import HTTPException

from app.dependencies.auth import get_current_client


def test_get_current_client_raises_when_api_key_missing():
    with pytest.raises(HTTPException) as exc:
        get_current_client(None)

    assert exc.value.status_code == 401
    assert exc.value.detail == "API key is required"


@patch("app.dependencies.auth.validate_client_api_key")
@patch("app.dependencies.auth.get_auth_engine")
def test_get_current_client_raises_when_api_key_invalid(
    mock_get_engine,
    mock_validate,
):
    mock_connection = MagicMock()

    mock_engine = MagicMock()
    mock_engine.connect.return_value.__enter__.return_value = mock_connection

    mock_get_engine.return_value = mock_engine
    mock_validate.return_value = None

    with pytest.raises(HTTPException) as exc:
        get_current_client("invalid-key")

    assert exc.value.status_code == 401
    assert exc.value.detail == "Invalid API key"


@patch("app.dependencies.auth.validate_client_api_key")
@patch("app.dependencies.auth.get_auth_engine")
def test_get_current_client_returns_authenticated_client(
    mock_get_engine,
    mock_validate,
):
    mock_connection = MagicMock()

    mock_engine = MagicMock()
    mock_engine.connect.return_value.__enter__.return_value = mock_connection

    mock_get_engine.return_value = mock_engine

    expected_client = {
        "client_id": "test-client",
        "client_name": "Test Client",
    }

    mock_validate.return_value = expected_client

    result = get_current_client("valid-key")

    assert result == expected_client


@patch("app.dependencies.auth.get_auth_engine")
def test_get_current_client_raises_when_auth_service_unavailable(
    mock_get_engine,
):
    mock_get_engine.side_effect = Exception("database unavailable")

    with pytest.raises(HTTPException) as exc:
        get_current_client("valid-key")

    assert exc.value.status_code == 503
    assert exc.value.detail == "Authentication service unavailable"
