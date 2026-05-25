# -*- coding: utf-8 -*-
from pathlib import Path
from pydantic import BaseModel
from functools import lru_cache

PROJECT_ROOT = Path(__file__).parent.parent.parent


class BaseSettings(BaseModel):
    # 服务基础
    SERVICE_PREFIX: str = "/api/v1"
    DEBUG: bool = True

    # Consul
    CONSUL_HOST: str = "127.0.0.1"
    CONSUL_PORT: int = 8500
    CONSUL_TAGS: list = ["erp-micro"]

    # Redis
    REDIS_HOST: str = "127.0.0.1"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ""
    REDIS_DB: int = 0

    # JWT
    JWT_SECRET: str = "xeerp-fastapi-2026"
    JWT_ALGORITHM: str = "HS256"
    EXPIRE_HOURS: int = 12

    # 数据库公共
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20


class Settings(BaseSettings):
    # 各微服务可独立扩展
    pass


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()