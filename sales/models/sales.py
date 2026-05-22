"""
Sales Service Models
销售服务数据模型
"""

from sqlalchemy import Column, Integer, String, Enum, Text, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base

class SalesOrderStatus(str, Enum):
    """销售订单状态"""
    PENDING = 'pending'      # 待审核
    APPROVED = 'approved'    # 已审核
    SHIPPED = 'shipped'      # 已发货
    COMPLETED = 'completed'  # 已完成
    CANCELLED = 'cancelled'  # 已取消

class DeliveryStatus(str, Enum):
    """发货状态"""
    PENDING = 'pending'      # 待发货
    PARTIAL = 'partial'      # 部分发货
    COMPLETED = 'completed'  # 已完成

class ReturnStatus(str, Enum):
    """退货状态"""
    PENDING = 'pending'      # 待审核
    APPROVED = 'approved'    # 已审核
    RETURNED = 'returned'    # 已退货
    REJECTED = 'rejected'    # 已拒绝

class SysSalesOrder(Base):
    """销售订单主表"""
    __tablename__ = 'sys_sales_order'
    
    sales_id = Column(Integer, primary_key=True, autoincrement=True, comment='销售订单ID')
    sales_code = Column(String(50), unique=True, nullable=False, comment='销售订单编号')
    customer_id = Column(Integer, nullable=False, comment='客户ID')
    customer_name = Column(String(100), comment='客户名称')
    warehouse_id = Column(Integer, comment='发货仓库ID')
    
    status = Column(Enum(SalesOrderStatus), default=SalesOrderStatus.PENDING, comment='订单状态')
    delivery_status = Column(Enum(DeliveryStatus), default=DeliveryStatus.PENDING, comment='发货状态')
    
    total_amount = Column(Float, default=0, comment='订单总金额')
    tax_amount = Column(Float, default=0, comment='税额')
    discount_amount = Column(Float, default=0, comment='优惠金额')
    paid_amount = Column(Float, default=0, comment='已付款金额')
    
    delivery_date = Column(DateTime, comment='预计发货日期')
    shipping_address = Column(Text, comment='收货地址')
    contact_person = Column(String(50), comment='联系人')
    contact_phone = Column(String(20), comment='联系电话')
    
    remark = Column(Text, comment='备注')
    is_delete = Column(Boolean, default=False, comment='是否删除')
    create_time = Column(DateTime, default=func.now(), comment='创建时间')
    update_time = Column(DateTime, onupdate=func.now(), comment='更新时间')
    create_user = Column(String(50), comment='创建人')
    update_user = Column(String(50), comment='更新人')
    
    items = relationship('SysSalesItem', backref='sales_order', cascade='all, delete-orphan')
    deliveries = relationship('SysSalesDelivery', backref='sales_order')
    returns = relationship('SysSalesReturn', backref='sales_order')

class SysSalesItem(Base):
    """销售订单明细表"""
    __tablename__ = 'sys_sales_item'
    
    item_id = Column(Integer, primary_key=True, autoincrement=True, comment='明细ID')
    sales_id = Column(Integer, ForeignKey('sys_sales_order.sales_id'), nullable=False, comment='销售订单ID')
    product_id = Column(Integer, nullable=False, comment='商品ID')
    product_name = Column(String(100), comment='商品名称')
    product_code = Column(String(50), comment='商品编码')
    unit = Column(String(20), comment='单位')
    quantity = Column(Float, nullable=False, comment='数量')
    delivered_quantity = Column(Float, default=0, comment='已发货数量')
    returned_quantity = Column(Float, default=0, comment='已退货数量')
    unit_price = Column(Float, nullable=False, comment='单价')
    amount = Column(Float, default=0, comment='金额')
    discount = Column(Float, default=0, comment='折扣率')
    
    remark = Column(String(200), comment='备注')

