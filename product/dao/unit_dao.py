# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: unit_dao.py
# @Software: PyCharm
# @Desc : 数据访问层

from datetime import datetime
from sqlalchemy import and_, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Tuple
from models.unit import SysProductUnit
from schemas.unit_schema import ProductUnitPageQueryModel


class ProductUnitDao:
    """
    商品单位数据访问对象
    """

    @classmethod
    async def get_unit_by_id(cls, db: AsyncSession, unit_id: int) -> Optional[SysProductUnit]:
        """
        根据ID获取单位
        """
        result = await db.execute(
            select(SysProductUnit).where(
                and_(SysProductUnit.unit_id == unit_id, SysProductUnit.is_delete == '0')
            )
        )
        return result.scalar_one_or_none()

    @classmethod
    async def get_unit_by_code(cls, db: AsyncSession, unit_code: str) -> Optional[SysProductUnit]:
        """
        根据编码获取单位
        """
        result = await db.execute(
            select(SysProductUnit).where(
                and_(SysProductUnit.unit_code == unit_code, SysProductUnit.is_delete == '0')
            )
        )
        return result.scalar_one_or_none()

    @classmethod
    async def get_unit_list(
        cls, db: AsyncSession, query_model: ProductUnitPageQueryModel
    ) -> Tuple[List[SysProductUnit], int]:
        """
        获取单位列表（分页）
        """
        conditions = [SysProductUnit.is_delete == '0']
        
        if query_model.unit_name:
            conditions.append(SysProductUnit.unit_name.like(f'%{query_model.unit_name}%'))
        if query_model.unit_code:
            conditions.append(SysProductUnit.unit_code.like(f'%{query_model.unit_code}%'))
        if query_model.status:
            conditions.append(SysProductUnit.status == query_model.status)

        # 查询总数
        count_result = await db.execute(
            select(func.count(SysProductUnit.unit_id)).where(and_(*conditions))
        )
        total = count_result.scalar()

        # 查询数据
        result = await db.execute(
            select(SysProductUnit)
            .where(and_(*conditions))
            .order_by(SysProductUnit.sort_order.asc(), SysProductUnit.create_time.desc())
            .offset((query_model.page_num - 1) * query_model.page_size)
            .limit(query_model.page_size)
        )
        units = result.scalars().all()

        return list(units), total

    @classmethod
    async def get_all_units(cls, db: AsyncSession) -> List[SysProductUnit]:
        """
        获取所有启用的单位列表（不分页）
        """
        result = await db.execute(
            select(SysProductUnit)
            .where(and_(SysProductUnit.is_delete == '0', SysProductUnit.status == '0'))
            .order_by(SysProductUnit.sort_order.asc())
        )
        return list(result.scalars().all())

    @classmethod
    async def add_unit(cls, db: AsyncSession, unit: SysProductUnit) -> SysProductUnit:
        """
        新增单位
        """
        db.add(unit)
        await db.flush()
        return unit

    @classmethod
    async def update_unit(cls, db: AsyncSession, unit: SysProductUnit) -> int:
        """
        更新单位
        """
        result = await db.execute(
            update(SysProductUnit)
            .where(SysProductUnit.unit_id == unit.unit_id)
            .values(
                unit_name=unit.unit_name,
                unit_code=unit.unit_code,
                sort_order=unit.sort_order,
                status=unit.status,
                update_by=unit.update_by,
                update_time=datetime.now(),
                remark=unit.remark,
            )
        )
        return result.rowcount

    @classmethod
    async def delete_unit(cls, db: AsyncSession, unit_id: int, update_by: str) -> int:
        """
        删除单位（逻辑删除）
        """
        result = await db.execute(
            update(SysProductUnit)
            .where(SysProductUnit.unit_id == unit_id)
            .values(
                is_delete='2',
                update_by=update_by,
                update_time=datetime.now(),
            )
        )
        return result.rowcount

    @classmethod
    async def batch_delete_unit(cls, db: AsyncSession, unit_ids: List[int], update_by: str) -> int:
        """
        批量删除单位（逻辑删除）
        """
        result = await db.execute(
            update(SysProductUnit)
            .where(SysProductUnit.unit_id.in_(unit_ids))
            .values(
                is_delete='2',
                update_by=update_by,
                update_time=datetime.now(),
            )
        )
        return result.rowcount

    @classmethod
    async def check_unit_code_exists(
        cls, db: AsyncSession, unit_code: str, exclude_id: Optional[int] = None
    ) -> bool:
        """
        检查单位编码是否存在
        """
        conditions = [
            SysProductUnit.unit_code == unit_code,
            SysProductUnit.is_delete == '0'
        ]
        if exclude_id:
            conditions.append(SysProductUnit.unit_id != exclude_id)
        
        result = await db.execute(
            select(func.count(SysProductUnit.unit_id)).where(and_(*conditions))
        )
        return result.scalar() > 0