# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: gatewayRun.py
# @Software: PyCharm
# @Desc : 模块文件

"""
Gateway Service Runner
网关服务启动器
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    import uvicorn
    from server import app
    from core.env import AppConfig

    uvicorn.run(
        "server:app",
        host=AppConfig.app_host,
        port=AppConfig.app_port,
        reload=True,
        reload_dirs=[os.path.dirname(os.path.abspath(__file__))]
    )