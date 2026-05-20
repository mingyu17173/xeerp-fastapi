from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class SysProductUnit(Base):
    """
    商品单位表
    """
    __tablename__ = 'sys_product_unit'

    unit_id = Column(Integer, primary_key=True, autoincrement=True, comment='单位ID')
    unit_name = Column(String(100), nullable=False, comment='单位名称')
    unit_code = Column(String(50), unique=True, nullable=False, comment='单位编码')
    sort_order = Column(Integer, nullable=False, default=0, comment='排序号')
    status = Column(String(1), nullable=False, default='0', comment='状态（0正常 1停用）')
    is_delete = Column(String(1), nullable=False, default='0', comment='删除标志（0代表存在 2代表删除）')
    create_by = Column(String(64), nullable=True, comment='创建者')
    create_time = Column(DateTime, nullable=True, default=datetime.now, comment='创建时间')
    update_by = Column(String(64), nullable=True, comment='更新者')
    update_time = Column(DateTime, nullable=True, onupdate=datetime.now, comment='更新时间')
    remark = Column(String(500), nullable=True, comment='备注')

    def __repr__(self):
        return f"<SysProductUnit(unit_id={self.unit_id}, unit_name='{self.unit_name}')>"