# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: __init__.py
# @Software: PyCharm
# @Desc : 中间件

from fastapi import FastAPI
from .ctx import TraceCtx
from .middle import TraceASGIMiddleware

__all__ = ('TraceASGIMiddleware', 'TraceCtx')

__version__ = '0.1.0'


def add_trace_middleware(app: FastAPI):
    """
    添加trace中间件

    :param app: FastAPI对象
    :return:
    """
    app.add_middleware(TraceASGIMiddleware)
