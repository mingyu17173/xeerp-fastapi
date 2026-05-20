from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from core.env import AppConfig
from core.get_db import init_create_table
from router import stock_router
from core.get_redis import get_redis
from core.logger import logger
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting stock-service...")
    await init_create_table()
    logger.info("Stock service started successfully")
    yield
    logger.info("Stopping stock-service...")

app = FastAPI(
    title="XEERP Stock Service",
    description="库存服务 - 仓库管理、库存数量、库存流水",
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

app.include_router(stock_router, prefix="/api")

@app.get("/health")
async def health_check():
    logger.info("Stock service health check")
    return {"status": "ok", "service": "stock-service"}