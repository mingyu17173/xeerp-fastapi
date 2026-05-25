# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: sales.py
# @Software: PyCharm
# @Desc : 数据模式

"""
Sales Service Schemas
销售服务请求/响应结构体
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

# 销售订单明细
class SalesItemModel(BaseModel):
    product_id: int = Field(..., description='商品ID')
    product_name: Optional[str] = Field(None, description='商品名称')
    product_code: Optional[str] = Field(None, description='商品编码')
    unit: str = Field(..., description='单位')
    quantity: float = Field(..., description='数量')
    unit_price: float = Field(..., description='单价')
    amount: Optional[float] = Field(None, description='金额')
    discount: Optional[float] = Field(0, description='折扣率')
    remark: Optional[str] = Field(None, description='备注')

# 新增销售订单
class AddSalesOrderModel(BaseModel):
    sales_code: str = Field(..., description='销售订单编号')
    customer_id: int = Field(..., description='客户ID')
    customer_name: Optional[str] = Field(None, description='客户名称')
    warehouse_id: Optional[int] = Field(None, description='发货仓库ID')
    
    total_amount: Optional[float] = Field(0, description='订单总金额')
    tax_amount: Optional[float] = Field(0, description='税额')
    discount_amount: Optional[float] = Field(0, description='优惠金额')
    
    delivery_date: Optional[datetime] = Field(None, description='预计发货日期')
    shipping_address: Optional[str] = Field(None, description='收货地址')
    contact_person: Optional[str] = Field(None, description='联系人')
    contact_phone: Optional[str] = Field(None, description='联系电话')
    
    remark: Optional[str] = Field(None, description='备注')
    items: List[SalesItemModel] = Field(..., description='订单明细')

# 编辑销售订单
class EditSalesOrderModel(BaseModel):
    sales_id: int = Field(..., description='销售订单ID')
    customer_id: Optional[int] = Field(None, description='客户ID')
    customer_name: Optional[str] = Field(None, description='客户名称')
    warehouse_id: Optional[int] = Field(None, description='发货仓库ID')
    
    delivery_date: Optional[datetime] = Field(None, description='预计发货日期')
    shipping_address: Optional[str] = Field(None, description='收货地址')
    contact_person: Optional[str] = Field(None, description='联系人')
    contact_phone: Optional[str] = Field(None, description='联系电话')
    
    remark: Optional[str] = Field(None, description='备注')

# 销售订单查询
class SalesOrderPageQueryModel(BaseModel):
    page_num: int = Field(1, description='页码')
    page_size: int = Field(10, description='每页大小')
    sales_code: Optional[str] = Field(None, description='销售订单编号')
    customer_name: Optional[str] = Field(None, description='客户名称')
    status: Optional[str] = Field(None, description='订单状态')
    start_date: Optional[datetime] = Field(None, description='开始日期')
    end_date: Optional[datetime] = Field(None, description='结束日期')

# 销售订单详情
class SalesOrderDetailModel(BaseModel):
    sales_id: int = Field(..., description='销售订单ID')
    sales_code: str = Field(..., description='销售订单编号')
    customer_id: int = Field(..., description='客户ID')
    customer_name: str = Field(..., description='客户名称')
    warehouse_id: Optional[int] = Field(None, description='发货仓库ID')
    
    status: str = Field(..., description='订单状态')
    delivery_status: str = Field(..., description='发货状态')
    
    total_amount: float = Field(..., description='订单总金额')
    tax_amount: float = Field(..., description='税额')
    discount_amount: float = Field(..., description='优惠金额')
    paid_amount: float = Field(..., description='已付款金额')
    
    delivery_date: Optional[datetime] = Field(None, description='预计发货日期')
    shipping_address: Optional[str] = Field(None, description='收货地址')
    contact_person: Optional[str] = Field(None, description='联系人')
    contact_phone: Optional[str] = Field(None, description='联系电话')
    
    remark: Optional[str] = Field(None, description='备注')
    create_time: datetime = Field(..., description='创建时间')
    create_user: str = Field(..., description='创建人')
    
    items: List[SalesItemModel] = Field(..., description='订单明细')

# 发货单明细
class DeliveryItemModel(BaseModel):
    sales_item_id: int = Field(..., description='销售明细ID')
    product_id: int = Field(..., description='商品ID')
    product_name: Optional[str] = Field(None, description='商品名称')
    unit: str = Field(..., description='单位')
    quantity: float = Field(..., description='发货数量')
    batch_no: Optional[str] = Field(None, description='批次号')

# 新增发货单
class AddDeliveryModel(BaseModel):
    delivery_code: str = Field(..., description='发货单编号')
    sales_id: int = Field(..., description='销售订单ID')
    warehouse_id: int = Field(..., description='发货仓库ID')
    warehouse_name: Optional[str] = Field(None, description='仓库名称')
    carrier: Optional[str] = Field(None, description='承运商')
    tracking_no: Optional[str] = Field(None, description='运单号')
    remark: Optional[str] = Field(None, description='备注')
    items: List[DeliveryItemModel] = Field(..., description='发货明细')

# 退货单明细
class ReturnItemModel(BaseModel):
    sales_item_id: int = Field(..., description='销售明细ID')
    product_id: int = Field(..., description='商品ID')
    product_name: Optional[str] = Field(None, description='商品名称')
    unit: str = Field(..., description='单位')
    quantity: float = Field(..., description='退货数量')
    unit_price: float = Field(..., description='单价')
    amount: Optional[float] = Field(None, description='金额')
    reason: Optional[str] = Field(None, description='退货原因')

# 新增退货单
class AddReturnModel(BaseModel):
    return_code: str = Field(..., description='退货单编号')
    sales_id: int = Field(..., description='销售订单ID')
    warehouse_id: Optional[int] = Field(None, description='退货入库仓库ID')
    total_amount: Optional[float] = Field(0, description='退货总金额')
    reason: Optional[str] = Field(None, description='退货原因')
    remark: Optional[str] = Field(None, description='备注')
    items: List[ReturnItemModel] = Field(..., description='退货明细')

# 退货单审核
class ApproveReturnModel(BaseModel):
    return_id: int = Field(..., description='退货单ID')
    approved: bool = Field(..., description='是否通过')
    remark: Optional[str] = Field(None, description='审核意见')