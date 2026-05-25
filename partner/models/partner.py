# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: partner.py
# @Software: PyCharm
# @Desc : 数据模型

from sqlalchemy import Column, Integer, String, Enum, Text, Boolean, DateTime, Float
from sqlalchemy.sql import func
from core.database import Base

class PartnerType(str, Enum):
    CUSTOMER = 'customer'
    SUPPLIER = 'supplier'
    BOTH = 'both'

class PartnerStatus(str, Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'

class SysPartner(Base):
    __tablename__ = 'sys_partner'
    
    partner_id = Column(Integer, primary_key=True, autoincrement=True, comment='往来单位ID')
    partner_code = Column(String(50), unique=True, nullable=False, comment='往来单位编码')
    partner_name = Column(String(100), nullable=False, comment='往来单位名称')
    short_name = Column(String(50), comment='简称')
    partner_type = Column(Enum(PartnerType), nullable=False, comment='类型：customer-客户, supplier-供应商, both-两者都是')
    status = Column(Enum(PartnerStatus), default=PartnerStatus.ACTIVE, comment='状态：active-启用, inactive-停用')
    
    contact_person = Column(String(50), comment='联系人')
    phone = Column(String(20), comment='联系电话')
    mobile = Column(String(20), comment='手机号码')
    email = Column(String(100), comment='邮箱')
    address = Column(Text, comment='地址')
    province = Column(String(50), comment='省份')
    city = Column(String(50), comment='城市')
    district = Column(String(50), comment='区县')
    
    tax_no = Column(String(50), comment='税号')
    bank_name = Column(String(100), comment='开户银行')
    bank_account = Column(String(50), comment='银行账号')
    
    credit_limit = Column(Float, default=0, comment='信用额度')
    credit_days = Column(Integer, default=0, comment='信用天数')
    
    remark = Column(Text, comment='备注')
    is_delete = Column(Boolean, default=False, comment='是否删除')
    create_time = Column(DateTime, default=func.now(), comment='创建时间')
    update_time = Column(DateTime, onupdate=func.now(), comment='更新时间')
    create_user = Column(String(50), comment='创建人')
    update_user = Column(String(50), comment='更新人')