"""
往来单位控制器
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from core import get_db, NotFoundException
from service.partner_service import PartnerService
from schemas.partner import PartnerCreate, PartnerUpdate, PartnerResponse

router = APIRouter()
service = PartnerService()


@router.post("/partners", response_model=PartnerResponse, summary="创建往来单位")
async def create_partner(
    data: PartnerCreate,
    db: Session = Depends(get_db)
):
    """创建新往来单位"""
    return service.create_partner(db, data)


@router.get("/partners", response_model=List[PartnerResponse], summary="获取往来单位列表")
async def get_partners(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    partner_type: Optional[int] = None,
    status: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """获取往来单位列表（支持分页和筛选）"""
    return service.get_partners(db, page, size, partner_type, status)


@router.get("/partners/{partner_id}", response_model=PartnerResponse, summary="获取往来单位详情")
async def get_partner(
    partner_id: int,
    db: Session = Depends(get_db)
):
    """根据ID获取往来单位详情"""
    partner = service.get_partner_by_id(db, partner_id)
    if not partner:
        raise NotFoundException("往来单位不存在")
    return partner


@router.put("/partners/{partner_id}", response_model=PartnerResponse, summary="更新往来单位")
async def update_partner(
    partner_id: int,
    data: PartnerUpdate,
    db: Session = Depends(get_db)
):
    """更新往来单位信息"""
    partner = service.update_partner(db, partner_id, data)
    if not partner:
        raise NotFoundException("往来单位不存在")
    return partner


@router.delete("/partners/{partner_id}", summary="删除往来单位")
async def delete_partner(
    partner_id: int,
    db: Session = Depends(get_db)
):
    """删除往来单位"""
    result = service.delete_partner(db, partner_id)
    if not result:
        raise NotFoundException("往来单位不存在")
    return {"message": "删除成功"}


@router.get("/partners/type/{partner_type}", response_model=List[PartnerResponse], summary="按类型获取往来单位")
async def get_partners_by_type(
    partner_type: int,
    db: Session = Depends(get_db)
):
    """按类型获取往来单位列表"""
    return service.get_partners_by_type(db, partner_type)