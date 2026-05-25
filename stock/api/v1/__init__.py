# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: __init__.py
# @Software: PyCharm
# @Desc : API模块

from .warehouse_controller import router as warehouse_router
from .inventory_controller import router as inventory_router

__all__ = ['warehouse_router', 'inventory_router']