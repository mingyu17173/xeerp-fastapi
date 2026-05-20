from pydantic import BaseModel, Field
from typing import Optional


class CrudResponseModel(BaseModel):
    """
    CRUD响应模型
    """
    is_success: bool = Field(default=True, description='操作是否成功')
    message: str = Field(default='', description='响应消息')