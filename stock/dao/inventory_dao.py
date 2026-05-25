# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: inventory_dao.py
# @Software: PyCharm
# @Desc : 数据访问层

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func
from typing import Optional, List, Tuple
from models.inventory import SysInventory
from models.warehouse import SysWarehouse
from schemas.inventory_schema import InventoryQueryModel

class InventoryDao:
    @classmethod
    async def get_inventory(cls, db: AsyncSession, product_id: int, warehouse_id: int) -> Optional[SysInventory]:
        result = await db.execute(
            select(SysInventory)
            .where(SysInventory.product_id == product_id, SysInventory.warehouse_id == warehouse_id)
        )
        return result.scalar_one_or_none()

    @classmethod
    async def get_inventory_by_id(cls, db: AsyncSession, inventory_id: int) -> Optional[SysInventory]:
        result = await db.execute(select(SysInventory).where(SysInventory.inventory_id == inventory_id))
        return result.scalar_one_or_none()

    @classmethod
    async def get_inventory_list(cls, db: AsyncSession, query_model: InventoryQueryModel) -> Tuple[List[SysInventory], int]:
        query = select(SysInventory)
        
        if query_model.product_id:
            query = query.where(SysInventory.product_id == query_model.product_id)
        if query_model.warehouse_id:
            query = query.where(SysInventory.warehouse_id == query_model.warehouse_id)
        
        query = query.order_by(SysInventory.product_id)
        
        total = await db.execute(select(func.count(SysInventory.inventory_id)))
        total_count = total.scalar_one()
        
        offset = (query_model.page_num - 1) * query_model.page_size
        query = query.offset(offset).limit(query_model.page_size)
        
        result = await db.execute(query)
        return result.scalars().all(), total_count

    @classmethod
    async def add_inventory(cls, db: AsyncSession, inventory: SysInventory):
        db.add(inventory)
        await db.flush()

    @classmethod
    async def update_inventory_quantity(cls, db: AsyncSession, inventory_id: int, quantity: int) -> int:
        result = await db.execute(
            update(SysInventory)
            .where(SysInventory.inventory_id == inventory_id)
            .values(quantity=quantity)
        )
        return result.rowcount

    @classmethod
    async def update_inventory(cls, db: AsyncSession, inventory: SysInventory) -> int:
        result = await db.execute(
            update(SysInventory)
            .where(SysInventory.inventory_id == inventory.inventory_id)
            .values(
                min_quantity=inventory.min_quantity,
                max_quantity=inventory.max_quantity,
                unit=inventory.unit,
                batch_no=inventory.batch_no,
                expire_date=inventory.expire_date,
            )
        )
        return result.rowcount