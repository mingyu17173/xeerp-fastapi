# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: approval_controller.py
# @Software: PyCharm
# @Desc : 控制器

"""
审批流控制器
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from core import get_db, NotFoundException
from service.approval_service import ApprovalService
from schemas.approval import ApprovalCreate, ApprovalUpdate, ApprovalResponse

router = APIRouter()
service = ApprovalService()


@router.post("/approvals", response_model=ApprovalResponse, summary="创建审批")
async def create_approval(
    data: ApprovalCreate,
    db: Session = Depends(get_db)
):
    """创建新的审批流程"""
    return service.create_approval(db, data)


@router.get("/approvals", response_model=List[ApprovalResponse], summary="获取审批列表")
async def get_approvals(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    status: Optional[int] = None,
    apply_user: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取审批列表（支持分页和筛选）"""
    return service.get_approvals(db, page, size, status, apply_user)


@router.get("/approvals/{approval_id}", response_model=ApprovalResponse, summary="获取审批详情")
async def get_approval(
    approval_id: int,
    db: Session = Depends(get_db)
):
    """根据ID获取审批详情"""
    approval = service.get_approval_by_id(db, approval_id)
    if not approval:
        raise NotFoundException("审批不存在")
    return approval


@router.put("/approvals/{approval_id}", response_model=ApprovalResponse, summary="更新审批")
async def update_approval(
    approval_id: int,
    data: ApprovalUpdate,
    db: Session = Depends(get_db)
):
    """更新审批信息"""
    approval = service.update_approval(db, approval_id, data)
    if not approval:
        raise NotFoundException("审批不存在")
    return approval


@router.delete("/approvals/{approval_id}", summary="删除审批")
async def delete_approval(
    approval_id: int,
    db: Session = Depends(get_db)
):
    """删除审批"""
    result = service.delete_approval(db, approval_id)
    if not result:
        raise NotFoundException("审批不存在")
    return {"message": "删除成功"}


@router.post("/approvals/{approval_id}/approve", summary="审批通过")
async def approve_approval(
    approval_id: int,
    comment: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """审批通过"""
    result = service.approve_approval(db, approval_id, comment)
    if not result:
        raise NotFoundException("审批不存在")
    return {"message": "审批通过"}


@router.post("/approvals/{approval_id}/reject", summary="拒绝审批")
async def reject_approval(
    approval_id: int,
    comment: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """拒绝审批"""
    result = service.reject_approval(db, approval_id, comment)
    if not result:
        raise NotFoundException("审批不存在")
    return {"message": "已拒绝"}