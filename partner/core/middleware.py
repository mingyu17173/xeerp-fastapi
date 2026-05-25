# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: middleware.py
# @Software: PyCharm
# @Desc : 核心配置

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from core.response import ResponseModel
import logging

logger = logging.getLogger(__name__)

async def exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP error occurred: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content=ResponseModel.error(code=exc.status_code, message=exc.detail).dict()
    )

async def logging_middleware(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response