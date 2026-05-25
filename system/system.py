# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: system.py
# @Software: PyCharm
# @Desc : 模块文件

import uvicorn
import orjson
from fastapi import FastAPI
from contextlib import asynccontextmanager
from core.system_env import AppConfig
from api import register_routers
from core.logger import logger
from core.get_db import init_create_table
from core.get_redis import RedisUtil
from core.get_scheduler import SchedulerUtil
from core.handle import handle_exception
from core.mounts.handle import handle_sub_applications
from middlewares.handle import handle_middleware

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
    await init_create_table()
    logger.info(f'⏰️ {AppConfig.app_name} Redis注册')
    app.state.redis = await RedisUtil.create_redis_pool()
    await RedisUtil.init_sys_dict(app.state.redis)
    await RedisUtil.init_sys_config(app.state.redis)
    await RedisUtil.init_sys_user(app.state.redis)
    await SchedulerUtil.init_system_scheduler()

    yield
    ConsulUtil.deregister_service(AppConfig.app_name, AppConfig.app_service_id)
    await RedisUtil.close_redis_pool(app)
    await SchedulerUtil.close_system_scheduler()

    logger.info(f'🚀 {AppConfig.app_name}注销成功')

# 初始化应用
app = FastAPI(
    title="system server",
    description=f'{AppConfig.app_name}接口文档',
    version="1.0.0",
    lifespan = lifespan,
    json_serializer=orjson.dumps,
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

# 注册路由
register_routers(app)

# 挂载子应用
handle_sub_applications(app)

# 加载中间件处理方法
handle_middleware(app)

# 加载全局异常处理方法
handle_exception(app)



if __name__ == "__main__":
    uvicorn.run("system:app", host=AppConfig.app_host, port=AppConfig.app_port, reload=True)
