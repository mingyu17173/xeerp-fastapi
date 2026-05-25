# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: get_redis.py
# @Software: PyCharm
# @Desc : 核心配置

from redis import asyncio as aioredis
from redis.exceptions import AuthenticationError, TimeoutError, RedisError
from core.partner_env import RedisConfig
from core.logger import logger


class RedisUtil:
    """
    Redis相关方法
    """

    @classmethod
    async def create_redis_pool(cls) -> aioredis.Redis:
        """
        应用启动时初始化redis连接

        :return: Redis连接对象
        """
        logger.info('🔎 开始连接redis...')
        redis = await aioredis.from_url(
            url=f'redis://{RedisConfig.redis_host}',
            port=RedisConfig.redis_port,
            username=RedisConfig.redis_username,
            password=RedisConfig.redis_password,
            db=RedisConfig.redis_database,
            encoding='utf-8',
            decode_responses=True,
        )
        try:
            connection = await redis.ping()
            if connection:
                logger.info('✅️ redis连接成功')
            else:
                logger.error('❌️ redis连接失败')
        except AuthenticationError as e:
            logger.error(f'❌️ redis用户名或密码错误，详细错误信息：{e}')
        except TimeoutError as e:
            logger.error(f'❌️ redis连接超时，详细错误信息：{e}')
        except RedisError as e:
            logger.error(f'❌️ redis连接错误，详细错误信息：{e}')
        return redis

    @classmethod
    async def close_redis_pool(cls, app):
        """
        应用关闭时关闭redis连接

        :param app: fastapi对象
        :return:
        """
        await app.state.redis.close()
        logger.info('✅️ 关闭redis连接成功')


async def get_redis():
    """
    获取 Redis 连接
    """
    from partner import app
    return app.state.redis
