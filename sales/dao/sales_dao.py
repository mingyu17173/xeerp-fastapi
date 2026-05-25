# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: sales_dao.py
# @Software: PyCharm
# @Desc : 数据访问层

"""
Sales Service DAO
销售服务数据访问层
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func
from models.sales import (
    SysSalesOrder, SysSalesItem, SysSalesDelivery, 
    SysSalesDeliveryItem, SysSalesReturn, SysSalesReturnItem,
    SalesOrderStatus, DeliveryStatus, ReturnStatus
)
from schemas.sales import (
    AddSalesOrderModel, EditSalesOrderModel, SalesOrderPageQueryModel,
    AddDeliveryModel, AddReturnModel
)

class SalesOrderDao:
    """销售订单数据访问"""
    
    @classmethod
    async def get_order_by_id(cls, db: AsyncSession, sales_id: int):
        """根据ID获取订单"""
        result = await db.execute(select(SysSalesOrder).where(SysSalesOrder.sales_id == sales_id))
        return result.scalar_one_or_none()
    
    @classmethod
    async def get_order_by_code(cls, db: AsyncSession, sales_code: str):
        """根据编号获取订单"""
        result = await db.execute(select(SysSalesOrder).where(SysSalesOrder.sales_code == sales_code))
        return result.scalar_one_or_none()
    
    @classmethod
    async def get_order_list(cls, db: AsyncSession, query: SalesOrderPageQueryModel):
        """获取订单列表（分页）"""
        stmt = select(SysSalesOrder).where(SysSalesOrder.is_delete == False)
        
        if query.sales_code:
            stmt = stmt.filter(SysSalesOrder.sales_code.like(f"%{query.sales_code}%"))
        if query.customer_name:
            stmt = stmt.filter(SysSalesOrder.customer_name.like(f"%{query.customer_name}%"))
        if query.status:
            stmt = stmt.filter(SysSalesOrder.status == query.status)
        if query.start_date:
            stmt = stmt.filter(SysSalesOrder.create_time >= query.start_date)
        if query.end_date:
            stmt = stmt.filter(SysSalesOrder.create_time <= query.end_date)
        
        stmt = stmt.offset((query.page_num - 1) * query.page_size).limit(query.page_size)
        result = await db.execute(stmt)
        return result.scalars().all()
    
    @classmethod
    async def get_order_count(cls, db: AsyncSession, query: SalesOrderPageQueryModel):
        """获取订单总数"""
        stmt = select(func.count(SysSalesOrder.sales_id)).where(SysSalesOrder.is_delete == False)
        
        if query.sales_code:
            stmt = stmt.filter(SysSalesOrder.sales_code.like(f"%{query.sales_code}%"))
        if query.customer_name:
            stmt = stmt.filter(SysSalesOrder.customer_name.like(f"%{query.customer_name}%"))
        if query.status:
            stmt = stmt.filter(SysSalesOrder.status == query.status)
        if query.start_date:
            stmt = stmt.filter(SysSalesOrder.create_time >= query.start_date)
        if query.end_date:
            stmt = stmt.filter(SysSalesOrder.create_time <= query.end_date)
        
        result = await db.execute(stmt)
        return result.scalar_one()
    
    @classmethod
    async def add_order(cls, db: AsyncSession, model: AddSalesOrderModel, create_user: str):
        """新增订单"""
        order = SysSalesOrder(
            sales_code=model.sales_code,
            customer_id=model.customer_id,
            customer_name=model.customer_name,
            warehouse_id=model.warehouse_id,
            total_amount=model.total_amount,
            tax_amount=model.tax_amount,
            discount_amount=model.discount_amount,
            delivery_date=model.delivery_date,
            shipping_address=model.shipping_address,
            contact_person=model.contact_person,
            contact_phone=model.contact_phone,
            remark=model.remark,
            create_user=create_user
        )
        db.add(order)
        await db.flush()
        
        # 添加明细
        for item in model.items:
            sales_item = SysSalesItem(
                sales_id=order.sales_id,
                product_id=item.product_id,
                product_name=item.product_name,
                product_code=item.product_code,
                unit=item.unit,
                quantity=item.quantity,
                unit_price=item.unit_price,
                amount=item.amount if item.amount else item.quantity * item.unit_price,
                discount=item.discount,
                remark=item.remark
            )
            db.add(sales_item)
        
        return order
    
    @classmethod
    async def update_order(cls, db: AsyncSession, model: EditSalesOrderModel, update_user: str):
        """更新订单"""
        stmt = update(SysSalesOrder).where(SysSalesOrder.sales_id == model.sales_id).values(
            customer_id=model.customer_id,
            customer_name=model.customer_name,
            warehouse_id=model.warehouse_id,
            delivery_date=model.delivery_date,
            shipping_address=model.shipping_address,
            contact_person=model.contact_person,
            contact_phone=model.contact_phone,
            remark=model.remark,
            update_user=update_user
        )
        await db.execute(stmt)
    
    @classmethod
    async def delete_order(cls, db: AsyncSession, sales_id: int, update_user: str):
        """删除订单"""
        stmt = update(SysSalesOrder).where(SysSalesOrder.sales_id == sales_id).values(
            is_delete=True,
            update_user=update_user
        )
        await db.execute(stmt)
    
    @classmethod
    async def update_order_status(cls, db: AsyncSession, sales_id: int, status: SalesOrderStatus):
        """更新订单状态"""
        stmt = update(SysSalesOrder).where(SysSalesOrder.sales_id == sales_id).values(
            status=status
        )
        await db.execute(stmt)

class SalesDeliveryDao:
    """销售发货数据访问"""
    
    @classmethod
    async def add_delivery(cls, db: AsyncSession, model: AddDeliveryModel, create_user: str):
        """新增发货单"""
        delivery = SysSalesDelivery(
            delivery_code=model.delivery_code,
            sales_id=model.sales_id,
            warehouse_id=model.warehouse_id,
            warehouse_name=model.warehouse_name,
            carrier=model.carrier,
            tracking_no=model.tracking_no,
            remark=model.remark,
            create_user=create_user
        )
        db.add(delivery)
        await db.flush()
        
        # 添加发货明细
        total_qty = 0
        for item in model.items:
            delivery_item = SysSalesDeliveryItem(
                delivery_id=delivery.delivery_id,
                sales_item_id=item.sales_item_id,
                product_id=item.product_id,
                product_name=item.product_name,
                unit=item.unit,
                quantity=item.quantity,
                batch_no=item.batch_no
            )
            db.add(delivery_item)
            total_qty += item.quantity
        
        delivery.total_quantity = total_qty
        return delivery

class SalesReturnDao:
    """销售退货数据访问"""
    
    @classmethod
    async def add_return(cls, db: AsyncSession, model: AddReturnModel, create_user: str):
        """新增退货单"""
        return_order = SysSalesReturn(
            return_code=model.return_code,
            sales_id=model.sales_id,
            warehouse_id=model.warehouse_id,
            total_amount=model.total_amount,
            reason=model.reason,
            remark=model.remark,
            create_user=create_user
        )
        db.add(return_order)
        await db.flush()
        
        # 添加退货明细
        for item in model.items:
            return_item = SysSalesReturnItem(
                return_id=return_order.return_id,
                sales_item_id=item.sales_item_id,
                product_id=item.product_id,
                product_name=item.product_name,
                unit=item.unit,
                quantity=item.quantity,
                unit_price=item.unit_price,
                amount=item.amount if item.amount else item.quantity * item.unit_price,
                reason=item.reason
            )
            db.add(return_item)
        
        return return_order
    
    @classmethod
    async def update_return_status(cls, db: AsyncSession, return_id: int, status: ReturnStatus, update_user: str):
        """更新退货状态"""
        stmt = update(SysSalesReturn).where(SysSalesReturn.return_id == return_id).values(
            status=status,
            update_user=update_user
        )
        await db.execute(stmt)