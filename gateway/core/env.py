# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: env.py
# @Software: PyCharm
# @Desc : 核心配置

from pydantic_settings import BaseSettings

class AppConfig(BaseSettings):
    app_name: str = "gateway-server"
    host: str = "0.0.0.0"
    port: int = 8000

    consul_host: str = "127.0.0.1"
    consul_port: int = 8500

    redis_host: str = "127.0.0.1"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: str = ""

    # 服务前缀映射（网关路径前缀 -> 服务名）
    service_prefix: dict = {
        "system": "system-service",
        "product": "product-service",
        "stock": "stock-service",
        "sales": "sales-service",
        "production": "production-service",
        "partner": "partner-service",
        "report": "report-service",
    }

    # 服务别名映射（网关使用别名 -> consul服务名）
    service_mapping: dict = {
        "system": "system-service",
        "product": "product-service",
        "stock": "stock-service",
        "sales": "sales-service",
        "production": "production-service",
        "partner": "partner-service",
        "report": "report-service",
        "order": "order-service",
        "purchase": "purchase-service",
    }

config = AppConfig()