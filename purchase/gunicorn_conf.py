# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: gunicorn_conf.py
# @Software: PyCharm
# @Desc : 模块文件

# =================================================
# Gunicorn + Uvicorn 生产配置文件
# 适用于：FastAPI 微服务 / system-service 所有服务
# 支持：MySQL / PostgreSQL / JWT / 高并发 / 自动重启 / 防卡死
# Windows 不支持 gunicorn，仅 Linux 使用
# =================================================

import multiprocessing
import os

# =============== 1. 服务绑定地址 ===============
bind = f"0.0.0.0:{os.getenv('PORT', '8001')}"

# =============== 2. 工作进程配置（最重要）===============
# 进程数：CPU核心数 * 2（企业标准）
workers = multiprocessing.cpu_count() * 2

# 最大并发连接（高并发可调 2000）
worker_connections = 1000

# =============== 3. ASGI 异步配置（必须）===============
# 使用 Uvicorn 异步 Worker（支持 FastAPI）
worker_class = "uvicorn.workers.UvicornWorker"

# 【关键】Windows 不支持 uvloop，所以强制使用 asyncio
# 全平台兼容，永不报错
loop = "asyncio"

# =============== 4. 自动重启 / 防卡死（生产必备）===============
# 超时：30秒没响应自动重启（防卡死）
timeout = 30

# 优雅重启超时
graceful_timeout = 30

# 长连接保持
keepalive = 5

# 每个 worker 处理 50000 请求后自动重启（防内存泄漏）
max_requests = 50000
max_requests_jitter = 1000  # 随机抖动，避免同时重启

# =============== 5. 日志配置 ===============
# 日志级别
loglevel = "warning"

# 关闭访问日志（减少IO，生产更稳）
accesslog = None

# 错误日志输出到控制台
errorlog = "-"

# =============== 6. 安全配置 ===============
# 限制最大请求头大小
limit_request_line = 4094
limit_request_fields = 100

# =============== 7. 进程名称 ===============
proc_name = "system_service"

# =============== 8. 工作目录 ===============
chdir = "/app"