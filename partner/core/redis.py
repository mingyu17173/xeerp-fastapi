# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: redis.py
# @Software: PyCharm
# @Desc : 核心配置

import redis
from core.config import settings

redis_client = redis.Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    db=settings.redis_db,
    decode_responses=True
)

def get_redis():
    return redis_client