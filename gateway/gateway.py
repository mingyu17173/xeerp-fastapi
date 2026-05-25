# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: gateway.py
# @Software: PyCharm
# @Desc : 模块文件

import asyncio
from fastapi import FastAPI, Request
from core.env import config
from core.logger import logger
from service.forward import forward_request
from service.monitor import check_all_services
from api.health import router as health_router
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 网关启动")
    asyncio.create_task(check_all_services())
    yield
    logger.info("🛑 网关关闭")

app = FastAPI(title="ERP 企业级网关", lifespan=lifespan)
app.include_router(health_router)

@app.api_route("/{service}/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def gateway(request: Request, service: str, full_path: str):
    return await forward_request(request, service, full_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("gateway:app", host=config.host, port=config.port, reload=True)