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