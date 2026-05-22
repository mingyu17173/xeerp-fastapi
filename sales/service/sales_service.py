"""
Sales Service Business Logic
销售服务业务逻辑层
"""

from sqlalchemy.ext.asyncio import AsyncSession
from dao.sales_dao import SalesOrderDao, SalesDeliveryDao, SalesReturnDao
from models.sales import SalesOrderStatus, DeliveryStatus, ReturnStatus
from schemas.sales import (
    AddSalesOrderModel, EditSalesOrderModel, SalesOrderPageQueryModel,
    AddDeliveryModel, AddReturnModel, ApproveReturnModel,
    SalesOrderDetailModel, SalesItemModel
)
from core.response import ResponseModel, PageResponseModel
from core.exceptions import (
    OrderNotFoundError, OrderCodeExistsError, OrderStatusError,
    InsufficientStockError
)

class SalesOrderService:
    """销售订单服务"""
    
    @classmethod
    async def get_order_detail(cls, db: AsyncSession, sales_id: int) -> ResponseModel:
        """获取订单详情"""
        order = await SalesOrderDao.get_order_by_id(db, sales_id)
        if not order:
            raise OrderNotFoundError()
        
        # 获取订单明细
        items = []
        for item in order.items:
            items.append(SalesItemModel(
                product_id=item.product_id,
                product_name=item.product_name,
                product_code=item.product_code,
                unit=item.unit,
                quantity=item.quantity,
                unit_price=item.unit_price,
                amount=item.amount,
                discount=item.discount,
                remark=item.remark
            ))
        
        data = SalesOrderDetailModel(
            sales_id=order.sales_id,
            sales_code=order.sales_code,
            customer_id=order.customer_id,
            customer_name=order.customer_name,
            warehouse_id=order.warehouse_id,
            status=order.status.value,
            delivery_status=order.delivery_status.value,
            total_amount=order.total_amount,
            tax_amount=order.tax_amount,
            discount_amount=order.discount_amount,
            paid_amount=order.paid_amount,
            delivery_date=order.delivery_date,
            shipping_address=order.shipping_address,
            contact_person=order.contact_person,
            contact_phone=order.contact_phone,
            remark=order.remark,
            create_time=order.create_time,
            create_user=order.create_user,
            items=items
        )
        
        return ResponseModel.success(data=data)
    
    @classmethod
    async def get_order_list(cls, db: AsyncSession, query: SalesOrderPageQueryModel) -> PageResponseModel:
        """获取订单列表"""
        orders = await SalesOrderDao.get_order_list(db, query)
        total = await SalesOrderDao.get_order_count(db, query)
        
        data = []
        for order in orders:
            items = []
            for item in order.items:
                items.append(SalesItemModel(
                    product_id=item.product_id,
                    product_name=item.product_name,
                    unit=item.unit,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    amount=item.amount
                ))
            
            data.append(SalesOrderDetailModel(
                sales_id=order.sales_id,
                sales_code=order.sales_code,
                customer_id=order.customer_id,
                customer_name=order.customer_name,
                status=order.status.value,
                delivery_status=order.delivery_status.value,
                total_amount=order.total_amount,
                create_time=order.create_time,
                items=items
            ))
        
        return PageResponseModel.success(
            rows=data,
            total=total,
            page_num=query.page_num,
            page_size=query.page_size
        )
    
    @classmethod
    async def add_order(cls, db: AsyncSession, model: AddSalesOrderModel, create_user: str) -> ResponseModel:
        """新增订单"""
        # 检查订单编号是否已存在
        existing = await SalesOrderDao.get_order_by_code(db, model.sales_code)
        if existing:
            raise OrderCodeExistsError()
        
        # 计算总金额
        total_amount = 0
        for item in model.items:
            item.amount = item.quantity * item.unit_price * (1 - item.discount / 100 if item.discount else 1)
            total_amount += item.amount
        
        model.total_amount = total_amount + (model.tax_amount or 0)
        
        # 创建订单
        await SalesOrderDao.add_order(db, model, create_user)
        await db.commit()
        
        return ResponseModel.success(message='订单创建成功')
    
    @classmethod
    async def edit_order(cls, db: AsyncSession, model: EditSalesOrderModel, update_user: str) -> ResponseModel:
        """编辑订单"""
        order = await SalesOrderDao.get_order_by_id(db, model.sales_id)
        if not order:
            raise OrderNotFoundError()
        
        # 检查订单状态
        if order.status != SalesOrderStatus.PENDING:
            raise OrderStatusError('已审核订单不能修改')
        
        await SalesOrderDao.update_order(db, model, update_user)
        await db.commit()
        
        return ResponseModel.success(message='订单修改成功')
    
    @classmethod
    async def delete_order(cls, db: AsyncSession, sales_id: int, update_user: str) -> ResponseModel:
        """删除订单"""
        order = await SalesOrderDao.get_order_by_id(db, sales_id)
        if not order:
            raise OrderNotFoundError()
        
        # 检查订单状态
        if order.status not in [SalesOrderStatus.PENDING, SalesOrderStatus.CANCELLED]:
            raise OrderStatusError('只能删除待审核或已取消的订单')
        
        await SalesOrderDao.delete_order(db, sales_id, update_user)
        await db.commit()
        
        return ResponseModel.success(message='订单删除成功')
    
    @classmethod
    async def approve_order(cls, db: AsyncSession, sales_id: int, update_user: str) -> ResponseModel:
        """审核订单"""
        order = await SalesOrderDao.get_order_by_id(db, sales_id)
        if not order:
            raise OrderNotFoundError()
        
        if order.status != SalesOrderStatus.PENDING:
            raise OrderStatusError('订单状态不正确')
        
        await SalesOrderDao.update_order_status(db, sales_id, SalesOrderStatus.APPROVED)
        await db.commit()
        
        return ResponseModel.success(message='订单审核通过')
    
    @classmethod
    async def cancel_order(cls, db: AsyncSession, sales_id: int, update_user: str) -> ResponseModel:
        """取消订单"""
        order = await SalesOrderDao.get_order_by_id(db, sales_id)
        if not order:
            raise OrderNotFoundError()
        
        if order.status in [SalesOrderStatus.COMPLETED, SalesOrderStatus.CANCELLED]:
            raise OrderStatusError('订单状态不允许取消')
        
        await SalesOrderDao.update_order_status(db, sales_id, SalesOrderStatus.CANCELLED)
        await db.commit()
        
        return ResponseModel.success(message='订单已取消')

