import time
from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import FastAPI
from fastapi import Request

from app.api.v1.products import router as products_router
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

    try:
        logger.info(
            "Request started method=%s path=%s client=%s",
            request.method,
            request.url.path,
            request.client.host if request.client else "-",
        )

        response = await call_next(request)

        duration_ms = (time.perf_counter() - started_at) * 1000
        response.headers["x-request-id"] = request_id

        logger.info(
            ("Request completed method=%s path=%s " "status_code=%s duration_ms=%.2f"),
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )

        return response
    except Exception:
        duration_ms = (time.perf_counter() - started_at) * 1000
        logger.exception(
            "Request failed method=%s path=%s duration_ms=%.2f",
            request.method,
            request.url.path,
            duration_ms,
        )
        raise
    finally:
        reset_request_id(request_id_token)


app.include_router(
    products_router,
    prefix="/api/v1",
)
