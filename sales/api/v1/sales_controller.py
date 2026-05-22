"""
销售控制器
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from core import get_db, NotFoundException
from service.sales_service import SalesService
from schemas.sales import SalesCreate, SalesUpdate, SalesResponse

router = APIRouter()
service = SalesService()


@router.post("/sales", response_model=SalesResponse, summary="创建销售订单")
async def create_sales(
    data: SalesCreate,
    db: Session = Depends(get_db)
):
    """创建新销售订单"""
    return service.create_sales(db, data)


@router.get("/sales", response_model=List[SalesResponse], summary="获取销售订单列表")
async def get_sales(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    status: Optional[int] = None,
    customer_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """获取销售订单列表（支持分页和筛选）"""
    return service.get_sales(db, page, size, status, customer_id)


@router.get("/sales/{sales_id}", response_model=SalesResponse, summary="获取销售订单详情")
async def get_sales_order(
    sales_id: int,
    db: Session = Depends(get_db)
):
    """根据ID获取销售订单详情"""
    sales = service.get_sales_by_id(db, sales_id)
    if not sales:
        raise NotFoundException("销售订单不存在")
    return sales


@router.put("/sales/{sales_id}", response_model=SalesResponse, summary="更新销售订单")
async def update_sales(
    sales_id: int,
    data: SalesUpdate,
    db: Session = Depends(get_db)
):
    """更新销售订单信息"""
    sales = service.update_sales(db, sales_id, data)
    if not sales:
        raise NotFoundException("销售订单不存在")
    return sales


@router.delete("/sales/{sales_id}", summary="删除销售订单")
async def delete_sales(
    sales_id: int,
    db: Session = Depends(get_db)
):
    """删除销售订单"""
    result = service.delete_sales(db, sales_id)
    if not result:
        raise NotFoundException("销售订单不存在")
    return {"message": "删除成功"}


@router.post("/sales/{sales_id}/ship", summary="发货")
async def ship_sales(
    sales_id: int,
    db: Session = Depends(get_db)
):
    """销售订单发货"""
    result = service.ship_sales(db, sales_id)
    if not result:
        raise NotFoundException("销售订单不存在")
    return {"message": "已发货"}


@router.post("/sales/{sales_id}/complete", summary="完成销售")
async def complete_sales(
    sales_id: int,
    db: Session = Depends(get_db)
):
    """完成销售订单"""
    result = service.complete_sales(db, sales_id)
    if not result:
        raise NotFoundException("销售订单不存在")
    return {"message": "销售完成"}