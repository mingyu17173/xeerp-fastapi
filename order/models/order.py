from sqlalchemy import Column, Integer, String, Enum, Text, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base

class OrderStatus(str, Enum):
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    SHIPPED = 'shipped'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'

class OrderType(str, Enum):
    SALES = 'sales'
    PURCHASE = 'purchase'

class SysOrder(Base):
    __tablename__ = 'sys_order'
    
    order_id = Column(Integer, primary_key=True, autoincrement=True, comment='订单ID')
    order_code = Column(String(50), unique=True, nullable=False, comment='订单编号')
    order_type = Column(Enum(OrderType), nullable=False, comment='订单类型')
    partner_id = Column(Integer, nullable=False, comment='客户/供应商ID')
    partner_name = Column(String(100), comment='客户/供应商名称')
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING, comment='订单状态')
    
    total_amount = Column(Float, default=0, comment='订单总金额')
    tax_amount = Column(Float, default=0, comment='税额')
    discount_amount = Column(Float, default=0, comment='折扣金额')
    pay_amount = Column(Float, default=0, comment='实付金额')
    
    shipping_address = Column(Text, comment='送货地址')
    contact_person = Column(String(50), comment='联系人')
    contact_phone = Column(String(20), comment='联系电话')
    
    delivery_date = Column(DateTime, comment='预计交货日期')
    remark = Column(Text, comment='备注')
    
    is_delete = Column(Boolean, default=False, comment='是否删除')
    create_time = Column(DateTime, default=func.now(), comment='创建时间')
    update_time = Column(DateTime, onupdate=func.now(), comment='更新时间')
    create_user = Column(String(50), comment='创建人')
    
    items = relationship('SysOrderItem', backref='order', cascade='all, delete-orphan')

class SysOrderItem(Base):
    __tablename__ = 'sys_order_item'
    
    item_id = Column(Integer, primary_key=True, autoincrement=True, comment='明细ID')
    order_id = Column(Integer, ForeignKey('sys_order.order_id'), nullable=False, comment='订单ID')
    product_id = Column(Integer, nullable=False, comment='商品ID')
    product_name = Column(String(100), comment='商品名称')
    unit = Column(String(20), comment='单位')
    quantity = Column(Float, nullable=False, comment='数量')
    unit_price = Column(Float, nullable=False, comment='单价')
    amount = Column(Float, default=0, comment='金额')
    remark = Column(String(200), comment='备注')