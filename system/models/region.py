# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: region.py
# @Software: PyCharm
# @Desc : 数据模型

from sqlalchemy import String, Integer, BINARY, Column
from core.database import Base


class SysRegion(Base):
    """
    地区表
    """

    __tablename__ = 'sys_region'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, comment='')
    code = Column(String(128), nullable=True, comment='统计用区划代码')
    name = Column(String(120), nullable=True, comment='名称')
    parent_id = Column(Integer, nullable=True, comment='父级')
    level = Column(BINARY, nullable=True, comment='级别')



