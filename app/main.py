import time
from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import FastAPI
from fastapi import Request

from app.api.v1.products import router as products_router
from app.api.v1.health import router as health_router
from app.api.v1.metrics import router as metrics_router
from app.metrics.metrics import REQUEST_COUNT
from app.metrics.metrics import REQUEST_DURATION
from app.core.config import settings
from app.core.logger import get_logger
from app.core.logger import reset_request_id
from app.core.logger import set_request_id


logger = get_logger(
    log_name="application",
    log_folder="system",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(
        "Application startup app=%s version=%s environment=%s",
        settings.app_name,
        settings.app_version,
        settings.environment,
    )

    yield

    logger.info("Application shutdown app=%s", settings.app_name)


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = request.headers.get("x-request-id", str(uuid4()))
    request_id_token = set_request_id(request_id)

    started_at = time.perf_counter()
    status_code = 500

    try:
        logger.info(
            "Request started method=%s path=%s client=%s",
            request.method,
            request.url.path,
            request.client.host if request.client else "-",
        )

        response = await call_next(request)

        status_code = response.status_code
        response.headers["x-request-id"] = request_id

        return response

    except Exception:
        logger.exception(
            "Request failed method=%s path=%s",
            request.method,
            request.url.path,
        )
        raise

    finally:
        duration_seconds = time.perf_counter() - started_at
        duration_ms = duration_seconds * 1000

        REQUEST_COUNT.labels(
            method=request.method,
            path=request.url.path,
            status_code=str(status_code),
        ).inc()

        REQUEST_DURATION.labels(
            method=request.method,
            path=request.url.path,
        ).observe(duration_seconds)

        logger.info(
            "Request completed method=%s path=%s status_code=%s duration_ms=%.2f",
            request.method,
            request.url.path,
            status_code,
            duration_ms,
        )

        reset_request_id(request_id_token)


app.include_router(
    health_router,
    prefix="/api/v1",
)

app.include_router(
    products_router,
    prefix="/api/v1",
)

app.include_router(
    metrics_router,
)
