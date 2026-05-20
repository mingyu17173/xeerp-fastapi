import os
import sys

# 添加项目根目录到 Python 路径，确保能加载 .env 和 utils 模块
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from fastapi import FastAPI
import uvicorn
from server import app, AppConfig


if __name__ == "__main__":
    uvicorn.run(
        app='run:app',
        host=AppConfig.app_host,
        port=AppConfig.app_port,
        root_path=AppConfig.app_root_path,
        reload=AppConfig.app_reload,
        reload_dirs=[os.path.join(os.path.dirname(__file__), 'api')],
    )