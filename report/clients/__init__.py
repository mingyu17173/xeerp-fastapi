# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: __init__.py
# @Software: PyCharm
# @Desc : 模块文件

"""
报表服务客户端模块
用于封装对其他微服务的 API 调用
"""
from clients.base_client import BaseClient
from clients.production_client import ProductionClient
from clients.stock_client import StockClient

__all__ = ['BaseClient', 'ProductionClient', 'StockClient']