"""
Sales Service API Router
销售服务API路由
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from core.deps import get_current_user
from core.response import ResponseModel, PageResponseModel
from schemas.sales import (
    AddSalesOrderModel, EditSalesOrderModel, SalesOrderPageQueryModel,
    AddDeliveryModel, AddReturnModel, ApproveReturnModel
)
from service.sales_service import SalesOrderService, SalesDeliveryService, SalesReturnService

router = APIRouter(prefix="/api/sales", tags=["销售管理"])

# ==================== 销售订单 ====================

@router.get("/orders", response_model=PageResponseModel)
async def get_order_list(
    page_num: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页大小"),
    sales_code: str = Query(None, description="订单编号"),
    customer_name: str = Query(None, description="客户名称"),
    status: str = Query(None, description="订单状态"),
    db: AsyncSession = Depends(get_db)
):
    """获取销售订单列表"""
    query = SalesOrderPageQueryModel(
        page_num=page_num,
        page_size=page_size,
        sales_code=sales_code,
        customer_name=customer_name,
        status=status
    )
    result = await SalesOrderService.get_order_list(db, query)
    return result

@router.get("/orders/{sales_id}", response_model=ResponseModel)
async def get_order_detail(sales_id: int, db: AsyncSession = Depends(get_db)):
    """获取销售订单详情"""
    result = await SalesOrderService.get_order_detail(db, sales_id)
    return result

@router.post("/orders", response_model=ResponseModel)
async def add_order(
    model: AddSalesOrderModel,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """新增销售订单"""
    result = await SalesOrderService.add_order(db, model, current_user["username"])
    return result

@router.put("/orders", response_model=ResponseModel)
async def edit_order(
    model: EditSalesOrderModel,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """编辑销售订单"""
    result = await SalesOrderService.edit_order(db, model, current_user["username"])
    return result

@router.delete("/orders/{sales_id}", response_model=ResponseModel)
async def delete_order(
    sales_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """删除销售订单"""
    result = await SalesOrderService.delete_order(db, sales_id, current_user["username"])
    return result

@router.post("/orders/{sales_id}/approve", response_model=ResponseModel)
async def approve_order(
    sales_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """审核销售订单"""
    result = await SalesOrderService.approve_order(db, sales_id, current_user["username"])
    return result

@router.post("/orders/{sales_id}/cancel", response_model=ResponseModel)
async def cancel_order(
    sales_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """取消销售订单"""
    result = await SalesOrderService.cancel_order(db, sales_id, current_user["username"])
    return result

# ==================== 销售发货 ====================

@router.post("/deliveries", response_model=ResponseModel)
async def create_delivery(
    model: AddDeliveryModel,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """创建发货单"""
    result = await SalesDeliveryService.create_delivery(db, model, current_user["username"])
    return result

# ==================== 销售退货 ====================

@router.post("/returns", response_model=ResponseModel)
async def create_return(
    model: AddReturnModel,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """创建退货单"""
    result = await SalesReturnService.create_return(db, model, current_user["username"])
    return result

@router.post("/returns/approve", response_model=ResponseModel)
async def approve_return(
    model: ApproveReturnModel,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """审核退货单"""
    result = await SalesReturnService.approve_return(db, model, current_user["username"])
    return result