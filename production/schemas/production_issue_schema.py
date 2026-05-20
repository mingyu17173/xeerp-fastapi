from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ProductionIssueItemModel(BaseModel):
    issue_item_id: int
    issue_id: int
    material_id: int
    material_name: Optional[str] = None
    unit: Optional[str] = None
    plan_quantity: float
    actual_quantity: float
    batch_no: Optional[str] = None

class ProductionIssueModel(BaseModel):
    issue_id: int
    issue_code: str
    plan_id: int
    plan_code: Optional[str] = None
    warehouse_id: int
    status: str
    remark: Optional[str] = None
    create_by: Optional[str] = None
    create_time: datetime
    update_by: Optional[str] = None
    update_time: Optional[datetime] = None
    items: List[ProductionIssueItemModel] = []

class AddProductionIssueModel(BaseModel):
    issue_code: str = Field(..., min_length=1, max_length=50, description='领料单编号')
    plan_id: int = Field(..., description='生产计划ID')
    warehouse_id: int = Field(..., description='仓库ID')
    remark: Optional[str] = Field(None, description='备注')
    items: List[dict] = Field(..., description='领料明细')

class ProductionIssuePageQueryModel(BaseModel):
    page_num: int = Field(1, ge=1, description='页码')
    page_size: int = Field(10, ge=1, le=100, description='每页数量')
    plan_code: Optional[str] = Field(None, description='生产计划编号')
    status: Optional[str] = Field(None, description='状态')