class SysSalesDelivery(Base):
    """销售发货单"""
    __tablename__ = 'sys_sales_delivery'
    
    delivery_id = Column(Integer, primary_key=True, autoincrement=True, comment='发货单ID')
    delivery_code = Column(String(50), unique=True, nullable=False, comment='发货单编号')
    sales_id = Column(Integer, ForeignKey('sys_sales_order.sales_id'), nullable=False, comment='销售订单ID')
    
    warehouse_id = Column(Integer, nullable=False, comment='发货仓库ID')
    warehouse_name = Column(String(100), comment='仓库名称')
    
    status = Column(Enum(DeliveryStatus), default=DeliveryStatus.PENDING, comment='发货状态')
    total_quantity = Column(Float, default=0, comment='发货总数量')
    
    delivery_time = Column(DateTime, comment='发货时间')
    carrier = Column(String(50), comment='承运商')
    tracking_no = Column(String(50), comment='运单号')
    
    remark = Column(Text, comment='备注')
    is_delete = Column(Boolean, default=False, comment='是否删除')
    create_time = Column(DateTime, default=func.now(), comment='创建时间')
    create_user = Column(String(50), comment='创建人')
    
    items = relationship('SysSalesDeliveryItem', backref='delivery', cascade='all, delete-orphan')

class SysSalesDeliveryItem(Base):
    """销售发货明细"""
    __tablename__ = 'sys_sales_delivery_item'
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment='ID')
    delivery_id = Column(Integer, ForeignKey('sys_sales_delivery.delivery_id'), nullable=False, comment='发货单ID')
    sales_item_id = Column(Integer, ForeignKey('sys_sales_item.item_id'), nullable=False, comment='销售明细ID')
    
    product_id = Column(Integer, nullable=False, comment='商品ID')
    product_name = Column(String(100), comment='商品名称')
    unit = Column(String(20), comment='单位')
    quantity = Column(Float, nullable=False, comment='发货数量')
    batch_no = Column(String(50), comment='批次号')
    
    remark = Column(String(200), comment='备注')

class SysSalesReturn(Base):
    """销售退货单"""
    __tablename__ = 'sys_sales_return'
    
    return_id = Column(Integer, primary_key=True, autoincrement=True, comment='退货单ID')
    return_code = Column(String(50), unique=True, nullable=False, comment='退货单编号')
    sales_id = Column(Integer, ForeignKey('sys_sales_order.sales_id'), nullable=False, comment='销售订单ID')
    
    warehouse_id = Column(Integer, comment='退货入库仓库ID')
    status = Column(Enum(ReturnStatus), default=ReturnStatus.PENDING, comment='退货状态')
    
    total_amount = Column(Float, default=0, comment='退货总金额')
    reason = Column(Text, comment='退货原因')
    
    remark = Column(Text, comment='备注')
    is_delete = Column(Boolean, default=False, comment='是否删除')
    create_time = Column(DateTime, default=func.now(), comment='创建时间')
    update_time = Column(DateTime, onupdate=func.now(), comment='更新时间')
    create_user = Column(String(50), comment='创建人')
    update_user = Column(String(50), comment='更新人')
    
    items = relationship('SysSalesReturnItem', backref='return_order', cascade='all, delete-orphan')

class SysSalesReturnItem(Base):
    """销售退货明细"""
    __tablename__ = 'sys_sales_return_item'
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment='ID')
    return_id = Column(Integer, ForeignKey('sys_sales_return.return_id'), nullable=False, comment='退货单ID')
    sales_item_id = Column(Integer, ForeignKey('sys_sales_item.item_id'), nullable=False, comment='销售明细ID')
    
    product_id = Column(Integer, nullable=False, comment='商品ID')
    product_name = Column(String(100), comment='商品名称')
    unit = Column(String(20), comment='单位')
    quantity = Column(Float, nullable=False, comment='退货数量')
    unit_price = Column(Float, nullable=False, comment='单价')
    amount = Column(Float, default=0, comment='金额')
    
    reason = Column(String(200), comment='退货原因')