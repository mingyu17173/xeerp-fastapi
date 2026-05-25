# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: warehouse_controller.py
# @Software: PyCharm
# @Desc : 控制器

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from ...core.get_db import get_db
from ...service.warehouse_service import WarehouseService
from ...schemas.warehouse_schema import WarehouseModel, AddWarehouseModel, EditWarehouseModel, WarehousePageQueryModel
from ...schemas.common_schema import CrudResponseModel, PageResponseModel

router = APIRouter(prefix='/warehouse', tags=['仓库管理'])

@router.get('/{warehouse_id}', response_model=WarehouseModel)
async def get_warehouse_detail(warehouse_id: int, db: AsyncSession = Depends(get_db)):
    return await WarehouseService.get_warehouse_detail(db, warehouse_id)

@router.get('/list', response_model=PageResponseModel[WarehouseModel])
async def get_warehouse_list(query: WarehousePageQueryModel = Depends(), db: AsyncSession = Depends(get_db)):
    return await WarehouseService.get_warehouse_list(db, query)

@router.post('', response_model=CrudResponseModel)
async def add_warehouse(request: Request, add_model: AddWarehouseModel, db: AsyncSession = Depends(get_db)):
    return await WarehouseService.add_warehouse(request, db, add_model)

@router.put('', response_model=CrudResponseModel)
async def edit_warehouse(request: Request, edit_model: EditWarehouseModel, db: AsyncSession = Depends(get_db)):
    return await WarehouseService.edit_warehouse(request, db, edit_model)

@router.delete('/{warehouse_id}', response_model=CrudResponseModel)
async def delete_warehouse(request: Request, warehouse_id: int, db: AsyncSession = Depends(get_db)):
    return await WarehouseService.delete_warehouse(request, db, warehouse_id)