# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: region_dao.py
# @Software: PyCharm
# @Desc : 数据访问层

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from models.region import SysRegion
from schemas.region_schema import RegionModel, RegionPageQueryModel
from utils.page_util import PageUtil


class RegionDao:
    """
    地区模块数据库操作层
    """

    @classmethod
    async def get_region_detail_by_id(cls, db: AsyncSession, id: int):
        """
        根据获取地区详细信息

        :param db: orm对象
        :param id: 
        :return: 地区信息对象
        """
        region_info = (
            (
                await db.execute(
                    select(SysRegion)
                    .where(
                        SysRegion.id == id
                    )
                )
            )
            .scalars()
            .first()
        )

        return region_info

    @classmethod
    async def get_region_detail_by_info(cls, db: AsyncSession, region: RegionModel):
        """
        根据地区参数获取地区信息

        :param db: orm对象
        :param region: 地区参数对象
        :return: 地区信息对象
        """
        region_info = (
            (
                await db.execute(
                    select(SysRegion).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return region_info

    @classmethod
    async def get_region_list(cls, db: AsyncSession, query_object: RegionPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取地区列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 地区列表信息对象
        """
        query = (
            select(SysRegion)
            .where(
                SysRegion.code == query_object.code if query_object.code else True,
                SysRegion.name.like(f'%{query_object.name}%') if query_object.name else True,
                SysRegion.parent_id == (query_object.parent_id if query_object.parent_id is not None else 0),
                SysRegion.level == query_object.level if query_object.level else True,
            )
            .order_by(SysRegion.id)
            .distinct()
        )
        region_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return region_list

    @classmethod
    async def add_region_dao(cls, db: AsyncSession, region: RegionModel):
        """
        新增地区数据库操作

        :param db: orm对象
        :param region: 地区对象
        :return:
        """
        db_region = SysRegion(**region.model_dump(exclude={}))
        db.add(db_region)
        await db.flush()

        return db_region

    @classmethod
    async def edit_region_dao(cls, db: AsyncSession, region: dict):
        """
        编辑地区数据库操作

        :param db: orm对象
        :param region: 需要更新的地区字典
        :return:
        """
        await db.execute(update(SysRegion), [region])

    @classmethod
    async def delete_region_dao(cls, db: AsyncSession, region: RegionModel):
        """
        删除地区数据库操作

        :param db: orm对象
        :param region: 地区对象
        :return:
        """
        await db.execute(delete(SysRegion).where(SysRegion.id.in_([region.id])))

