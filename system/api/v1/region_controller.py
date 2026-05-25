# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: region_controller.py
# @Software: PyCharm
# @Desc : 控制器

from datetime import datetime
from fastapi import APIRouter, Depends, Form, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from core.enums import BusinessType
from core.get_db import get_db
from core.annotation.log_annotation import Log
from core.aspect.interface_auth import CheckUserInterfaceAuth
from schemas.user_schema import CurrentUserModel
from service.login_service import LoginService
from service.region_service import RegionService
from schemas.region_schema import DeleteRegionModel, RegionModel, RegionPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


regionController = APIRouter(prefix='/system/region', dependencies=[Depends(LoginService.get_current_user)])


@regionController.get('/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('system:region:list'))])
async def get_system_region_list(
    request: Request,
    region_page_query: RegionPageQueryModel = Depends(RegionPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取分页数据
    region_page_query_result = await RegionService.get_region_list_services(query_db, region_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=region_page_query_result)


@regionController.post('', dependencies=[Depends(CheckUserInterfaceAuth('system:region:add'))])
@ValidateFields(validate_model='add_region')
@Log(title='地区', business_type=BusinessType.INSERT)
async def add_system_region(
    request: Request,
    add_region: RegionModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_region_result = await RegionService.add_region_services(query_db, add_region)
    logger.info(add_region_result.message)

    return ResponseUtil.success(msg=add_region_result.message)


@regionController.put('', dependencies=[Depends(CheckUserInterfaceAuth('system:region:edit'))])
@ValidateFields(validate_model='edit_region')
@Log(title='地区', business_type=BusinessType.UPDATE)
async def edit_system_region(
    request: Request,
    edit_region: RegionModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_region.update_by = current_user.user.user_name
    edit_region.update_time = datetime.now()
    edit_region_result = await RegionService.edit_region_services(query_db, edit_region)
    logger.info(edit_region_result.message)

    return ResponseUtil.success(msg=edit_region_result.message)


@regionController.delete('/{ids}', dependencies=[Depends(CheckUserInterfaceAuth('system:region:remove'))])
@Log(title='地区', business_type=BusinessType.DELETE)
async def delete_system_region(request: Request, ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_region = DeleteRegionModel(ids=ids)
    delete_region_result = await RegionService.delete_region_services(query_db, delete_region)
    logger.info(delete_region_result.message)

    return ResponseUtil.success(msg=delete_region_result.message)


@regionController.get('/{id}', response_model=RegionModel, dependencies=[Depends(CheckUserInterfaceAuth('system:region:query'))])
async def query_detail_system_region(request: Request, id: int, query_db: AsyncSession = Depends(get_db)):
    region_detail_result = await RegionService.region_detail_services(query_db, id)
    logger.info(f'获取id为{id}的信息成功')

    return ResponseUtil.success(data=region_detail_result)


@regionController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('system:region:export'))])
@Log(title='地区', business_type=BusinessType.EXPORT)
async def export_system_region_list(
    request: Request,
    region_page_query: RegionPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    region_query_result = await RegionService.get_region_list_services(query_db, region_page_query, is_page=False)
    region_export_result = await RegionService.export_region_list_services(region_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(region_export_result))
