# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: redis.py
# @Software: PyCharm
# @Desc : 核心配置

"""
Sales Service Redis Configuration
销售服务Redis配置
"""

import redis.asyncio as redis
from .config import settings

redis_client = None

async def get_redis():
    """获取Redis客户端"""
    global redis_client
    if redis_client is None:
        redis_client = redis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            password=settings.redis_password,
            db=settings.redis_database,
            decode_responses=True
        )
    return redis_client

async def close_redis():
    """关闭Redis连接"""
    global redis_client
    if redis_client is not None:
        await redis_client.close()