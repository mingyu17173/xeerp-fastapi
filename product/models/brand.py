from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class SysProductBrand(Base):
    """
    商品品牌表
    """
    __tablename__ = 'sys_product_brand'

    brand_id = Column(Integer, primary_key=True, autoincrement=True, comment='品牌ID')
    brand_name = Column(String(200), nullable=False, comment='品牌名称')
    brand_code = Column(String(100), unique=True, nullable=False, comment='品牌编码')
    brand_logo = Column(String(500), nullable=True, comment='品牌logo路径')
    sort_order = Column(Integer, nullable=False, default=0, comment='排序号')
    status = Column(String(1), nullable=False, default='0', comment='状态（0正常 1停用）')
    is_delete = Column(String(1), nullable=False, default='0', comment='删除标志（0代表存在 2代表删除）')
    create_by = Column(String(64), nullable=True, comment='创建者')
    create_time = Column(DateTime, nullable=True, default=datetime.now, comment='创建时间')
    update_by = Column(String(64), nullable=True, comment='更新者')
    update_time = Column(DateTime, nullable=True, onupdate=datetime.now, comment='更新时间')
    remark = Column(String(500), nullable=True, comment='备注')

    def __repr__(self):
        return f"<SysProductBrand(brand_id={self.brand_id}, brand_name='{self.brand_name}')>"