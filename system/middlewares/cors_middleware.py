# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: cors_middleware.py
# @Software: PyCharm
# @Desc : 中间件

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def add_cors_middleware(app: FastAPI):
    """
    添加跨域中间件

    :param app: FastAPI对象
    :return:
    """
    # 前端页面url
    origins = [
        'http://localhost:9080',
        'http://127.0.0.1:9080',
    ]

    # 后台api允许跨域
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
