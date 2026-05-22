"""
Sales Service Response Utilities
销售服务响应工具
"""

from typing import Any, Optional, Generic, TypeVar
from pydantic import BaseModel

T = TypeVar('T')

class ResponseModel(BaseModel):
    """统一响应模型"""
    code: int = 200
    message: str = "success"
    data: Optional[Any] = None
    
    @classmethod
    def success(cls, data: Any = None, message: str = "success") -> 'ResponseModel':
        return cls(code=200, message=message, data=data)
    
    @classmethod
    def failure(cls, message: str = "failure", data: Any = None) -> 'ResponseModel':
        return cls(code=400, message=message, data=data)
    
    @classmethod
    def error(cls, message: str = "error", data: Any = None) -> 'ResponseModel':
        return cls(code=500, message=message, data=data)
    
    @classmethod
    def unauthorized(cls, message: str = "Unauthorized") -> 'ResponseModel':
        return cls(code=401, message=message)
    
    @classmethod
    def forbidden(cls, message: str = "Forbidden") -> 'ResponseModel':
        return cls(code=403, message=message)

class PageResponseModel(ResponseModel, Generic[T]):
    """分页响应模型"""
    page_num: int = 1
    page_size: int = 10
    total: int = 0
    rows: list[T] = []
    
    @classmethod
    def success(cls, rows: list[T], total: int, page_num: int, page_size: int) -> 'PageResponseModel':
        return cls(
            code=200,
            message="success",
            data=None,
            page_num=page_num,
            page_size=page_size,
            total=total,
            rows=rows
        )