from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class BomItemModel(BaseModel):
    bom_item_id: int
    bom_id: int
    material_id: int
    material_name: Optional[str] = None
    unit: Optional[str] = None
    quantity: float
    scrap_rate: float
    remark: Optional[str] = None

class BomModel(BaseModel):
    bom_id: int
    product_id: int
    product_name: Optional[str] = None
    version: str
    status: str
    remark: Optional[str] = None
    create_by: Optional[str] = None
    create_time: datetime
    update_by: Optional[str] = None
    update_time: Optional[datetime] = None
    items: List[BomItemModel] = []

class AddBomModel(BaseModel):
    product_id: int = Field(..., description='成品ID')
    product_name: Optional[str] = Field(None, description='成品名称')
    version: str = Field('V1.0', description='版本号')
    status: str = Field('0', pattern='^[01]$', description='状态')
    remark: Optional[str] = Field(None, description='备注')
    items: List[dict] = Field(..., description='BOM明细')

class EditBomModel(BaseModel):
    bom_id: int = Field(..., description='BOMID')
    product_id: int = Field(..., description='成品ID')
    product_name: Optional[str] = Field(None, description='成品名称')
    version: str = Field(..., description='版本号')
    status: str = Field('0', pattern='^[01]$', description='状态')
    remark: Optional[str] = Field(None, description='备注')
    items: List[dict] = Field(..., description='BOM明细')

class BomPageQueryModel(BaseModel):
    page_num: int = Field(1, ge=1, description='页码')
    page_size: int = Field(10, ge=1, le=100, description='每页数量')
    product_name: Optional[str] = Field(None, description='成品名称')