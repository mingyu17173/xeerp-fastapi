# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: inventory_controller.py
# @Software: PyCharm
# @Desc : 控制器

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from ...core.get_db import get_db
from ...service.inventory_service import InventoryService
from ...service.inventory_flow_service import InventoryFlowService
from ...schemas.inventory_schema import InventoryModel, InventoryQueryModel, InventoryAdjustModel
from ...schemas.inventory_flow_schema import InventoryFlowModel, InventoryFlowQueryModel
from ...schemas.common_schema import CrudResponseModel, PageResponseModel
from typing import List

router = APIRouter(prefix='/stock', tags=['库存管理'])

@router.get('/inventory/{product_id}/{warehouse_id}', response_model=InventoryModel)
async def get_inventory(product_id: int, warehouse_id: int, db: AsyncSession = Depends(get_db)):
    return await InventoryService.get_inventory(db, product_id, warehouse_id)

@router.get('/inventory/list', response_model=PageResponseModel[InventoryModel])
async def get_inventory_list(query: InventoryQueryModel = Depends(), db: AsyncSession = Depends(get_db)):
    return await InventoryService.get_inventory_list(db, query)

@router.get('/quantity/{product_id}/{warehouse_id}')
async def get_inventory_quantity(product_id: int, warehouse_id: int, db: AsyncSession = Depends(get_db)):
    quantity = await InventoryService.get_inventory_quantity(db, product_id, warehouse_id)
    return {'product_id': product_id, 'warehouse_id': warehouse_id, 'quantity': quantity}

@router.post('/adjust', response_model=CrudResponseModel)
async def adjust_inventory(request: Request, adjust_model: InventoryAdjustModel, db: AsyncSession = Depends(get_db)):
    return await InventoryService.adjust_inventory(request, db, adjust_model)

@router.post('/batch-adjust', response_model=CrudResponseModel)
async def batch_adjust_inventory(request: Request, items: List[dict], db: AsyncSession = Depends(get_db)):
    return await InventoryService.batch_adjust_inventory(request, db, items)

@router.get('/flow/list', response_model=PageResponseModel[InventoryFlowModel])
async def get_flow_list(query: InventoryFlowQueryModel = Depends(), db: AsyncSession = Depends(get_db)):
    return await InventoryFlowService.get_flow_list(db, query)