# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: config.py
# @Software: PyCharm
# @Desc : 核心配置

"""
Sales Service Configuration
销售服务配置
"""

import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from pathlib import Path

# 加载环境变量
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)

class Settings(BaseSettings):
    app_name: str = "XEERP Sales Service"
    app_version: str = "1.0.0"
    app_host: str = "0.0.0.0"
    app_port: int = 8010
    
    # 数据库配置
    db_type: str = os.getenv("DB_TYPE", "mysql")
    db_host: str = os.getenv("DB_HOST", "192.168.40.32")
    db_port: int = int(os.getenv("DB_PORT", 3307))
    db_username: str = os.getenv("DB_USERNAME", "root")
    db_password: str = os.getenv("DB_PASSWORD", "welcome123!")
    db_database: str = os.getenv("DB_DATABASE", "xeapp")
    
    # Redis配置
    redis_host: str = os.getenv("REDIS_HOST", "192.168.40.14")
    redis_port: int = int(os.getenv("REDIS_PORT", 6379))
    redis_password: str = os.getenv("REDIS_PASSWORD", "")
    redis_database: int = int(os.getenv("REDIS_DATABASE", 3))
    
    # JWT配置
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "b01c66dc2c58dc6a0aabfe2144256be36226de378bf87f72c0c795dda67f4d55")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    
    @property
    def database_url(self):
        if self.db_type == "mysql":
            return f"mysql+aiomysql://{self.db_username}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_database}"
        return f"sqlite+aiosqlite:///./sales.db"

settings = Settings()