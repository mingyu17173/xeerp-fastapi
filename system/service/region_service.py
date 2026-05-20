from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from core.exception import ServiceException
from schemas.common_schema import CrudResponseModel
from dao.region_dao import RegionDao
from schemas.region_schema import DeleteRegionModel, RegionModel, RegionPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class RegionService:
    """
    地区模块服务层
    """

    @classmethod
    async def get_region_list_services(
        cls, query_db: AsyncSession, query_object: RegionPageQueryModel, is_page: bool = False
    ):
        """
        获取地区列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 地区列表信息对象
        """
        region_list_result = await RegionDao.get_region_list(query_db, query_object, is_page)

        return region_list_result


    @classmethod
    async def add_region_services(cls, query_db: AsyncSession, page_object: RegionModel):
        """
        新增地区信息service

        :param query_db: orm对象
        :param page_object: 新增地区对象
        :return: 新增地区校验结果
        """
        try:
            await RegionDao.add_region_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_region_services(cls, query_db: AsyncSession, page_object: RegionModel):
        """
        编辑地区信息service

        :param query_db: orm对象
        :param page_object: 编辑地区对象
        :return: 编辑地区校验结果
        """
        edit_region = page_object.model_dump(exclude_unset=True, exclude={})
        region_info = await cls.region_detail_services(query_db, page_object.id)
        if region_info.id:
            try:
                await RegionDao.edit_region_dao(query_db, edit_region)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='地区不存在')

    @classmethod
    async def delete_region_services(cls, query_db: AsyncSession, page_object: DeleteRegionModel):
        """
        删除地区信息service

        :param query_db: orm对象
        :param page_object: 删除地区对象
        :return: 删除地区校验结果
        """
        if page_object.ids:
            id_list = page_object.ids.split(',')
            try:
                for id in id_list:
                    await RegionDao.delete_region_dao(query_db, RegionModel(id=id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入为空')

    @classmethod
    async def region_detail_services(cls, query_db: AsyncSession, id: int):
        """
        获取地区详细信息service

        :param query_db: orm对象
        :param id: 
        :return: 对应的信息
        """
        region = await RegionDao.get_region_detail_by_id(query_db, id=id)
        if region:
            result = RegionModel(**CamelCaseUtil.transform_result(region))
        else:
            result = RegionModel(**dict())

        return result

    @staticmethod
    async def export_region_list_services(region_list: List):
        """
        导出地区信息service

        :param region_list: 地区信息列表
        :return: 地区信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'id': '',
            'code': '统计用区划代码',
            'name': '名称',
            'parentId': '父级',
            'level': '级别',
        }
        binary_data = ExcelUtil.export_list2excel(region_list, mapping_dict)

        return binary_data
