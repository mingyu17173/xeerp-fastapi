# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: common_schema.py
# @Software: PyCharm
# @Desc : 数据模式

from pydantic import BaseModel, Field
from typing import Optional

class CrudResponseModel(BaseModel):
    is_success: bool = Field(..., description='操作是否成功')
    message: str = Field(..., description='操作消息')
    data: Optional[dict] = Field(None, description='返回数据')