# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: __init__.py
# @Software: PyCharm
# @Desc : API模块

"""
生产服务 API 模块
"""
from fastapi import APIRouter, FastAPI
from api.v1 import (
    bom_router,
    production_plan_router,
    production_issue_router,
    production_receipt_router,
    production_return_router,
    production_scrap_router
)

production_router_v1 = APIRouter()

production_router_v1.include_router(bom_router)
production_router_v1.include_router(production_plan_router)
production_router_v1.include_router(production_issue_router)
production_router_v1.include_router(production_receipt_router)
production_router_v1.include_router(production_return_router)
production_router_v1.include_router(production_scrap_router)

# 注册路由
def register_routers(app: FastAPI):

    app.include_router(production_router_v1)