from fastapi import FastAPI

from app.api.v1.products import router as products_router

app = FastAPI(
    title="CommerceAI Product Intelligence Service",
    version="1.0.0",
)

app.include_router(
    products_router,
    prefix="/api/v1",
)
