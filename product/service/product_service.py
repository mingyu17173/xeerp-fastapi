# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: product_service.py
# @Software: PyCharm
# @Desc : 业务服务

from datetime import datetime
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Tuple
from dao.product_dao import ProductDao
from models.product import SysProduct
from schemas.common_schema import CrudResponseModel
from schemas.product_schema import (
    AddProductModel,
    DeleteProductModel,
    EditProductModel,
    ProductModel,
    ProductPageQueryModel,
)


class ProductService:
    """
    商品服务类
    """

    @classmethod
    async def get_product_detail_services(
        cls, db: AsyncSession, product_id: int
    ) -> Optional[ProductModel]:
        """
        获取商品详情
        """
        product = await ProductDao.get_product_by_id(db, product_id)
        if product:
            return ProductModel.model_validate(product)
        return None

    @classmethod
    async def get_product_list_services(
        cls, db: AsyncSession, query_model: ProductPageQueryModel
    ) -> Tuple[List[ProductModel], int]:
        """
        获取商品列表（分页）
        """
        products, total = await ProductDao.get_product_list(db, query_model)
        product_models = [ProductModel.model_validate(product) for product in products]
        return product_models, total

    @classmethod
    async def add_product_services(
        cls, request: Request, db: AsyncSession, add_model: AddProductModel
    ) -> CrudResponseModel:
        """
        新增商品
        """
        # 检查商品编码是否已存在
        if await ProductDao.check_product_code_exists(db, add_model.product_code):
            return CrudResponseModel(is_success=False, message=f"商品编码 '{add_model.product_code}' 已存在")

        # 创建商品对象
        product = SysProduct(
            product_name=add_model.product_name,
            product_code=add_model.product_code,
            category_id=add_model.category_id,
            brand_id=add_model.brand_id,
            unit_id=add_model.unit_id,
            description=add_model.description,
            price=add_model.price,
            cost_price=add_model.cost_price,
            stock=add_model.stock,
            status=add_model.status,
            create_by=getattr(request.state, 'user_name', 'system'),
            create_time=datetime.now(),
            remark=add_model.remark,
        )

        # 保存商品
        await ProductDao.add_product(db, product)
        await db.commit()

        return CrudResponseModel(is_success=True, message='新增成功')

    @classmethod
    async def edit_product_services(
        cls, request: Request, db: AsyncSession, edit_model: EditProductModel
    ) -> CrudResponseModel:
        """
        编辑商品
        """
        # 检查商品是否存在
        existing_product = await ProductDao.get_product_by_id(db, edit_model.product_id)
        if not existing_product:
            return CrudResponseModel(is_success=False, message='商品不存在')

        # 检查商品编码是否与其他商品重复
        if await ProductDao.check_product_code_exists(
            db, edit_model.product_code, exclude_id=edit_model.product_id
        ):
            return CrudResponseModel(is_success=False, message=f"商品编码 '{edit_model.product_code}' 已存在")

        # 更新商品对象
        product = SysProduct(
            product_id=edit_model.product_id,
            product_name=edit_model.product_name,
            product_code=edit_model.product_code,
            category_id=edit_model.category_id,
            brand_id=edit_model.brand_id,
            unit_id=edit_model.unit_id,
            description=edit_model.description,
            price=edit_model.price,
            cost_price=edit_model.cost_price,
            stock=edit_model.stock,
            status=edit_model.status,
            update_by=getattr(request.state, 'user_name', 'system'),
            remark=edit_model.remark,
        )

        # 更新商品
        result = await ProductDao.update_product(db, product)
        await db.commit()

        if result > 0:
            return CrudResponseModel(is_success=True, message='修改成功')
        return CrudResponseModel(is_success=False, message='修改失败')

    @classmethod
    async def delete_product_services(
        cls, request: Request, db: AsyncSession, product_id: int
    ) -> CrudResponseModel:
        """
        删除商品
        """
        # 检查商品是否存在
        existing_product = await ProductDao.get_product_by_id(db, product_id)
        if not existing_product:
            return CrudResponseModel(is_success=False, message='商品不存在')

        # 删除商品
        update_by = getattr(request.state, 'user_name', 'system')
        result = await ProductDao.delete_product(db, product_id, update_by)
        await db.commit()

        if result > 0:
            return CrudResponseModel(is_success=True, message='删除成功')
        return CrudResponseModel(is_success=False, message='删除失败')

    @classmethod
    async def batch_delete_product_services(
        cls, request: Request, db: AsyncSession, delete_model: DeleteProductModel
    ) -> CrudResponseModel:
        """
        批量删除商品
        """
        # 解析商品ID列表
        try:
            product_ids = [int(id_str) for id_str in delete_model.product_ids.split(',') if id_str.strip()]
        except ValueError:
            return CrudResponseModel(is_success=False, message='商品ID格式错误')

        if not product_ids:
            return CrudResponseModel(is_success=False, message='请选择要删除的商品')

        # 批量删除商品
        update_by = getattr(request.state, 'user_name', 'system')
        result = await ProductDao.batch_delete_product(db, product_ids, update_by)
        await db.commit()

        if result > 0:
            return CrudResponseModel(is_success=True, message=f'成功删除 {result} 条记录')
        return CrudResponseModel(is_success=False, message='删除失败')