from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from core.get_db import get_db
from service.production_plan_service import ProductionPlanService
from schemas.production_plan_schema import ProductionPlanModel, AddProductionPlanModel, EditProductionPlanModel, ProductionPlanPageQueryModel
from schemas.common_schema import CrudResponseModel, PageResponseModel

router = APIRouter(prefix='/production/plan', tags=['生产计划'])

@router.get('/{plan_id}', response_model=ProductionPlanModel)
async def get_plan_detail(plan_id: int, db: AsyncSession = Depends(get_db)):
    return await ProductionPlanService.get_plan_detail(db, plan_id)

@router.get('/list', response_model=PageResponseModel[ProductionPlanModel])
async def get_plan_list(query: ProductionPlanPageQueryModel = Depends(), db: AsyncSession = Depends(get_db)):
    return await ProductionPlanService.get_plan_list(db, query)

@router.post('', response_model=CrudResponseModel)
async def add_plan(request: Request, add_model: AddProductionPlanModel, db: AsyncSession = Depends(get_db)):
    return await ProductionPlanService.add_plan(request, db, add_model)

@router.put('', response_model=CrudResponseModel)
async def edit_plan(request: Request, edit_model: EditProductionPlanModel, db: AsyncSession = Depends(get_db)):
    return await ProductionPlanService.edit_plan(request, db, edit_model)

@router.post('/{plan_id}/start', response_model=CrudResponseModel)
async def start_production(request: Request, plan_id: int, db: AsyncSession = Depends(get_db)):
    return await ProductionPlanService.start_production(request, db, plan_id)