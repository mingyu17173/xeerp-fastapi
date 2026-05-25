# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: env.py
# @Software: PyCharm
# @Desc : 核心配置

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """
    应用配置
    """
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')
    
    app_env: str = 'dev'
    app_name: str = 'product-service'
    app_root_path: str = ''
    app_host: str = '0.0.0.0'
    app_port: int = 8002  # Product service port
    app_version: str = '1.0.0'
    app_reload: bool = True


class DataBaseSettings(BaseSettings):
    """
    数据库配置
    """
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')
    
    db_type: str = 'mysql'
    db_host: str = '192.168.40.32'
    db_port: int = 3307
    db_username: str = 'root'
    db_password: str = 'welcome123!'
    db_database: str = 'xeapp'
    db_echo: bool = False
    db_max_overflow: int = 10
    db_pool_size: int = 10
    db_pool_recycle: int = 3600
    db_pool_timeout: int = 30


class RedisSettings(BaseSettings):
    """
    Redis配置
    """
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')
    
    redis_host: str = '192.168.40.14'
    redis_port: int = 6379
    redis_username: str = ''
    redis_password: str = ''
    redis_database: int = 2


class GetConfig:
    """
    获取配置
    """

    def __init__(self):
        self.load_env()

    @staticmethod
    def load_env():
        """
        加载环境变量
        """
        # 查找 .env 文件：优先当前目录，然后是父目录（项目根目录）
        env_file = '.env'
        env_path = Path(env_file)
        if not env_path.exists():
            # 尝试从 product 目录向上查找项目根目录
            current_dir = Path(__file__).resolve().parent
            project_root = current_dir.parent.parent
            env_path = project_root / env_file
        # 加载配置
        if env_path.exists():
            load_dotenv(env_path)

    @lru_cache()
    def get_app_config(self):
        """
        获取应用配置
        """
        return AppSettings()

    @lru_cache()
    def get_database_config(self):
        """
        获取数据库配置
        """
        return DataBaseSettings()

    @lru_cache()
    def get_redis_config(self):
        """
        获取Redis配置
        """
        return RedisSettings()


# 实例化获取配置类
get_config = GetConfig()
# 应用配置
AppConfig = get_config.get_app_config()
# 数据库配置
DataBaseConfig = get_config.get_database_config()
# Redis配置
RedisConfig = get_config.get_redis_config()