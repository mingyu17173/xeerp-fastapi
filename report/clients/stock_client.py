# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: stock_client.py
# @Software: PyCharm
# @Desc : 模块文件

from typing import Any, Dict, Optional, Tuple
from clients.base_client import BaseClient
from core.env import AppConfig


class StockClient(BaseClient):
    def __init__(self):
        super().__init__(base_url=AppConfig.stock_service_url)

    async def get_inventory_list(self, page_num: int = 1, page_size: int = 100) -> Tuple[int, Dict[str, Any]]:
        params = {'page_num': page_num, 'page_size': page_size}
        return await self.get('/api/stock/inventory/list', params=params)

    async def get_warehouse_list(self) -> Tuple[int, Dict[str, Any]]:
        return await self.get('/api/warehouse/list')

    async def get_inventory_flow_list(
        self,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None
    ) -> Tuple[int, Dict[str, Any]]:
        params = {}
        if start_time:
            params['start_time'] = start_time
        if end_time:
            params['end_time'] = end_time
        return await self.get('/api/stock/flow/list', params=params)