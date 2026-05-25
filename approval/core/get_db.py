# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: get_db.py
# @Software: PyCharm
# @Desc : 核心配置

"""
数据库会话获取器
"""

from typing import Generator
from .database import SessionLocal


def get_db() -> Generator:
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()