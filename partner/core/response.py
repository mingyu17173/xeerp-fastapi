from typing import Optional, Generic, TypeVar
from pydantic import BaseModel, Field

T = TypeVar('T')

class ResponseModel(BaseModel, Generic[T]):
    code: int = Field(0, description='状态码')
    message: str = Field('success', description='消息')
    data: Optional[T] = Field(None, description='数据')

    @classmethod
    def success(cls, data: T = None, message: str = 'success'):
        return cls(code=0, message=message, data=data)

    @classmethod
    def error(cls, code: int = -1, message: str = 'error'):
        return cls(code=code, message=message, data=None)

class PageResponseModel(BaseModel, Generic[T]):
    code: int = Field(0, description='状态码')
    message: str = Field('success', description='消息')
    rows: Optional[list[T]] = Field([], description='数据列表')
    total: int = Field(0, description='总记录数')
    page_num: int = Field(1, description='当前页码')
    page_size: int = Field(10, description='每页数量')

    @classmethod
    def success(cls, rows: list[T], total: int, page_num: int, page_size: int):
        return cls(
            code=0,
            message='success',
            rows=rows,
            total=total,
            page_num=page_num,
            page_size=page_size
        )