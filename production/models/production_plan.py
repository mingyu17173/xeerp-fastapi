# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: production_plan.py
# @Software: PyCharm
# @Desc : 数据模型

from sqlalchemy import Column, Integer, String, Numeric, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime

class SysProductionPlan(Base):
    __tablename__ = 'sys_production_plan'
    
    plan_id = Column(Integer, primary_key=True, autoincrement=True, comment='生产计划ID')
    plan_code = Column(String(50), unique=True, nullable=False, comment='生产计划编号')
    product_id = Column(Integer, nullable=False, comment='产品ID')
    product_name = Column(String(200), comment='产品名称')
    bom_id = Column(Integer, ForeignKey('sys_bom.bom_id'), nullable=False, comment='BOMID')
    plan_quantity = Column(Integer, nullable=False, comment='计划数量')
    finished_quantity = Column(Integer, default=0, comment='已完成数量')
    warehouse_id = Column(Integer, comment='入库仓库ID')
    start_date = Column(DateTime, nullable=False, comment='计划开始日期')
    end_date = Column(DateTime, nullable=False, comment='计划结束日期')
    status = Column(String(1), nullable=False, default='0', comment='状态 0待生产 1生产中 2已完成 3已取消')
    remark = Column(String(500), comment='备注')
    create_by = Column(String(50), comment='创建人')
    create_time = Column(DateTime, default=datetime.now, comment='创建时间')
    update_by = Column(String(50), comment='更新人')
    update_time = Column(DateTime, onupdate=datetime.now, comment='更新时间')
    
    bom = relationship('SysBom')
    issues = relationship('SysProductionIssue', backref='plan')
    receipts = relationship('SysProductionReceipt', backref='plan')