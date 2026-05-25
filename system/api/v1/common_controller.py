# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: common_Route.py
# @Software: PyCharm
# @Desc : 控制器

from fastapi import APIRouter, BackgroundTasks, Depends, File, Query, Request, UploadFile
from service.common_service import CommonService
from service.login_service import LoginService
from common.utils.log_util import logger
from common.utils.response_util import ResponseUtil


commonRoute = APIRouter(prefix='/common', dependencies=[Depends(LoginService.get_current_user)])

@commonRoute.post('/upload')
async def common_upload(request: Request, file: UploadFile = File(...)):
    upload_result = await CommonService.upload_service(request, file)
    logger.info('上传成功')

    return ResponseUtil.success(model_content=upload_result.result)


@commonRoute.get('/download')
async def common_download(
    request: Request,
    background_tasks: BackgroundTasks,
    file_name: str = Query(alias='fileName'),
    delete: bool = Query(),
):
    download_result = await CommonService.download_services(background_tasks, file_name, delete)
    logger.info(download_result.message)

    return ResponseUtil.streaming(data=download_result.result)


@commonRoute.get('/download/resource')
async def common_download_resource(request: Request, resource: str = Query()):
    download_resource_result = await CommonService.download_resource_services(resource)
    logger.info(download_resource_result.message)

    return ResponseUtil.streaming(data=download_resource_result.result)
