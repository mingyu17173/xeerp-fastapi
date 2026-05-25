# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: product_client.py
# @Software: PyCharm
# @Desc : 模块文件

from typing import Any, Dict, Optional, Tuple, List
from clients.base_client import BaseClient
from core.env import AppConfig


class ProductClient(BaseClient):
    """
    商品服务客户端
    封装对 product-service 的 API 调用
    """

    def __init__(self):
        """
        初始化商品服务客户端
        从配置中获取商品服务地址
        """
        product_base_url = 'http://127.0.0.1:8002' if AppConfig.app_env == 'dev' else 'http://xeapp-product-service:8002'
        super().__init__(base_url=product_base_url)

    async def get_product_info(self, product_id: int) -> Tuple[int, Dict[str, Any]]:
        """
        获取商品详情
        :param product_id: 商品ID
        :return: 商品信息
        """
        return await self.get(f'/api/product/{product_id}')

    async def get_product_list(
        self,
        page_num: int = 1,
        page_size: int = 10,
        product_name: Optional[str] = None,
        product_code: Optional[str] = None,
    ) -> Tuple[int, Dict[str, Any]]:
        """
        获取商品列表
        :param page_num: 页码
        :param page_size: 每页数量
        :param product_name: 商品名称（可选）
        :param product_code: 商品编码（可选）
        :return: 商品列表
        """
        params = {
            'page_num': page_num,
            'page_size': page_size,
        }
        if product_name:
            params['product_name'] = product_name
        if product_code:
            params['product_code'] = product_code
        return await self.get('/api/product/list', params=params)

    async def add_product(self, product_data: Dict[str, Any]) -> Tuple[int, Dict[str, Any]]:
        """
        新增商品
        :param product_data: 商品数据
        :return: 新增结果
        """
        return await self.post('/api/product', data=product_data)

    async def update_product(self, product_id: int, product_data: Dict[str, Any]) -> Tuple[int, Dict[str, Any]]:
        """
        更新商品
        :param product_id: 商品ID
        :param product_data: 商品数据
        :return: 更新结果
        """
        return await self.put(f'/api/product/{product_id}', data=product_data)

    async def delete_product(self, product_id: int) -> Tuple[int, Dict[str, Any]]:
        """
        删除商品
        :param product_id: 商品ID
        :return: 删除结果
        """
        return await self.delete(f'/api/product/{product_id}')

    async def get_category_list(self) -> Tuple[int, Dict[str, Any]]:
        """
        获取商品分类列表
        :return: 分类列表
        """
        return await self.get('/api/product/category/list')

    async def get_category_tree(self) -> Tuple[int, Dict[str, Any]]:
        """
        获取商品分类树形结构
        :return: 分类树
        """
        return await self.get('/api/product/category/tree')

    async def get_brand_list(self) -> Tuple[int, Dict[str, Any]]:
        """
        获取商品品牌列表
        :return: 品牌列表
        """
        return await self.get('/api/product/brand/list')

    async def get_unit_list(self) -> Tuple[int, Dict[str, Any]]:
        """
        获取商品单位列表
        :return: 单位列表
        """
        return await self.get('/api/product/unit/list')

    async def batch_get_products(self, product_ids: List[int]) -> Tuple[int, Dict[str, Any]]:
        """
        批量获取商品信息
        :param product_ids: 商品ID列表
        :return: 商品信息列表
        """
        return await self.post('/api/product/batch', data={'product_ids': product_ids})

    async def get_product_count(self) -> Tuple[int, Dict[str, Any]]:
        """
        获取商品总数
        :return: 商品数量
        """
        return await self.get('/api/product/count')