# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: production_return_service.py
# @Software: PyCharm
# @Desc : 业务服务

from datetime import datetime
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import httpx
from dao.production_receipt_dao import ProductionReturnDao
from dao.production_issue_dao import ProductionIssueDao
from models.production_receipt import SysProductionReturn, SysProductionReturnItem
from schemas.common_schema import CrudResponseModel, PageResponseModel
from schemas.production_return_schema import ProductionReturnModel, AddProductionReturnModel, ProductionReturnPageQueryModel
from core.production_env import AppConfig

class ProductionReturnService:
    @classmethod
    async def get_return_detail(cls, db: AsyncSession, return_id: int) -> Optional[ProductionReturnModel]:
        return_obj = await ProductionReturnDao.get_return_by_id(db, return_id)
        if return_obj:
            return ProductionReturnModel.model_validate(return_obj)
        return None

    @classmethod
    async def get_return_list(cls, db: AsyncSession, query_model: ProductionReturnPageQueryModel) -> PageResponseModel:
        returns, total = await ProductionReturnDao.get_return_list(db, query_model)
        return_models = [ProductionReturnModel.model_validate(r) for r in returns]
        return PageResponseModel(
            rows=return_models,
            total=total,
            page_num=query_model.page_num,
            page_size=query_model.page_size
        )

    @classmethod
    async def add_return(cls, request: Request, db: AsyncSession, add_model: AddProductionReturnModel) -> CrudResponseModel:
        if await ProductionReturnDao.get_return_by_code(db, add_model.return_code):
            return CrudResponseModel(is_success=False, message=f"退料单编号 '{add_model.return_code}' 已存在")

        issue = await ProductionIssueDao.get_issue_by_id(db, add_model.issue_id)
        if not issue:
            return CrudResponseModel(is_success=False, message='领料单不存在')

        return_obj = SysProductionReturn(
            return_code=add_model.return_code,
            issue_id=add_model.issue_id,
            warehouse_id=add_model.warehouse_id,
            remark=add_model.remark,
            create_by=getattr(request.state, 'user_name', 'system'),
            create_time=datetime.now()
        )

        for item in add_model.items:
            return_item = SysProductionReturnItem(
                material_id=item['material_id'],
                material_name=item.get('material_name'),
                unit=item.get('unit'),
                quantity=item['quantity'],
                batch_no=item.get('batch_no'),
                reason=item.get('reason')
            )
            return_obj.items.append(return_item)

        await ProductionReturnDao.add_return(db, return_obj)
        await db.commit()
        return CrudResponseModel(is_success=True, message='新增成功')

    @classmethod
    async def approve_return(cls, request: Request, db: AsyncSession, return_id: int) -> CrudResponseModel:
        return_obj = await ProductionReturnDao.get_return_by_id(db, return_id)
        if not return_obj:
            return CrudResponseModel(is_success=False, message='退料单不存在')

        if return_obj.status != '0':
            return CrudResponseModel(is_success=False, message='只能审核待审核状态的退料单')

        await ProductionReturnDao.update_return_status(db, return_id, '1', getattr(request.state, 'user_name', 'system'))
        await db.commit()
        return CrudResponseModel(is_success=True, message='审核成功')

    @classmethod
    async def return_stock(cls, request: Request, db: AsyncSession, return_id: int) -> CrudResponseModel:
        return_obj = await ProductionReturnDao.get_return_by_id(db, return_id)
        if not return_obj:
            return CrudResponseModel(is_success=False, message='退料单不存在')

        if return_obj.status != '1':
            return CrudResponseModel(is_success=False, message='只能退料已审核的退料单')

        async with httpx.AsyncClient() as client:
            stock_items = []
            for item in return_obj.items:
                stock_items.append({
                    'product_id': item.material_id,
                    'warehouse_id': return_obj.warehouse_id,
                    'quantity': item.quantity,
                    'source_type': 'production_return',
                    'source_id': return_id
                })
            
            response = await client.post(f"{AppConfig.stock_service_url}/api/stock/batch-adjust", json=stock_items)
            if response.status_code != 200:
                await db.rollback()
                return CrudResponseModel(is_success=False, message='库存增加失败')

        await ProductionReturnDao.update_return_status(db, return_id, '2', getattr(request.state, 'user_name', 'system'))
        await db.commit()
        return CrudResponseModel(is_success=True, message='退料成功')