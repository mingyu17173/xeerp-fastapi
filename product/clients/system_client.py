# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: system_client.py
# @Software: PyCharm
# @Desc : 模块文件

from typing import Any, Dict, Optional, Tuple, List
from clients.base_client import BaseClient
from core.env import AppConfig


class SystemClient(BaseClient):
    """
    系统服务客户端
    封装对 system-service 的 API 调用
    """

    def __init__(self):
        """
        初始化系统服务客户端
        从配置中获取系统服务地址
        """
        # 从配置或环境变量获取系统服务地址
        system_base_url = 'http://127.0.0.1:8001' if AppConfig.app_env == 'dev' else 'http://xeapp-system-service:8001'
        super().__init__(base_url=system_base_url)

    async def get_user_info(self, user_id: int) -> Tuple[int, Dict[str, Any]]:
        """
        获取用户信息
        :param user_id: 用户ID
        :return: 用户信息
        """
        return await self.get(f'/api/user/{user_id}')

    async def get_user_list(
        self,
        page_num: int = 1,
        page_size: int = 10,
        user_name: Optional[str] = None
    ) -> Tuple[int, Dict[str, Any]]:
        """
        获取用户列表
        :param page_num: 页码
        :param page_size: 每页数量
        :param user_name: 用户名（可选）
        :return: 用户列表
        """
        params = {
            'page_num': page_num,
            'page_size': page_size,
        }
        if user_name:
            params['user_name'] = user_name
        return await self.get('/api/user/list', params=params)

    async def get_role_info(self, role_id: int) -> Tuple[int, Dict[str, Any]]:
        """
        获取角色信息
        :param role_id: 角色ID
        :return: 角色信息
        """
        return await self.get(f'/api/role/{role_id}')

    async def get_dept_info(self, dept_id: int) -> Tuple[int, Dict[str, Any]]:
        """
        获取部门信息
        :param dept_id: 部门ID
        :return: 部门信息
        """
        return await self.get(f'/api/dept/{dept_id}')

    async def validate_token(self, token: str) -> Tuple[int, Dict[str, Any]]:
        """
        验证 Token 有效性
        :param token: JWT Token
        :return: 验证结果
        """
        headers = {'Authorization': f'Bearer {token}'}
        return await self.get('/api/auth/validate', headers=headers)

    async def get_config_by_key(self, config_key: str) -> Tuple[int, Dict[str, Any]]:
        """
        获取系统配置
        :param config_key: 配置键
        :return: 配置值
        """
        return await self.get(f'/api/config/{config_key}')

    async def batch_get_users(self, user_ids: List[int]) -> Tuple[int, Dict[str, Any]]:
        """
        批量获取用户信息
        :param user_ids: 用户ID列表
        :return: 用户信息列表
        """
        return await self.post('/api/user/batch', data={'user_ids': user_ids})