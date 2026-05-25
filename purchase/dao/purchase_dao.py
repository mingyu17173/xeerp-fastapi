# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: purchase_dao.py
# @Software: PyCharm
# @Desc : 数据访问层

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func
from models.purchase import SysPurchaseOrder, SysPurchaseItem, PurchaseStatus
from schemas.purchase import AddPurchaseOrderModel
from typing import Optional, List

class PurchaseDao:
    @classmethod
    async def get_purchase_by_id(cls, db: AsyncSession, purchase_id: int) -> Optional[SysPurchaseOrder]:
        result = await db.execute(select(SysPurchaseOrder).where(
            SysPurchaseOrder.purchase_id == purchase_id,
            SysPurchaseOrder.is_delete == False
        ))
        return result.scalar_one_or_none()

    @classmethod
    async def get_purchase_by_code(cls, db: AsyncSession, purchase_code: str) -> Optional[SysPurchaseOrder]:
        result = await db.execute(select(SysPurchaseOrder).where(
            SysPurchaseOrder.purchase_code == purchase_code,
            SysPurchaseOrder.is_delete == False
        ))
        return result.scalar_one_or_none()

    @classmethod
    async def get_purchase_list(cls, db: AsyncSession, query) -> List[SysPurchaseOrder]:
        stmt = select(SysPurchaseOrder).where(SysPurchaseOrder.is_delete == False)
        
        if query.purchase_code:
            stmt = stmt.filter(SysPurchaseOrder.purchase_code.like(f'%{query.purchase_code}%'))
        if query.supplier_id:
            stmt = stmt.filter(SysPurchaseOrder.supplier_id == query.supplier_id)
        if query.status:
            stmt = stmt.filter(SysPurchaseOrder.status == query.status)
        
        stmt = stmt.order_by(SysPurchaseOrder.create_time.desc())
        
        offset = (query.page_num - 1) * query.page_size
        stmt = stmt.offset(offset).limit(query.page_size)
        
        result = await db.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def get_purchase_count(cls, db: AsyncSession, query) -> int:
        stmt = select(func.count(SysPurchaseOrder.purchase_id)).where(SysPurchaseOrder.is_delete == False)
        
        if query.purchase_code:
            stmt = stmt.filter(SysPurchaseOrder.purchase_code.like(f'%{query.purchase_code}%'))
        if query.supplier_id:
            stmt = stmt.filter(SysPurchaseOrder.supplier_id == query.supplier_id)
        if query.status:
            stmt = stmt.filter(SysPurchaseOrder.status == query.status)
        
        result = await db.execute(stmt)
        return result.scalar_one()

    @classmethod
    async def add_purchase(cls, db: AsyncSession, add_model: AddPurchaseOrderModel, create_user: str):
        purchase = SysPurchaseOrder(
            purchase_code=add_model.purchase_code,
            supplier_id=add_model.supplier_id,
            warehouse_id=add_model.warehouse_id,
            expected_date=add_model.expected_date,
            remark=add_model.remark,
            create_user=create_user
        )
        
        total_amount = 0
        items = []
        for item_data in add_model.items:
            amount = item_data['plan_quantity'] * item_data['unit_price']
            total_amount += amount
            item = SysPurchaseItem(
                product_id=item_data['product_id'],
                product_name=item_data.get('product_name', ''),
                unit=item_data.get('unit', '件'),
                plan_quantity=item_data['plan_quantity'],
                unit_price=item_data['unit_price'],
                amount=amount,
                remark=item_data.get('remark')
            )
            items.append(item)
        
        purchase.total_amount = total_amount
        purchase.items = items
        
        db.add(purchase)
        await db.flush()
        return purchase

    @classmethod
    async def update_purchase_status(cls, db: AsyncSession, purchase_id: int, status: PurchaseStatus, update_user: str):
        stmt = update(SysPurchaseOrder).where(SysPurchaseOrder.purchase_id == purchase_id).values(
            status=status,
            update_user=update_user
        )
        await db.execute(stmt)

    @classmethod
    async def update_purchase_items_actual(cls, db: AsyncSession, purchase_id: int, items: List[dict]):
        for item_data in items:
            stmt = update(SysPurchaseItem).where(
                SysPurchaseItem.item_id == item_data['item_id']
            ).values(
                actual_quantity=item_data['actual_quantity']
            )
            await db.execute(stmt)

    @classmethod
    async def delete_purchase(cls, db: AsyncSession, purchase_id: int, update_user: str):
        stmt = update(SysPurchaseOrder).where(SysPurchaseOrder.purchase_id == purchase_id).values(
            is_delete=True,
            update_user=update_user
        )
        await db.execute(stmt)