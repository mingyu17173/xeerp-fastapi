# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: production_receipt_controller.py
# @Software: PyCharm
# @Desc : 控制器

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from core.get_db import get_db
from service.production_receipt_service import ProductionReceiptService
from schemas.production_receipt_schema import ProductionReceiptModel, AddProductionReceiptModel, ProductionReceiptPageQueryModel
from schemas.common_schema import CrudResponseModel, PageResponseModel

router = APIRouter(prefix='/production/receipt', tags=['生产入库'])

@router.get('/{receipt_id}', response_model=ProductionReceiptModel)
async def get_receipt_detail(receipt_id: int, db: AsyncSession = Depends(get_db)):
    return await ProductionReceiptService.get_receipt_detail(db, receipt_id)

@router.get('/list', response_model=PageResponseModel[ProductionReceiptModel])
async def get_receipt_list(query: ProductionReceiptPageQueryModel = Depends(), db: AsyncSession = Depends(get_db)):
    return await ProductionReceiptService.get_receipt_list(db, query)

@router.post('', response_model=CrudResponseModel)
async def add_receipt(request: Request, add_model: AddProductionReceiptModel, db: AsyncSession = Depends(get_db)):
    return await ProductionReceiptService.add_receipt(request, db, add_model)

@router.post('/{receipt_id}/approve', response_model=CrudResponseModel)
async def approve_receipt(request: Request, receipt_id: int, db: AsyncSession = Depends(get_db)):
    return await ProductionReceiptService.approve_receipt(request, db, receipt_id)

@router.post('/{receipt_id}/stock', response_model=CrudResponseModel)
async def receipt_stock(request: Request, receipt_id: int, db: AsyncSession = Depends(get_db)):
    return await ProductionReceiptService.receipt_stock(request, db, receipt_id)