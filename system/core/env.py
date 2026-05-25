# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: env.py
# @Software: PyCharm
# @Desc : 核心配置

"""
Core 模块导入统一封装
将 system_env 中的配置重新导出，方便 from core.env import 风格的导入
"""
from core.system_env import (
    AppConfig,
    AppSettings,
    JwtConfig,
    JwtSettings,
    DataBaseConfig,
    DataBaseSettings,
    RedisConfig,
    RedisSettings,
    GenConfig,
    GenSettings,
    UploadConfig,
    UploadSettings,
    CachePathConfig,
    get_config,
)

__all__ = [
    "AppConfig",
    "AppSettings",
    "JwtConfig",
    "JwtSettings",
    "DataBaseConfig",
    "DataBaseSettings",
    "RedisConfig",
    "RedisSettings",
    "GenConfig",
    "GenSettings",
    "UploadConfig",
    "UploadSettings",
    "CachePathConfig",
    "get_config",
]
