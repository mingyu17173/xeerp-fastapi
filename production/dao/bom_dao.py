from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from typing import Optional, List, Tuple
from models.bom import SysBom, SysBomItem
from schemas.bom_schema import BomPageQueryModel

class BomDao:
    @classmethod
    async def get_bom_by_id(cls, db: AsyncSession, bom_id: int) -> Optional[SysBom]:
        result = await db.execute(select(SysBom).where(SysBom.bom_id == bom_id, SysBom.is_delete == False))
        return result.scalar_one_or_none()

    @classmethod
    async def get_bom_list(cls, db: AsyncSession, query_model: BomPageQueryModel) -> Tuple[List[SysBom], int]:
        query = select(SysBom).where(SysBom.is_delete == False)
        
        if query_model.product_name:
            query = query.where(SysBom.product_name.like(f'%{query_model.product_name}%'))
        
        query = query.order_by(SysBom.create_time.desc())
        
        total = await db.execute(select(SysBom).where(SysBom.is_delete == False))
        total_count = len(total.scalars().all())
        
        offset = (query_model.page_num - 1) * query_model.page_size
        query = query.offset(offset).limit(query_model.page_size)
        
        result = await db.execute(query)
        return result.scalars().all(), total_count

    @classmethod
    async def add_bom(cls, db: AsyncSession, bom: SysBom):
        db.add(bom)
        await db.flush()

    @classmethod
    async def update_bom(cls, db: AsyncSession, bom: SysBom) -> int:
        result = await db.execute(
            update(SysBom)
            .where(SysBom.bom_id == bom.bom_id)
            .values(
                product_id=bom.product_id,
                product_name=bom.product_name,
                version=bom.version,
                status=bom.status,
                remark=bom.remark,
                update_by=bom.update_by,
                update_time=bom.update_time
            )
        )
        return result.rowcount

    @classmethod
    async def delete_bom(cls, db: AsyncSession, bom_id: int, update_by: str) -> int:
        result = await db.execute(
            update(SysBom)
            .where(SysBom.bom_id == bom_id)
            .values(is_delete=True, update_by=update_by)
        )
        return result.rowcount

    @classmethod
    async def delete_bom_items(cls, db: AsyncSession, bom_id: int):
        await db.execute(delete(SysBomItem).where(SysBomItem.bom_id == bom_id))