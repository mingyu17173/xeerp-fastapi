"""
Gateway Service Main Entry
网关服务主入口
"""
import time
import uuid
import threading
import requests
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from core.env import AppConfig
from core.limiter import limiter, rate_limit_exceeded_handler
from core.auth import verify_jwt_token
from core.logger import logger
from router import gateway_router
from utils.consul_register import ConsulClient


SERVICE_INSTANCE_MAP = {}
consul = ConsulClient()


# 定时拉取Nacos服务列表
def refresh_service_list():
    global SERVICE_INSTANCE_MAP
    service_list = ["system-server","product-server","production-server"]
    while True:
        temp_map = {}
        for service in service_list:
            instances = consul.get_service_url(service)
            if instances:
                # 取第一个实例，可自行实现轮询/随机负载均衡
                ins = instances[0]
                temp_map[service] = f"{ins.ip}:{ins.port}"
        SERVICE_INSTANCE_MAP = temp_map
        print("🔄 网关刷新服务列表：",SERVICE_INSTANCE_MAP)
        time.sleep(6)

# 启动刷新线程
threading.Thread(target=refresh_service_list, daemon=True).start()



@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用生命周期管理
    """
    logger.info(f"🚀 {AppConfig.app_name} 开始启动...")
    logger.info(f"📦 环境: {AppConfig.app_env}")
    logger.info(f"🔌 端口: {AppConfig.app_port}")

    yield

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
    认证中间件 - JWT Token验证
    """
    # 精确匹配的公开路径
    PUBLIC_PATHS = {
        "/api/docs",
        "/api/redoc",
        "/api/openapi.json",
        "/api/captchaImage",
        "/health",
    }

    # 前缀匹配的公开路径
    PUBLIC_PREFIXES = {
        "/api/auth/",      # 认证相关接口
        "/api/public/",    # 公开数据接口
    }

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # 检查精确匹配
        if path in self.PUBLIC_PATHS:
            return await call_next(request)

        # 检查前缀匹配
        for prefix in self.PUBLIC_PREFIXES:
            if path.startswith(prefix):
                return await call_next(request)

        # 获取Authorization头
        authorization = request.headers.get("Authorization")
        if not authorization:
            logger.warning(f"🔒 未授权访问: {path}")
            return JSONResponse(
                status_code=401,
                content={"code": 401, "message": "未授权访问，请先登录"}
            )

        # 验证JWT Token
        try:
            token = authorization.replace("Bearer ", "")
            payload = verify_jwt_token(token)
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

# 注册路由
app.include_router(gateway_router, prefix="/api")



# 网关统一转发路由
@app.api_route("/{service_name}/{api_path:path}", methods=["GET", "POST"])
async def gateway_route(service_name: str, api_path: str, req: Request):
    if service_name not in SERVICE_INSTANCE_MAP:
        return {"code": 404, "msg": "目标服务未注册或不存在"}

    target_url = f"http://{SERVICE_INSTANCE_MAP[service_name]}/{api_path}"
    method = req.method

    try:
        if method == "GET":
            res = requests.get(target_url, params=req.query_params)
        else:
            json_data = await req.json()
            res = requests.post(target_url, json=json_data)
        return res.json()
    except Exception as e:
        return {"code": 500, "msg": "服务调用失败", "error": str(e)}

@app.get("/health", tags=["健康检查"])
async def health_check():
    """
    健康检查接口
    """
    return {"status": "ok", "service": "gateway-service", "version": AppConfig.app_version}

@app.get("/", tags=["首页"])
async def index():
    """
    网关首页
    """
    return {
        "service": "XEERP Gateway Service",
        "version": AppConfig.app_version,
        "description": "统一网关服务 - 路由转发、认证鉴权、限流控制",
        "docs": "/api/docs"
    }