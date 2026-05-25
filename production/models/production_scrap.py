# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: production_scrap.py
# @Software: PyCharm
# @Desc : 数据模型

from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime

class SysProductionScrap(Base):
    __tablename__ = 'sys_production_scrap'
    
    scrap_id = Column(Integer, primary_key=True, autoincrement=True, comment='损耗记录ID')
    scrap_code = Column(String(50), unique=True, nullable=False, comment='损耗单号')
    plan_id = Column(Integer, ForeignKey('sys_production_plan.plan_id'), nullable=False, comment='生产计划ID')
    issue_id = Column(Integer, ForeignKey('sys_production_issue.issue_id'), comment='领料单ID')
    warehouse_id = Column(Integer, nullable=False, comment='仓库ID')
    status = Column(String(1), nullable=False, default='0', comment='状态 0待审核 1已审核 2已记账 3已取消')
    remark = Column(String(500), comment='备注')
    create_by = Column(String(50), comment='创建人')
    create_time = Column(DateTime, default=datetime.now, comment='创建时间')
    update_by = Column(String(50), comment='更新人')
    update_time = Column(DateTime, onupdate=datetime.now, comment='更新时间')
    
    items = relationship('SysProductionScrapItem', backref='scrap', cascade='all, delete-orphan')

class SysProductionScrapItem(Base):
    __tablename__ = 'sys_production_scrap_item'
    
    scrap_item_id = Column(Integer, primary_key=True, autoincrement=True, comment='损耗明细ID')
    scrap_id = Column(Integer, ForeignKey('sys_production_scrap.scrap_id'), nullable=False, comment='损耗记录ID')
    material_id = Column(Integer, nullable=False, comment='物料ID')
    material_name = Column(String(200), comment='物料名称')
    unit = Column(String(20), comment='单位')
    quantity = Column(Numeric(18, 4), nullable=False, comment='损耗数量')
    batch_no = Column(String(50), comment='批次号')
    reason = Column(String(200), comment='损耗原因')