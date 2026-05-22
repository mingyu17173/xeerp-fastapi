"""
Sales Service Main Entry
销售服务主入口
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from core.database import init_db
from core.logger import logger
from api.sales import router as sales_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting sales service...")
    await init_db()
    logger.info("Sales service started successfully")
    yield
    logger.info("Stopping sales service...")

app = FastAPI(
    title="XEERP Sales Service",
    description="销售服务 - 销售订单、销售出库、销售退货",
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

app.include_router(sales_router)

@app.get("/health")
async def health_check():
    logger.info("Sales service health check")
    return {"status": "ok", "service": "sales-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.app_host, port=settings.app_port, reload=True)