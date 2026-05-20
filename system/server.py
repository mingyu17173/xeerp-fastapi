from contextlib import asynccontextmanager
import orjson
from core.env import AppConfig
from core.get_db import init_create_table
from core.get_redis import RedisUtil
from core.get_scheduler import SchedulerUtil
from core.handle import handle_exception
from core.mounts.handle import handle_sub_applications
from middlewares.handle import handle_middleware
from api import register_routers
from utils.common_util import worship
from utils.log_util import logger
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f'⏰️ {AppConfig.app_name}开始启动')
    worship()
    await init_create_table()
    app.state.redis = await RedisUtil.create_redis_pool()
    await RedisUtil.init_sys_dict(app.state.redis)
    await RedisUtil.init_sys_config(app.state.redis)
    await RedisUtil.init_sys_user(app.state.redis)
    await SchedulerUtil.init_system_scheduler()
    logger.info(f'🚀 {AppConfig.app_name}启动成功')
    yield
    await RedisUtil.close_redis_pool(app)
    await SchedulerUtil.close_system_scheduler()


# 初始化FastAPI对象
app = FastAPI(
    root_path=AppConfig.app_root_path,
    title=AppConfig.app_name,
    description=f'{AppConfig.app_name}接口文档',
    version=AppConfig.app_version,
    lifespan=lifespan,
    json_serializer=orjson.dumps,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# 注册路由
register_routers(app)

# 挂载子应用
handle_sub_applications(app)

# 加载中间件处理方法
handle_middleware(app)

# 加载全局异常处理方法
handle_exception(app)
