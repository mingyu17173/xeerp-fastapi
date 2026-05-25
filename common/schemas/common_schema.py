# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: __init__.py
# @Software: PyCharm
# @Desc : 全局公共结构体,所有微服务通用的 Pydantic 模型、请求、响应、枚举模块文件

from typing import Any, Generic, List, Optional, TypeVar
from pydantic import BaseModel, Field
from enum import Enum

# ==============================================
# 全局泛型（支持所有业务模型）
# ==============================================
T = TypeVar("T")


# ==============================================
# 全局状态枚举
# ==============================================
class StatusEnum(int, Enum):
    """
    通用状态：启用 / 禁用
    """
    ENABLE = 1
    DISABLE = 0


# ==============================================
# 全局通用 ID 入参（单 ID / 批量 ID）
# ==============================================
class IdParam(BaseModel):
    """
    单 ID 参数
    """
    id: int = Field(..., description="主键ID")


class IdsParam(BaseModel):
    """
    批量 ID 参数
    """
    ids: List[int] = Field(..., description="主键ID列表")


# ==============================================
# 全局分页请求结构体（所有列表查询通用）
# ==============================================
class PageParam(BaseModel):
    """
    分页查询通用入参
    所有服务的列表接口都用这个
    """
    page: int = Field(1, ge=1, description="页码")
    size: int = Field(10, ge=1, le=100, description="每页条数")
    sort_field: Optional[str] = Field(None, description="排序字段")
    sort_type: Optional[str] = Field(None, description="排序方式 asc/desc")

    class Config:
        json_schema_extra = {
            "example": {
                "page": 1,
                "size": 10,
                "sort_field": "id",
                "sort_type": "desc"
            }
        }


# ==============================================
# 全局分页响应结构体
# ==============================================
class PageResult(PageParam, Generic[T]):
    """
    统一分页出参
    """
    total: int = Field(0, description="总条数")
    records: List[T] = Field([], description="数据列表")

    class Config:
        arbitrary_types_allowed = True


# ==============================================
# 全局统一响应体（前端固定格式）
# ==============================================
class ApiResult(BaseModel, Generic[T]):
    """
    全局统一返回格式
    {
        "code": 200,
        "msg": "操作成功",
        "data": T
    }
    """
    code: int = Field(200, description="响应码")
    msg: str = Field("操作成功", description="响应消息")
    data: Optional[T] = Field(None, description="响应数据")

    @staticmethod
    def success(data: Any = None, msg: str = "操作成功") -> "ApiResult":
        return ApiResult(code=200, msg=msg, data=data)

    @staticmethod
    def fail(msg: str = "操作失败", code: int = 500) -> "ApiResult":
        return ApiResult(code=code, msg=msg, data=None)


# ==============================================
# 全局登录用户信息（JWT 解析后）
# ==============================================
class LoginUserInfo(BaseModel):
    """
    网关/系统服务 传递的当前登录用户
    所有服务都能接收
    """
    user_id: int = Field(..., description="用户ID")
    username: str = Field(..., description="账号")
    nickname: Optional[str] = Field(None, description="昵称")
    dept_id: Optional[int] = Field(None, description="部门ID")
    role_ids: Optional[List[int]] = Field(None, description="角色ID列表")
    perms: Optional[List[str]] = Field(None, description="权限标识列表")
    data_scope: Optional[int] = Field(None, description="数据权限范围")


# ==============================================
# 全局服务间调用请求体
# ==============================================
class ServiceRequest(BaseModel):
    """
    微服务之间 HTTP 调用统一格式
    """
    user_id: Optional[int] = None
    data: Optional[Any] = None


# ==============================================
# 全局下拉框选项结构体
# ==============================================
class OptionItem(BaseModel):
    """
    前端下拉框通用结构
    """
    label: str = Field(..., description="显示名称")
    value: Any = Field(..., description="提交值")


# ==============================================
# 全局树结构（菜单、部门、商品分类）
# ==============================================
class TreeItem(BaseModel):
    """
    通用树结构
    """
    id: Any
    label: str
    parent_id: Optional[Any] = None
    children: Optional[List["TreeItem"]] = []


# 允许递归
TreeItem.model_rebuild()