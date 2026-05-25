# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: env.py
# @Software: PyCharm
# @Desc : 核心配置

from pydantic_settings import BaseSettings, SettingsConfigDict

class AppConfig(BaseSettings):
    app_name: str = "xeerp-report"
    app_version: str = "1.0.0"
    app_env: str = "dev"
    
    db_host: str = "localhost"
    db_port: int = 3306
    db_name: str = "xeerp_report"
    db_user: str = "root"
    db_password: str = "123456"
    
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 3
    
    production_service_url: str = "http://127.0.0.1:8004"
    stock_service_url: str = "http://127.0.0.1:8003"
    product_service_url: str = "http://127.0.0.1:8002"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

AppConfig = AppConfig()