"""
Gateway Nacos Service Discovery
网关Nacos服务发现模块
"""

from typing import Dict, Optional
from utils.nacos_util import NacosUtil

class NacosServiceDiscovery:
    """
    Nacos服务发现
    """
    _instance_cache: Dict[str, str] = {}
    _nacos_enabled: bool = False
    
    @classmethod
    def enable(cls, enabled: bool = True):
        """
        启用/禁用Nacos服务发现
        """
        cls._nacos_enabled = enabled
    
    @classmethod
    def is_enabled(cls) -> bool:
        """
        检查是否启用Nacos
        """
        return cls._nacos_enabled
    
    @classmethod
    def get_service_url(cls, service_name: str) -> Optional[str]:
        """
        获取服务URL
        
        Args:
            service_name: 服务名称
            
        Returns:
            服务URL，例如: http://127.0.0.1:8001
        """
        if not cls._nacos_enabled:
            return None
        
        # 检查缓存
        if service_name in cls._instance_cache:
            return cls._instance_cache[service_name]
        
        # 从Nacos获取服务实例
        try:
            instances = NacosUtil.get_service_instances(service_name)
            
            if not instances:
                print(f"⚠️ 服务 {service_name} 无可用实例")
                return None
            
            # 选择第一个健康的实例
            for instance in instances:
                if instance.get('healthy', False) and instance.get('enabled', True):
                    ip = instance.get('ip')
                    port = instance.get('port')
                    url = f"http://{ip}:{port}"
                    
                    # 缓存服务URL
                    cls._instance_cache[service_name] = url
                    
                    print(f"✅ 从Nacos获取服务 {service_name}: {url}")
                    return url
            
            print(f"⚠️ 服务 {service_name} 无健康实例")
            return None
        
        except Exception as e:
            print(f"❌ 获取服务 {service_name} 失败: {str(e)}")
            return None
    
    @classmethod
    def clear_cache(cls):
        """
        清除服务缓存
        """
        cls._instance_cache.clear()
        print("🗑️ 服务缓存已清除")
    
    @classmethod
    def get_service_url_with_fallback(
        cls,
        service_name: str,
        fallback_url: str
    ) -> str:
        """
        获取服务URL，支持降级
        
        Args:
            service_name: 服务名称
            fallback_url: 降级URL
            
        Returns:
            服务URL
        """
        if cls._nacos_enabled:
            url = cls.get_service_url(service_name)
            if url:
                return url
            print(f"⚠️ Nacos获取失败，使用降级URL: {fallback_url}")
        
        return fallback_url