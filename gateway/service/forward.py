# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: forward.py
# @Software: PyCharm
# @Desc : 业务服务

import httpx
from fastapi import Request, HTTPException
from core.logger import logger
from .discovery import get_service_url
from core.env import config

async def forward_request(request: Request, service: str, path: str):
    if service not in config.service_mapping:
        raise HTTPException(404, "服务不存在")

    base_url = await get_service_url(service)

    if not base_url:
        raise HTTPException(503, f"服务 {service} 不健康")

    target = f"{base_url}/{path}"

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            return await client.request(
                method=request.method,
                url=target,
                headers=dict(request.headers),
                params=request.query_params,
                content=await request.body()
            )
    except Exception as e:
        logger.error(f"转发失败 {target}: {e}")
        raise HTTPException(500, "网关转发失败")