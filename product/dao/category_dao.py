# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: category_dao.py
# @Software: PyCharm
# @Desc : 数据访问层

from datetime import datetime
from sqlalchemy import and_, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Tuple
from models.category import SysProductCategory
from schemas.category_schema import ProductCategoryPageQueryModel


class ProductCategoryDao:
    """
    商品分类数据访问对象
    """

    @classmethod
    async def get_category_by_id(cls, db: AsyncSession, category_id: int) -> Optional[SysProductCategory]:
        """
        根据ID获取分类
        """
        result = await db.execute(
            select(SysProductCategory).where(
                and_(SysProductCategory.category_id == category_id, SysProductCategory.is_delete == '0')
            )
        )
        return result.scalar_one_or_none()

    @classmethod
    async def get_category_by_code(cls, db: AsyncSession, category_code: str) -> Optional[SysProductCategory]:
        """
        根据编码获取分类
        """
        result = await db.execute(
            select(SysProductCategory).where(
                and_(SysProductCategory.category_code == category_code, SysProductCategory.is_delete == '0')
            )
        )
        return result.scalar_one_or_none()

    @classmethod
    async def get_category_list(
        cls, db: AsyncSession, query_model: ProductCategoryPageQueryModel
    ) -> Tuple[List[SysProductCategory], int]:
        """
        获取分类列表（分页）
        """
        conditions = [SysProductCategory.is_delete == '0']
        
        if query_model.category_name:
            conditions.append(SysProductCategory.category_name.like(f'%{query_model.category_name}%'))
        if query_model.category_code:
            conditions.append(SysProductCategory.category_code.like(f'%{query_model.category_code}%'))
        if query_model.parent_id is not None:
            conditions.append(SysProductCategory.parent_id == query_model.parent_id)
        if query_model.status:
            conditions.append(SysProductCategory.status == query_model.status)

        # 查询总数
        count_result = await db.execute(
            select(func.count(SysProductCategory.category_id)).where(and_(*conditions))
        )
        total = count_result.scalar()

        # 查询数据
        result = await db.execute(
            select(SysProductCategory)
            .where(and_(*conditions))
            .order_by(SysProductCategory.sort_order.asc(), SysProductCategory.create_time.desc())
            .offset((query_model.page_num - 1) * query_model.page_size)
            .limit(query_model.page_size)
        )
        categories = result.scalars().all()

        return list(categories), total

    @classmethod
    async def get_all_categories(cls, db: AsyncSession) -> List[SysProductCategory]:
        """
        获取所有启用的分类列表（不分页）
        """
        result = await db.execute(
            select(SysProductCategory)
            .where(and_(SysProductCategory.is_delete == '0', SysProductCategory.status == '0'))
            .order_by(SysProductCategory.sort_order.asc())
        )
        return list(result.scalars().all())

    @classmethod
    async def get_category_tree(cls, db: AsyncSession, parent_id: Optional[int] = None) -> List[SysProductCategory]:
        """
        获取分类树形结构
        """
        conditions = [SysProductCategory.is_delete == '0', SysProductCategory.status == '0']
        if parent_id is not None:
            conditions.append(SysProductCategory.parent_id == parent_id)
        else:
            conditions.append(SysProductCategory.parent_id.is_(None) | (SysProductCategory.parent_id == 0))
        
        result = await db.execute(
            select(SysProductCategory)
            .where(and_(*conditions))
            .order_by(SysProductCategory.sort_order.asc())
        )
        return list(result.scalars().all())

    @classmethod
    async def get_child_categories(cls, db: AsyncSession, parent_id: int) -> List[SysProductCategory]:
        """
        获取子分类列表
        """
        result = await db.execute(
            select(SysProductCategory)
            .where(and_(SysProductCategory.parent_id == parent_id, SysProductCategory.is_delete == '0'))
            .order_by(SysProductCategory.sort_order.asc())
        )
        return list(result.scalars().all())

    @classmethod
    async def add_category(cls, db: AsyncSession, category: SysProductCategory) -> SysProductCategory:
        """
        新增分类
        """
        db.add(category)
        await db.flush()
        return category

    @classmethod
    async def update_category(cls, db: AsyncSession, category: SysProductCategory) -> int:
        """
        更新分类
        """
        result = await db.execute(
            update(SysProductCategory)
            .where(SysProductCategory.category_id == category.category_id)
            .values(
                parent_id=category.parent_id,
                category_name=category.category_name,
                category_code=category.category_code,
                sort_order=category.sort_order,
                status=category.status,
                update_by=category.update_by,
                update_time=datetime.now(),
                remark=category.remark,
            )
        )
        return result.rowcount

    @classmethod
    async def delete_category(cls, db: AsyncSession, category_id: int, update_by: str) -> int:
        """
        删除分类（逻辑删除）
        """
        result = await db.execute(
            update(SysProductCategory)
            .where(SysProductCategory.category_id == category_id)
            .values(
                is_delete='2',
                update_by=update_by,
                update_time=datetime.now(),
            )
        )
        return result.rowcount

    @classmethod
    async def batch_delete_category(cls, db: AsyncSession, category_ids: List[int], update_by: str) -> int:
        """
        批量删除分类（逻辑删除）
        """
        result = await db.execute(
            update(SysProductCategory)
            .where(SysProductCategory.category_id.in_(category_ids))
            .values(
                is_delete='2',
                update_by=update_by,
                update_time=datetime.now(),
            )
        )
        return result.rowcount

    @classmethod
    async def check_category_code_exists(
        cls, db: AsyncSession, category_code: str, exclude_id: Optional[int] = None
    ) -> bool:
        """
        检查分类编码是否存在
        """
        conditions = [
            SysProductCategory.category_code == category_code,
            SysProductCategory.is_delete == '0'
        ]
        if exclude_id:
            conditions.append(SysProductCategory.category_id != exclude_id)
        
        result = await db.execute(
            select(func.count(SysProductCategory.category_id)).where(and_(*conditions))
        )
        return result.scalar() > 0

    @classmethod
    async def has_children(cls, db: AsyncSession, category_id: int) -> bool:
        """
        检查是否有子分类
        """
        result = await db.execute(
            select(func.count(SysProductCategory.category_id))
            .where(and_(SysProductCategory.parent_id == category_id, SysProductCategory.is_delete == '0'))
        )
        return result.scalar() > 0