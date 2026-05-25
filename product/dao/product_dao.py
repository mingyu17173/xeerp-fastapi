# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: product_dao.py
# @Software: PyCharm
# @Desc : 数据访问层

from datetime import datetime
from sqlalchemy import and_, delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Tuple
from models.product import SysProduct
from schemas.product_schema import ProductPageQueryModel


class ProductDao:
    """
    商品数据访问对象
    """

    @classmethod
    async def get_product_by_id(cls, db: AsyncSession, product_id: int) -> Optional[SysProduct]:
        """
        根据ID获取商品
        """
        result = await db.execute(
            select(SysProduct).where(
                and_(SysProduct.product_id == product_id, SysProduct.is_delete == '0')
            )
        )
        return result.scalar_one_or_none()

    @classmethod
    async def get_product_by_code(cls, db: AsyncSession, product_code: str) -> Optional[SysProduct]:
        """
        根据编码获取商品
        """
        result = await db.execute(
            select(SysProduct).where(
                and_(SysProduct.product_code == product_code, SysProduct.is_delete == '0')
            )
        )
        return result.scalar_one_or_none()

    @classmethod
    async def get_product_list(
        cls, db: AsyncSession, query_model: ProductPageQueryModel
    ) -> Tuple[List[SysProduct], int]:
        """
        获取商品列表（分页）
        """
        # 构建查询条件
        conditions = [SysProduct.is_delete == '0']
        
        if query_model.product_name:
            conditions.append(SysProduct.product_name.like(f'%{query_model.product_name}%'))
        if query_model.product_code:
            conditions.append(SysProduct.product_code.like(f'%{query_model.product_code}%'))
        if query_model.category_id:
            conditions.append(SysProduct.category_id == query_model.category_id)
        if query_model.brand_id:
            conditions.append(SysProduct.brand_id == query_model.brand_id)
        if query_model.unit_id:
            conditions.append(SysProduct.unit_id == query_model.unit_id)
        if query_model.status:
            conditions.append(SysProduct.status == query_model.status)

        # 查询总数
        count_result = await db.execute(
            select(func.count(SysProduct.product_id)).where(and_(*conditions))
        )
        total = count_result.scalar()

        # 查询数据
        result = await db.execute(
            select(SysProduct)
            .where(and_(*conditions))
            .order_by(SysProduct.create_time.desc())
            .offset((query_model.page_num - 1) * query_model.page_size)
            .limit(query_model.page_size)
        )
        products = result.scalars().all()

        return list(products), total

    @classmethod
    async def add_product(cls, db: AsyncSession, product: SysProduct) -> SysProduct:
        """
        新增商品
        """
        db.add(product)
        await db.flush()
        return product

    @classmethod
    async def update_product(cls, db: AsyncSession, product: SysProduct) -> int:
        """
        更新商品
        """
        result = await db.execute(
            update(SysProduct)
            .where(SysProduct.product_id == product.product_id)
            .values(
                product_name=product.product_name,
                product_code=product.product_code,
                category_id=product.category_id,
                brand_id=product.brand_id,
                unit_id=product.unit_id,
                description=product.description,
                price=product.price,
                cost_price=product.cost_price,
                stock=product.stock,
                status=product.status,
                update_by=product.update_by,
                update_time=datetime.now(),
                remark=product.remark,
            )
        )
        return result.rowcount

    @classmethod
    async def delete_product(cls, db: AsyncSession, product_id: int, update_by: str) -> int:
        """
        删除商品（逻辑删除）
        """
        result = await db.execute(
            update(SysProduct)
            .where(SysProduct.product_id == product_id)
            .values(
                is_delete='2',
                update_by=update_by,
                update_time=datetime.now(),
            )
        )
        return result.rowcount

    @classmethod
    async def batch_delete_product(cls, db: AsyncSession, product_ids: List[int], update_by: str) -> int:
        """
        批量删除商品（逻辑删除）
        """
        result = await db.execute(
            update(SysProduct)
            .where(SysProduct.product_id.in_(product_ids))
            .values(
                is_delete='2',
                update_by=update_by,
                update_time=datetime.now(),
            )
        )
        return result.rowcount

    @classmethod
    async def check_product_code_exists(
        cls, db: AsyncSession, product_code: str, exclude_id: Optional[int] = None
    ) -> bool:
        """
        检查商品编码是否存在
        """
        conditions = [
            SysProduct.product_code == product_code,
            SysProduct.is_delete == '0'
        ]
        if exclude_id:
            conditions.append(SysProduct.product_id != exclude_id)
        
        result = await db.execute(
            select(func.count(SysProduct.product_id)).where(and_(*conditions))
        )
        return result.scalar() > 0