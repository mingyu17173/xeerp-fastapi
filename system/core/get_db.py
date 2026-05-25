# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: get_db.py
# @Software: PyCharm
# @Desc : 核心配置

from .database import async_engine, AsyncSessionLocal, Base
from common.utils.log_util import logger
from core.system_env import DataBaseConfig


async def get_db():
    """
       FastAPI 依赖：获取异步数据库会话
       每个请求独立连接，请求结束自动关闭
       """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()


async def init_create_table():
    """
    项目启动时自动创建表（如果不存在）
    支持 MySQL / PostgreSQL 自动识别
    """
    try:
        db_type = DataBaseConfig.db_type.upper()
        logger.info(f"🔎 正在初始化 {db_type} 数据库连接...")

        async with async_engine.begin() as conn:
            # 自动创建所有表
            await conn.run_sync(Base.metadata.create_all)

        logger.info(f"✅ {db_type} 数据库连接成功，表结构初始化完成！")

    except Exception as e:
        logger.error(f"❌ 数据库初始化失败：{str(e)}")
        raise  # 启动失败直接退出
