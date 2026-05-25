# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: production_scrap_dao.py
# @Software: PyCharm
# @Desc : 数据访问层

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func
from typing import Optional, List, Tuple
from models.production_scrap import SysProductionScrap, SysProductionScrapItem
from schemas.production_scrap_schema import ProductionScrapPageQueryModel

class ProductionScrapDao:
    @classmethod
    async def get_scrap_by_id(cls, db: AsyncSession, scrap_id: int) -> Optional[SysProductionScrap]:
        result = await db.execute(select(SysProductionScrap).where(SysProductionScrap.scrap_id == scrap_id))
        return result.scalar_one_or_none()

    @classmethod
    async def get_scrap_by_code(cls, db: AsyncSession, scrap_code: str) -> Optional[SysProductionScrap]:
        result = await db.execute(select(SysProductionScrap).where(SysProductionScrap.scrap_code == scrap_code))
        return result.scalar_one_or_none()

    @classmethod
    async def get_scrap_list(cls, db: AsyncSession, query_model: ProductionScrapPageQueryModel) -> Tuple[List[SysProductionScrap], int]:
        query = select(SysProductionScrap)
        
        if query_model.plan_code:
            query = query.join(SysProductionScrap.plan).where(SysProductionScrap.plan.has(plan_code=query_model.plan_code))
        if query_model.status:
            query = query.where(SysProductionScrap.status == query_model.status)
        
        query = query.order_by(SysProductionScrap.create_time.desc())
        
        total = await db.execute(select(func.count(SysProductionScrap.scrap_id)))
        total_count = total.scalar_one()
        
        offset = (query_model.page_num - 1) * query_model.page_size
        query = query.offset(offset).limit(query_model.page_size)
        
        result = await db.execute(query)
        return result.scalars().all(), total_count

    @classmethod
    async def add_scrap(cls, db: AsyncSession, scrap: SysProductionScrap):
        db.add(scrap)
        await db.flush()

    @classmethod
    async def update_scrap_status(cls, db: AsyncSession, scrap_id: int, status: str, update_by: str) -> int:
        result = await db.execute(
            update(SysProductionScrap)
            .where(SysProductionScrap.scrap_id == scrap_id)
            .values(status=status, update_by=update_by)
        )
        return result.rowcount