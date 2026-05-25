# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: inventory_schema.py
# @Software: PyCharm
# @Desc : 数据模式

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class InventoryModel(BaseModel):
    inventory_id: int
    product_id: int
    warehouse_id: int
    warehouse_name: Optional[str] = None
    product_name: Optional[str] = None
    quantity: int
    min_quantity: int
    max_quantity: int
    unit: Optional[str] = None
    batch_no: Optional[str] = None
    expire_date: Optional[datetime] = None
    create_time: datetime
    update_time: Optional[datetime] = None

class InventoryQueryModel(BaseModel):
    page_num: int = Field(1, ge=1, description='页码')
    page_size: int = Field(10, ge=1, le=100, description='每页数量')
    product_id: Optional[int] = Field(None, description='商品ID')
    warehouse_id: Optional[int] = Field(None, description='仓库ID')
    product_name: Optional[str] = Field(None, description='商品名称')

class InventoryAdjustModel(BaseModel):
    product_id: int = Field(..., description='商品ID')
    warehouse_id: int = Field(..., description='仓库ID')
    quantity: int = Field(..., description='调整数量（正数增加，负数减少）')
    remark: Optional[str] = Field(None, description='调整原因')