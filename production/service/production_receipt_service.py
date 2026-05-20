from datetime import datetime
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import httpx
from dao.production_receipt_dao import ProductionReceiptDao
from dao.production_plan_dao import ProductionPlanDao
from models.production_receipt import SysProductionReceipt
from schemas.common_schema import CrudResponseModel, PageResponseModel
from schemas.production_receipt_schema import ProductionReceiptModel, AddProductionReceiptModel, ProductionReceiptPageQueryModel
from core.env import AppConfig

class ProductionReceiptService:
    @classmethod
    async def get_receipt_detail(cls, db: AsyncSession, receipt_id: int) -> Optional[ProductionReceiptModel]:
        receipt = await ProductionReceiptDao.get_receipt_by_id(db, receipt_id)
        if receipt:
            return ProductionReceiptModel.model_validate(receipt)
        return None

    @classmethod
    async def get_receipt_list(cls, db: AsyncSession, query_model: ProductionReceiptPageQueryModel) -> PageResponseModel:
        receipts, total = await ProductionReceiptDao.get_receipt_list(db, query_model)
        receipt_models = [ProductionReceiptModel.model_validate(r) for r in receipts]
        return PageResponseModel(
            rows=receipt_models,
            total=total,
            page_num=query_model.page_num,
            page_size=query_model.page_size
        )

    @classmethod
    async def add_receipt(cls, request: Request, db: AsyncSession, add_model: AddProductionReceiptModel) -> CrudResponseModel:
        if await ProductionReceiptDao.get_receipt_by_code(db, add_model.receipt_code):
            return CrudResponseModel(is_success=False, message=f"入库单编号 '{add_model.receipt_code}' 已存在")

        plan = await ProductionPlanDao.get_plan_by_id(db, add_model.plan_id)
        if not plan:
            return CrudResponseModel(is_success=False, message='生产计划不存在')

        if plan.finished_quantity + add_model.quantity > plan.plan_quantity:
            return CrudResponseModel(is_success=False, message='入库数量超过计划数量')

        receipt = SysProductionReceipt(
            receipt_code=add_model.receipt_code,
            plan_id=add_model.plan_id,
            warehouse_id=add_model.warehouse_id,
            quantity=add_model.quantity,
            remark=add_model.remark,
            create_by=getattr(request.state, 'user_name', 'system'),
            create_time=datetime.now()
        )

        await ProductionReceiptDao.add_receipt(db, receipt)
        await db.commit()
        return CrudResponseModel(is_success=True, message='新增成功')

    @classmethod
    async def approve_receipt(cls, request: Request, db: AsyncSession, receipt_id: int) -> CrudResponseModel:
        receipt = await ProductionReceiptDao.get_receipt_by_id(db, receipt_id)
        if not receipt:
            return CrudResponseModel(is_success=False, message='入库单不存在')

        if receipt.status != '0':
            return CrudResponseModel(is_success=False, message='只能审核待审核状态的入库单')

        await ProductionReceiptDao.update_receipt_status(db, receipt_id, '1', getattr(request.state, 'user_name', 'system'))
        await db.commit()
        return CrudResponseModel(is_success=True, message='审核成功')

    @classmethod
    async def receipt_stock(cls, request: Request, db: AsyncSession, receipt_id: int) -> CrudResponseModel:
        receipt = await ProductionReceiptDao.get_receipt_by_id(db, receipt_id)
        if not receipt:
            return CrudResponseModel(is_success=False, message='入库单不存在')

        if receipt.status != '1':
            return CrudResponseModel(is_success=False, message='只能入库已审核的入库单')

        plan = await ProductionPlanDao.get_plan_by_id(db, receipt.plan_id)
        
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{AppConfig.stock_service_url}/api/stock/adjust", json={
                'product_id': plan.product_id,
                'warehouse_id': receipt.warehouse_id,
                'quantity': receipt.quantity,
                'remark': f'生产入库 {receipt.receipt_code}'
            })
            if response.status_code != 200:
                await db.rollback()
                return CrudResponseModel(is_success=False, message='库存增加失败')

        finished_quantity = plan.finished_quantity + receipt.quantity
        await ProductionPlanDao.update_plan_finished(db, receipt.plan_id, finished_quantity)

        if finished_quantity >= plan.plan_quantity:
            plan.status = '2'
            await ProductionPlanDao.update_plan(db, plan)

        await ProductionReceiptDao.update_receipt_status(db, receipt_id, '2', getattr(request.state, 'user_name', 'system'))
        await db.commit()
        return CrudResponseModel(is_success=True, message='入库成功')