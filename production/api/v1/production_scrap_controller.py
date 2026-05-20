from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from core.get_db import get_db
from service.production_scrap_service import ProductionScrapService
from schemas.production_scrap_schema import ProductionScrapModel, AddProductionScrapModel, ProductionScrapPageQueryModel
from schemas.common_schema import CrudResponseModel, PageResponseModel

router = APIRouter(prefix='/production/scrap', tags=['生产损耗'])

@router.get('/{scrap_id}', response_model=ProductionScrapModel)
async def get_scrap_detail(scrap_id: int, db: AsyncSession = Depends(get_db)):
    return await ProductionScrapService.get_scrap_detail(db, scrap_id)

@router.get('/list', response_model=PageResponseModel[ProductionScrapModel])
async def get_scrap_list(query: ProductionScrapPageQueryModel = Depends(), db: AsyncSession = Depends(get_db)):
    return await ProductionScrapService.get_scrap_list(db, query)

@router.post('', response_model=CrudResponseModel)
async def add_scrap(request: Request, add_model: AddProductionScrapModel, db: AsyncSession = Depends(get_db)):
    return await ProductionScrapService.add_scrap(request, db, add_model)

@router.post('/{scrap_id}/approve', response_model=CrudResponseModel)
async def approve_scrap(request: Request, scrap_id: int, db: AsyncSession = Depends(get_db)):
    return await ProductionScrapService.approve_scrap(request, db, scrap_id)

@router.post('/{scrap_id}/record', response_model=CrudResponseModel)
async def record_scrap(request: Request, scrap_id: int, db: AsyncSession = Depends(get_db)):
    return await ProductionScrapService.record_scrap(request, db, scrap_id)