# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: production_plan_schema.py
# @Software: PyCharm
# @Desc : 数据模式

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ProductionPlanModel(BaseModel):
    plan_id: int
    plan_code: str
    product_id: int
    product_name: Optional[str] = None
    bom_id: int
    plan_quantity: int
    finished_quantity: int
    warehouse_id: Optional[int] = None
    start_date: datetime
    end_date: datetime
    status: str
    remark: Optional[str] = None
    create_by: Optional[str] = None
    create_time: datetime
    update_by: Optional[str] = None
    update_time: Optional[datetime] = None

class AddProductionPlanModel(BaseModel):
    plan_code: str = Field(..., min_length=1, max_length=50, description='生产计划编号')
    product_id: int = Field(..., description='产品ID')
    product_name: Optional[str] = Field(None, description='产品名称')
    bom_id: int = Field(..., description='BOMID')
    plan_quantity: int = Field(..., ge=1, description='计划数量')
    warehouse_id: Optional[int] = Field(None, description='入库仓库ID')
    start_date: datetime = Field(..., description='计划开始日期')
    end_date: datetime = Field(..., description='计划结束日期')
    remark: Optional[str] = Field(None, description='备注')

class EditProductionPlanModel(BaseModel):
    plan_id: int = Field(..., description='生产计划ID')
    plan_code: str = Field(..., min_length=1, max_length=50, description='生产计划编号')
    product_id: int = Field(..., description='产品ID')
    product_name: Optional[str] = Field(None, description='产品名称')
    bom_id: int = Field(..., description='BOMID')
    plan_quantity: int = Field(..., ge=1, description='计划数量')
    warehouse_id: Optional[int] = Field(None, description='入库仓库ID')
    start_date: datetime = Field(..., description='计划开始日期')
    end_date: datetime = Field(..., description='计划结束日期')
    remark: Optional[str] = Field(None, description='备注')

class ProductionPlanPageQueryModel(BaseModel):
    page_num: int = Field(1, ge=1, description='页码')
    page_size: int = Field(10, ge=1, le=100, description='每页数量')
    product_name: Optional[str] = Field(None, description='产品名称')
    status: Optional[str] = Field(None, description='状态')