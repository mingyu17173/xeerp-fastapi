# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: brand_service.py
# @Software: PyCharm
# @Desc : 业务服务

from datetime import datetime
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Tuple
from dao.brand_dao import ProductBrandDao
from models.brand import SysProductBrand
from schemas.brand_schema import (
    AddProductBrandModel,
    DeleteProductBrandModel,
    EditProductBrandModel,
    ProductBrandModel,
    ProductBrandPageQueryModel,
)
from schemas.common_schema import CrudResponseModel


class ProductBrandService:
    """
    商品品牌服务类
    """

    @classmethod
    async def get_brand_detail_services(
        cls, db: AsyncSession, brand_id: int
    ) -> Optional[ProductBrandModel]:
        """
        获取品牌详情
        """
        brand = await ProductBrandDao.get_brand_by_id(db, brand_id)
        if brand:
            return ProductBrandModel.model_validate(brand)
        return None

    @classmethod
    async def get_brand_list_services(
        cls, db: AsyncSession, query_model: ProductBrandPageQueryModel
    ) -> Tuple[List[ProductBrandModel], int]:
        """
        获取品牌列表（分页）
        """
        brands, total = await ProductBrandDao.get_brand_list(db, query_model)
        brand_models = [ProductBrandModel.model_validate(brand) for brand in brands]
        return brand_models, total

    @classmethod
    async def get_all_brands_services(cls, db: AsyncSession) -> List[ProductBrandModel]:
        """
        获取所有启用的品牌列表
        """
        brands = await ProductBrandDao.get_all_brands(db)
        return [ProductBrandModel.model_validate(brand) for brand in brands]

    @classmethod
    async def add_brand_services(
        cls, request: Request, db: AsyncSession, add_model: AddProductBrandModel
    ) -> CrudResponseModel:
        """
        新增品牌
        """
        if await ProductBrandDao.check_brand_code_exists(db, add_model.brand_code):
            return CrudResponseModel(is_success=False, message=f"品牌编码 '{add_model.brand_code}' 已存在")

        brand = SysProductBrand(
            brand_name=add_model.brand_name,
            brand_code=add_model.brand_code,
            brand_logo=add_model.brand_logo,
            sort_order=add_model.sort_order,
            status=add_model.status,
            create_by=getattr(request.state, 'user_name', 'system'),
            create_time=datetime.now(),
            remark=add_model.remark,
        )

        await ProductBrandDao.add_brand(db, brand)
        await db.commit()

        return CrudResponseModel(is_success=True, message='新增成功')

    @classmethod
    async def edit_brand_services(
        cls, request: Request, db: AsyncSession, edit_model: EditProductBrandModel
    ) -> CrudResponseModel:
        """
        编辑品牌
        """
        existing_brand = await ProductBrandDao.get_brand_by_id(db, edit_model.brand_id)
        if not existing_brand:
            return CrudResponseModel(is_success=False, message='品牌不存在')

        if await ProductBrandDao.check_brand_code_exists(
            db, edit_model.brand_code, exclude_id=edit_model.brand_id
        ):
            return CrudResponseModel(is_success=False, message=f"品牌编码 '{edit_model.brand_code}' 已存在")

        brand = SysProductBrand(
            brand_id=edit_model.brand_id,
            brand_name=edit_model.brand_name,
            brand_code=edit_model.brand_code,
            brand_logo=edit_model.brand_logo,
            sort_order=edit_model.sort_order,
            status=edit_model.status,
            update_by=getattr(request.state, 'user_name', 'system'),
            remark=edit_model.remark,
        )

        result = await ProductBrandDao.update_brand(db, brand)
        await db.commit()

        if result > 0:
            return CrudResponseModel(is_success=True, message='修改成功')
        return CrudResponseModel(is_success=False, message='修改失败')

    @classmethod
    async def delete_brand_services(
        cls, request: Request, db: AsyncSession, brand_id: int
    ) -> CrudResponseModel:
        """
        删除品牌
        """
        existing_brand = await ProductBrandDao.get_brand_by_id(db, brand_id)
        if not existing_brand:
            return CrudResponseModel(is_success=False, message='品牌不存在')

        update_by = getattr(request.state, 'user_name', 'system')
        result = await ProductBrandDao.delete_brand(db, brand_id, update_by)
        await db.commit()

        if result > 0:
            return CrudResponseModel(is_success=True, message='删除成功')
        return CrudResponseModel(is_success=False, message='删除失败')

    @classmethod
    async def batch_delete_brand_services(
        cls, request: Request, db: AsyncSession, delete_model: DeleteProductBrandModel
    ) -> CrudResponseModel:
        """
        批量删除品牌
        """
        try:
            brand_ids = [int(id_str) for id_str in delete_model.brand_ids.split(',') if id_str.strip()]
        except ValueError:
            return CrudResponseModel(is_success=False, message='品牌ID格式错误')

        if not brand_ids:
            return CrudResponseModel(is_success=False, message='请选择要删除的品牌')

        update_by = getattr(request.state, 'user_name', 'system')
        result = await ProductBrandDao.batch_delete_brand(db, brand_ids, update_by)
        await db.commit()

        if result > 0:
            return CrudResponseModel(is_success=True, message=f'成功删除 {result} 条记录')
        return CrudResponseModel(is_success=False, message='删除失败')