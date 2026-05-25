# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: get_redis.py
# @Software: PyCharm
# @Desc : 核心配置

from redis import asyncio as aioredis
from redis.exceptions import AuthenticationError, TimeoutError, RedisError, ConnectionError
from core.database import AsyncSessionLocal
from core.system_env import RedisConfig
from service.config_service import ConfigService
from service.dict_service import DictDataService
from service.user_service import UserService
from core.logger import logger


class RedisUtil:
    """Redis 工具类（生产级异步连接池）"""

    @classmethod
    async def create_redis_pool(cls) -> aioredis.Redis:
        """
        应用启动时初始化 Redis 连接池
        支持：redis 6.0+ / 密码 / 用户名 / 多数据库
        """
        logger.info("🔎 正在初始化 Redis 连接...")

        try:
            # 构建 Redis 连接（兼容无密码、无用户名）
            redis = await aioredis.from_url(
                url=f"redis://{RedisConfig.redis_host}",
                port=RedisConfig.redis_port,
                username=RedisConfig.redis_username or None,
                password=RedisConfig.redis_password or None,
                db=RedisConfig.redis_database,
                encoding="utf-8",
                decode_responses=True,

                # 连接池配置（生产级）
                socket_timeout=5,
                socket_connect_timeout=5,
                health_check_interval=30,
            )

            # 测试连通性
            await redis.ping()
            logger.info(f"✅ Redis 连接成功 | DB:{RedisConfig.redis_database} | {RedisConfig.redis_host}:{RedisConfig.redis_port}")
            return redis

        except AuthenticationError:
            logger.error("❌ Redis 认证失败：用户名或密码错误")
            raise
        except ConnectionError:
            logger.error("❌ Redis 连接失败：无法连接到 Redis 服务")
            raise
        except TimeoutError:
            logger.error("❌ Redis 连接超时")
            raise
        except RedisError as e:
            logger.error(f"❌ Redis 未知错误：{str(e)}")
            raise
        except Exception as e:
            logger.error(f"❌ Redis 初始化异常：{str(e)}")
            raise

    @classmethod
    async def close_redis_pool(cls, app):
        """
        应用关闭时安全关闭 Redis 连接池
        """
        try:
            await app.state.redis.close()
            await app.state.redis.connection_pool.disconnect()
            logger.info("✅ Redis 连接池已安全关闭")
        except Exception as e:
            logger.error(f"❌ 关闭 Redis 失败：{str(e)}")


    @classmethod
    async def init_sys_dict(cls, redis):
        """
        应用启动时缓存字典表

        :param redis: redis对象
        :return:
        """
        async with AsyncSessionLocal() as session:
            await DictDataService.init_cache_sys_dict_services(session, redis)

    @classmethod
    async def init_sys_config(cls, redis):
        """
        应用启动时缓存参数配置表

        :param redis: redis对象
        :return:
        """
        async with AsyncSessionLocal() as session:
            await ConfigService.init_cache_sys_config_services(session, redis)


    @classmethod
    async def init_sys_user(cls, redis):
        """
        应用启动时缓存用户表

        :param redis: redis对象
        :return:
        """
        async with AsyncSessionLocal() as session:
            await UserService.init_cache_sys_user_services(session, redis)
