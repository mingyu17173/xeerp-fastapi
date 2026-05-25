# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: partner.py
# @Software: PyCharm
# @Desc : 模块文件

import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from core.partner_env import AppConfig
from core.logger import logger
from utils.consul_util import ConsulUtil

@asynccontextmanager
async def lifespan(app: FastAPI):
    ConsulUtil.init_client()
    logger.info(f'⏰️ {AppConfig.app_name}服务注册')
    ConsulUtil.register_service(
        AppConfig.app_name,
        None,  # 自动获取本地IP
        AppConfig.app_port,
        AppConfig.app_service_id
    )
    yield
    ConsulUtil.deregister_service(AppConfig.app_name, AppConfig.app_service_id)
    logger.info(f'🚀 {AppConfig.app_name}注销成功')

# 初始化应用
app = FastAPI(
    title="partner server",
    description=f'{AppConfig.app_name}接口文档',
    version="1.0.0",
    lifespan = lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# 健康检查接口（供Consul探测）
@app.get("/health")
async def health_check():
    return {"code": 200, "status": "UP"}

# 示例接口
@app.get("/")
async def index():
    return {"msg": "服务运行正常"}

if __name__ == "__main__":
    uvicorn.run("partner:app", host=AppConfig.app_host, port=AppConfig.app_port, reload=True)
