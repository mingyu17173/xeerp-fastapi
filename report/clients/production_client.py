# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: production_client.py
# @Software: PyCharm
# @Desc : 模块文件

from typing import Any, Dict, Optional, Tuple
from clients.base_client import BaseClient
from core.env import AppConfig


class ProductionClient(BaseClient):
    def __init__(self):
        super().__init__(base_url=AppConfig.production_service_url)

    async def get_production_plan_list(self, status: Optional[str] = None) -> Tuple[int, Dict[str, Any]]:
        params = {}
        if status:
            params['status'] = status
        return await self.get('/api/production/plan/list', params=params)

    async def get_production_issue_list(self, status: Optional[str] = None) -> Tuple[int, Dict[str, Any]]:
        params = {}
        if status:
            params['status'] = status
        return await self.get('/api/production/issue/list', params=params)

    async def get_production_receipt_list(self, status: Optional[str] = None) -> Tuple[int, Dict[str, Any]]:
        params = {}
        if status:
            params['status'] = status
        return await self.get('/api/production/receipt/list', params=params)

    async def get_production_return_list(self, status: Optional[str] = None) -> Tuple[int, Dict[str, Any]]:
        params = {}
        if status:
            params['status'] = status
        return await self.get('/api/production/return/list', params=params)

    async def get_production_scrap_list(self, status: Optional[str] = None) -> Tuple[int, Dict[str, Any]]:
        params = {}
        if status:
            params['status'] = status
        return await self.get('/api/production/scrap/list', params=params)