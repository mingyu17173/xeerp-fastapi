from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from service.order_service import OrderService
from schemas.order import AddOrderModel, OrderPageQueryModel
from core.response import ResponseModel, PageResponseModel

router = APIRouter(prefix='/order', tags=['订单管理'])

@router.get('/{order_id}', response_model=ResponseModel)
async def get_order_detail(order_id: int, db: AsyncSession = Depends(get_db)):
    return await OrderService.get_order_detail(db, order_id)

@router.get('/list', response_model=PageResponseModel)
async def get_order_list(query: OrderPageQueryModel = Depends(), db: AsyncSession = Depends(get_db)):
    return await OrderService.get_order_list(db, query)

@router.post('', response_model=ResponseModel)
async def add_order(request: Request, add_model: AddOrderModel, db: AsyncSession = Depends(get_db)):
    user_name = getattr(request.state, 'user_name', 'system')
    return await OrderService.add_order(db, add_model, user_name)

@router.post('/{order_id}/confirm', response_model=ResponseModel)
async def confirm_order(request: Request, order_id: int, db: AsyncSession = Depends(get_db)):
    user_name = getattr(request.state, 'user_name', 'system')
    return await OrderService.confirm_order(db, order_id, user_name)

@router.post('/{order_id}/cancel', response_model=ResponseModel)
async def cancel_order(request: Request, order_id: int, db: AsyncSession = Depends(get_db)):
    user_name = getattr(request.state, 'user_name', 'system')
    return await OrderService.cancel_order(db, order_id, user_name)

@router.delete('/{order_id}', response_model=ResponseModel)
async def delete_order(request: Request, order_id: int, db: AsyncSession = Depends(get_db)):
    user_name = getattr(request.state, 'user_name', 'system')
    return await OrderService.delete_order(db, order_id, user_name)