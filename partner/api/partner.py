from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from service.partner_service import PartnerService
from schemas.partner import AddPartnerModel, EditPartnerModel, PartnerPageQueryModel
from core.response import ResponseModel, PageResponseModel

router = APIRouter(prefix='/partner', tags=['往来单位管理'])

@router.get('/{partner_id}', response_model=ResponseModel)
async def get_partner_detail(partner_id: int, db: AsyncSession = Depends(get_db)):
    return await PartnerService.get_partner_detail(db, partner_id)

@router.get('/list', response_model=PageResponseModel)
async def get_partner_list(query: PartnerPageQueryModel = Depends(), db: AsyncSession = Depends(get_db)):
    return await PartnerService.get_partner_list(db, query)

@router.get('/customers', response_model=ResponseModel)
async def get_customers(db: AsyncSession = Depends(get_db)):
    return await PartnerService.get_customers(db)

@router.get('/suppliers', response_model=ResponseModel)
async def get_suppliers(db: AsyncSession = Depends(get_db)):
    return await PartnerService.get_suppliers(db)

@router.post('', response_model=ResponseModel)
async def add_partner(request: Request, add_model: AddPartnerModel, db: AsyncSession = Depends(get_db)):
    user_name = getattr(request.state, 'user_name', 'system')
    return await PartnerService.add_partner(db, add_model, user_name)

@router.put('', response_model=ResponseModel)
async def edit_partner(request: Request, edit_model: EditPartnerModel, db: AsyncSession = Depends(get_db)):
    user_name = getattr(request.state, 'user_name', 'system')
    return await PartnerService.edit_partner(db, edit_model, user_name)

@router.delete('/{partner_id}', response_model=ResponseModel)
async def delete_partner(request: Request, partner_id: int, db: AsyncSession = Depends(get_db)):
    user_name = getattr(request.state, 'user_name', 'system')
    return await PartnerService.delete_partner(db, partner_id, user_name)