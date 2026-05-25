# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: bom.py
# @Software: PyCharm
# @Desc : 数据模型

from sqlalchemy import Column, Integer, String, Numeric, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime

class SysBom(Base):
    __tablename__ = 'sys_bom'
    
    bom_id = Column(Integer, primary_key=True, autoincrement=True, comment='BOMID')
    product_id = Column(Integer, nullable=False, comment='成品ID')
    product_name = Column(String(200), comment='成品名称')
    version = Column(String(20), nullable=False, default='V1.0', comment='版本号')
    status = Column(String(1), nullable=False, default='0', comment='状态 0启用 1禁用')
    remark = Column(String(500), comment='备注')
    create_by = Column(String(50), comment='创建人')
    create_time = Column(DateTime, default=datetime.now, comment='创建时间')
    update_by = Column(String(50), comment='更新人')
    update_time = Column(DateTime, onupdate=datetime.now, comment='更新时间')
    is_delete = Column(Boolean, default=False, comment='是否删除')
    
    items = relationship('SysBomItem', backref='bom', cascade='all, delete-orphan')

class SysBomItem(Base):
    __tablename__ = 'sys_bom_item'
    
    bom_item_id = Column(Integer, primary_key=True, autoincrement=True, comment='BOM明细ID')
    bom_id = Column(Integer, ForeignKey('sys_bom.bom_id'), nullable=False, comment='BOMID')
    material_id = Column(Integer, nullable=False, comment='物料ID')
    material_name = Column(String(200), comment='物料名称')
    unit = Column(String(20), comment='单位')
    quantity = Column(Numeric(18, 4), nullable=False, comment='用量')
    scrap_rate = Column(Numeric(10, 4), default=0, comment='损耗率')
    remark = Column(String(500), comment='备注')