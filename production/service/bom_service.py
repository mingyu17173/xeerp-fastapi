# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: bom_service.py
# @Software: PyCharm
# @Desc : 业务服务

from datetime import datetime
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from dao.bom_dao import BomDao
from models.bom import SysBom, SysBomItem
from schemas.common_schema import CrudResponseModel, PageResponseModel
from schemas.bom_schema import BomModel, AddBomModel, EditBomModel, BomPageQueryModel

class BomService:
    @classmethod
    async def get_bom_detail(cls, db: AsyncSession, bom_id: int) -> Optional[BomModel]:
        bom = await BomDao.get_bom_by_id(db, bom_id)
        if bom:
            return BomModel.model_validate(bom)
        return None

    @classmethod
    async def get_bom_list(cls, db: AsyncSession, query_model: BomPageQueryModel) -> PageResponseModel:
        boms, total = await BomDao.get_bom_list(db, query_model)
        bom_models = [BomModel.model_validate(b) for b in boms]
        return PageResponseModel(
            rows=bom_models,
            total=total,
            page_num=query_model.page_num,
            page_size=query_model.page_size
        )

    @classmethod
    async def add_bom(cls, request: Request, db: AsyncSession, add_model: AddBomModel) -> CrudResponseModel:
        bom = SysBom(
            product_id=add_model.product_id,
            product_name=add_model.product_name,
            version=add_model.version,
            status=add_model.status,
            remark=add_model.remark,
            create_by=getattr(request.state, 'user_name', 'system'),
            create_time=datetime.now()
        )

        for item in add_model.items:
            bom_item = SysBomItem(
                material_id=item['material_id'],
                material_name=item.get('material_name'),
                unit=item.get('unit'),
                quantity=item['quantity'],
                scrap_rate=item.get('scrap_rate', 0),
                remark=item.get('remark')
            )
            bom.items.append(bom_item)

        await BomDao.add_bom(db, bom)
        await db.commit()
        return CrudResponseModel(is_success=True, message='新增成功')

    @classmethod
    async def edit_bom(cls, request: Request, db: AsyncSession, edit_model: EditBomModel) -> CrudResponseModel:
        existing = await BomDao.get_bom_by_id(db, edit_model.bom_id)
        if not existing:
            return CrudResponseModel(is_success=False, message='BOM不存在')

        await BomDao.delete_bom_items(db, edit_model.bom_id)

        bom = SysBom(
            bom_id=edit_model.bom_id,
            product_id=edit_model.product_id,
            product_name=edit_model.product_name,
            version=edit_model.version,
            status=edit_model.status,
            remark=edit_model.remark,
            update_by=getattr(request.state, 'user_name', 'system'),
            update_time=datetime.now()
        )

        for item in edit_model.items:
            bom_item = SysBomItem(
                material_id=item['material_id'],
                material_name=item.get('material_name'),
                unit=item.get('unit'),
                quantity=item['quantity'],
                scrap_rate=item.get('scrap_rate', 0),
                remark=item.get('remark')
            )
            bom.items.append(bom_item)

        await BomDao.update_bom(db, bom)
        await db.commit()
        return CrudResponseModel(is_success=True, message='修改成功')

    @classmethod
    async def delete_bom(cls, request: Request, db: AsyncSession, bom_id: int) -> CrudResponseModel:
        existing = await BomDao.get_bom_by_id(db, bom_id)
        if not existing:
            return CrudResponseModel(is_success=False, message='BOM不存在')

        update_by = getattr(request.state, 'user_name', 'system')
        result = await BomDao.delete_bom(db, bom_id, update_by)
        await db.commit()

        return CrudResponseModel(is_success=True, message='删除成功') if result > 0 else CrudResponseModel(is_success=False, message='删除失败')