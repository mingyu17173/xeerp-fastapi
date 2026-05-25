# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: base_client.py
# @Software: PyCharm
# @Desc : 模块文件

import asyncio
import json
from typing import Any, Dict, Optional, Tuple
import aiohttp
from fastapi import HTTPException


class BaseClient:
    """
    基础 HTTP 客户端类
    封装通用的异步 HTTP 请求逻辑
    """

    def __init__(self, base_url: str, timeout: int = 30):
        """
        初始化客户端
        :param base_url: 目标服务基础 URL
        :param timeout: 请求超时时间（秒）
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self._session: Optional[aiohttp.ClientSession] = None

    async def get_session(self) -> aiohttp.ClientSession:
        """
        获取或创建 HTTP 会话
        """
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
        """
        关闭 HTTP 会话
        """
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
        """
        发起 HTTP 请求
        :param method: HTTP 方法（GET, POST, PUT, DELETE 等）
        :param path: 请求路径
        :param params: URL 参数
        :param data: 请求体数据
        :param headers: 自定义请求头
        :return: (状态码, 响应数据)
        """
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

    async def get(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Tuple[int, Dict[str, Any]]:
        """
        发起 GET 请求
        """
        return await self._request('GET', path, params=params, headers=headers)

    async def post(
        self,
        path: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Tuple[int, Dict[str, Any]]:
        """
        发起 POST 请求
        """
        return await self._request('POST', path, params=params, data=data, headers=headers)

    async def put(
        self,
        path: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Tuple[int, Dict[str, Any]]:
        """
        发起 PUT 请求
        """
        return await self._request('PUT', path, params=params, data=data, headers=headers)

    async def delete(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Tuple[int, Dict[str, Any]]:
        """
        发起 DELETE 请求
        """
        return await self._request('DELETE', path, params=params, headers=headers)