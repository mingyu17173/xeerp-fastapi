from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class WarehouseModel(BaseModel):
    warehouse_id: int
    warehouse_code: str
    warehouse_name: str
    address: Optional[str] = None
    manager: Optional[str] = None
    phone: Optional[str] = None
    status: str
    remark: Optional[str] = None
    create_by: Optional[str] = None
    create_time: datetime
    update_by: Optional[str] = None
    update_time: Optional[datetime] = None

class AddWarehouseModel(BaseModel):
    warehouse_code: str = Field(..., min_length=1, max_length=50, description='仓库编码')
    warehouse_name: str = Field(..., min_length=1, max_length=100, description='仓库名称')
    address: Optional[str] = Field(None, max_length=500, description='仓库地址')
    manager: Optional[str] = Field(None, max_length=50, description='仓库管理员')
    phone: Optional[str] = Field(None, max_length=20, description='联系电话')
    status: str = Field('0', pattern='^[01]$', description='状态')
    remark: Optional[str] = Field(None, description='备注')

class EditWarehouseModel(BaseModel):
    warehouse_id: int = Field(..., description='仓库ID')
    warehouse_code: str = Field(..., min_length=1, max_length=50, description='仓库编码')
    warehouse_name: str = Field(..., min_length=1, max_length=100, description='仓库名称')
    address: Optional[str] = Field(None, max_length=500, description='仓库地址')
    manager: Optional[str] = Field(None, max_length=50, description='仓库管理员')
    phone: Optional[str] = Field(None, max_length=20, description='联系电话')
    status: str = Field('0', pattern='^[01]$', description='状态')
    remark: Optional[str] = Field(None, description='备注')

class WarehousePageQueryModel(BaseModel):
    page_num: int = Field(1, ge=1, description='页码')
    page_size: int = Field(10, ge=1, le=100, description='每页数量')
    warehouse_name: Optional[str] = Field(None, description='仓库名称')
    warehouse_code: Optional[str] = Field(None, description='仓库编码')