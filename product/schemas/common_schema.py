# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: common_schema.py
# @Software: PyCharm
# @Desc : 数据模式

from pydantic import BaseModel, Field
from typing import Optional


class CrudResponseModel(BaseModel):
    """
    CRUD响应模型
    """
    is_success: bool = Field(default=True, description='操作是否成功')
    message: str = Field(default='', description='响应消息')