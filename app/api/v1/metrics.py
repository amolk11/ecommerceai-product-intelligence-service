from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.responses import Response
from prometheus_client import CONTENT_TYPE_LATEST
from prometheus_client import generate_latest

from app.core.config import settings

router = APIRouter(tags=["Monitoring"])


@router.get(
    settings.metrics_path,
    summary="Prometheus Metrics",
)
def metrics():
    """
    Prometheus metrics endpoint.
    """

    if not settings.metrics_enabled:
        raise HTTPException(
            status_code=404,
            detail="Metrics endpoint disabled",
        )

    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )
