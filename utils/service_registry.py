# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: service_registry.py
# @Software: PyCharm
# @Desc : 业务服务

"""
Service Registry Helper
服务注册助手（基于 Consul）
"""

import atexit
import signal
import sys
from typing import Optional
from utils.consul_util import ConsulUtil, SERVICE_CONFIG

class ServiceRegistry:
    """
    服务注册助手类
    提供统一的服务注册接口，支持自动注销和信号处理
    """
    
    _service_key: Optional[str] = None
    _service_name: Optional[str] = None
    _ip: Optional[str] = None
    _port: Optional[int] = None
    _service_id: Optional[str] = None
    _registered: bool = False
    
    @classmethod
    def register(
        cls, 
        service_key: str, 
        ip: Optional[str] = None, 
        port: Optional[int] = None, 
        required: bool = False
    ) -> bool:
        """
        注册服务到 Consul
        
        Args:
            service_key: 服务配置键（如"system", "product"等）
            ip: 服务IP地址（可选，默认自动获取）
            port: 服务端口（可选，默认从配置读取）
            required: 是否必须注册成功（True则失败会抛出异常）
            
        Returns:
            是否注册成功
        """
        if service_key not in SERVICE_CONFIG:
            print(f"❌ 未知的服务键: {service_key}")
            return False
        
        config = SERVICE_CONFIG[service_key]
        cls._service_key = service_key
        cls._service_name = config["service_name"]
        cls._ip = ip or ConsulUtil.get_local_ip()
        cls._port = port or config["port"]
        
        print(f"🔗 尝试注册服务到 Consul...")
        print(f"   服务名称: {cls._service_name}")
        print(f"   服务地址: {cls._ip}:{cls._port}")
        
        # 注册服务
        success = ConsulUtil.register_service(
            service_name=cls._service_name,
            ip=cls._ip,
            port=cls._port,
            metadata={"description": config["description"]}
        )
        
        if success:
            cls._registered = True
            
            # 获取注册的服务ID（用于注销）
            instances = ConsulUtil.get_service_instances(cls._service_name)
            for inst in instances:
                if inst["ip"] == cls._ip and inst["port"] == cls._port:
                    cls._service_id = inst["service_id"]
                    break
            
            # 注册退出时的注销函数
            atexit.register(cls._deregister_on_exit)
            
            # 注册信号处理
            signal.signal(signal.SIGTERM, cls._signal_handler)
            signal.signal(signal.SIGINT, cls._signal_handler)
            
            return True
        else:
            print(f"⚠️  服务 {cls._service_name} 注册失败（Consul 不可用）")
            print(f"   服务将使用本地配置继续运行")
            
            if required:
                raise RuntimeError(f"服务 {cls._service_name} 注册失败且标记为必须")
            
            return False
    
    @classmethod
    def _deregister_on_exit(cls):
        """
        退出时注销服务
        """
        if cls._registered and cls._service_name and cls._service_id:
            print(f"\n🛑 正在注销服务 {cls._service_name}...")
            ConsulUtil.deregister_service(
                service_name=cls._service_name,
                service_id=cls._service_id
            )
    
    @classmethod
    def _signal_handler(cls, signum, frame):
        """
        信号处理器
        """
        print(f"\n📨 收到信号 {signum}，准备退出...")
        cls._deregister_on_exit()
        sys.exit(0)
    
    @classmethod
    def get_service_info(cls) -> Optional[dict]:
        """
        获取已注册服务的信息
        
        Returns:
            服务信息字典，包含 service_name, ip, port, service_id
        """
        if cls._service_name and cls._ip and cls._port:
            return {
                "service_name": cls._service_name,
                "ip": cls._ip,
                "port": cls._port,
                "service_id": cls._service_id
            }
        return None


def auto_register(service_key: str, ip: Optional[str] = None, port: Optional[int] = None, enabled: bool = True) -> bool:
    """
    自动注册服务的便捷函数
    
    Args:
        service_key: 服务配置键（如"system", "product"等）
        ip: 服务IP地址（可选）
        port: 服务端口（可选）
        enabled: 是否启用 Consul 注册（设为 False 可临时禁用）
        
    Returns:
        是否注册成功
        
    Example:
        from utils.service_registry import auto_register
        
        # 启用注册（默认）
        auto_register("system")
        
        # 禁用注册
        auto_register("system", enabled=False)
    """
    if not enabled:
        print(f"⏭️  Consul 注册已禁用，跳过服务注册")
        return False
    
    return ServiceRegistry.register(service_key, ip, port)


# 初始化 Consul 客户端
# 默认使用本地 Consul，如需连接远程服务器可在启动前调用 ConsulUtil.init_client(host, port)
ConsulUtil.init_client()
