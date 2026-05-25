# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: brand_dao.py
# @Software: PyCharm
# @Desc : 数据访问层

from datetime import datetime
from sqlalchemy import and_, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Tuple
from models.brand import SysProductBrand
from schemas.brand_schema import ProductBrandPageQueryModel


class ProductBrandDao:
    """
    商品品牌数据访问对象
    """

    @classmethod
    async def get_brand_by_id(cls, db: AsyncSession, brand_id: int) -> Optional[SysProductBrand]:
        """
        根据ID获取品牌
        """
        result = await db.execute(
            select(SysProductBrand).where(
                and_(SysProductBrand.brand_id == brand_id, SysProductBrand.is_delete == '0')
            )
        )
        return result.scalar_one_or_none()

    @classmethod
    async def get_brand_by_code(cls, db: AsyncSession, brand_code: str) -> Optional[SysProductBrand]:
        """
        根据编码获取品牌
        """
        result = await db.execute(
            select(SysProductBrand).where(
                and_(SysProductBrand.brand_code == brand_code, SysProductBrand.is_delete == '0')
            )
        )
        return result.scalar_one_or_none()

    @classmethod
    async def get_brand_list(
        cls, db: AsyncSession, query_model: ProductBrandPageQueryModel
    ) -> Tuple[List[SysProductBrand], int]:
        """
        获取品牌列表（分页）
        """
        conditions = [SysProductBrand.is_delete == '0']
        
        if query_model.brand_name:
            conditions.append(SysProductBrand.brand_name.like(f'%{query_model.brand_name}%'))
        if query_model.brand_code:
            conditions.append(SysProductBrand.brand_code.like(f'%{query_model.brand_code}%'))
        if query_model.status:
            conditions.append(SysProductBrand.status == query_model.status)

        # 查询总数
        count_result = await db.execute(
            select(func.count(SysProductBrand.brand_id)).where(and_(*conditions))
        )
        total = count_result.scalar()

        # 查询数据
        result = await db.execute(
            select(SysProductBrand)
            .where(and_(*conditions))
            .order_by(SysProductBrand.sort_order.asc(), SysProductBrand.create_time.desc())
            .offset((query_model.page_num - 1) * query_model.page_size)
            .limit(query_model.page_size)
        )
        brands = result.scalars().all()

        return list(brands), total

    @classmethod
    async def get_all_brands(cls, db: AsyncSession) -> List[SysProductBrand]:
        """
        获取所有启用的品牌列表（不分页）
        """
        result = await db.execute(
            select(SysProductBrand)
            .where(and_(SysProductBrand.is_delete == '0', SysProductBrand.status == '0'))
            .order_by(SysProductBrand.sort_order.asc())
        )
        return list(result.scalars().all())

    @classmethod
    async def add_brand(cls, db: AsyncSession, brand: SysProductBrand) -> SysProductBrand:
        """
        新增品牌
        """
        db.add(brand)
        await db.flush()
        return brand

    @classmethod
    async def update_brand(cls, db: AsyncSession, brand: SysProductBrand) -> int:
        """
        更新品牌
        """
        result = await db.execute(
            update(SysProductBrand)
            .where(SysProductBrand.brand_id == brand.brand_id)
            .values(
                brand_name=brand.brand_name,
                brand_code=brand.brand_code,
                brand_logo=brand.brand_logo,
                sort_order=brand.sort_order,
                status=brand.status,
                update_by=brand.update_by,
                update_time=datetime.now(),
                remark=brand.remark,
            )
        )
        return result.rowcount

    @classmethod
    async def delete_brand(cls, db: AsyncSession, brand_id: int, update_by: str) -> int:
        """
        删除品牌（逻辑删除）
        """
        result = await db.execute(
            update(SysProductBrand)
            .where(SysProductBrand.brand_id == brand_id)
            .values(
                is_delete='2',
                update_by=update_by,
                update_time=datetime.now(),
            )
        )
        return result.rowcount

    @classmethod
    async def batch_delete_brand(cls, db: AsyncSession, brand_ids: List[int], update_by: str) -> int:
        """
        批量删除品牌（逻辑删除）
        """
        result = await db.execute(
            update(SysProductBrand)
            .where(SysProductBrand.brand_id.in_(brand_ids))
            .values(
                is_delete='2',
                update_by=update_by,
                update_time=datetime.now(),
            )
        )
        return result.rowcount

    @classmethod
    async def check_brand_code_exists(
        cls, db: AsyncSession, brand_code: str, exclude_id: Optional[int] = None
    ) -> bool:
        """
        检查品牌编码是否存在
        """
        conditions = [
            SysProductBrand.brand_code == brand_code,
            SysProductBrand.is_delete == '0'
        ]
        if exclude_id:
            conditions.append(SysProductBrand.brand_id != exclude_id)
        
        result = await db.execute(
            select(func.count(SysProductBrand.brand_id)).where(and_(*conditions))
        )
        return result.scalar() > 0