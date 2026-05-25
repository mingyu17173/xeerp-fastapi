# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: logger.py
# @Software: PyCharm
# @Desc : 核心配置

"""
Sales Service Logger Configuration
销售服务日志配置
"""

import sys
import os

# 获取当前文件的绝对路径
current_file = os.path.abspath(__file__)
# 向上三级目录：sales/core/logger.py -> sales/core -> sales -> XEERP-FASTAPI
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
# 确保路径唯一添加
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from utils.log_util import setup_logger

# 创建销售服务日志记录器
logger = setup_logger('sales')
