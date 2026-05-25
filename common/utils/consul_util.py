# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: consul_util.py
# @Software: PyCharm
# @Desc : 工具类

"""
Consul 服务注册与发现工具类
基于 python-consul 库实现微服务注册、发现和健康检查
"""

import socket
import random
from typing import Optional, List, Dict, Any
import consul
from consul import Check
from utils.log_util import logger

class ConsulUtil:
    """
    Consul 服务注册与发现工具类
    采用单例模式，避免重复创建连接
    """
    
    _client = None
    _host = "127.0.0.1"
    _port = 8500
    _registered_services: Dict[str, dict] = {}
    
    @classmethod
    def init_client(cls, host: str = "127.0.0.1", port: int = 8500) -> bool:
        """
        初始化 Consul 客户端
        
        Args:
            host: Consul 服务器地址
            port: Consul 服务器端口
            
        Returns:
            是否初始化成功
        """
        try:
            cls._host = host
            cls._port = port
            cls._client = consul.Consul(host=host, port=port)
            
            # 测试连接
            cls._client.agent.self()
            logger.info(f"✅ Consul 客户端初始化成功：http://{host}:{port}")
            return True
        except Exception as e:
            logger.error(f"✅ Consul 客户端初始化失败：{str(e)}")
            return False
    
    @classmethod
    def get_client(cls):
        """获取 Consul 客户端实例"""
        if cls._client is None:
            cls.init_client()
        return cls._client
    
    @classmethod
    def get_local_ip(cls) -> str:
        """
        获取本地 IPv4 地址
        
        Returns:
            本地 IP 地址，失败返回 127.0.0.1
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.connect(("8.8.8.8", 80))
            ip = sock.getsockname()[0]
            sock.close()
            return ip
        except Exception:
            try:
                # 备用方案：获取所有网卡地址
                hostname = socket.gethostname()
                return socket.gethostbyname(hostname)
            except Exception:
                return "127.0.0.1"
    
    @classmethod
    def register_service(
        cls,
        service_name: str,
        ip: Optional[str] = None,
        port: int = 8000,
        service_id: Optional[str] = None,
        cluster_name: str = "DEFAULT",
        weight: float = 1.0,
        metadata: Optional[dict] = None,
        health_check_path: str = "/health",
        health_check_interval: str = "10s",
        health_check_timeout: str = "5s",
        deregister_after: str = "30s"
    ) -> bool:
        """
        注册服务到 Consul
        
        Args:
            service_name: 服务名称
            ip: 服务 IP 地址（可选，默认自动获取）
            port: 服务端口
            service_id: 服务唯一标识（可选，默认自动生成）
            cluster_name: 集群名称
            weight: 权重（用于负载均衡）
            metadata: 元数据
            health_check_path: 健康检查路径
            health_check_interval: 健康检查间隔
            health_check_timeout: 健康检查超时时间
            deregister_after: 服务失效后自动注销时间
            
        Returns:
            是否注册成功
        """
        try:
            client = cls.get_client()
            if not client:
                return False
            
            local_ip = ip or cls.get_local_ip()
            service_id = service_id or f"{service_name}-{local_ip}-{port}"
            
            # 构建健康检查 URL
            health_url = f"http://{local_ip}:{port}{health_check_path}"
            
            # 构建元数据
            tags = [cluster_name, f"weight={weight}"]
            if metadata:
                for key, value in metadata.items():
                    tags.append(f"{key}={value}")
            
            # 注册服务
            client.agent.service.register(
                name=service_name,
                service_id=service_id,
                address=local_ip,
                port=port,
                tags=tags,
                check=Check.http(
                    url=health_url,
                    interval=health_check_interval,
                    timeout=health_check_timeout
                )
            )
            
            # 记录已注册的服务
            cls._registered_services[service_name] = {
                "service_id": service_id,
                "ip": local_ip,
                "port": port
            }
            logger.info(f"✅ 服务 {service_name} 注册成功: {local_ip}:{port}")
            return True
            
        except Exception as e:
            logger.error(f"❌ 服务 {service_name} 注册失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    @classmethod
    def deregister_service(cls, service_name: str, service_id: Optional[str] = None) -> bool:
        """
        从 Consul 注销服务
        
        Args:
            service_name: 服务名称
            service_id: 服务 ID（可选，如果不提供则从已注册服务中查找）
            
        Returns:
            是否注销成功
        """
        try:
            client = cls.get_client()
            if not client:
                return False
            
            # 获取服务 ID
            target_service_id = service_id
            if not target_service_id and service_name in cls._registered_services:
                target_service_id = cls._registered_services[service_name]["service_id"]
            
            if not target_service_id:
                logger.info(f"⚠️  未找到服务 {service_name} 的注册信息")
                return False
            
            client.agent.service.deregister(target_service_id)
            
            # 从已注册列表中移除
            if service_name in cls._registered_services:
                del cls._registered_services[service_name]

            logger.info(f"✅ 服务 {service_name} 注销成功")
            return True
            
        except Exception as e:
            logger.error(f"❌ 服务 {service_name} 注销失败: {str(e)}")
            return False
    
    @classmethod
    def get_service_instances(cls, service_name: str, healthy_only: bool = True) -> List[dict]:
        """
        获取服务的所有实例
        
        Args:
            service_name: 服务名称
            healthy_only: 是否只返回健康实例
            
        Returns:
            实例列表，每个实例包含 ip, port, healthy, metadata 等信息
        """
        instances = []
        
        try:
            client = cls.get_client()
            if not client:
                return instances
            
            _, services = client.health.service(
                service=service_name,
                passing=healthy_only
            )
            
            for service in services:
                instance = {
                    "ip": service["Service"]["Address"],
                    "port": service["Service"]["Port"],
                    "service_id": service["Service"]["ID"],
                    "service_name": service["Service"]["Service"],
                    "healthy": service["Checks"][0]["Status"] == "passing" if service["Checks"] else False,
                    "metadata": cls._parse_tags(service["Service"].get("Tags", []))
                }
                instances.append(instance)
            
        except Exception as e:
            logger.error(f"❌ 获取服务实例失败: {str(e)}")
        
        return instances
    
    @classmethod
    def discover_service(cls, service_name: str, strategy: str = "random") -> Optional[dict]:
        """
        发现服务实例（支持负载均衡策略）
        
        Args:
            service_name: 服务名称
            strategy: 负载均衡策略（random-随机, round-robin-轮询, weight-权重）
            
        Returns:
            选中的服务实例信息
        """
        instances = cls.get_service_instances(service_name, healthy_only=True)
        
        if not instances:
            logger.error(f"⚠️  未找到健康的 {service_name} 服务实例")
            return None
        
        if strategy == "random":
            return random.choice(instances)
        
        elif strategy == "round_robin":
            # 简单轮询实现
            if not hasattr(cls, '_round_robin_index'):
                cls._round_robin_index = {}
            
            idx = cls._round_robin_index.get(service_name, 0)
            selected = instances[idx % len(instances)]
            cls._round_robin_index[service_name] = idx + 1
            return selected
        
        elif strategy == "weight":
            # 基于权重的选择（需要在 tags 中设置 weight=x）
            total_weight = sum(
                float(inst["metadata"].get("weight", "1.0")) 
                for inst in instances
            )
            
            if total_weight <= 0:
                return random.choice(instances)
            
            random_val = random.uniform(0, total_weight)
            current_sum = 0
            
            for inst in instances:
                weight = float(inst["metadata"].get("weight", "1.0"))
                current_sum += weight
                if current_sum >= random_val:
                    return inst
            
            return instances[0]
        
        else:
            return instances[0]
    
    @classmethod
    def list_services(cls) -> List[str]:
        """
        获取所有已注册的服务名称
        
        Returns:
            服务名称列表
        """
        try:
            client = cls.get_client()
            if not client:
                return []
            
            _, services = client.catalog.services()
            return list(services.keys())
        
        except Exception as e:
            logger.error(f"❌ 获取服务列表失败: {str(e)}")
            return []
    
    @classmethod
    def get_health_status(cls, service_name: str) -> Dict[str, str]:
        """
        获取服务的健康状态
        
        Args:
            service_name: 服务名称
            
        Returns:
            服务 ID 到健康状态的映射
        """
        status = {}
        
        try:
            client = cls.get_client()
            if not client:
                return status
            
            _, checks = client.health.checks(service_name)
            
            for check in checks:
                status[check["ServiceID"]] = check["Status"]
            
        except Exception as e:
            logger.error(f"❌ 获取健康状态失败: {str(e)}")
        
        return status
    
    @classmethod
    def set_config(cls, key: str, value: str) -> bool:
        """
        设置配置到 Consul KV 存储
        
        Args:
            key: 配置键
            value: 配置值
            
        Returns:
            是否设置成功
        """
        try:
            client = cls.get_client()
            if not client:
                return False
            
            client.kv.put(key, value)
            return True
            
        except Exception as e:
            logger.error(f"❌ 设置配置失败: {str(e)}")
            return False
    
    @classmethod
    def get_config(cls, key: str) -> Optional[str]:
        """
        从 Consul KV 存储获取配置
        
        Args:
            key: 配置键
            
        Returns:
            配置值，如果不存在返回 None
        """
        try:
            client = cls.get_client()
            if not client:
                return None
            
            _, data = client.kv.get(key)
            return data["Value"].decode('utf-8') if data else None
            
        except Exception as e:
            logger.error(f"❌ 获取配置失败: {str(e)}")
            return None
    
    @classmethod
    def _parse_tags(cls, tags: List[str]) -> Dict[str, str]:
        """
        解析 Consul 服务标签为字典
        
        Args:
            tags: 标签列表，格式为 ["key1=value1", "key2=value2"]
            
        Returns:
            解析后的字典
        """
        metadata = {}
        for tag in tags:
            if '=' in tag:
                key, value = tag.split('=', 1)
                metadata[key] = value
            else:
                metadata[tag] = ""
        return metadata


# 服务配置映射
SERVICE_CONFIG = {
    "system": {
        "service_name": "system-service",
        "port": 8001,
        "description": "系统服务"
    },
    "product": {
        "service_name": "product-service",
        "port": 8002,
        "description": "商品服务"
    },
    "stock": {
        "service_name": "stock-service",
        "port": 8003,
        "description": "库存服务"
    },
    "production": {
        "service_name": "production-service",
        "port": 8004,
        "description": "生产服务"
    },
    "report": {
        "service_name": "report-service",
        "port": 8005,
        "description": "报表服务"
    },
    "approval": {
        "service_name": "approval-service",
        "port": 8006,
        "description": "审批流服务"
    },
    "partner": {
        "service_name": "partner-service",
        "port": 8007,
        "description": "往来单位服务"
    },
    "order": {
        "service_name": "order-service",
        "port": 8008,
        "description": "订单中心服务"
    },
    "purchase": {
        "service_name": "purchase-service",
        "port": 8009,
        "description": "采购中心服务"
    },
    "gateway": {
        "service_name": "gateway-service",
        "port": 8000,
        "description": "网关服务"
    }
}
