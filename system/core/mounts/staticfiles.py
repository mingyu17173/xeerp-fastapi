# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: staticfiles.py
# @Software: PyCharm
# @Desc : 核心配置

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from core.env import UploadConfig


def mount_staticfiles(app: FastAPI):
    """
    挂载静态文件
    """
    app.mount(f'{UploadConfig.UPLOAD_PREFIX}', StaticFiles(directory=f'{UploadConfig.UPLOAD_PATH}'), name='profile')
