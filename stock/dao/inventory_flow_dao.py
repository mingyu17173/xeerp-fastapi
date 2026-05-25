# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: inventory_flow_dao.py
# @Software: PyCharm
# @Desc : 数据访问层

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional, List, Tuple
from models.inventory_flow import SysInventoryFlow
from schemas.inventory_flow_schema import InventoryFlowQueryModel

class InventoryFlowDao:
    @classmethod
    async def add_flow(cls, db: AsyncSession, flow: SysInventoryFlow):
        db.add(flow)
        await db.flush()

    @classmethod
    async def get_flow_list(cls, db: AsyncSession, query_model: InventoryFlowQueryModel) -> Tuple[List[SysInventoryFlow], int]:
        query = select(SysInventoryFlow)
        
        if query_model.product_id:
            query = query.where(SysInventoryFlow.product_id == query_model.product_id)
        if query_model.warehouse_id:
            query = query.where(SysInventoryFlow.warehouse_id == query_model.warehouse_id)
        if query_model.flow_type:
            query = query.where(SysInventoryFlow.flow_type == query_model.flow_type)
        if query_model.start_time:
            query = query.where(SysInventoryFlow.create_time >= query_model.start_time)
        if query_model.end_time:
            query = query.where(SysInventoryFlow.create_time <= query_model.end_time)
        
        query = query.order_by(SysInventoryFlow.create_time.desc())
        
        total = await db.execute(select(func.count(SysInventoryFlow.flow_id)))
        total_count = total.scalar_one()
        
        offset = (query_model.page_num - 1) * query_model.page_size
        query = query.offset(offset).limit(query_model.page_size)
        
        result = await db.execute(query)
        return result.scalars().all(), total_count

    @classmethod
    async def get_flow_by_source(cls, db: AsyncSession, source_type: str, source_id: int) -> List[SysInventoryFlow]:
        result = await db.execute(
            select(SysInventoryFlow)
            .where(SysInventoryFlow.source_type == source_type, SysInventoryFlow.source_id == source_id)
        )
        return result.scalars().all()