# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: category.py
# @Software: PyCharm
# @Desc : 数据模型

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class SysProductCategory(Base):
    """
    商品分类表
    """
    __tablename__ = 'sys_product_category'

    category_id = Column(Integer, primary_key=True, autoincrement=True, comment='分类ID')
    parent_id = Column(Integer, ForeignKey('sys_product_category.category_id'), nullable=True, comment='父分类ID')
    category_name = Column(String(200), nullable=False, comment='分类名称')
    category_code = Column(String(100), unique=True, nullable=False, comment='分类编码')
    sort_order = Column(Integer, nullable=False, default=0, comment='排序号')
    status = Column(String(1), nullable=False, default='0', comment='状态（0正常 1停用）')
    is_delete = Column(String(1), nullable=False, default='0', comment='删除标志（0代表存在 2代表删除）')
    create_by = Column(String(64), nullable=True, comment='创建者')
    create_time = Column(DateTime, nullable=True, default=datetime.now, comment='创建时间')
    update_by = Column(String(64), nullable=True, comment='更新者')
    update_time = Column(DateTime, nullable=True, onupdate=datetime.now, comment='更新时间')
    remark = Column(String(500), nullable=True, comment='备注')

    # 自关联关系
    parent = relationship('SysProductCategory', remote_side=[category_id], backref='children')

    def __repr__(self):
        return f"<SysProductCategory(category_id={self.category_id}, category_name='{self.category_name}')>"