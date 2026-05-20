from sqlalchemy.ext.asyncio import AsyncSession
from dao.purchase_dao import PurchaseDao
from schemas.purchase import PurchaseOrderModel, PurchaseItemModel, AddPurchaseOrderModel, PurchasePageQueryModel
from core.response import ResponseModel, PageResponseModel
from models.purchase import PurchaseStatus

class PurchaseService:
    @classmethod
    async def get_purchase_detail(cls, db: AsyncSession, purchase_id: int) -> ResponseModel:
        purchase = await PurchaseDao.get_purchase_by_id(db, purchase_id)
        if not purchase:
            return ResponseModel.error(code=404, message='采购单不存在')
        
        data = PurchaseOrderModel.from_orm(purchase)
        data.items = [PurchaseItemModel.from_orm(item) for item in purchase.items]
        return ResponseModel.success(data=data)

    @classmethod
    async def get_purchase_list(cls, db: AsyncSession, query: PurchasePageQueryModel) -> PageResponseModel:
        rows = await PurchaseDao.get_purchase_list(db, query)
        total = await PurchaseDao.get_purchase_count(db, query)
        
        data = []
        for purchase in rows:
            purchase_data = PurchaseOrderModel.from_orm(purchase)
            purchase_data.items = [PurchaseItemModel.from_orm(item) for item in purchase.items]
            data.append(purchase_data)
        
        return PageResponseModel.success(rows=data, total=total, page_num=query.page_num, page_size=query.page_size)

    @classmethod
    async def add_purchase(cls, db: AsyncSession, add_model: AddPurchaseOrderModel, create_user: str) -> ResponseModel:
        existing = await PurchaseDao.get_purchase_by_code(db, add_model.purchase_code)
        if existing:
            return ResponseModel.error(code=-1, message='采购单编号已存在')
        
        purchase = await PurchaseDao.add_purchase(db, add_model, create_user)
        await db.commit()
        
        data = PurchaseOrderModel.from_orm(purchase)
        data.items = [PurchaseItemModel.from_orm(item) for item in purchase.items]
        return ResponseModel.success(data=data, message='创建成功')

    @classmethod
    async def approve_purchase(cls, db: AsyncSession, purchase_id: int, update_user: str) -> ResponseModel:
        purchase = await PurchaseDao.get_purchase_by_id(db, purchase_id)
        if not purchase:
            return ResponseModel.error(code=404, message='采购单不存在')
        
        if purchase.status != PurchaseStatus.PENDING:
            return ResponseModel.error(code=-1, message='只能审核待审核的采购单')
        
        await PurchaseDao.update_purchase_status(db, purchase_id, PurchaseStatus.APPROVED, update_user)
        await db.commit()
        
        return ResponseModel.success(message='审核通过')

    @classmethod
    async def receive_purchase(cls, db: AsyncSession, purchase_id: int, items: List[dict], update_user: str) -> ResponseModel:
        purchase = await PurchaseDao.get_purchase_by_id(db, purchase_id)
        if not purchase:
            return ResponseModel.error(code=404, message='采购单不存在')
        
        if purchase.status != PurchaseStatus.ORDERED:
            return ResponseModel.error(code=-1, message='只能收货已下单的采购单')
        
        await PurchaseDao.update_purchase_items_actual(db, purchase_id, items)
        
        all_received = True
        for item in items:
            if item['actual_quantity'] < item['plan_quantity']:
                all_received = False
                break
        
        if all_received:
            await PurchaseDao.update_purchase_status(db, purchase_id, PurchaseStatus.COMPLETED, update_user)
        else:
            await PurchaseDao.update_purchase_status(db, purchase_id, PurchaseStatus.RECEIVED, update_user)
        
        await db.commit()
        
        return ResponseModel.success(message='收货成功')

    @classmethod
    async def delete_purchase(cls, db: AsyncSession, purchase_id: int, update_user: str) -> ResponseModel:
        purchase = await PurchaseDao.get_purchase_by_id(db, purchase_id)
        if not purchase:
            return ResponseModel.error(code=404, message='采购单不存在')
        
        if purchase.status in [PurchaseStatus.ORDERED, PurchaseStatus.RECEIVED]:
            return ResponseModel.error(code=-1, message='已下单或已收货的采购单无法删除')
        
        await PurchaseDao.delete_purchase(db, purchase_id, update_user)
        await db.commit()
        
        return ResponseModel.success(message='删除成功')