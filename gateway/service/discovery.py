# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: discovery.py
# @Software: PyCharm
# @Desc : 业务服务

from typing import Optional, Dict, List
from utils.consul_util import ConsulUtil
from core.logger import logger
from core.env import config

class ServiceDiscovery:

    @classmethod
    async def get_healthy_instance(
        cls,
        service_alias: str,
        strategy: str = "random"
    ) -> Optional[Dict]:
        """
        根据别名获取【一个健康服务实例】
        例如：system → system-service
        """
        if service_alias not in config.service_mapping:
            logger.error(f"❌ 服务别名不存在: {service_alias}")
            return None

        consul_service = config.service_mapping[service_alias]
        instance = ConsulUtil.discover_service(consul_service, strategy)

        if instance:
            logger.info(f"✅ 发现服务 [{service_alias}] → {instance['ip']}:{instance['port']}")
        return instance

    @classmethod
    async def get_service_url(cls, service_alias: str) -> Optional[str]:
        """获取服务 URL: http://ip:port"""
        instance = await cls.get_healthy_instance(service_alias)
        if not instance:
            return None
        return f"http://{instance['ip']}:{instance['port']}"

    @classmethod
    async def get_all_healthy_instances(cls, service_alias: str) -> List[Dict]:
        """获取某个服务的所有健康实例"""
        if service_alias not in config.service_mapping:
            return []
        consul_service = config.service_mapping[service_alias]
        return ConsulUtil.get_service_instances(consul_service, healthy_only=True)

    @classmethod
    async def get_all_services(cls) -> List[str]:
        """获取Consul里所有服务列表"""
        return ConsulUtil.list_services()


# 快速调用（推荐）
async def get_service_url(service_alias: str) -> Optional[str]:
    return await ServiceDiscovery.get_service_url(service_alias)