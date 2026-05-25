# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: scheduler_test.py
# @Software: PyCharm
# @Desc : 模块文件

from datetime import datetime


def job(*args, **kwargs):
    """
    定时任务执行同步函数示例
    """
    print(args)
    print(kwargs)
    print(f'{datetime.now()}同步函数执行了')


async def async_job(*args, **kwargs):
    """
    定时任务执行异步函数示例
    """
    print(args)
    print(kwargs)
    print(f'{datetime.now()}异步函数执行了')
