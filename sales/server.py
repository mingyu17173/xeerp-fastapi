"""
FastAPI 应用入口
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import settings
from api.v1 import sales_controller
from utils.service_registry import ServiceRegistry


@asynccontextmanager
async def lifespan(app: FastAPI):
    ServiceRegistry.register("sales", port=settings.SERVICE_PORT)
    yield
    ServiceRegistry.deregister("sales")


app = FastAPI(
    title="销售服务",
    description="XEERP 销售服务 API 文档",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware)

app.include_router(
    sales_controller.router,
    prefix="/api/v1",
    tags=["销售管理"]
)


@app.get("/health", tags=["健康检查"])
async def health_check():
    return {"status": "UP", "service": settings.SERVICE_NAME}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=settings.SERVICE_PORT,
        reload=True
    )