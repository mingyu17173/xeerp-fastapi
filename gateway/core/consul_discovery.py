# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: consul_discovery.py
# @Software: PyCharm
# @Desc : 核心配置

"""
Gateway Consul Service Discovery
网关Consul服务发现模块
"""

import time
from typing import Dict, Optional, List
from utils.consul_util import ConsulUtil, SERVICE_CONFIG

class ConsulServiceDiscovery:
    """
    Consul服务发现
    支持服务缓存、负载均衡和降级策略
    """
    _instance_cache: Dict[str, str] = {}
    _cache_timestamp: Dict[str, float] = {}
    _cache_ttl: int = 30  # 缓存有效期（秒）
    
    @classmethod
    def init_consul(cls, host: str = "127.0.0.1", port: int = 8500) -> bool:
        """
        初始化Consul客户端
        
        Args:
            host: Consul服务器地址
            port: Consul服务器端口
            
        Returns:
            是否初始化成功
        """
        return ConsulUtil.init_client(host, port)
    
    @classmethod
    def is_consul_available(cls) -> bool:
        """
        检查Consul是否可用
        """
        try:
            client = ConsulUtil.get_client()
            if client:
                client.agent.self()
                return True
            return False
        except Exception:
            return False
    
    @classmethod
    def get_service_url(cls, service_name: str, strategy: str = "round_robin") -> Optional[str]:
        """
        获取服务URL（带缓存）
        
        Args:
            service_name: 服务名称
            strategy: 负载均衡策略（random/round_robin/weight）
            
        Returns:
            服务URL，例如: http://127.0.0.1:8001
        """
        # 检查缓存是否有效
        if service_name in cls._instance_cache:
            age = time.time() - cls._cache_timestamp.get(service_name, 0)
            if age < cls._cache_ttl:
                return cls._instance_cache[service_name]
        
        # 从Consul获取服务实例
        try:
            instance = ConsulUtil.discover_service(service_name, strategy=strategy)
            
            if not instance:
                print(f"⚠️ 服务 {service_name} 无可用实例")
                # 返回缓存（如果存在）
                return cls._instance_cache.get(service_name)
            
            ip = instance.get('ip')
            port = instance.get('port')
            url = f"http://{ip}:{port}"
            
            # 更新缓存
            cls._instance_cache[service_name] = url
            cls._cache_timestamp[service_name] = time.time()
            
            print(f"✅ 从Consul获取服务 {service_name}: {url}")
            return url
        
        except Exception as e:
            print(f"❌ 获取服务 {service_name} 失败: {str(e)}")
            # 返回缓存（如果存在）
            return cls._instance_cache.get(service_name)
    
    @classmethod
    def get_service_url_with_fallback(cls, service_name: str, fallback_url: str) -> str:
        """
        获取服务URL，支持降级
        
        Args:
            service_name: 服务名称
            fallback_url: 降级URL
            
        Returns:
            服务URL
        """
        if cls.is_consul_available():
            url = cls.get_service_url(service_name)
            if url:
                return url
            print(f"⚠️ Consul获取失败，使用降级URL: {fallback_url}")
        
        return fallback_url
    
    @classmethod
    def refresh_all_services(cls):
        """
        刷新所有服务缓存
        """
        cls._instance_cache.clear()
        cls._cache_timestamp.clear()
        print("🗑️ 服务缓存已清除")
    
    @classmethod
    def get_all_services(cls) -> Dict[str, str]:
        """
        获取所有服务的URL映射
        
        Returns:
            服务名称到URL的映射
        """
        services = {}
        for key, config in SERVICE_CONFIG.items():
            service_name = config["service_name"]
            url = cls.get_service_url(service_name)
            if url:
                services[service_name] = url
        return services
    
    @classmethod
    def get_service_instances(cls, service_name: str) -> List[dict]:
        """
        获取服务的所有实例
        
        Args:
            service_name: 服务名称
            
        Returns:
            实例列表
        """
        return ConsulUtil.get_service_instances(service_name)
    
    @classmethod
    def list_all_services(cls) -> List[str]:
        """
        获取所有已注册的服务名称
        
        Returns:
            服务名称列表
        """
        return ConsulUtil.list_services()