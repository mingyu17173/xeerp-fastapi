# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: common_schema.py
# @Software: PyCharm
# @Desc : 数据模式

from pydantic import BaseModel, Field
from typing import Optional, List, TypeVar, Generic

T = TypeVar('T')

class CrudResponseModel(BaseModel):
    is_success: bool = Field(..., description='操作是否成功')
    message: str = Field(..., description='操作消息')
    data: Optional[dict] = Field(None, description='返回数据')

class PageResponseModel(BaseModel, Generic[T]):
    rows: List[T] = Field(..., description='数据列表')
    total: int = Field(..., description='总记录数')
    page_num: int = Field(..., description='当前页码')
    page_size: int = Field(..., description='每页数量')

class DeleteModel(BaseModel):
    ids: str = Field(..., description='要删除的ID，逗号分隔')