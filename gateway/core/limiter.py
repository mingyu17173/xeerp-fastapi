# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: limiter.py
# @Software: PyCharm
# @Desc : 核心配置

"""
Gateway Service Rate Limiter
网关服务限流模块
"""

import redis.asyncio as redis
from fastapi import HTTPException, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from core.env import AppConfig

# 异步Redis客户端
redis_client = redis.Redis(
    host=AppConfig.redis_host,
    port=AppConfig.redis_port,
    db=AppConfig.redis_db,
    password=AppConfig.redis_password,
    decode_responses=True,
    socket_timeout=5,
    socket_connect_timeout=5
)

# 初始化限流器
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=f"redis://{AppConfig.redis_host}:{AppConfig.redis_port}/{AppConfig.redis_db}"
)

def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    """
    限流异常处理
    """
    raise HTTPException(
        status_code=429,
        detail={
            "code": 429,
            "message": f"请求过于频繁，请稍后再试",
            "limit": exc.limit,
            "timeframe": str(exc.timeframe),
            "retry_after": exc.retry_after
        }
    )