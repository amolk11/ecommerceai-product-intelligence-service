from fastapi import APIRouter
from fastapi import HTTPException
from sqlalchemy import text

from app.cache.redis_client import get_redis_client
from app.core.database import get_engine
from app.core.logger import get_logger

logger = get_logger(log_name="health", log_folder="system")

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    summary="Liveness Probe",
)
def health():
    """
    Basic liveness check.

    Verifies that the application process is running.
    Does not check external dependencies.
    """

    logger.info("Liveness check requested")

    return {
        "status": "healthy",
        "service": "product-intelligence-service",
        "version": "0.1.0",
    }


@router.get(
    "/ready",
    summary="Readiness Probe",
)
def ready():
    """
    Readiness check.

    Verifies:
    - Database connectivity
    - Redis connectivity
    """

    logger.info("Readiness check requested")

    database_status = "down"
    cache_status = "down"

    try:
        engine = get_engine()

        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        database_status = "up"

        logger.info("Database readiness check successful")

    except Exception:
        logger.exception("Database readiness check failed")

    try:
        redis_client = get_redis_client()

        if redis_client.ping():
            cache_status = "up"

        logger.info("Redis readiness check successful")

    except Exception:
        logger.exception("Redis readiness check failed")

    if database_status != "up" or cache_status != "up":
        logger.warning(
            "Readiness check failed database=%s cache=%s",
            database_status,
            cache_status,
        )

        raise HTTPException(
            status_code=503,
            detail={
                "status": "not_ready",
                "database": database_status,
                "cache": cache_status,
            },
        )

    logger.info(
        "Readiness check successful database=%s cache=%s",
        database_status,
        cache_status,
    )

    return {
        "status": "ready",
        "database": database_status,
        "cache": cache_status,
    }
