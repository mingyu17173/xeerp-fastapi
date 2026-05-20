from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from service.purchase_service import PurchaseService
from schemas.purchase import AddPurchaseOrderModel, PurchasePageQueryModel
from core.response import ResponseModel, PageResponseModel
from typing import List

router = APIRouter(prefix='/purchase', tags=['采购管理'])

@router.get('/{purchase_id}', response_model=ResponseModel)
async def get_purchase_detail(purchase_id: int, db: AsyncSession = Depends(get_db)):
    return await PurchaseService.get_purchase_detail(db, purchase_id)

@router.get('/list', response_model=PageResponseModel)
async def get_purchase_list(query: PurchasePageQueryModel = Depends(), db: AsyncSession = Depends(get_db)):
    return await PurchaseService.get_purchase_list(db, query)

@router.post('', response_model=ResponseModel)
async def add_purchase(request: Request, add_model: AddPurchaseOrderModel, db: AsyncSession = Depends(get_db)):
    user_name = getattr(request.state, 'user_name', 'system')
    return await PurchaseService.add_purchase(db, add_model, user_name)

@router.post('/{purchase_id}/approve', response_model=ResponseModel)
async def approve_purchase(request: Request, purchase_id: int, db: AsyncSession = Depends(get_db)):
    user_name = getattr(request.state, 'user_name', 'system')
    return await PurchaseService.approve_purchase(db, purchase_id, user_name)

@router.post('/{purchase_id}/receive', response_model=ResponseModel)
async def receive_purchase(request: Request, purchase_id: int, items: List[dict], db: AsyncSession = Depends(get_db)):
    user_name = getattr(request.state, 'user_name', 'system')
    return await PurchaseService.receive_purchase(db, purchase_id, items, user_name)

@router.delete('/{purchase_id}', response_model=ResponseModel)
async def delete_purchase(request: Request, purchase_id: int, db: AsyncSession = Depends(get_db)):
    user_name = getattr(request.state, 'user_name', 'system')
    return await PurchaseService.delete_purchase(db, purchase_id, user_name)