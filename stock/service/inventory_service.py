from datetime import datetime
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Tuple
from dao.inventory_dao import InventoryDao
from dao.inventory_flow_dao import InventoryFlowDao
from models.inventory import SysInventory
from models.inventory_flow import SysInventoryFlow
from schemas.common_schema import CrudResponseModel, PageResponseModel
from schemas.inventory_schema import InventoryModel, InventoryQueryModel, InventoryAdjustModel
from core.get_redis import get_redis
from core.env import AppConfig

class InventoryService:
    @classmethod
    async def get_inventory(cls, db: AsyncSession, product_id: int, warehouse_id: int) -> Optional[InventoryModel]:
        inventory = await InventoryDao.get_inventory(db, product_id, warehouse_id)
        if inventory:
            return InventoryModel.model_validate(inventory)
        return None

    @classmethod
    async def get_inventory_list(cls, db: AsyncSession, query_model: InventoryQueryModel) -> PageResponseModel:
        inventories, total = await InventoryDao.get_inventory_list(db, query_model)
        inventory_models = [InventoryModel.model_validate(i) for i in inventories]
        return PageResponseModel(
            rows=inventory_models,
            total=total,
            page_num=query_model.page_num,
            page_size=query_model.page_size
        )

    @classmethod
    async def get_inventory_quantity(cls, db: AsyncSession, product_id: int, warehouse_id: int) -> int:
        redis_client = get_redis()
        cache_key = f"inventory:{product_id}:{warehouse_id}"
        
        cached = redis_client.get(cache_key)
        if cached:
            return int(cached)
        
        inventory = await InventoryDao.get_inventory(db, product_id, warehouse_id)
        quantity = inventory.quantity if inventory else 0
        
        redis_client.setex(cache_key, AppConfig.cache_expire_seconds, quantity)
        return quantity

    @classmethod
    async def adjust_inventory(cls, request: Request, db: AsyncSession, adjust_model: InventoryAdjustModel) -> CrudResponseModel:
        inventory = await InventoryDao.get_inventory(db, adjust_model.product_id, adjust_model.warehouse_id)
        
        if not inventory:
            inventory = SysInventory(
                product_id=adjust_model.product_id,
                warehouse_id=adjust_model.warehouse_id,
                quantity=0
            )
            await InventoryDao.add_inventory(db, inventory)
            await db.flush()
        
        before_quantity = inventory.quantity
        after_quantity = before_quantity + adjust_model.quantity
        
        if after_quantity < 0:
            return CrudResponseModel(is_success=False, message='库存不足')
        
        await InventoryDao.update_inventory_quantity(db, inventory.inventory_id, after_quantity)
        
        flow_type = 'in' if adjust_model.quantity > 0 else 'out' if adjust_model.quantity < 0 else 'adjust'
        flow = SysInventoryFlow(
            product_id=adjust_model.product_id,
            warehouse_id=adjust_model.warehouse_id,
            flow_type=flow_type,
            quantity=abs(adjust_model.quantity),
            before_quantity=before_quantity,
            after_quantity=after_quantity,
            remark=adjust_model.remark,
            create_by=getattr(request.state, 'user_name', 'system'),
            create_time=datetime.now()
        )
        await InventoryFlowDao.add_flow(db, flow)
        
        redis_client = get_redis()
        cache_key = f"inventory:{adjust_model.product_id}:{adjust_model.warehouse_id}"
        redis_client.setex(cache_key, AppConfig.cache_expire_seconds, after_quantity)
        
        await db.commit()
        return CrudResponseModel(is_success=True, message='库存调整成功')

    @classmethod
    async def batch_adjust_inventory(cls, request: Request, db: AsyncSession, items: List[dict]) -> CrudResponseModel:
        redis_client = get_redis()
        
        for item in items:
            product_id = item['product_id']
            warehouse_id = item['warehouse_id']
            quantity = item['quantity']
            
            inventory = await InventoryDao.get_inventory(db, product_id, warehouse_id)
            
            if not inventory:
                inventory = SysInventory(
                    product_id=product_id,
                    warehouse_id=warehouse_id,
                    quantity=0
                )
                await InventoryDao.add_inventory(db, inventory)
                await db.flush()
            
            before_quantity = inventory.quantity
            after_quantity = before_quantity + quantity
            
            if after_quantity < 0:
                await db.rollback()
                return CrudResponseModel(is_success=False, message=f'商品ID {product_id} 库存不足')
            
            await InventoryDao.update_inventory_quantity(db, inventory.inventory_id, after_quantity)
            
            flow_type = 'in' if quantity > 0 else 'out' if quantity < 0 else 'adjust'
            flow = SysInventoryFlow(
                product_id=product_id,
                warehouse_id=warehouse_id,
                flow_type=flow_type,
                quantity=abs(quantity),
                before_quantity=before_quantity,
                after_quantity=after_quantity,
                source_type=item.get('source_type'),
                source_id=item.get('source_id'),
                create_by=getattr(request.state, 'user_name', 'system'),
                create_time=datetime.now()
            )
            await InventoryFlowDao.add_flow(db, flow)
            
            cache_key = f"inventory:{product_id}:{warehouse_id}"
            redis_client.setex(cache_key, AppConfig.cache_expire_seconds, after_quantity)
        
        await db.commit()
        return CrudResponseModel(is_success=True, message='批量调整成功')