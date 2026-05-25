# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: logger.py
# @Software: PyCharm
# @Desc : 核心配置

"""
System Service Logger Configuration
系统服务日志配置
"""

import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils.log_util import setup_logger

# 创建订单服务日志记录器
logger = setup_logger('system')
