from sqlalchemy.ext.asyncio import AsyncSession
from dao.order_dao import OrderDao
from schemas.order import OrderModel, OrderItemModel, AddOrderModel, OrderPageQueryModel
from core.response import ResponseModel, PageResponseModel
from models.order import OrderStatus

class OrderService:
    @classmethod
    async def get_order_detail(cls, db: AsyncSession, order_id: int) -> ResponseModel:
        order = await OrderDao.get_order_by_id(db, order_id)
        if not order:
            return ResponseModel.error(code=404, message='订单不存在')
        
        data = OrderModel.from_orm(order)
        data.items = [OrderItemModel.from_orm(item) for item in order.items]
        return ResponseModel.success(data=data)

    @classmethod
    async def get_order_list(cls, db: AsyncSession, query: OrderPageQueryModel) -> PageResponseModel:
        rows = await OrderDao.get_order_list(db, query)
        total = await OrderDao.get_order_count(db, query)
        
        data = []
        for order in rows:
            order_data = OrderModel.from_orm(order)
            order_data.items = [OrderItemModel.from_orm(item) for item in order.items]
            data.append(order_data)
        
        return PageResponseModel.success(rows=data, total=total, page_num=query.page_num, page_size=query.page_size)

    @classmethod
    async def add_order(cls, db: AsyncSession, add_model: AddOrderModel, create_user: str) -> ResponseModel:
        existing = await OrderDao.get_order_by_code(db, add_model.order_code)
        if existing:
            return ResponseModel.error(code=-1, message='订单编号已存在')
        
        order = await OrderDao.add_order(db, add_model, create_user)
        await db.commit()
        
        data = OrderModel.from_orm(order)
        data.items = [OrderItemModel.from_orm(item) for item in order.items]
        return ResponseModel.success(data=data, message='创建成功')

    @classmethod
    async def confirm_order(cls, db: AsyncSession, order_id: int, update_user: str) -> ResponseModel:
        order = await OrderDao.get_order_by_id(db, order_id)
        if not order:
            return ResponseModel.error(code=404, message='订单不存在')
        
        if order.status != OrderStatus.PENDING:
            return ResponseModel.error(code=-1, message='只能确认待审核的订单')
        
        await OrderDao.update_order_status(db, order_id, OrderStatus.CONFIRMED, update_user)
        await db.commit()
        
        return ResponseModel.success(message='确认成功')

    @classmethod
    async def cancel_order(cls, db: AsyncSession, order_id: int, update_user: str) -> ResponseModel:
        order = await OrderDao.get_order_by_id(db, order_id)
        if not order:
            return ResponseModel.error(code=404, message='订单不存在')
        
        if order.status == OrderStatus.COMPLETED:
            return ResponseModel.error(code=-1, message='已完成的订单无法取消')
        
        await OrderDao.update_order_status(db, order_id, OrderStatus.CANCELLED, update_user)
        await db.commit()
        
        return ResponseModel.success(message='取消成功')

    @classmethod
    async def delete_order(cls, db: AsyncSession, order_id: int, update_user: str) -> ResponseModel:
        order = await OrderDao.get_order_by_id(db, order_id)
        if not order:
            return ResponseModel.error(code=404, message='订单不存在')
        
        await OrderDao.delete_order(db, order_id, update_user)
        await db.commit()
        
        return ResponseModel.success(message='删除成功')