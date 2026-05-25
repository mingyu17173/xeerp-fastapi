# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: inventory_flow_schema.py
# @Software: PyCharm
# @Desc : 数据模式

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class InventoryFlowModel(BaseModel):
    flow_id: int
    product_id: int
    warehouse_id: int
    flow_type: str
    quantity: int
    before_quantity: int
    after_quantity: int
    batch_no: Optional[str] = None
    source_type: Optional[str] = None
    source_id: Optional[int] = None
    remark: Optional[str] = None
    create_by: Optional[str] = None
    create_time: datetime

class InventoryFlowQueryModel(BaseModel):
    page_num: int = Field(1, ge=1, description='页码')
    page_size: int = Field(10, ge=1, le=100, description='每页数量')
    product_id: Optional[int] = Field(None, description='商品ID')
    warehouse_id: Optional[int] = Field(None, description='仓库ID')
    flow_type: Optional[str] = Field(None, description='流水类型')
    start_time: Optional[datetime] = Field(None, description='开始时间')
    end_time: Optional[datetime] = Field(None, description='结束时间')

class InventoryFlowCreateModel(BaseModel):
    product_id: int = Field(..., description='商品ID')
    warehouse_id: int = Field(..., description='仓库ID')
    flow_type: str = Field(..., pattern='^(in|out|adjust)$', description='流水类型')
    quantity: int = Field(..., description='数量')
    batch_no: Optional[str] = Field(None, description='批次号')
    source_type: Optional[str] = Field(None, description='来源类型')
    source_id: Optional[int] = Field(None, description='来源单据ID')
    remark: Optional[str] = Field(None, description='备注')