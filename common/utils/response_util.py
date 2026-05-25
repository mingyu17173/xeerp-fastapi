# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: response_util.py
# @Software: PyCharm
# @Desc : 工具类

from datetime import datetime
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from starlette.background import BackgroundTask
from typing import Any, Dict, Mapping, Optional
from utils.constant_util import HttpStatusConstant


class ResponseUtil:
    """FastAPI 统一响应工具类（企业标准版）"""

    # ====================== 【核心】公共构建方法（消除重复） ======================
    @classmethod
    def __build(
        cls,
        code: int,
        msg: str,
        success: bool,
        data: Optional[Any] = None,
        rows: Optional[Any] = None,
        dict_content: Optional[Dict] = None,
        model_content: Optional[BaseModel] = None,
        headers: Optional[Mapping[str, str]] = None,
        media_type: Optional[str] = None,
        background: Optional[BackgroundTask] = None,
        http_status: int = status.HTTP_200_OK,
    ) -> JSONResponse:
        # 基础结构
        result = {
            "code": code,
            "msg": msg,
            "success": success,
            "time": datetime.now().isoformat()  # 标准时间格式
        }

        # 附加数据
        if data is not None:
            result["data"] = data
        if rows is not None:
            result["rows"] = rows
        if dict_content is not None:
            result.update(dict_content)
        if model_content is not None:
            result.update(model_content.model_dump(by_alias=True))

        # 统一 JSON 序列化
        return JSONResponse(
            status_code=http_status,
            content=jsonable_encoder(result, exclude_none=True),  # 自动过滤 null
            headers=headers,
            media_type=media_type,
            background=background,
        )

    # ====================== 成功响应 ======================
    @classmethod
    def success(
        cls,
        msg: str = "操作成功",
        data: Optional[Any] = None,
        rows: Optional[Any] = None,
        dict_content: Optional[Dict] = None,
        model_content: Optional[BaseModel] = None,
        headers: Optional[Mapping[str, str]] = None,
        media_type: Optional[str] = None,
        background: Optional[BackgroundTask] = None,
    ) -> JSONResponse:
        return cls.__build(
            code=HttpStatusConstant.SUCCESS,
            msg=msg,
            success=True,
            data=data,
            rows=rows,
            dict_content=dict_content,
            model_content=model_content,
            headers=headers,
            media_type=media_type,
            background=background,
        )

    # ====================== 业务失败 ======================
    @classmethod
    def failure(
        cls,
        msg: str = "操作失败",
        data: Optional[Any] = None,
        rows: Optional[Any] = None,
        dict_content: Optional[Dict] = None,
        model_content: Optional[BaseModel] = None,
        headers: Optional[Mapping[str, str]] = None,
        media_type: Optional[str] = None,
        background: Optional[BackgroundTask] = None,
    ) -> JSONResponse:
        return cls.__build(
            code=HttpStatusConstant.WARN,
            msg=msg,
            success=False,
            data=data,
            rows=rows,
            dict_content=dict_content,
            model_content=model_content,
            headers=headers,
            media_type=media_type,
            background=background,
        )

    # ====================== 未登录 ======================
    @classmethod
    def unauthorized(
        cls,
        msg: str = "登录已过期，请重新登录",
        headers: Optional[Mapping[str, str]] = None,
        background: Optional[BackgroundTask] = None,
    ) -> JSONResponse:
        return cls.__build(
            code=HttpStatusConstant.UNAUTHORIZED,
            msg=msg,
            success=False,
            headers=headers,
            background=background,
            http_status=status.HTTP_401_UNAUTHORIZED,  # 标准 HTTP 状态码
        )

    # ====================== 无权限 ======================
    @classmethod
    def forbidden(
        cls,
        msg: str = "无此接口权限",
        headers: Optional[Mapping[str, str]] = None,
        background: Optional[BackgroundTask] = None,
    ) -> JSONResponse:
        return cls.__build(
            code=HttpStatusConstant.FORBIDDEN,
            msg=msg,
            success=False,
            headers=headers,
            background=background,
            http_status=status.HTTP_403_FORBIDDEN,
        )

    # ====================== 服务器错误 ======================
    @classmethod
    def error(
        cls,
        msg: str = "服务器异常",
        data: Optional[Any] = None,
        headers: Optional[Mapping[str, str]] = None,
        background: Optional[BackgroundTask] = None,
    ) -> JSONResponse:
        return cls.__build(
            code=HttpStatusConstant.ERROR,
            msg=msg,
            success=False,
            data=data,
            headers=headers,
            background=background,
            http_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    # ====================== 流式响应（文件/导出） ======================
    @classmethod
    def streaming(
        cls,
        content: Any,
        headers: Optional[Mapping[str, str]] = None,
        media_type: str = "application/octet-stream",
        background: Optional[BackgroundTask] = None,
    ) -> StreamingResponse:
        return StreamingResponse(
            content=content,
            status_code=status.HTTP_200_OK,
            headers=headers,
            media_type=media_type,
            background=background,
        )

    # ====================== 扩展：空数据（常用） ======================
    @classmethod
    def empty(cls, msg: str = "暂无数据") -> JSONResponse:
        return cls.success(msg=msg, data=[])

    # ====================== 扩展：分页响应（常用） ======================
    @classmethod
    def page(cls, total: int, list: Any, msg: str = "查询成功") -> JSONResponse:
        return cls.success(msg=msg, dict_content={"total": total, "list": list})