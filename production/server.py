from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from core.env import AppConfig
from core.get_db import init_create_table
from router import production_router
from core.get_redis import get_redis
from core.logger import logger
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting production-service...")
    await init_create_table()
    logger.info("Production service started successfully")
    yield
    logger.info("Stopping production-service...")

app = FastAPI(
    title="XEERP Production Service",
    description="生产服务 - BOM管理、生产计划、领料、入库、退料、损耗",
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

app.include_router(production_router, prefix="/api")

@app.get("/health")
async def health_check():
    logger.info("Production service health check")
    return {"status": "ok", "service": "production-service"}