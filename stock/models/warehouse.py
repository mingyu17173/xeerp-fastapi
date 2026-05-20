from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from core.database import Base
from datetime import datetime

class SysWarehouse(Base):
    __tablename__ = 'sys_warehouse'
    
    warehouse_id = Column(Integer, primary_key=True, autoincrement=True, comment='仓库ID')
    warehouse_code = Column(String(50), unique=True, nullable=False, comment='仓库编码')
    warehouse_name = Column(String(100), nullable=False, comment='仓库名称')
    address = Column(String(500), comment='仓库地址')
    manager = Column(String(50), comment='仓库管理员')
    phone = Column(String(20), comment='联系电话')
    status = Column(String(1), nullable=False, default='0', comment='状态 0启用 1禁用')
    remark = Column(Text, comment='备注')
    create_by = Column(String(50), comment='创建人')
    create_time = Column(DateTime, default=datetime.now, comment='创建时间')
    update_by = Column(String(50), comment='更新人')
    update_time = Column(DateTime, onupdate=datetime.now, comment='更新时间')
    is_delete = Column(Boolean, default=False, comment='是否删除')