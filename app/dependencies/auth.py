from fastapi import Header
from fastapi import HTTPException
from fastapi import status

from platform_core.auth import validate_api_key
from platform_core.database import get_platform_engine

from app.core.logger import get_logger
from app.metrics.metrics import (
    AUTH_REQUESTS_TOTAL,
    AUTH_SUCCESS_TOTAL,
    AUTH_MISSING_API_KEY_TOTAL,
    AUTH_INVALID_API_KEY_TOTAL,
    AUTH_SERVICE_ERRORS_TOTAL,
)

logger = get_logger(
    log_name="authentication",
    log_folder="security",
)


def get_auth_engine():
    return get_platform_engine()


def validate_client_api_key(connection, api_key: str):
    return validate_api_key(
        connection=connection,
        api_key=api_key,
    )


def get_current_client(
    x_api_key: str | None = Header(
        default=None,
        alias="X-API-Key",
    ),
) -> dict:

    AUTH_REQUESTS_TOTAL.inc()

    logger.debug("Authentication request received")

    if not x_api_key:
        AUTH_MISSING_API_KEY_TOTAL.inc()

        logger.warning("Authentication failed reason=missing_api_key")

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is required",
        )

    logger.debug("Validating API key")

    try:
        engine = get_auth_engine()

        with engine.connect() as connection:
            client = validate_client_api_key(
                connection=connection,
                api_key=x_api_key,
            )

    except Exception:
        AUTH_SERVICE_ERRORS_TOTAL.inc()

        logger.exception("Authentication validation error")

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication service unavailable",
        )

    if client is None:
        AUTH_INVALID_API_KEY_TOTAL.inc()

        logger.warning("Authentication failed reason=invalid_api_key")

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
    AUTH_SUCCESS_TOTAL.inc()

    logger.info(
        "Authentication successful client_id=%s client_name=%s",
        client.get("client_id"),
        client.get("client_name"),
    )

    return client
