from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from core.config import settings
from core.database import init_db
from core.logger import logger
from api.order import router as order_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting order service...")
    await init_db()
    logger.info("Order service started successfully")
    yield
    logger.info("Stopping order service...")

app = FastAPI(
    title="XEERP Order Service",
    description="订单服务",
    version=settings.app_version,
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(order_router, prefix="/api")

@app.get("/health")
async def health_check():
    logger.info("Order service health check")
    return {"status": "ok", "service": "order-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8008, reload=True)