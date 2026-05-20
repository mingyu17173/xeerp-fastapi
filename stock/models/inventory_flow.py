from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from core.database import Base
from datetime import datetime

class SysInventoryFlow(Base):
    __tablename__ = 'sys_inventory_flow'
    
    flow_id = Column(Integer, primary_key=True, autoincrement=True, comment='流水ID')
    product_id = Column(Integer, nullable=False, comment='商品ID')
    warehouse_id = Column(Integer, nullable=False, comment='仓库ID')
    flow_type = Column(String(20), nullable=False, comment='流水类型：in-入库 out-出库 adjust-调整')
    quantity = Column(Integer, nullable=False, comment='数量')
    before_quantity = Column(Integer, nullable=False, comment='变动前数量')
    after_quantity = Column(Integer, nullable=False, comment='变动后数量')
    batch_no = Column(String(50), comment='批次号')
    source_type = Column(String(50), comment='来源类型：purchase-采购 production-生产 sales-销售')
    source_id = Column(Integer, comment='来源单据ID')
    remark = Column(String(500), comment='备注')
    create_by = Column(String(50), comment='操作人')
    create_time = Column(DateTime, default=datetime.now, comment='操作时间')