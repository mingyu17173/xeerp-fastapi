import redis
from fastapi import HTTPException, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from core.env import AppConfig

redis_client = redis.Redis(
    host=AppConfig.redis_host,
    port=AppConfig.redis_port,
    db=AppConfig.redis_db,
    decode_responses=True
)

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=f"redis://{AppConfig.redis_host}:{AppConfig.redis_port}/{AppConfig.redis_db}"
)

def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    raise HTTPException(
        status_code=429,
        detail=f"请求过于频繁，请稍后再试。限制：{exc.limit}次/{exc.timeframe}"
    )