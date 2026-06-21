from fastapi import Header
from fastapi import HTTPException
from fastapi import status

from platform_core.auth import validate_api_key
from platform_core.database import get_platform_engine

from app.core.logger import get_logger

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

    logger.debug("Authentication request received")

    if not x_api_key:
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
        logger.exception("Authentication validation error")

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication service unavailable",
        )

    if client is None:
        logger.warning("Authentication failed reason=invalid_api_key")

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    logger.info(
        "Authentication successful client_id=%s client_name=%s",
        client.get("client_id"),
        client.get("client_name"),
    )

    return client
