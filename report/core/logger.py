# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: logger.py
# @Software: PyCharm
# @Desc : 核心配置

"""
Report Service Logger Configuration
报表服务日志配置
"""

import sys
import os

# 获取当前文件的绝对路径
current_file = os.path.abspath(__file__)
# 向上三级目录：report/core/logger.py -> report/core -> report -> XEERP-FASTAPI
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
# 确保路径唯一添加
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from utils.log_util import setup_logger

# 创建报表服务日志记录器
logger = setup_logger('report')
