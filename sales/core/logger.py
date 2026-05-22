"""
Sales Service Logger Configuration
销售服务日志配置
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils.log_util import setup_logger

logger = setup_logger('sales')