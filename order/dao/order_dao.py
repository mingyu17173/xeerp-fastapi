from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func
from models.order import SysOrder, SysOrderItem, OrderStatus
from schemas.order import AddOrderModel
from typing import Optional, List

class OrderDao:
    @classmethod
    async def get_order_by_id(cls, db: AsyncSession, order_id: int) -> Optional[SysOrder]:
        result = await db.execute(select(SysOrder).where(
            SysOrder.order_id == order_id,
            SysOrder.is_delete == False
        ))
        return result.scalar_one_or_none()

    @classmethod
    async def get_order_by_code(cls, db: AsyncSession, order_code: str) -> Optional[SysOrder]:
        result = await db.execute(select(SysOrder).where(
            SysOrder.order_code == order_code,
            SysOrder.is_delete == False
        ))
        return result.scalar_one_or_none()

    @classmethod
    async def get_order_list(cls, db: AsyncSession, query) -> List[SysOrder]:
        stmt = select(SysOrder).where(SysOrder.is_delete == False)
        
        if query.order_code:
            stmt = stmt.filter(SysOrder.order_code.like(f'%{query.order_code}%'))
        if query.partner_id:
            stmt = stmt.filter(SysOrder.partner_id == query.partner_id)
        if query.order_type:
            stmt = stmt.filter(SysOrder.order_type == query.order_type)
        if query.status:
            stmt = stmt.filter(SysOrder.status == query.status)
        
        stmt = stmt.order_by(SysOrder.create_time.desc())
        
        offset = (query.page_num - 1) * query.page_size
        stmt = stmt.offset(offset).limit(query.page_size)
        
        result = await db.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def get_order_count(cls, db: AsyncSession, query) -> int:
        stmt = select(func.count(SysOrder.order_id)).where(SysOrder.is_delete == False)
        
        if query.order_code:
            stmt = stmt.filter(SysOrder.order_code.like(f'%{query.order_code}%'))
        if query.partner_id:
            stmt = stmt.filter(SysOrder.partner_id == query.partner_id)
        if query.order_type:
            stmt = stmt.filter(SysOrder.order_type == query.order_type)
        if query.status:
            stmt = stmt.filter(SysOrder.status == query.status)
        
        result = await db.execute(stmt)
        return result.scalar_one()

    @classmethod
    async def add_order(cls, db: AsyncSession, add_model: AddOrderModel, create_user: str):
        order = SysOrder(
            order_code=add_model.order_code,
            order_type=add_model.order_type,
            partner_id=add_model.partner_id,
            shipping_address=add_model.shipping_address,
            contact_person=add_model.contact_person,
            contact_phone=add_model.contact_phone,
            delivery_date=add_model.delivery_date,
            remark=add_model.remark,
            create_user=create_user
        )
        
        total_amount = 0
        items = []
        for item_data in add_model.items:
            amount = item_data['quantity'] * item_data['unit_price']
            total_amount += amount
            item = SysOrderItem(
                product_id=item_data['product_id'],
                product_name=item_data.get('product_name', ''),
                unit=item_data.get('unit', '件'),
                quantity=item_data['quantity'],
                unit_price=item_data['unit_price'],
                amount=amount,
                remark=item_data.get('remark')
            )
            items.append(item)
        
        order.total_amount = total_amount
        order.pay_amount = total_amount
        order.items = items
        
        db.add(order)
        await db.flush()
        return order

    @classmethod
    async def update_order_status(cls, db: AsyncSession, order_id: int, status: OrderStatus, update_user: str):
        stmt = update(SysOrder).where(SysOrder.order_id == order_id).values(
            status=status,
            update_user=update_user
        )
        await db.execute(stmt)

    @classmethod
    async def delete_order(cls, db: AsyncSession, order_id: int, update_user: str):
        stmt = update(SysOrder).where(SysOrder.order_id == order_id).values(
            is_delete=True,
            update_user=update_user
        )
        await db.execute(stmt)