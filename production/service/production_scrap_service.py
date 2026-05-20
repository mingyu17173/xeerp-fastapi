from datetime import datetime
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import httpx
from dao.production_scrap_dao import ProductionScrapDao
from models.production_scrap import SysProductionScrap, SysProductionScrapItem
from schemas.common_schema import CrudResponseModel, PageResponseModel
from schemas.production_scrap_schema import ProductionScrapModel, AddProductionScrapModel, ProductionScrapPageQueryModel
from core.env import AppConfig

class ProductionScrapService:
    @classmethod
    async def get_scrap_detail(cls, db: AsyncSession, scrap_id: int) -> Optional[ProductionScrapModel]:
        scrap = await ProductionScrapDao.get_scrap_by_id(db, scrap_id)
        if scrap:
            return ProductionScrapModel.model_validate(scrap)
        return None

    @classmethod
    async def get_scrap_list(cls, db: AsyncSession, query_model: ProductionScrapPageQueryModel) -> PageResponseModel:
        scraps, total = await ProductionScrapDao.get_scrap_list(db, query_model)
        scrap_models = [ProductionScrapModel.model_validate(s) for s in scraps]
        return PageResponseModel(
            rows=scrap_models,
            total=total,
            page_num=query_model.page_num,
            page_size=query_model.page_size
        )

    @classmethod
    async def add_scrap(cls, request: Request, db: AsyncSession, add_model: AddProductionScrapModel) -> CrudResponseModel:
        if await ProductionScrapDao.get_scrap_by_code(db, add_model.scrap_code):
            return CrudResponseModel(is_success=False, message=f"损耗单号 '{add_model.scrap_code}' 已存在")

        scrap = SysProductionScrap(
            scrap_code=add_model.scrap_code,
            plan_id=add_model.plan_id,
            issue_id=add_model.issue_id,
            warehouse_id=add_model.warehouse_id,
            remark=add_model.remark,
            create_by=getattr(request.state, 'user_name', 'system'),
            create_time=datetime.now()
        )

        for item in add_model.items:
            scrap_item = SysProductionScrapItem(
                material_id=item['material_id'],
                material_name=item.get('material_name'),
                unit=item.get('unit'),
                quantity=item['quantity'],
                batch_no=item.get('batch_no'),
                reason=item.get('reason')
            )
            scrap.items.append(scrap_item)

        await ProductionScrapDao.add_scrap(db, scrap)
        await db.commit()
        return CrudResponseModel(is_success=True, message='新增成功')

    @classmethod
    async def approve_scrap(cls, request: Request, db: AsyncSession, scrap_id: int) -> CrudResponseModel:
        scrap = await ProductionScrapDao.get_scrap_by_id(db, scrap_id)
        if not scrap:
            return CrudResponseModel(is_success=False, message='损耗记录不存在')

        if scrap.status != '0':
            return CrudResponseModel(is_success=False, message='只能审核待审核状态的损耗记录')

        await ProductionScrapDao.update_scrap_status(db, scrap_id, '1', getattr(request.state, 'user_name', 'system'))
        await db.commit()
        return CrudResponseModel(is_success=True, message='审核成功')

    @classmethod
    async def record_scrap(cls, request: Request, db: AsyncSession, scrap_id: int) -> CrudResponseModel:
        scrap = await ProductionScrapDao.get_scrap_by_id(db, scrap_id)
        if not scrap:
            return CrudResponseModel(is_success=False, message='损耗记录不存在')

        if scrap.status != '1':
            return CrudResponseModel(is_success=False, message='只能记账已审核的损耗记录')

        async with httpx.AsyncClient() as client:
            stock_items = []
            for item in scrap.items:
                stock_items.append({
                    'product_id': item.material_id,
                    'warehouse_id': scrap.warehouse_id,
                    'quantity': -item.quantity,
                    'source_type': 'production_scrap',
                    'source_id': scrap_id
                })
            
            response = await client.post(f"{AppConfig.stock_service_url}/api/stock/batch-adjust", json=stock_items)
            if response.status_code != 200:
                await db.rollback()
                return CrudResponseModel(is_success=False, message='库存扣减失败')

        await ProductionScrapDao.update_scrap_status(db, scrap_id, '2', getattr(request.state, 'user_name', 'system'))
        await db.commit()
        return CrudResponseModel(is_success=True, message='记账成功')