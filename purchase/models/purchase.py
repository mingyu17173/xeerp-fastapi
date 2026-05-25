# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: purchase.py
# @Software: PyCharm
# @Desc : 数据模型

from sqlalchemy import Column, Integer, String, Enum, Text, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base

class PurchaseStatus(str, Enum):
    PENDING = 'pending'
    APPROVED = 'approved'
    ORDERED = 'ordered'
    RECEIVED = 'received'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'

class SysPurchaseOrder(Base):
    __tablename__ = 'sys_purchase_order'
    
    purchase_id = Column(Integer, primary_key=True, autoincrement=True, comment='采购单ID')
    purchase_code = Column(String(50), unique=True, nullable=False, comment='采购单编号')
    supplier_id = Column(Integer, nullable=False, comment='供应商ID')
    supplier_name = Column(String(100), comment='供应商名称')
    warehouse_id = Column(Integer, comment='入库仓库ID')
    status = Column(Enum(PurchaseStatus), default=PurchaseStatus.PENDING, comment='采购状态')
    
    total_amount = Column(Float, default=0, comment='采购总金额')
    tax_amount = Column(Float, default=0, comment='税额')
    
    expected_date = Column(DateTime, comment='预计到货日期')
    remark = Column(Text, comment='备注')
    
    is_delete = Column(Boolean, default=False, comment='是否删除')
    create_time = Column(DateTime, default=func.now(), comment='创建时间')
    update_time = Column(DateTime, onupdate=func.now(), comment='更新时间')
    create_user = Column(String(50), comment='创建人')
    
    items = relationship('SysPurchaseItem', backref='purchase', cascade='all, delete-orphan')

class SysPurchaseItem(Base):
    __tablename__ = 'sys_purchase_item'
    
    item_id = Column(Integer, primary_key=True, autoincrement=True, comment='明细ID')
    purchase_id = Column(Integer, ForeignKey('sys_purchase_order.purchase_id'), nullable=False, comment='采购单ID')
    product_id = Column(Integer, nullable=False, comment='商品ID')
    product_name = Column(String(100), comment='商品名称')
    unit = Column(String(20), comment='单位')
    plan_quantity = Column(Float, nullable=False, comment='计划数量')
    actual_quantity = Column(Float, default=0, comment='实际到货数量')
    unit_price = Column(Float, nullable=False, comment='单价')
    amount = Column(Float, default=0, comment='金额')
    remark = Column(String(200), comment='备注')