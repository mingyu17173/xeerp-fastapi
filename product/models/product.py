# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: product.py
# @Software: PyCharm
# @Desc : 数据模型

from datetime import datetime
from sqlalchemy import Column, Integer, String, Numeric, DateTime, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class SysProduct(Base):
    """
    商品信息表
    """
    __tablename__ = 'sys_product'

    product_id = Column(Integer, primary_key=True, autoincrement=True, comment='商品ID')
    product_name = Column(String(200), nullable=False, comment='商品名称')
    product_code = Column(String(100), unique=True, nullable=False, comment='商品编码')
    category_id = Column(Integer, ForeignKey('sys_product_category.category_id'), nullable=True, comment='分类ID')
    brand_id = Column(Integer, ForeignKey('sys_product_brand.brand_id'), nullable=True, comment='品牌ID')
    unit_id = Column(Integer, ForeignKey('sys_product_unit.unit_id'), nullable=True, comment='单位ID')
    description = Column(Text, nullable=True, comment='商品描述')
    price = Column(Numeric(18, 2), nullable=False, default=0.00, comment='售价')
    cost_price = Column(Numeric(18, 2), nullable=False, default=0.00, comment='成本价')
    stock = Column(Integer, nullable=False, default=0, comment='库存数量')
    status = Column(String(1), nullable=False, default='0', comment='状态（0正常 1停用）')
    is_delete = Column(String(1), nullable=False, default='0', comment='删除标志（0代表存在 2代表删除）')
    create_by = Column(String(64), nullable=True, comment='创建者')
    create_time = Column(DateTime, nullable=True, default=datetime.now, comment='创建时间')
    update_by = Column(String(64), nullable=True, comment='更新者')
    update_time = Column(DateTime, nullable=True, onupdate=datetime.now, comment='更新时间')
    remark = Column(String(500), nullable=True, comment='备注')

    # 关联关系
    category = relationship('SysProductCategory', backref='products')
    brand = relationship('SysProductBrand', backref='products')
    unit = relationship('SysProductUnit', backref='products')

    def __repr__(self):
        return f"<SysProduct(product_id={self.product_id}, product_name='{self.product_name}')>"