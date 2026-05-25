# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: cache_Route.py
# @Software: PyCharm
# @Desc : 缓存控制器

from fastapi import APIRouter, Depends, Request
from typing import List
from core.aspect.interface_auth import CheckUserInterfaceAuth
from schemas.cache_schema import CacheInfoModel, CacheMonitorModel
from service.cache_service import CacheService
from service.login_service import LoginService
from common.utils.log_util import logger
from common.utils.response_util import ResponseUtil


cacheRoute = APIRouter(prefix='/monitor/cache', dependencies=[Depends(LoginService.get_current_user)])

@cacheRoute.get(
    '', 
    response_model=CacheMonitorModel, 
    dependencies=[Depends(CheckUserInterfaceAuth('monitor:cache:list'))]
)
async def get_monitor_cache_info(request: Request):
    # 获取全量数据
    cache_info_query_result = await CacheService.get_cache_monitor_statistical_info_services(request)
    logger.info('获取成功')
    return ResponseUtil.success(data=cache_info_query_result)


@cacheRoute.get(
    '/getNames',
    response_model=List[CacheInfoModel],
    dependencies=[Depends(CheckUserInterfaceAuth('monitor:cache:list'))],
)
async def get_monitor_cache_name(request: Request):
    # 获取全量数据
    cache_name_list_result = await CacheService.get_cache_monitor_cache_name_services()
    logger.info('获取成功')
    return ResponseUtil.success(data=cache_name_list_result)


@cacheRoute.get(
    '/getKeys/{cache_name}',
    response_model=List[str],
    dependencies=[Depends(CheckUserInterfaceAuth('monitor:cache:list'))],
)
async def get_monitor_cache_key(request: Request, cache_name: str):
    # 获取全量数据
    cache_key_list_result = await CacheService.get_cache_monitor_cache_key_services(request, cache_name)
    logger.info('获取成功')

    return ResponseUtil.success(data=cache_key_list_result)


@cacheRoute.get(
    '/getValue/{cache_name}/{cache_key}',
    response_model=CacheInfoModel,
    dependencies=[Depends(CheckUserInterfaceAuth('monitor:cache:list'))],
)
async def get_monitor_cache_value(request: Request, cache_name: str, cache_key: str):
    # 获取全量数据
    cache_value_list_result = await CacheService.get_cache_monitor_cache_value_services(request, cache_name, cache_key)
    logger.info('获取成功')
    return ResponseUtil.success(data=cache_value_list_result)


@cacheRoute.delete(
    '/clearCacheName/{cache_name}', 
    dependencies=[Depends(CheckUserInterfaceAuth('monitor:cache:list'))]
)
async def clear_monitor_cache_name(request: Request, cache_name: str):
    clear_cache_name_result = await CacheService.clear_cache_monitor_cache_name_services(request, cache_name)
    logger.info(clear_cache_name_result.message)
    return ResponseUtil.success(msg=clear_cache_name_result.message)


@cacheRoute.delete(
    '/clearCacheKey/{cache_key}',
    dependencies=[Depends(CheckUserInterfaceAuth('monitor:cache:list'))]
)
async def clear_monitor_cache_key(request: Request, cache_key: str):
    clear_cache_key_result = await CacheService.clear_cache_monitor_cache_key_services(request, cache_key)
    logger.info(clear_cache_key_result.message)
    return ResponseUtil.success(msg=clear_cache_key_result.message)


@cacheRoute.delete(
    '/clearCacheAll',
    dependencies=[Depends(CheckUserInterfaceAuth('monitor:cache:list'))]
)
async def clear_monitor_cache_all(request: Request):
    clear_cache_all_result = await CacheService.clear_cache_monitor_all_services(request)
    logger.info(clear_cache_all_result.message)
    return ResponseUtil.success(msg=clear_cache_all_result.message)
