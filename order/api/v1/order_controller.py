"""
订单控制器
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from core import get_db, NotFoundException
from service.order_service import OrderService
from schemas.order import OrderCreate, OrderUpdate, OrderResponse

router = APIRouter()
service = OrderService()


@router.post("/orders", response_model=OrderResponse, summary="创建订单")
async def create_order(
    data: OrderCreate,
    db: Session = Depends(get_db)
):
    """创建新订单"""
    return service.create_order(db, data)


@router.get("/orders", response_model=List[OrderResponse], summary="获取订单列表")
async def get_orders(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    status: Optional[int] = None,
    customer_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """获取订单列表（支持分页和筛选）"""
    return service.get_orders(db, page, size, status, customer_id)


@router.get("/orders/{order_id}", response_model=OrderResponse, summary="获取订单详情")
async def get_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    """根据ID获取订单详情"""
    order = service.get_order_by_id(db, order_id)
    if not order:
        raise NotFoundException("订单不存在")
    return order


@router.put("/orders/{order_id}", response_model=OrderResponse, summary="更新订单")
async def update_order(
    order_id: int,
    data: OrderUpdate,
    db: Session = Depends(get_db)
):
    """更新订单信息"""
    order = service.update_order(db, order_id, data)
    if not order:
        raise NotFoundException("订单不存在")
    return order


@router.delete("/orders/{order_id}", summary="删除订单")
async def delete_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    """删除订单"""
    result = service.delete_order(db, order_id)
    if not result:
        raise NotFoundException("订单不存在")
    return {"message": "删除成功"}


@router.post("/orders/{order_id}/cancel", summary="取消订单")
async def cancel_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    """取消订单"""
    result = service.cancel_order(db, order_id)
    if not result:
        raise NotFoundException("订单不存在")
    return {"message": "订单已取消"}


@router.post("/orders/{order_id}/confirm", summary="确认订单")
async def confirm_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    """确认订单"""
    result = service.confirm_order(db, order_id)
    if not result:
        raise NotFoundException("订单不存在")
    return {"message": "订单已确认"}