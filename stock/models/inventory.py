# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: inventory.py
# @Software: PyCharm
# @Desc : 数据模型

from sqlalchemy import Column, Integer, String, Numeric, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime

class SysInventory(Base):
    __tablename__ = 'sys_inventory'
    
    inventory_id = Column(Integer, primary_key=True, autoincrement=True, comment='库存ID')
    product_id = Column(Integer, nullable=False, comment='商品ID')
    warehouse_id = Column(Integer, ForeignKey('sys_warehouse.warehouse_id'), nullable=False, comment='仓库ID')
    quantity = Column(Integer, nullable=False, default=0, comment='库存数量')
    min_quantity = Column(Integer, default=0, comment='最低库存')
    max_quantity = Column(Integer, default=999999, comment='最高库存')
    unit = Column(String(20), comment='单位')
    batch_no = Column(String(50), comment='批次号')
    expire_date = Column(DateTime, comment='有效期')
    create_time = Column(DateTime, default=datetime.now, comment='创建时间')
    update_time = Column(DateTime, onupdate=datetime.now, comment='更新时间')
    
    warehouse = relationship('SysWarehouse', backref='inventories')