from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from typing import Optional, List, Tuple
from models.warehouse import SysWarehouse
from schemas.warehouse_schema import WarehousePageQueryModel

class WarehouseDao:
    @classmethod
    async def get_warehouse_by_id(cls, db: AsyncSession, warehouse_id: int) -> Optional[SysWarehouse]:
        result = await db.execute(select(SysWarehouse).where(SysWarehouse.warehouse_id == warehouse_id, SysWarehouse.is_delete == False))
        return result.scalar_one_or_none()

    @classmethod
    async def get_warehouse_by_code(cls, db: AsyncSession, warehouse_code: str) -> Optional[SysWarehouse]:
        result = await db.execute(select(SysWarehouse).where(SysWarehouse.warehouse_code == warehouse_code, SysWarehouse.is_delete == False))
        return result.scalar_one_or_none()

    @classmethod
    async def get_warehouse_list(cls, db: AsyncSession, query_model: WarehousePageQueryModel) -> Tuple[List[SysWarehouse], int]:
        query = select(SysWarehouse).where(SysWarehouse.is_delete == False)
        
        if query_model.warehouse_name:
            query = query.where(SysWarehouse.warehouse_name.like(f'%{query_model.warehouse_name}%'))
        if query_model.warehouse_code:
            query = query.where(SysWarehouse.warehouse_code.like(f'%{query_model.warehouse_code}%'))
        
        query = query.order_by(SysWarehouse.create_time.desc())
        
        total = await db.execute(select(SysWarehouse).where(SysWarehouse.is_delete == False))
        total_count = len(total.scalars().all())
        
        offset = (query_model.page_num - 1) * query_model.page_size
        query = query.offset(offset).limit(query_model.page_size)
        
        result = await db.execute(query)
        return result.scalars().all(), total_count

    @classmethod
    async def add_warehouse(cls, db: AsyncSession, warehouse: SysWarehouse):
        db.add(warehouse)
        await db.flush()

    @classmethod
    async def update_warehouse(cls, db: AsyncSession, warehouse: SysWarehouse) -> int:
        result = await db.execute(
            update(SysWarehouse)
            .where(SysWarehouse.warehouse_id == warehouse.warehouse_id)
            .values(
                warehouse_code=warehouse.warehouse_code,
                warehouse_name=warehouse.warehouse_name,
                address=warehouse.address,
                manager=warehouse.manager,
                phone=warehouse.phone,
                status=warehouse.status,
                remark=warehouse.remark,
                update_by=warehouse.update_by,
                update_time=warehouse.update_time
            )
        )
        return result.rowcount

    @classmethod
    async def delete_warehouse(cls, db: AsyncSession, warehouse_id: int, update_by: str) -> int:
        result = await db.execute(
            update(SysWarehouse)
            .where(SysWarehouse.warehouse_id == warehouse_id)
            .values(is_delete=True, update_by=update_by)
        )
        return result.rowcount