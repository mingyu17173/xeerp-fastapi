# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: unit_service.py
# @Software: PyCharm
# @Desc : 业务服务

from datetime import datetime
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Tuple
from dao.unit_dao import ProductUnitDao
from models.unit import SysProductUnit
from schemas.common_schema import CrudResponseModel
from schemas.unit_schema import (
    AddProductUnitModel,
    DeleteProductUnitModel,
    EditProductUnitModel,
    ProductUnitModel,
    ProductUnitPageQueryModel,
)


class ProductUnitService:
    """
    商品单位服务类
    """

    @classmethod
    async def get_unit_detail_services(
        cls, db: AsyncSession, unit_id: int
    ) -> Optional[ProductUnitModel]:
        """
        获取单位详情
        """
        unit = await ProductUnitDao.get_unit_by_id(db, unit_id)
        if unit:
            return ProductUnitModel.model_validate(unit)
        return None

    @classmethod
    async def get_unit_list_services(
        cls, db: AsyncSession, query_model: ProductUnitPageQueryModel
    ) -> Tuple[List[ProductUnitModel], int]:
        """
        获取单位列表（分页）
        """
        units, total = await ProductUnitDao.get_unit_list(db, query_model)
        unit_models = [ProductUnitModel.model_validate(unit) for unit in units]
        return unit_models, total

    @classmethod
    async def get_all_units_services(cls, db: AsyncSession) -> List[ProductUnitModel]:
        """
        获取所有启用的单位列表
        """
        units = await ProductUnitDao.get_all_units(db)
        return [ProductUnitModel.model_validate(unit) for unit in units]

    @classmethod
    async def add_unit_services(
        cls, request: Request, db: AsyncSession, add_model: AddProductUnitModel
    ) -> CrudResponseModel:
        """
        新增单位
        """
        if await ProductUnitDao.check_unit_code_exists(db, add_model.unit_code):
            return CrudResponseModel(is_success=False, message=f"单位编码 '{add_model.unit_code}' 已存在")

        unit = SysProductUnit(
            unit_name=add_model.unit_name,
            unit_code=add_model.unit_code,
            sort_order=add_model.sort_order,
            status=add_model.status,
            create_by=getattr(request.state, 'user_name', 'system'),
            create_time=datetime.now(),
            remark=add_model.remark,
        )

        await ProductUnitDao.add_unit(db, unit)
        await db.commit()

        return CrudResponseModel(is_success=True, message='新增成功')

    @classmethod
    async def edit_unit_services(
        cls, request: Request, db: AsyncSession, edit_model: EditProductUnitModel
    ) -> CrudResponseModel:
        """
        编辑单位
        """
        existing_unit = await ProductUnitDao.get_unit_by_id(db, edit_model.unit_id)
        if not existing_unit:
            return CrudResponseModel(is_success=False, message='单位不存在')

        if await ProductUnitDao.check_unit_code_exists(
            db, edit_model.unit_code, exclude_id=edit_model.unit_id
        ):
            return CrudResponseModel(is_success=False, message=f"单位编码 '{edit_model.unit_code}' 已存在")

        unit = SysProductUnit(
            unit_id=edit_model.unit_id,
            unit_name=edit_model.unit_name,
            unit_code=edit_model.unit_code,
            sort_order=edit_model.sort_order,
            status=edit_model.status,
            update_by=getattr(request.state, 'user_name', 'system'),
            remark=edit_model.remark,
        )

        result = await ProductUnitDao.update_unit(db, unit)
        await db.commit()

        if result > 0:
            return CrudResponseModel(is_success=True, message='修改成功')
        return CrudResponseModel(is_success=False, message='修改失败')

    @classmethod
    async def delete_unit_services(
        cls, request: Request, db: AsyncSession, unit_id: int
    ) -> CrudResponseModel:
        """
        删除单位
        """
        existing_unit = await ProductUnitDao.get_unit_by_id(db, unit_id)
        if not existing_unit:
            return CrudResponseModel(is_success=False, message='单位不存在')

        update_by = getattr(request.state, 'user_name', 'system')
        result = await ProductUnitDao.delete_unit(db, unit_id, update_by)
        await db.commit()

        if result > 0:
            return CrudResponseModel(is_success=True, message='删除成功')
        return CrudResponseModel(is_success=False, message='删除失败')

    @classmethod
    async def batch_delete_unit_services(
        cls, request: Request, db: AsyncSession, delete_model: DeleteProductUnitModel
    ) -> CrudResponseModel:
        """
        批量删除单位
        """
        try:
            unit_ids = [int(id_str) for id_str in delete_model.unit_ids.split(',') if id_str.strip()]
        except ValueError:
            return CrudResponseModel(is_success=False, message='单位ID格式错误')

        if not unit_ids:
            return CrudResponseModel(is_success=False, message='请选择要删除的单位')

        update_by = getattr(request.state, 'user_name', 'system')
        result = await ProductUnitDao.batch_delete_unit(db, unit_ids, update_by)
        await db.commit()

        if result > 0:
            return CrudResponseModel(is_success=True, message=f'成功删除 {result} 条记录')
        return CrudResponseModel(is_success=False, message='删除失败')