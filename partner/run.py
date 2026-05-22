"""
服务启动脚本
"""

import os
import sys

os.environ.setdefault("SERVICE_NAME", "partner-service")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from server import app
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8007,
        reload=True,
        workers=1
    )