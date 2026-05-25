# -*- coding: utf-8 -*-
import redis.asyncio as aredis
from common.core.system_env import settings
from common.core.exception import ServiceException


class RedisUtil:
    _redis: aredis.Redis = None

    @classmethod
    async def init_redis(cls):
        try:
            cls._redis = aredis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                password=settings.REDIS_PASSWORD,
                db=settings.REDIS_DB,
                decode_responses=True
            )
        except Exception as e:
            raise ServiceException(f"Redis 连接失败 {e}")

    @classmethod
    async def close(cls):
        if cls._redis:
            await cls._redis.close()

    @classmethod
    async def set(cls, key: str, value: str, ex: int = None):
        await cls._redis.set(key, value, ex=ex)

    @classmethod
    async def get(cls, key: str):
        return await cls._redis.get(key)

    @classmethod
    async def delete(cls, key: str):
        await cls._redis.delete(key)

    @classmethod
    async def exists(cls, key: str):
        return await cls._redis.exists(key)