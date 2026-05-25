# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: approval_service.py
# @Software: PyCharm
# @Desc : 业务服务

from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from dao.approval_dao import ApprovalDao
from schemas.approval import ApprovalInstanceModel, AddApprovalInstanceModel, ApprovalActionModel
from schemas.approval import ApprovalFlowModel, ApprovalNodeModel
from core.response import ResponseModel, PageResponseModel
from models.approval import ApprovalStatus, ApprovalNodeType

class ApprovalService:
    @classmethod
    async def get_flow_list(cls, db: AsyncSession, approval_type: str = None) -> ResponseModel:
        flows = await ApprovalDao.get_flow_list(db, approval_type)
        data = []
        for flow in flows:
            nodes = await ApprovalDao.get_nodes_by_flow(db, flow.flow_id)
            flow_data = ApprovalFlowModel.from_orm(flow)
            flow_data.__dict__['nodes'] = [ApprovalNodeModel.from_orm(n) for n in nodes]
            data.append(flow_data.__dict__)
        return ResponseModel.success(data=data)

    @classmethod
    async def get_instance_detail(cls, db: AsyncSession, instance_id: int) -> ResponseModel:
        instance = await ApprovalDao.get_instance_by_id(db, instance_id)
        if not instance:
            return ResponseModel.error(code=404, message='审批实例不存在')
        
        data = ApprovalInstanceModel.from_orm(instance)
        return ResponseModel.success(data=data)

    @classmethod
    async def get_instance_list(cls, db: AsyncSession, user_id: str = None) -> PageResponseModel:
        instances = await ApprovalDao.get_instance_list(db, user_id)
        data = [ApprovalInstanceModel.from_orm(i) for i in instances]
        return PageResponseModel.success(rows=data, total=len(data), page_num=1, page_size=len(data))

    @classmethod
    async def submit_approval(cls, db: AsyncSession, add_model: AddApprovalInstanceModel, submit_user: str) -> ResponseModel:
        existing = await ApprovalDao.get_instance_by_source(db, add_model.source_type, add_model.source_id)
        if existing and existing.status != ApprovalStatus.CANCELLED:
            return ResponseModel.error(code=-1, message='该业务已有审批流程')
        
        instance = await ApprovalDao.create_instance(db, add_model, submit_user)
        await db.commit()
        
        data = ApprovalInstanceModel.from_orm(instance)
        return ResponseModel.success(data=data, message='提交成功')

    @classmethod
    async def approve(cls, db: AsyncSession, action_model: ApprovalActionModel, approver: str) -> ResponseModel:
        instance = await ApprovalDao.get_instance_by_id(db, action_model.instance_id)
        if not instance:
            return ResponseModel.error(code=404, message='审批实例不存在')
        
        if instance.status == ApprovalStatus.APPROVED:
            return ResponseModel.error(code=-1, message='已通过审批')
        
        if instance.status == ApprovalStatus.REJECTED:
            return ResponseModel.error(code=-1, message='已被驳回')
        
        nodes = await ApprovalDao.get_nodes_by_flow(db, instance.flow_id)
        current_node = next((n for n in nodes if n.node_id == instance.current_node_id), None)
        
        if action_model.action == 'approve':
            await ApprovalDao.add_record(db, instance.instance_id, current_node.node_id, ApprovalStatus.APPROVED, approver, action_model.comment)
            
            node_index = nodes.index(current_node)
            next_nodes = nodes[node_index + 1:]
            next_approve_node = next((n for n in next_nodes if n.node_type == ApprovalNodeType.APPROVE), None)
            
            if next_approve_node:
                await ApprovalDao.update_current_node(db, instance.instance_id, next_approve_node.node_id)
            else:
                await ApprovalDao.update_instance_status(db, instance.instance_id, ApprovalStatus.APPROVED, datetime.now())
                await ApprovalDao.update_current_node(db, instance.instance_id, None)
            
            await db.commit()
            return ResponseModel.success(message='审批通过')
        
        elif action_model.action == 'reject':
            await ApprovalDao.add_record(db, instance.instance_id, current_node.node_id, ApprovalStatus.REJECTED, approver, action_model.comment)
            await ApprovalDao.update_instance_status(db, instance.instance_id, ApprovalStatus.REJECTED, datetime.now())
            await db.commit()
            return ResponseModel.success(message='已驳回')
        
        else:
            return ResponseModel.error(code=-1, message='无效的操作')