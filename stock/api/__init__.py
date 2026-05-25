# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: __init__.py
# @Software: PyCharm
# @Desc : API模块

"""
库存服务 API 模块
"""
from fastapi import APIRouter, FastAPI
from .v1 import warehouse_router, inventory_router

stock_router_v1 = APIRouter()

stock_router_v1.include_router(warehouse_router)
stock_router_v1.include_router(inventory_router)

# 注册路由
def register_routers(app: FastAPI):
    app.include_router(stock_router_v1)
