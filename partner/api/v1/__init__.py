# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: __init__.py
# @Software: PyCharm
# @Desc : API模块

"""
API模块初始化
"""

from .partner_controller import router

__all__ = ["router"]