from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from models.purchase import PurchaseStatus

class PurchaseItemModel(BaseModel):
    item_id: int = Field(..., description='明细ID')
    purchase_id: int = Field(..., description='采购单ID')
    product_id: int = Field(..., description='商品ID')
    product_name: str = Field(..., description='商品名称')
    unit: str = Field(..., description='单位')
    plan_quantity: float = Field(..., description='计划数量')
    actual_quantity: float = Field(0, description='实际到货数量')
    unit_price: float = Field(..., description='单价')
    amount: float = Field(..., description='金额')
    remark: Optional[str] = Field(None, description='备注')

class PurchaseOrderModel(BaseModel):
    purchase_id: int = Field(..., description='采购单ID')
    purchase_code: str = Field(..., description='采购单编号')
    supplier_id: int = Field(..., description='供应商ID')
    supplier_name: str = Field(..., description='供应商名称')
    warehouse_id: Optional[int] = Field(None, description='入库仓库ID')
    status: PurchaseStatus = Field(..., description='采购状态')
    total_amount: float = Field(..., description='采购总金额')
    tax_amount: float = Field(0, description='税额')
    expected_date: Optional[datetime] = Field(None, description='预计到货日期')
    remark: Optional[str] = Field(None, description='备注')
    create_time: datetime = Field(..., description='创建时间')
    items: List[PurchaseItemModel] = Field([], description='采购明细')

class AddPurchaseOrderModel(BaseModel):
    purchase_code: str = Field(..., description='采购单编号')
    supplier_id: int = Field(..., description='供应商ID')
    warehouse_id: Optional[int] = Field(None, description='入库仓库ID')
    expected_date: Optional[datetime] = Field(None, description='预计到货日期')
    remark: Optional[str] = Field(None, description='备注')
    items: List[dict] = Field(..., description='采购明细')

class PurchasePageQueryModel(BaseModel):
    page_num: int = Field(1, description='页码')
    page_size: int = Field(10, description='每页数量')
    purchase_code: Optional[str] = Field(None, description='采购单编号')
    supplier_id: Optional[int] = Field(None, description='供应商ID')
    status: Optional[PurchaseStatus] = Field(None, description='采购状态')