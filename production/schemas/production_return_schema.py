# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: production_return_schema.py
# @Software: PyCharm
# @Desc : 数据模式

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ProductionReturnItemModel(BaseModel):
    return_item_id: int
    return_id: int
    material_id: int
    material_name: Optional[str] = None
    unit: Optional[str] = None
    quantity: float
    batch_no: Optional[str] = None
    reason: Optional[str] = None

class ProductionReturnModel(BaseModel):
    return_id: int
    return_code: str
    issue_id: int
    issue_code: Optional[str] = None
    warehouse_id: int
    status: str
    remark: Optional[str] = None
    create_by: Optional[str] = None
    create_time: datetime
    update_by: Optional[str] = None
    update_time: Optional[datetime] = None
    items: List[ProductionReturnItemModel] = []

class AddProductionReturnModel(BaseModel):
    return_code: str = Field(..., min_length=1, max_length=50, description='退料单编号')
    issue_id: int = Field(..., description='领料单ID')
    warehouse_id: int = Field(..., description='退料仓库ID')
    remark: Optional[str] = Field(None, description='备注')
    items: List[dict] = Field(..., description='退料明细')

class ProductionReturnPageQueryModel(BaseModel):
    page_num: int = Field(1, ge=1, description='页码')
    page_size: int = Field(10, ge=1, le=100, description='每页数量')
    issue_code: Optional[str] = Field(None, description='领料单编号')
    status: Optional[str] = Field(None, description='状态')