from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime

class ProductionProgressItem(BaseModel):
    plan_id: int
    plan_code: str
    product_name: str
    plan_quantity: int
    finished_quantity: int
    progress: float
    status: str
    status_text: str
    start_date: datetime
    end_date: datetime

class ProductionProgressReport(BaseModel):
    total_plans: int = Field(..., description='总计划数')
    completed_plans: int = Field(..., description='已完成计划数')
    in_progress_plans: int = Field(..., description='进行中计划数')
    pending_plans: int = Field(..., description='待生产计划数')
    total_quantity: int = Field(..., description='计划总数量')
    finished_quantity: int = Field(..., description='已完成数量')
    overall_progress: float = Field(..., description='整体进度')
    details: List[ProductionProgressItem] = Field(..., description='计划明细')

class IssueDetailItem(BaseModel):
    issue_id: int
    issue_code: str
    plan_code: str
    material_id: int
    material_name: str
    plan_quantity: float
    actual_quantity: float
    unit: str
    warehouse_id: int
    status: str
    status_text: str
    create_time: datetime

class IssueDetailReport(BaseModel):
    total_issues: int = Field(..., description='总领料单数')
    issued_issues: int = Field(..., description='已发料数')
    total_material_value: float = Field(..., description='领料总金额')
    details: List[IssueDetailItem] = Field(..., description='领料明细')

class ReceiptCostItem(BaseModel):
    receipt_id: int
    receipt_code: str
    plan_code: str
    product_id: int
    product_name: str
    quantity: int
    unit_cost: float = Field(0, description='单位成本')
    total_cost: float = Field(0, description='总成本')
    warehouse_id: int
    status: str
    create_time: datetime

class ReceiptCostReport(BaseModel):
    total_receipts: int = Field(..., description='总入库单数')
    received_receipts: int = Field(..., description='已入库数')
    total_quantity: int = Field(..., description='入库总数量')
    total_cost: float = Field(..., description='入库总成本')
    average_cost: float = Field(..., description='平均成本')
    details: List[ReceiptCostItem] = Field(..., description='入库明细')

class InventoryLedgerItem(BaseModel):
    product_id: int
    product_name: str
    warehouse_id: int
    warehouse_name: str
    quantity: int
    unit: str
    batch_no: Optional[str] = None
    expire_date: Optional[datetime] = None

class InventoryLedgerReport(BaseModel):
    total_products: int = Field(..., description='商品种类数')
    total_quantity: int = Field(..., description='库存总数量')
    total_warehouses: int = Field(..., description='仓库数量')
    details: List[InventoryLedgerItem] = Field(..., description='库存台账')

class ReportQueryModel(BaseModel):
    start_date: Optional[datetime] = Field(None, description='开始日期')
    end_date: Optional[datetime] = Field(None, description='结束日期')
    warehouse_id: Optional[int] = Field(None, description='仓库ID')
    product_id: Optional[int] = Field(None, description='商品ID')