# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: production_receipt_schema.py
# @Software: PyCharm
# @Desc : 数据模式

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ProductionReceiptModel(BaseModel):
    receipt_id: int
    receipt_code: str
    plan_id: int
    plan_code: Optional[str] = None
    warehouse_id: int
    quantity: int
    status: str
    remark: Optional[str] = None
    create_by: Optional[str] = None
    create_time: datetime
    update_by: Optional[str] = None
    update_time: Optional[datetime] = None

class AddProductionReceiptModel(BaseModel):
    receipt_code: str = Field(..., min_length=1, max_length=50, description='入库单编号')
    plan_id: int = Field(..., description='生产计划ID')
    warehouse_id: int = Field(..., description='入库仓库ID')
    quantity: int = Field(..., ge=1, description='入库数量')
    remark: Optional[str] = Field(None, description='备注')

class ProductionReceiptPageQueryModel(BaseModel):
    page_num: int = Field(1, ge=1, description='页码')
    page_size: int = Field(10, ge=1, le=100, description='每页数量')
    plan_code: Optional[str] = Field(None, description='生产计划编号')
    status: Optional[str] = Field(None, description='状态')