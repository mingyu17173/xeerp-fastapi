# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: __init__.py
# @Software: PyCharm
# @Desc : API模块

from .bom_controller import router as bom_router
from .production_plan_controller import router as production_plan_router
from .production_issue_controller import router as production_issue_router
from .production_receipt_controller import router as production_receipt_router
from .production_return_controller import router as production_return_router
from .production_scrap_controller import router as production_scrap_router

__all__ = [
    'bom_router', 'production_plan_router', 'production_issue_router',
    'production_receipt_router', 'production_return_router', 'production_scrap_router'
]