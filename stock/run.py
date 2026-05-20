import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    import uvicorn
    from server import app

    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8003,
        reload=True,
        reload_dirs=[os.path.dirname(os.path.abspath(__file__))]
    )