# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: approval.py
# @Software: PyCharm
# @Desc : 数据模型

from sqlalchemy import Column, Integer, String, Enum, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base

class ApprovalType(str, Enum):
    PRODUCTION_PLAN = 'production_plan'
    PRODUCTION_ISSUE = 'production_issue'
    PURCHASE_ORDER = 'purchase_order'
    OTHER = 'other'

class ApprovalStatus(str, Enum):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    CANCELLED = 'cancelled'

class ApprovalNodeType(str, Enum):
    START = 'start'
    APPROVE = 'approve'
    CC = 'cc'
    END = 'end'

class SysApprovalFlow(Base):
    __tablename__ = 'sys_approval_flow'
    
    flow_id = Column(Integer, primary_key=True, autoincrement=True, comment='流程ID')
    flow_code = Column(String(50), unique=True, nullable=False, comment='流程编码')
    flow_name = Column(String(100), nullable=False, comment='流程名称')
    approval_type = Column(Enum(ApprovalType), nullable=False, comment='审批类型')
    description = Column(Text, comment='流程描述')
    is_active = Column(Boolean, default=True, comment='是否启用')
    create_time = Column(DateTime, default=func.now(), comment='创建时间')
    create_user = Column(String(50), comment='创建人')
    
    nodes = relationship('SysApprovalNode', backref='flow', cascade='all, delete-orphan')

class SysApprovalNode(Base):
    __tablename__ = 'sys_approval_node'
    
    node_id = Column(Integer, primary_key=True, autoincrement=True, comment='节点ID')
    flow_id = Column(Integer, ForeignKey('sys_approval_flow.flow_id'), nullable=False, comment='流程ID')
    node_name = Column(String(50), nullable=False, comment='节点名称')
    node_type = Column(Enum(ApprovalNodeType), nullable=False, comment='节点类型')
    node_order = Column(Integer, nullable=False, comment='节点顺序')
    approver_role = Column(String(50), comment='审批角色')
    approver_user = Column(String(50), comment='审批人')
    is_multiple = Column(Boolean, default=False, comment='是否多人审批')
    condition_expression = Column(Text, comment='条件表达式')

class SysApprovalInstance(Base):
    __tablename__ = 'sys_approval_instance'
    
    instance_id = Column(Integer, primary_key=True, autoincrement=True, comment='审批实例ID')
    flow_id = Column(Integer, ForeignKey('sys_approval_flow.flow_id'), nullable=False, comment='流程ID')
    source_type = Column(String(50), nullable=False, comment='业务类型')
    source_id = Column(Integer, nullable=False, comment='业务ID')
    source_code = Column(String(50), comment='业务编码')
    status = Column(Enum(ApprovalStatus), default=ApprovalStatus.PENDING, comment='审批状态')
    current_node_id = Column(Integer, comment='当前节点ID')
    submit_time = Column(DateTime, default=func.now(), comment='提交时间')
    submit_user = Column(String(50), comment='提交人')
    finish_time = Column(DateTime, comment='完成时间')
    remark = Column(Text, comment='备注')
    
    records = relationship('SysApprovalRecord', backref='instance', cascade='all, delete-orphan')

class SysApprovalRecord(Base):
    __tablename__ = 'sys_approval_record'
    
    record_id = Column(Integer, primary_key=True, autoincrement=True, comment='审批记录ID')
    instance_id = Column(Integer, ForeignKey('sys_approval_instance.instance_id'), nullable=False, comment='审批实例ID')
    node_id = Column(Integer, ForeignKey('sys_approval_node.node_id'), nullable=False, comment='节点ID')
    status = Column(Enum(ApprovalStatus), nullable=False, comment='审批状态')
    approver = Column(String(50), nullable=False, comment='审批人')
    approve_time = Column(DateTime, default=func.now(), comment='审批时间')
    comment = Column(Text, comment='审批意见')