# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: __init__.py
# @Software: PyCharm
# @Desc : API模块

from fastapi import FastAPI
from api.v1.product_controller import productController
from api.v1.unit_controller import unitController
from api.v1.category_controller import categoryController
from api.v1.brand_controller import brandController


def register_routers(app: FastAPI):
    """
    注册路由
    """
    # 注册商品相关路由
    app.include_router(productController, prefix="/product", tags=["商品管理"])
    # 注册商品单位路由
    app.include_router(unitController, prefix="/product/unit", tags=["商品单位"])
    # 注册商品分类路由
    app.include_router(categoryController, prefix="/product/category", tags=["商品分类"])
    # 注册商品品牌路由
    app.include_router(brandController, prefix="/product/brand", tags=["商品品牌"])