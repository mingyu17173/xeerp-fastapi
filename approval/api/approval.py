# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: approval.py
# @Software: PyCharm
# @Desc : API模块

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from service.approval_service import ApprovalService
from schemas.approval import AddApprovalInstanceModel, ApprovalActionModel
from core.response import ResponseModel, PageResponseModel

router = APIRouter(prefix='/approval', tags=['审批管理'])

@router.get('/flow/list', response_model=ResponseModel)
async def get_flow_list(approval_type: str = None, db: AsyncSession = Depends(get_db)):
    return await ApprovalService.get_flow_list(db, approval_type)

@router.get('/instance/{instance_id}', response_model=ResponseModel)
async def get_instance_detail(instance_id: int, db: AsyncSession = Depends(get_db)):
    return await ApprovalService.get_instance_detail(db, instance_id)

@router.get('/instance/list', response_model=PageResponseModel)
async def get_instance_list(user_id: str = None, db: AsyncSession = Depends(get_db)):
    return await ApprovalService.get_instance_list(db, user_id)

@router.post('/submit', response_model=ResponseModel)
async def submit_approval(request: Request, add_model: AddApprovalInstanceModel, db: AsyncSession = Depends(get_db)):
    user_name = getattr(request.state, 'user_name', 'system')
    return await ApprovalService.submit_approval(db, add_model, user_name)

@router.post('/action', response_model=ResponseModel)
async def approval_action(request: Request, action_model: ApprovalActionModel, db: AsyncSession = Depends(get_db)):
    user_name = getattr(request.state, 'user_name', 'system')
    return await ApprovalService.approve(db, action_model, user_name)