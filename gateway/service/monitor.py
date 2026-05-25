# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: monitor.py
# @Software: PyCharm
# @Desc : 业务服务

import asyncio
import subprocess
import sys
from core.logger import logger
from utils.consul_util import ConsulUtil
from core.env import config

SERVICE_PATH = {
    "system-service": "system/system.py",
    "product-service": "product/product.py",
    "stock-service": "stock/stock.py",
    "sales-service": "sales/sales.py",
    "production-service": "production/production.py",
    "partner-service": "partner/partner.py",
    "report-service": "report/report.py",
}

status_cache = {}

async def restart_service(svc: str):
    if svc not in SERVICE_PATH:
        return
    logger.error(f"🔴 服务 {svc} 已下线 → 自动重启")
    try:
        path = SERVICE_PATH[svc]
        if sys.platform == "win32":
            subprocess.Popen(f"start cmd /k python {path}", shell=True)
        else:
            subprocess.Popen(f"nohup python {path} > logs/{svc}.log 2>&1 &", shell=True)
        logger.info(f"🟢 {svc} 重启成功")
    except:
        logger.error(f"🔴 {svc} 重启失败")

async def check_all_services():
    while True:
        try:
            _, services = ConsulUtil.catalog.services()
            for svc in services:
                if svc in ["consul"]:
                    continue
                _, nodes = ConsulUtil.health.service(svc, passing=True)
                if not nodes:
                    if status_cache.get(svc, True):
                        await restart_service(svc)
                    status_cache[svc] = False
                else:
                    status_cache[svc] = True
        except:
            pass
        await asyncio.sleep(10)