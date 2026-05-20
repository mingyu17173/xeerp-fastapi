from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from models.approval import ApprovalType, ApprovalStatus, ApprovalNodeType

class ApprovalFlowModel(BaseModel):
    flow_id: int = Field(..., description='流程ID')
    flow_code: str = Field(..., description='流程编码')
    flow_name: str = Field(..., description='流程名称')
    approval_type: ApprovalType = Field(..., description='审批类型')
    description: Optional[str] = Field(None, description='流程描述')
    is_active: bool = Field(True, description='是否启用')
    create_time: datetime = Field(..., description='创建时间')

class ApprovalNodeModel(BaseModel):
    node_id: int = Field(..., description='节点ID')
    flow_id: int = Field(..., description='流程ID')
    node_name: str = Field(..., description='节点名称')
    node_type: ApprovalNodeType = Field(..., description='节点类型')
    node_order: int = Field(..., description='节点顺序')
    approver_role: Optional[str] = Field(None, description='审批角色')
    approver_user: Optional[str] = Field(None, description='审批人')
    is_multiple: bool = Field(False, description='是否多人审批')

class ApprovalInstanceModel(BaseModel):
    instance_id: int = Field(..., description='审批实例ID')
    flow_id: int = Field(..., description='流程ID')
    source_type: str = Field(..., description='业务类型')
    source_id: int = Field(..., description='业务ID')
    source_code: Optional[str] = Field(None, description='业务编码')
    status: ApprovalStatus = Field(..., description='审批状态')
    current_node_id: Optional[int] = Field(None, description='当前节点ID')
    submit_time: datetime = Field(..., description='提交时间')
    submit_user: str = Field(..., description='提交人')
    finish_time: Optional[datetime] = Field(None, description='完成时间')
    remark: Optional[str] = Field(None, description='备注')

class AddApprovalInstanceModel(BaseModel):
    flow_id: int = Field(..., description='流程ID')
    source_type: str = Field(..., description='业务类型')
    source_id: int = Field(..., description='业务ID')
    source_code: Optional[str] = Field(None, description='业务编码')
    remark: Optional[str] = Field(None, description='备注')

class ApprovalActionModel(BaseModel):
    instance_id: int = Field(..., description='审批实例ID')
    action: str = Field(..., description='操作：approve/reject')
    comment: Optional[str] = Field(None, description='审批意见')