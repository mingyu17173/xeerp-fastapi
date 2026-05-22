from contextlib import asynccontextmanager
import orjson
from fastapi import FastAPI
from core.env import AppConfig
from core.get_db import init_create_table
from core.logger import logger
from api import register_routers
from utils.service_registry import auto_register


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用生命周期管理
    """
    logger.info(f'[START] {AppConfig.app_name} starting...')
    
    # 注册服务到Nacos
    logger.info("🔗 正在注册服务到Nacos...")
    auto_register("product")
    
    # 初始化数据库表
    await init_create_table()
    logger.info(f'[SUCCESS] {AppConfig.app_name} started successfully')
    yield
    logger.info(f'[STOP] {AppConfig.app_name} stopped')


# 初始化FastAPI对象
app = FastAPI(
    root_path=AppConfig.app_root_path,
    title=AppConfig.app_name,
    description=f'{AppConfig.app_name} API Documentation',
    version=AppConfig.app_version,
    lifespan=lifespan,
    json_serializer=orjson.dumps,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# 注册路由
register_routers(app)