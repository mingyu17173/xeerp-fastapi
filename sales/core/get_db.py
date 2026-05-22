"""
数据库会话获取器
"""

from typing import Generator
from .database import SessionLocal


def get_db() -> Generator:
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()