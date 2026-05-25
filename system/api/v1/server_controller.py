# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: server_Route.py
# @Software: PyCharm
# @Desc : 控制器

from fastapi import APIRouter, Depends, Request
from core.aspect.interface_auth import CheckUserInterfaceAuth
from schemas.server_schema import ServerMonitorModel
from service.login_service import LoginService
from service.server_service import ServerService
from common.utils.response_util import ResponseUtil
from common.utils.log_util import logger


serverRoute = APIRouter(
    prefix='/monitor/server', 
    dependencies=[Depends(LoginService.get_current_user)]
)

@serverRoute.get(
    '', 
    response_model=ServerMonitorModel, 
    dependencies=[Depends(CheckUserInterfaceAuth('monitor:server:list'))]
)
async def get_monitor_server_info(request: Request):
    # 获取全量数据
    server_info_query_result = await ServerService.get_server_monitor_info()
    logger.info('获取成功')

    return ResponseUtil.success(data=server_info_query_result)
