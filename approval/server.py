# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: server.py
# @Software: PyCharm
# @Desc : 模块文件

"""
FastAPI 应用入口
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import settings
from api.v1 import approval_controller
from utils.service_registry import ServiceRegistry


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 服务启动时注册
    ServiceRegistry.register("approval", port=settings.SERVICE_PORT)
    
    yield
    
    # 服务关闭时注销
    ServiceRegistry.deregister("approval")


# 创建 FastAPI 应用
app = FastAPI(
    title="审批流服务",
    description="XEERP 审批流服务 API 文档",
    version="1.0.0",
    lifespan=lifespan
)

# 配置跨域中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 配置 Gzip 中间件
app.add_middleware(GZipMiddleware)

# 注册路由
app.include_router(
    approval_controller.router,
    prefix="/api/v1",
    tags=["审批流"]
)

# 健康检查端点
@app.get("/health", tags=["健康检查"])
async def health_check():
    """健康检查"""
    return {"status": "UP", "service": settings.SERVICE_NAME}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=settings.SERVICE_PORT,
        reload=True
    )