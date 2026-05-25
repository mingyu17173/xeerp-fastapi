# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: run.py
# @Software: PyCharm
# @Desc : 模块文件

"""
服务启动脚本
"""

import os
import sys

# 设置环境变量
os.environ.setdefault("SERVICE_NAME", "approval-service")

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from server import app
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8006,
        reload=True,
        workers=1
    )