from pydantic import BaseModel, Field
from typing import Optional

class CrudResponseModel(BaseModel):
    is_success: bool = Field(..., description='操作是否成功')
    message: str = Field(..., description='操作消息')
    data: Optional[dict] = Field(None, description='返回数据')