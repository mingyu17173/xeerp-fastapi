# -*- coding: utf-8 -*-
from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from common.schemas.common_schema import ApiResult


# 业务异常
class ServiceException(Exception):
    def __init__(self, msg: str = "业务异常", code: int = 400):
        self.msg = msg
        self.code = code
        super().__init__(self.msg)


# 业务异常处理器
async def biz_exception_handler(request: Request, exc: ServiceException):
    return JSONResponse(
        content=ApiResult.fail(code=exc.code, msg=exc.msg).dict()
    )


# HTTP 异常处理器
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        content=ApiResult.fail(code=exc.status_code, msg=exc.detail).dict()
    )


# 参数校验异常
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    msg = "参数错误：" + str(exc.errors())[:100]
    return JSONResponse(
        content=ApiResult.fail(code=400, msg=msg).dict()
    )


# 全局兜底异常
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        content=ApiResult.fail(code=500, msg="服务器异常：" + str(exc)).dict()
    )