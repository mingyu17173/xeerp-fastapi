# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: production_plan_dao.py
# @Software: PyCharm
# @Desc : 数据访问层

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func
from typing import Optional, List, Tuple
from models.production_plan import SysProductionPlan
from schemas.production_plan_schema import ProductionPlanPageQueryModel

class ProductionPlanDao:
    @classmethod
    async def get_plan_by_id(cls, db: AsyncSession, plan_id: int) -> Optional[SysProductionPlan]:
        result = await db.execute(select(SysProductionPlan).where(SysProductionPlan.plan_id == plan_id))
        return result.scalar_one_or_none()

    @classmethod
    async def get_plan_by_code(cls, db: AsyncSession, plan_code: str) -> Optional[SysProductionPlan]:
        result = await db.execute(select(SysProductionPlan).where(SysProductionPlan.plan_code == plan_code))
        return result.scalar_one_or_none()

    @classmethod
    async def get_plan_list(cls, db: AsyncSession, query_model: ProductionPlanPageQueryModel) -> Tuple[List[SysProductionPlan], int]:
        query = select(SysProductionPlan)
        
        if query_model.product_name:
            query = query.where(SysProductionPlan.product_name.like(f'%{query_model.product_name}%'))
        if query_model.status:
            query = query.where(SysProductionPlan.status == query_model.status)
        
        query = query.order_by(SysProductionPlan.create_time.desc())
        
        total = await db.execute(select(func.count(SysProductionPlan.plan_id)))
        total_count = total.scalar_one()
        
        offset = (query_model.page_num - 1) * query_model.page_size
        query = query.offset(offset).limit(query_model.page_size)
        
        result = await db.execute(query)
        return result.scalars().all(), total_count

    @classmethod
    async def add_plan(cls, db: AsyncSession, plan: SysProductionPlan):
        db.add(plan)
        await db.flush()

    @classmethod
    async def update_plan(cls, db: AsyncSession, plan: SysProductionPlan) -> int:
        result = await db.execute(
            update(SysProductionPlan)
            .where(SysProductionPlan.plan_id == plan.plan_id)
            .values(
                plan_code=plan.plan_code,
                product_id=plan.product_id,
                product_name=plan.product_name,
                bom_id=plan.bom_id,
                plan_quantity=plan.plan_quantity,
                warehouse_id=plan.warehouse_id,
                start_date=plan.start_date,
                end_date=plan.end_date,
                status=plan.status,
                remark=plan.remark,
                update_by=plan.update_by,
                update_time=plan.update_time
            )
        )
        return result.rowcount

    @classmethod
    async def update_plan_finished(cls, db: AsyncSession, plan_id: int, finished_quantity: int) -> int:
        result = await db.execute(
            update(SysProductionPlan)
            .where(SysProductionPlan.plan_id == plan_id)
            .values(finished_quantity=finished_quantity)
        )
        return result.rowcount