class SalesDeliveryService:
    """销售发货服务"""
    
    @classmethod
    async def create_delivery(cls, db: AsyncSession, model: AddDeliveryModel, create_user: str) -> ResponseModel:
        """创建发货单"""
        # 检查订单
        order = await SalesOrderDao.get_order_by_id(db, model.sales_id)
        if not order:
            raise OrderNotFoundError()
        
        if order.status != SalesOrderStatus.APPROVED:
            raise OrderStatusError('只能对已审核的订单发货')
        
        # 创建发货单
        await SalesDeliveryDao.add_delivery(db, model, create_user)
        
        # 更新订单发货状态
        await db.execute(
            f"UPDATE sys_sales_item SET delivered_quantity = delivered_quantity + "
            f"(SELECT quantity FROM sys_sales_delivery_item WHERE sales_item_id = sys_sales_item.item_id) "
            f"WHERE sales_id = {model.sales_id}"
        )
        
        await db.commit()
        
        return ResponseModel.success(message='发货单创建成功')

class SalesReturnService:
    """销售退货服务"""
    
    @classmethod
    async def create_return(cls, db: AsyncSession, model: AddReturnModel, create_user: str) -> ResponseModel:
        """创建退货单"""
        # 检查订单
        order = await SalesOrderDao.get_order_by_id(db, model.sales_id)
        if not order:
            raise OrderNotFoundError()
        
        if order.status not in [SalesOrderStatus.SHIPPED, SalesOrderStatus.COMPLETED]:
            raise OrderStatusError('只能对已发货或已完成的订单退货')
        
        # 创建退货单
        await SalesReturnDao.add_return(db, model, create_user)
        await db.commit()
        
        return ResponseModel.success(message='退货单创建成功')
    
    @classmethod
    async def approve_return(cls, db: AsyncSession, model: ApproveReturnModel, update_user: str) -> ResponseModel:
        """审核退货单"""
        status = ReturnStatus.APPROVED if model.approved else ReturnStatus.REJECTED
        await SalesReturnDao.update_return_status(db, model.return_id, status, update_user)
        await db.commit()
        
        message = '退货审核通过' if model.approved else '退货已拒绝'
        return ResponseModel.success(message=message)