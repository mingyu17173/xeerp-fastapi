# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: handle.py
# @Software: PyCharm
# @Desc : 核心配置

from fastapi import FastAPI
from core.mounts.staticfiles import mount_staticfiles


def handle_sub_applications(app: FastAPI):
    """
    全局处理子应用挂载
    """
    # 挂载静态文件
    mount_staticfiles(app)
