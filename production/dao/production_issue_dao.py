from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func
from typing import Optional, List, Tuple
from models.production_issue import SysProductionIssue, SysProductionIssueItem
from schemas.production_issue_schema import ProductionIssuePageQueryModel

class ProductionIssueDao:
    @classmethod
    async def get_issue_by_id(cls, db: AsyncSession, issue_id: int) -> Optional[SysProductionIssue]:
        result = await db.execute(select(SysProductionIssue).where(SysProductionIssue.issue_id == issue_id))
        return result.scalar_one_or_none()

    @classmethod
    async def get_issue_by_code(cls, db: AsyncSession, issue_code: str) -> Optional[SysProductionIssue]:
        result = await db.execute(select(SysProductionIssue).where(SysProductionIssue.issue_code == issue_code))
        return result.scalar_one_or_none()

    @classmethod
    async def get_issue_list(cls, db: AsyncSession, query_model: ProductionIssuePageQueryModel) -> Tuple[List[SysProductionIssue], int]:
        query = select(SysProductionIssue)
        
        if query_model.plan_code:
            query = query.join(SysProductionIssue.plan).where(SysProductionIssue.plan.has(plan_code=query_model.plan_code))
        if query_model.status:
            query = query.where(SysProductionIssue.status == query_model.status)
        
        query = query.order_by(SysProductionIssue.create_time.desc())
        
        total = await db.execute(select(func.count(SysProductionIssue.issue_id)))
        total_count = total.scalar_one()
        
        offset = (query_model.page_num - 1) * query_model.page_size
        query = query.offset(offset).limit(query_model.page_size)
        
        result = await db.execute(query)
        return result.scalars().all(), total_count

    @classmethod
    async def add_issue(cls, db: AsyncSession, issue: SysProductionIssue):
        db.add(issue)
        await db.flush()

    @classmethod
    async def update_issue_status(cls, db: AsyncSession, issue_id: int, status: str, update_by: str) -> int:
        result = await db.execute(
            update(SysProductionIssue)
            .where(SysProductionIssue.issue_id == issue_id)
            .values(status=status, update_by=update_by)
        )
        return result.rowcount

    @classmethod
    async def update_issue_items_actual(cls, db: AsyncSession, issue_id: int, items: List[dict]) -> int:
        count = 0
        for item in items:
            result = await db.execute(
                update(SysProductionIssueItem)
                .where(SysProductionIssueItem.issue_item_id == item['issue_item_id'])
                .values(actual_quantity=item['actual_quantity'])
            )
            count += result.rowcount
        return count