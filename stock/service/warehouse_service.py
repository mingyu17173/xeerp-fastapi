# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: warehouse_service.py
# @Software: PyCharm
# @Desc : 业务服务

from datetime import datetime
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Tuple
from dao.warehouse_dao import WarehouseDao
from models.warehouse import SysWarehouse
from schemas.common_schema import CrudResponseModel, PageResponseModel
from schemas.warehouse_schema import WarehouseModel, AddWarehouseModel, EditWarehouseModel, WarehousePageQueryModel

class WarehouseService:
    @classmethod
    async def get_warehouse_detail(cls, db: AsyncSession, warehouse_id: int) -> Optional[WarehouseModel]:
        warehouse = await WarehouseDao.get_warehouse_by_id(db, warehouse_id)
        if warehouse:
            return WarehouseModel.model_validate(warehouse)
        return None

    @classmethod
    async def get_warehouse_list(cls, db: AsyncSession, query_model: WarehousePageQueryModel) -> PageResponseModel:
        warehouses, total = await WarehouseDao.get_warehouse_list(db, query_model)
        warehouse_models = [WarehouseModel.model_validate(w) for w in warehouses]
        return PageResponseModel(
            rows=warehouse_models,
            total=total,
            page_num=query_model.page_num,
            page_size=query_model.page_size
        )

    @classmethod
    async def add_warehouse(cls, request: Request, db: AsyncSession, add_model: AddWarehouseModel) -> CrudResponseModel:
        if await WarehouseDao.get_warehouse_by_code(db, add_model.warehouse_code):
            return CrudResponseModel(is_success=False, message=f"仓库编码 '{add_model.warehouse_code}' 已存在")

        warehouse = SysWarehouse(
            warehouse_code=add_model.warehouse_code,
            warehouse_name=add_model.warehouse_name,
            address=add_model.address,
            manager=add_model.manager,
            phone=add_model.phone,
            status=add_model.status,
            remark=add_model.remark,
            create_by=getattr(request.state, 'user_name', 'system'),
            create_time=datetime.now()
        )

        await WarehouseDao.add_warehouse(db, warehouse)
        await db.commit()
        return CrudResponseModel(is_success=True, message='新增成功')

    @classmethod
    async def edit_warehouse(cls, request: Request, db: AsyncSession, edit_model: EditWarehouseModel) -> CrudResponseModel:
        existing = await WarehouseDao.get_warehouse_by_id(db, edit_model.warehouse_id)
        if not existing:
            return CrudResponseModel(is_success=False, message='仓库不存在')

        code_exists = await WarehouseDao.get_warehouse_by_code(db, edit_model.warehouse_code)
        if code_exists and code_exists.warehouse_id != edit_model.warehouse_id:
            return CrudResponseModel(is_success=False, message=f"仓库编码 '{edit_model.warehouse_code}' 已存在")

        warehouse = SysWarehouse(
            warehouse_id=edit_model.warehouse_id,
            warehouse_code=edit_model.warehouse_code,
            warehouse_name=edit_model.warehouse_name,
            address=edit_model.address,
            manager=edit_model.manager,
            phone=edit_model.phone,
            status=edit_model.status,
            remark=edit_model.remark,
            update_by=getattr(request.state, 'user_name', 'system'),
            update_time=datetime.now()
        )

        result = await WarehouseDao.update_warehouse(db, warehouse)
        await db.commit()

        return CrudResponseModel(is_success=True, message='修改成功') if result > 0 else CrudResponseModel(is_success=False, message='修改失败')

    @classmethod
    async def delete_warehouse(cls, request: Request, db: AsyncSession, warehouse_id: int) -> CrudResponseModel:
        existing = await WarehouseDao.get_warehouse_by_id(db, warehouse_id)
        if not existing:
            return CrudResponseModel(is_success=False, message='仓库不存在')

        update_by = getattr(request.state, 'user_name', 'system')
        result = await WarehouseDao.delete_warehouse(db, warehouse_id, update_by)
        await db.commit()

        return CrudResponseModel(is_success=True, message='删除成功') if result > 0 else CrudResponseModel(is_success=False, message='删除失败')