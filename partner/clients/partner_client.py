# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: partner_client.py
# @Software: PyCharm
# @Desc : 模块文件

import asyncio
import json
from typing import Any, Dict, Optional, Tuple
import aiohttp
from fastapi import HTTPException


class PartnerClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8007", timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self._session: Optional[aiohttp.ClientSession] = None

    async def get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                timeout=self.timeout,
                headers={
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                }
            )
        return self._session

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()

    async def _request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Tuple[int, Dict[str, Any]]:
        url = f"{self.base_url}/{path.lstrip('/')}"
        session = await self.get_session()

        try:
            async with session.request(
                method=method,
                url=url,
                params=params,
                json=data,
                headers=headers,
            ) as response:
                status_code = response.status
                
                try:
                    response_data = await response.json()
                except json.JSONDecodeError:
                    response_data = {'detail': await response.text()}
                
                return status_code, response_data

        except asyncio.TimeoutError:
            raise HTTPException(
                status_code=504,
                detail=f"请求超时: {url}"
            )
        except aiohttp.ClientError as e:
            raise HTTPException(
                status_code=503,
                detail=f"服务调用失败: {str(e)}"
            )

    async def get_partner(self, partner_id: int) -> Tuple[int, Dict[str, Any]]:
        return await self._request('GET', f'/api/partner/{partner_id}')

    async def get_partner_list(
        self,
        page_num: int = 1,
        page_size: int = 10,
        partner_type: Optional[str] = None
    ) -> Tuple[int, Dict[str, Any]]:
        params = {'page_num': page_num, 'page_size': page_size}
        if partner_type:
            params['partner_type'] = partner_type
        return await self._request('GET', '/api/partner/list', params=params)

    async def get_customers(self) -> Tuple[int, Dict[str, Any]]:
        return await self._request('GET', '/api/partner/customers')

    async def get_suppliers(self) -> Tuple[int, Dict[str, Any]]:
        return await self._request('GET', '/api/partner/suppliers')

    async def add_partner(self, data: Dict[str, Any]) -> Tuple[int, Dict[str, Any]]:
        return await self._request('POST', '/api/partner', data=data)

    async def update_partner(self, data: Dict[str, Any]) -> Tuple[int, Dict[str, Any]]:
        return await self._request('PUT', '/api/partner', data=data)

    async def delete_partner(self, partner_id: int) -> Tuple[int, Dict[str, Any]]:
        return await self._request('DELETE', f'/api/partner/{partner_id}')