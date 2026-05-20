"""
Production Service Logger Configuration
生产服务日志配置
"""

import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils.log_util import setup_logger

# 创建生产服务日志记录器
logger = setup_logger('production')
