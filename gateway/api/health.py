# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: health.py
# @Software: PyCharm
# @Desc : API模块

from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health():
    return {"status": "UP", "service": "gateway"}