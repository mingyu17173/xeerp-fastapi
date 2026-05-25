# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: server.py
# @Software: PyCharm
# @Desc : 模块文件

"""
Gateway Service Main Entry
网关服务主入口
"""
import time
import uuid
import threading
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
import httpx

from core.env import AppConfig
from core.limiter import limiter, rate_limit_exceeded_handler
from core.auth import verify_jwt_token, verify_jwt_token_with_redis
from core.logger import logger
from core.consul_discovery import ConsulServiceDiscovery
from core.get_redis import RedisUtil
from core.whitelist import WhitelistConfig
from router import gateway_router


# 服务实例映射（缓存）
SERVICE_INSTANCE_MAP = {}


def refresh_service_list():
    """
    定时刷新服务列表（从Consul获取）
    """
    global SERVICE_INSTANCE_MAP
    while True:
        try:
            # 从Consul获取所有服务
            service_list = ConsulServiceDiscovery.list_all_services()
            
            # 过滤我们关心的服务
            temp_map = {}
            for service_name in service_list:
                # 获取服务URL
                url = ConsulServiceDiscovery.get_service_url(service_name)
                if url:
                    temp_map[service_name] = url
            
            SERVICE_INSTANCE_MAP = temp_map
            logger.info(f"🔄 网关刷新服务列表: {list(SERVICE_INSTANCE_MAP.keys())}")
            
        except Exception as e:
            logger.error(f"❌ 刷新服务列表失败: {str(e)}")
        
        time.sleep(AppConfig.service_cache_ttl)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用生命周期管理
    """
    logger.info(f"🚀 {AppConfig.app_name} 开始启动...")
    logger.info(f"📦 环境: {AppConfig.app_env}")
    logger.info(f"🔌 端口: {AppConfig.app_port}")
    
    # 初始化Redis连接
    app.state.redis = await RedisUtil.create_redis_pool()
    
    # 初始化Consul
    ConsulServiceDiscovery.init_consul(
        host=AppConfig.consul_host,
        port=AppConfig.consul_port
    )
    
    # 启动服务列表刷新线程
    threading.Thread(target=refresh_service_list, daemon=True).start()
    
    yield
    
    # 关闭Redis连接
    await RedisUtil.close_redis_pool(app)
    
    logger.info(f"🛑 {AppConfig.app_name} 正在停止...")


app = FastAPI(
    title="XEERP Gateway Service",
    description="统一网关服务 - 路由转发、认证鉴权、限流控制",
    version=AppConfig.app_version,
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# 注册限流处理器
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

# CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Trace-Id"],
)


class RequestIdMiddleware(BaseHTTPMiddleware):
    """
    请求ID中间件 - 为每个请求生成唯一标识
    """
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())[:8]
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Trace-Id"] = request_id
        return response


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    日志中间件 - 记录请求和响应信息
    """
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        request_id = getattr(request.state, "request_id", "unknown")

        # 记录请求信息
        logger.info(
            f"📥 [{request_id}] {request.method} {request.url.path} "
            f"from {request.client.host}:{request.client.port}"
        )

        # 执行请求
        try:
            response = await call_next(request)
        except Exception as e:
            logger.error(
                f"❌ [{request_id}] 请求异常: {str(e)}"
            )
            raise

        # 记录响应信息
        process_time = time.time() - start_time
        logger.info(
            f"📤 [{request_id}] {request.method} {request.url.path} "
            f"{response.status_code} {process_time:.4f}s"
        )

        return response


class AuthMiddleware(BaseHTTPMiddleware):
    """
    认证中间件 - JWT Token验证（带Redis验证）
    使用统一的白名单配置管理免鉴权接口
    """

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        method = request.method

        # 检查白名单（支持精确匹配、前缀匹配、正则匹配、方法级匹配）
        if WhitelistConfig.is_whitelisted(path, method):
            return await call_next(request)

        # 获取Authorization头
        authorization = request.headers.get("Authorization")
        if not authorization:
            logger.warning(f"🔒 未授权访问: {path}")
            return JSONResponse(
                status_code=401,
                content={"code": 401, "message": "未授权访问，请先登录"}
            )

        # 验证JWT Token（带Redis验证）
        try:
            token = authorization.replace("Bearer ", "")
            
            # 获取Redis连接
            redis = getattr(request.app.state, 'redis', None)
            if not redis:
                logger.error(f"❌ Redis连接不可用: {path}")
                return JSONResponse(
                    status_code=500,
                    content={"code": 500, "message": "Redis连接不可用"}
                )
            
            # 验证Token（JWT + Redis）
            payload = await verify_jwt_token_with_redis(token, redis)
            request.state.user = payload
            request.state.token = token
        except HTTPException as e:
            logger.warning(f"🔒 Token验证失败: {path}, 错误: {e.detail}")
            return JSONResponse(
                status_code=e.status_code,
                content={"code": e.status_code, "message": e.detail}
            )

        return await call_next(request)


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """
    错误处理中间件 - 统一异常处理
    """
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except HTTPException as e:
            return JSONResponse(
                status_code=e.status_code,
                content={"code": e.status_code, "message": str(e.detail)}
            )
        except Exception as e:
            request_id = getattr(request.state, "request_id", "unknown")
            logger.error(f"💥 [{request_id}] 未处理异常: {str(e)}")
            return JSONResponse(
                status_code=500,
                content={"code": 500, "message": "服务器内部错误"}
            )


# 注册中间件（顺序很重要）
app.add_middleware(RequestIdMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(AuthMiddleware)
app.add_middleware(ErrorHandlingMiddleware)

# 注册路由（使用gateway_router统一处理路由转发）
app.include_router(gateway_router, prefix="/api")


@app.get("/health", tags=["健康检查"])
async def health_check():
    """
    健康检查接口
    """
    consul_available = ConsulServiceDiscovery.is_consul_available()
    return {
        "status": "ok",
        "service": "gateway-service",
        "version": AppConfig.app_version,
        "consul_available": consul_available,
        "registered_services": list(SERVICE_INSTANCE_MAP.keys())
    }


@app.get("/", tags=["首页"])
async def index():
    """
    网关首页
    """
    return {
        "service": "XEERP Gateway Service",
        "version": AppConfig.app_version,
        "description": "统一网关服务 - 路由转发、认证鉴权、限流控制",
        "docs": "/api/docs",
        "registered_services": list(SERVICE_INSTANCE_MAP.keys())
    }


@app.get("/services", tags=["服务管理"])
async def list_services():
    """
    获取所有已注册的服务列表
    """
    return {
        "services": SERVICE_INSTANCE_MAP,
        "count": len(SERVICE_INSTANCE_MAP)
    }