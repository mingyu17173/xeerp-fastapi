# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: database.py
# @Software: PyCharm
# @Desc : 核心配置

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from urllib.parse import quote_plus
from core.system_env import DataBaseConfig


# ====================== 【自动】构建异步数据库连接URL ======================
def get_db_url():
    """自动根据数据库类型生成连接URL，支持 mysql / postgresql"""
    db_type = DataBaseConfig.db_type.lower()

    # 驱动映射
    driver_map = {
        "mysql": "mysql+asyncmy",
        "postgresql": "postgresql+asyncpg"
    }

    if db_type not in driver_map:
        raise ValueError(f"不支持的数据库类型: {db_type}，仅支持 mysql / postgresql")

    driver = driver_map[db_type]
    user = DataBaseConfig.db_username
    pwd = quote_plus(DataBaseConfig.db_password)  # 密码特殊字符编码
    host = DataBaseConfig.db_host
    port = DataBaseConfig.db_port
    db = DataBaseConfig.db_database

    return f"{driver}://{user}:{pwd}@{host}:{port}/{db}"

# ====================== 创建异步引擎 ======================
async_engine = create_async_engine(
    url=get_db_url(),
    echo=DataBaseConfig.db_echo,
    # 连接池配置（生产级）
    pool_size=DataBaseConfig.db_pool_size,
    max_overflow=DataBaseConfig.db_max_overflow,
    pool_recycle=DataBaseConfig.db_pool_recycle,  # 连接回收时间，防断开
    pool_timeout=DataBaseConfig.db_pool_timeout,
    pool_pre_ping=True,  # 【关键】连接前健康检查
    # 异步优化
    future=True,
)

# ====================== 异步会话工厂 ======================
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,  # 【重要】查询后对象不失效，生产必备
)

# ====================== ORM 基类 ======================
class Base(AsyncAttrs, DeclarativeBase):
    """ORM模型基类，所有Model继承此类"""
    pass
