# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: auth_client.py
# @Software: PyCharm
# @Desc : 模块文件

from typing import Any, Dict, Optional, Tuple
from clients.base_client import BaseClient
from core.env import AppConfig


class AuthClient(BaseClient):
    """
    认证服务客户端
    封装对认证服务的 API 调用
    """

    def __init__(self):
        """
        初始化认证服务客户端
        """
        auth_base_url = 'http://127.0.0.1:8001' if AppConfig.app_env == 'dev' else 'http://xeapp-system-service:8001'
        super().__init__(base_url=auth_base_url)

    async def login(self, username: str, password: str) -> Tuple[int, Dict[str, Any]]:
        """
        用户登录
        :param username: 用户名
        :param password: 密码
        :return: 登录结果（包含 token）
        """
        data = {
            'username': username,
            'password': password
        }
        return await self.post('/api/login', data=data)

    async def logout(self, token: str) -> Tuple[int, Dict[str, Any]]:
        """
        用户退出登录
        :param token: 用户 Token
        :return: 退出结果
        """
        headers = {'Authorization': f'Bearer {token}'}
        return await self.post('/api/logout', headers=headers)

    async def refresh_token(self, refresh_token: str) -> Tuple[int, Dict[str, Any]]:
        """
        刷新 Token
        :param refresh_token: 刷新 Token
        :return: 新的 Token
        """
        data = {'refresh_token': refresh_token}
        return await self.post('/api/refresh', data=data)

    async def get_current_user(self, token: str) -> Tuple[int, Dict[str, Any]]:
        """
        获取当前登录用户信息
        :param token: 用户 Token
        :return: 用户信息
        """
        headers = {'Authorization': f'Bearer {token}'}
        return await self.get('/api/current/user', headers=headers)