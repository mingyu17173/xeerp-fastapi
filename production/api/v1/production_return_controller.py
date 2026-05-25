# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: production_return_controller.py
# @Software: PyCharm
# @Desc : 控制器

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from core.get_db import get_db
from service.production_return_service import ProductionReturnService
from schemas.production_return_schema import ProductionReturnModel, AddProductionReturnModel, ProductionReturnPageQueryModel
from schemas.common_schema import CrudResponseModel, PageResponseModel

router = APIRouter(prefix='/production/return', tags=['生产退料'])

@router.get('/{return_id}', response_model=ProductionReturnModel)
async def get_return_detail(return_id: int, db: AsyncSession = Depends(get_db)):
    return await ProductionReturnService.get_return_detail(db, return_id)

@router.get('/list', response_model=PageResponseModel[ProductionReturnModel])
async def get_return_list(query: ProductionReturnPageQueryModel = Depends(), db: AsyncSession = Depends(get_db)):
    return await ProductionReturnService.get_return_list(db, query)

@router.post('', response_model=CrudResponseModel)
async def add_return(request: Request, add_model: AddProductionReturnModel, db: AsyncSession = Depends(get_db)):
    return await ProductionReturnService.add_return(request, db, add_model)

@router.post('/{return_id}/approve', response_model=CrudResponseModel)
async def approve_return(request: Request, return_id: int, db: AsyncSession = Depends(get_db)):
    return await ProductionReturnService.approve_return(request, db, return_id)

@router.post('/{return_id}/stock', response_model=CrudResponseModel)
async def return_stock(request: Request, return_id: int, db: AsyncSession = Depends(get_db)):
    return await ProductionReturnService.return_stock(request, db, return_id)