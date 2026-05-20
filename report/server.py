from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from core.env import AppConfig
from router import report_router
from core.get_redis import get_redis
from core.logger import logger
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting report-service...")
    logger.info("Report service started successfully")
    yield
    logger.info("Stopping report-service...")

app = FastAPI(
    title="XEERP Report Service",
    description="报表服务 - 生产进度报表、领料明细报表、入库成本报表、库存台账",
    version="1.0.0",
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

app.include_router(report_router, prefix="/api")

@app.get("/health")
async def health_check():
    logger.info("Report service health check")
    return {"status": "ok", "service": "report-service"}