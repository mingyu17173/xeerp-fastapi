from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func
from typing import Optional, List, Tuple
from models.production_receipt import SysProductionReceipt, SysProductionReturn, SysProductionReturnItem
from schemas.production_receipt_schema import ProductionReceiptPageQueryModel
from schemas.production_return_schema import ProductionReturnPageQueryModel

class ProductionReceiptDao:
    @classmethod
    async def get_receipt_by_id(cls, db: AsyncSession, receipt_id: int) -> Optional[SysProductionReceipt]:
        result = await db.execute(select(SysProductionReceipt).where(SysProductionReceipt.receipt_id == receipt_id))
        return result.scalar_one_or_none()

    @classmethod
    async def get_receipt_by_code(cls, db: AsyncSession, receipt_code: str) -> Optional[SysProductionReceipt]:
        result = await db.execute(select(SysProductionReceipt).where(SysProductionReceipt.receipt_code == receipt_code))
        return result.scalar_one_or_none()

    @classmethod
    async def get_receipt_list(cls, db: AsyncSession, query_model: ProductionReceiptPageQueryModel) -> Tuple[List[SysProductionReceipt], int]:
        query = select(SysProductionReceipt)
        
        if query_model.plan_code:
            query = query.join(SysProductionReceipt.plan).where(SysProductionReceipt.plan.has(plan_code=query_model.plan_code))
        if query_model.status:
            query = query.where(SysProductionReceipt.status == query_model.status)
        
        query = query.order_by(SysProductionReceipt.create_time.desc())
        
        total = await db.execute(select(func.count(SysProductionReceipt.receipt_id)))
        total_count = total.scalar_one()
        
        offset = (query_model.page_num - 1) * query_model.page_size
        query = query.offset(offset).limit(query_model.page_size)
        
        result = await db.execute(query)
        return result.scalars().all(), total_count

    @classmethod
    async def add_receipt(cls, db: AsyncSession, receipt: SysProductionReceipt):
        db.add(receipt)
        await db.flush()

    @classmethod
    async def update_receipt_status(cls, db: AsyncSession, receipt_id: int, status: str, update_by: str) -> int:
        result = await db.execute(
            update(SysProductionReceipt)
            .where(SysProductionReceipt.receipt_id == receipt_id)
            .values(status=status, update_by=update_by)
        )
        return result.rowcount


class ProductionReturnDao:
    @classmethod
    async def get_return_by_id(cls, db: AsyncSession, return_id: int) -> Optional[SysProductionReturn]:
        result = await db.execute(select(SysProductionReturn).where(SysProductionReturn.return_id == return_id))
        return result.scalar_one_or_none()

    @classmethod
    async def get_return_by_code(cls, db: AsyncSession, return_code: str) -> Optional[SysProductionReturn]:
        result = await db.execute(select(SysProductionReturn).where(SysProductionReturn.return_code == return_code))
        return result.scalar_one_or_none()

    @classmethod
    async def get_return_list(cls, db: AsyncSession, query_model: ProductionReturnPageQueryModel) -> Tuple[List[SysProductionReturn], int]:
        query = select(SysProductionReturn)
        
        if query_model.issue_code:
            query = query.join(SysProductionReturn.return_obj).where(SysProductionReturn.return_obj.has(issue_code=query_model.issue_code))
        if query_model.status:
            query = query.where(SysProductionReturn.status == query_model.status)
        
        query = query.order_by(SysProductionReturn.create_time.desc())
        
        total = await db.execute(select(func.count(SysProductionReturn.return_id)))
        total_count = total.scalar_one()
        
        offset = (query_model.page_num - 1) * query_model.page_size
        query = query.offset(offset).limit(query_model.page_size)
        
        result = await db.execute(query)
        return result.scalars().all(), total_count

    @classmethod
    async def add_return(cls, db: AsyncSession, return_obj: SysProductionReturn):
        db.add(return_obj)
        await db.flush()

    @classmethod
    async def update_return_status(cls, db: AsyncSession, return_id: int, status: str, update_by: str) -> int:
        result = await db.execute(
            update(SysProductionReturn)
            .where(SysProductionReturn.return_id == return_id)
            .values(status=status, update_by=update_by)
        )
        return result.rowcount