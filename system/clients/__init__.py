"""
微服务客户端模块
用于封装对其他微服务的 API 调用
"""
from clients.base_client import BaseClient
from clients.product_client import ProductClient

__all__ = ['BaseClient', 'ProductClient']