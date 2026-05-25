# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: purchase_controller.py
# @Software: PyCharm
# @Desc : 控制器

"""
采购控制器
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from core import get_db, NotFoundException
from service.purchase_service import PurchaseService
from schemas.purchase import PurchaseCreate, PurchaseUpdate, PurchaseResponse

router = APIRouter()
service = PurchaseService()


@router.post("/purchases", response_model=PurchaseResponse, summary="创建采购单")
async def create_purchase(
    data: PurchaseCreate,
    db: Session = Depends(get_db)
):
    """创建新采购单"""
    return service.create_purchase(db, data)


@router.get("/purchases", response_model=List[PurchaseResponse], summary="获取采购单列表")
async def get_purchases(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    status: Optional[int] = None,
    supplier_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """获取采购单列表（支持分页和筛选）"""
    return service.get_purchases(db, page, size, status, supplier_id)


@router.get("/purchases/{purchase_id}", response_model=PurchaseResponse, summary="获取采购单详情")
async def get_purchase(
    purchase_id: int,
    db: Session = Depends(get_db)
):
    """根据ID获取采购单详情"""
    purchase = service.get_purchase_by_id(db, purchase_id)
    if not purchase:
        raise NotFoundException("采购单不存在")
    return purchase


@router.put("/purchases/{purchase_id}", response_model=PurchaseResponse, summary="更新采购单")
async def update_purchase(
    purchase_id: int,
    data: PurchaseUpdate,
    db: Session = Depends(get_db)
):
    """更新采购单信息"""
    purchase = service.update_purchase(db, purchase_id, data)
    if not purchase:
        raise NotFoundException("采购单不存在")
    return purchase


@router.delete("/purchases/{purchase_id}", summary="删除采购单")
async def delete_purchase(
    purchase_id: int,
    db: Session = Depends(get_db)
):
    """删除采购单"""
    result = service.delete_purchase(db, purchase_id)
    if not result:
        raise NotFoundException("采购单不存在")
    return {"message": "删除成功"}


@router.post("/purchases/{purchase_id}/approve", summary="审批采购单")
async def approve_purchase(
    purchase_id: int,
    db: Session = Depends(get_db)
):
    """审批采购单"""
    result = service.approve_purchase(db, purchase_id)
    if not result:
        raise NotFoundException("采购单不存在")
    return {"message": "审批通过"}


@router.post("/purchases/{purchase_id}/reject", summary="拒绝采购单")
async def reject_purchase(
    purchase_id: int,
    reason: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """拒绝采购单"""
    result = service.reject_purchase(db, purchase_id, reason)
    if not result:
        raise NotFoundException("采购单不存在")
    return {"message": "已拒绝"}