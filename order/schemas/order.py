from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from models.order import OrderStatus, OrderType

class OrderItemModel(BaseModel):
    item_id: int = Field(..., description='明细ID')
    order_id: int = Field(..., description='订单ID')
    product_id: int = Field(..., description='商品ID')
    product_name: str = Field(..., description='商品名称')
    unit: str = Field(..., description='单位')
    quantity: float = Field(..., description='数量')
    unit_price: float = Field(..., description='单价')
    amount: float = Field(..., description='金额')
    remark: Optional[str] = Field(None, description='备注')

class OrderModel(BaseModel):
    order_id: int = Field(..., description='订单ID')
    order_code: str = Field(..., description='订单编号')
    order_type: OrderType = Field(..., description='订单类型')
    partner_id: int = Field(..., description='客户/供应商ID')
    partner_name: str = Field(..., description='客户/供应商名称')
    status: OrderStatus = Field(..., description='订单状态')
    total_amount: float = Field(..., description='订单总金额')
    tax_amount: float = Field(0, description='税额')
    discount_amount: float = Field(0, description='折扣金额')
    pay_amount: float = Field(..., description='实付金额')
    shipping_address: Optional[str] = Field(None, description='送货地址')
    contact_person: Optional[str] = Field(None, description='联系人')
    contact_phone: Optional[str] = Field(None, description='联系电话')
    delivery_date: Optional[datetime] = Field(None, description='预计交货日期')
    remark: Optional[str] = Field(None, description='备注')
    create_time: datetime = Field(..., description='创建时间')
    items: List[OrderItemModel] = Field([], description='订单明细')

class AddOrderModel(BaseModel):
    order_code: str = Field(..., description='订单编号')
    order_type: OrderType = Field(..., description='订单类型')
    partner_id: int = Field(..., description='客户/供应商ID')
    shipping_address: Optional[str] = Field(None, description='送货地址')
    contact_person: Optional[str] = Field(None, description='联系人')
    contact_phone: Optional[str] = Field(None, description='联系电话')
    delivery_date: Optional[datetime] = Field(None, description='预计交货日期')
    remark: Optional[str] = Field(None, description='备注')
    items: List[dict] = Field(..., description='订单明细')

class OrderPageQueryModel(BaseModel):
    page_num: int = Field(1, description='页码')
    page_size: int = Field(10, description='每页数量')
    order_code: Optional[str] = Field(None, description='订单编号')
    partner_id: Optional[int] = Field(None, description='客户/供应商ID')
    order_type: Optional[OrderType] = Field(None, description='订单类型')
    status: Optional[OrderStatus] = Field(None, description='订单状态')