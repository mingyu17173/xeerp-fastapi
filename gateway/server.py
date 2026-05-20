from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from core.env import AppConfig
from core.limiter import limiter
from core.auth import JWTBearer, verify_jwt_token
from core.logger import logger
from router import gateway_router
import time

app = FastAPI(
    title="XEERP Gateway Service",
    description="统一网关服务 - 路由转发、认证鉴权、限流控制",
    version="1.0.0",
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

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        logger.info(
            f"{request.method} {request.url.path} {response.status_code} "
            f"{process_time:.4f}s {request.client.host}"
        )
        return response

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        public_paths = [
            "/api/docs",
            "/api/redoc",
            "/api/openapi.json",
            "/api/auth/login",
        ]
        
        if request.url.path in public_paths or request.url.path.startswith("/api/auth/"):
            return await call_next(request)
        
        authorization = request.headers.get("Authorization")
        if not authorization:
            return JSONResponse(
                status_code=401,
                content={"detail": "未授权访问"}
            )
        
        try:
            token = authorization.replace("Bearer ", "")
            payload = verify_jwt_token(token)
            request.state.user = payload
        except Exception as e:
            return JSONResponse(
                status_code=401,
                content={"detail": str(e)}
            )
        
        return await call_next(request)

app.add_middleware(LoggingMiddleware)
app.add_middleware(AuthMiddleware)
app.include_router(gateway_router, prefix="/api")

@app.get("/health")
async def health_check():
    logger.info("Gateway health check")
    return {"status": "ok", "service": "gateway-service"}