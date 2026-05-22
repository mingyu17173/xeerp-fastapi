"""
微服务注册与发现集成测试
测试所有微服务的注册、发现和健康检查功能
"""

import pytest
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from unittest.mock import Mock, patch
from utils.consul_util import ConsulUtil, SERVICE_CONFIG
from utils.service_registry import ServiceRegistry, auto_register


# 模拟健康检查服务器
class MockHealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status": "UP"}')
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass  # 禁用日志输出


class TestMicroServiceRegistry:
    """微服务注册与发现集成测试"""

    @pytest.fixture
    def mock_consul_client(self):
        """模拟 Consul 客户端"""
        with patch('utils.consul_util.consul.Consul') as mock_consul_class:
            mock_client = Mock()
            mock_consul_class.return_value = mock_client
            mock_client.agent.self.return_value = {}
            yield mock_client

    @pytest.fixture
    def health_server(self):
        """启动健康检查服务器"""
        server = None
        try:
            server = HTTPServer(('127.0.0.1', 9999), MockHealthHandler)
            thread = threading.Thread(target=server.serve_forever)
            thread.daemon = True
            thread.start()
            time.sleep(0.5)
            yield server
        finally:
            if server:
                server.shutdown()

    def test_all_services_config(self):
        """测试所有服务的配置是否正确"""
        expected_services = {
            "system": {"service_name": "system-service", "port": 8001, "description": "系统服务"},
            "product": {"service_name": "product-service", "port": 8002, "description": "商品服务"},
            "stock": {"service_name": "stock-service", "port": 8003, "description": "库存服务"},
            "production": {"service_name": "production-service", "port": 8004, "description": "生产服务"},
            "report": {"service_name": "report-service", "port": 8005, "description": "报表服务"},
            "approval": {"service_name": "approval-service", "port": 8006, "description": "审批流服务"},
            "partner": {"service_name": "partner-service", "port": 8007, "description": "往来单位服务"},
            "order": {"service_name": "order-service", "port": 8008, "description": "订单中心服务"},
            "purchase": {"service_name": "purchase-service", "port": 8009, "description": "采购中心服务"},
            "gateway": {"service_name": "gateway-service", "port": 8000, "description": "网关服务"}
        }

        assert SERVICE_CONFIG == expected_services

    @pytest.mark.parametrize("service_key,service_name,port,description", [
        ("system", "system-service", 8001, "系统服务"),
        ("product", "product-service", 8002, "商品服务"),
        ("stock", "stock-service", 8003, "库存服务"),
        ("production", "production-service", 8004, "生产服务"),
        ("report", "report-service", 8005, "报表服务"),
        ("approval", "approval-service", 8006, "审批流服务"),
        ("partner", "partner-service", 8007, "往来单位服务"),
        ("order", "order-service", 8008, "订单中心服务"),
        ("purchase", "purchase-service", 8009, "采购中心服务"),
        ("gateway", "gateway-service", 8000, "网关服务")
    ])
    def test_register_single_service(self, mock_consul_client, service_key, service_name, port, description):
        """测试单个服务注册"""
        result = ConsulUtil.register_service(
            service_name=service_name,
            ip="192.168.1.100",
            port=port,
            metadata={"description": description}
        )

        assert result is True
        mock_consul_client.agent.service.register.assert_called_once()

    def test_register_all_services(self, mock_consul_client):
        """测试注册所有服务"""
        registered_count = 0

        for service_key, config in SERVICE_CONFIG.items():
            result = ConsulUtil.register_service(
                service_name=config["service_name"],
                ip="192.168.1.100",
                port=config["port"],
                metadata={"description": config["description"]}
            )
            if result:
                registered_count += 1

        assert registered_count == 10
        assert mock_consul_client.agent.service.register.call_count == 10

    def test_discover_all_services(self, mock_consul_client):
        """测试发现所有服务"""
        mock_consul_client.health.service.return_value = (
            None,
            [
                {
                    "Service": {
                        "Address": "192.168.1.100",
                        "Port": 8001,
                        "ID": "system-service-192.168.1.100-8001",
                        "Service": "system-service",
                        "Tags": []
                    },
                    "Checks": [{"Status": "passing"}]
                },
                {
                    "Service": {
                        "Address": "192.168.1.100",
                        "Port": 8002,
                        "ID": "product-service-192.168.1.100-8002",
                        "Service": "product-service",
                        "Tags": []
                    },
                    "Checks": [{"Status": "passing"}]
                }
            ]
        )

        services = ConsulUtil.list_services()
        assert "system-service" in services
        assert "product-service" in services

    @pytest.mark.parametrize("service_name", [
        "system-service",
        "product-service",
        "stock-service",
        "production-service",
        "report-service",
        "approval-service",
        "partner-service",
        "order-service",
        "purchase-service",
        "gateway-service"
    ])
    def test_discover_service_by_name(self, mock_consul_client, service_name):
        """测试按服务名发现服务"""
        mock_consul_client.health.service.return_value = (
            None,
            [
                {
                    "Service": {
                        "Address": "192.168.1.100",
                        "Port": 8000,
                        "ID": f"{service_name}-192.168.1.100-8000",
                        "Service": service_name,
                        "Tags": []
                    },
                    "Checks": [{"Status": "passing"}]
                }
            ]
        )

        instance = ConsulUtil.discover_service(service_name)
        assert instance is not None
        assert instance["service_name"] == service_name

    def test_service_registry_register_all(self, mock_consul_client):
        """测试使用 ServiceRegistry 注册所有服务"""
        registered_services = []

        for service_key in SERVICE_CONFIG.keys():
            result = ServiceRegistry.register(service_key, ip="192.168.1.100")
            if result:
                registered_services.append(service_key)

        assert len(registered_services) == 10

    def test_auto_register_all_services(self, mock_consul_client):
        """测试使用 auto_register 注册所有服务"""
        registered_services = []

        for service_key in SERVICE_CONFIG.keys():
            result = auto_register(service_key, ip="192.168.1.100")
            if result:
                registered_services.append(service_key)

        assert len(registered_services) == 10

    def test_auto_register_disabled(self, mock_consul_client):
        """测试禁用自动注册"""
        result = auto_register("system", enabled=False)
        assert result is False
        mock_consul_client.agent.service.register.assert_not_called()

    def test_deregister_all_services(self, mock_consul_client):
        """测试注销所有服务"""
        # 先注册所有服务
        for service_key, config in SERVICE_CONFIG.items():
            ConsulUtil.register_service(
                service_name=config["service_name"],
                ip="192.168.1.100",
                port=config["port"]
            )

        # 注销所有服务
        deregistered_count = 0
        for service_key, config in SERVICE_CONFIG.items():
            result = ConsulUtil.deregister_service(config["service_name"])
            if result:
                deregistered_count += 1

        assert deregistered_count == 10
        assert mock_consul_client.agent.service.deregister.call_count == 10

    def test_service_discovery_strategies(self, mock_consul_client):
        """测试不同的服务发现策略"""
        mock_consul_client.health.service.return_value = (
            None,
            [
                {
                    "Service": {
                        "Address": "192.168.1.100",
                        "Port": 8001,
                        "ID": "system-service-192.168.1.100-8001",
                        "Service": "system-service",
                        "Tags": ["weight=1.0"]
                    },
                    "Checks": [{"Status": "passing"}]
                },
                {
                    "Service": {
                        "Address": "192.168.1.101",
                        "Port": 8001,
                        "ID": "system-service-192.168.1.101-8001",
                        "Service": "system-service",
                        "Tags": ["weight=2.0"]
                    },
                    "Checks": [{"Status": "passing"}]
                }
            ]
        )

        # 测试随机策略
        instance_random = ConsulUtil.discover_service("system-service", strategy="random")
        assert instance_random is not None

        # 测试轮询策略
        instance_round_robin1 = ConsulUtil.discover_service("system-service", strategy="round_robin")
        instance_round_robin2 = ConsulUtil.discover_service("system-service", strategy="round_robin")
        assert instance_round_robin1 is not None
        assert instance_round_robin2 is not None

        # 测试权重策略
        instance_weight = ConsulUtil.discover_service("system-service", strategy="weight")
        assert instance_weight is not None

    def test_get_service_instances_healthy_only(self, mock_consul_client):
        """测试只获取健康的服务实例"""
        mock_consul_client.health.service.return_value = (
            None,
            [
                {
                    "Service": {
                        "Address": "192.168.1.100",
                        "Port": 8001,
                        "ID": "system-service-192.168.1.100-8001",
                        "Service": "system-service",
                        "Tags": []
                    },
                    "Checks": [{"Status": "passing"}]
                },
                {
                    "Service": {
                        "Address": "192.168.1.101",
                        "Port": 8001,
                        "ID": "system-service-192.168.1.101-8001",
                        "Service": "system-service",
                        "Tags": []
                    },
                    "Checks": [{"Status": "critical"}]
                }
            ]
        )

        # 获取所有实例
        all_instances = ConsulUtil.get_service_instances("system-service", healthy_only=False)
        assert len(all_instances) == 2

        # 只获取健康实例
        healthy_instances = ConsulUtil.get_service_instances("system-service", healthy_only=True)
        assert len(healthy_instances) == 1
        assert healthy_instances[0]["healthy"] is True

    def test_service_health_status(self, mock_consul_client):
        """测试服务健康状态查询"""
        mock_consul_client.health.checks.return_value = [
            {"ServiceID": "system-service-192.168.1.100-8001", "Status": "passing"},
            {"ServiceID": "system-service-192.168.1.101-8001", "Status": "critical"}
        ]

        status = ConsulUtil.get_health_status("system-service")
        assert len(status) == 2
        assert status["system-service-192.168.1.100-8001"] == "passing"
        assert status["system-service-192.168.1.101-8001"] == "critical"

    def test_kv_config_storage(self, mock_consul_client):
        """测试 KV 配置存储"""
        # 设置配置
        ConsulUtil.set_config("app/database/host", "192.168.1.100")
        assert mock_consul_client.kv.put.called

        # 获取配置
        mock_consul_client.kv.get.return_value = (None, {"Value": b"192.168.1.100"})
        value = ConsulUtil.get_config("app/database/host")
        assert value == "192.168.1.100"

    def test_concurrent_service_registration(self, mock_consul_client):
        """测试并发服务注册"""
        import concurrent.futures

        def register_service(service_key):
            config = SERVICE_CONFIG[service_key]
            return ConsulUtil.register_service(
                service_name=config["service_name"],
                ip="192.168.1.100",
                port=config["port"]
            )

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(register_service, key) for key in SERVICE_CONFIG.keys()]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]

        assert all(results)
        assert mock_consul_client.agent.service.register.call_count == 10


class TestServiceIntegration:
    """服务集成测试"""

    def test_service_lifecycle(self, mock_consul_client):
        """测试服务完整生命周期"""
        service_name = "system-service"
        port = 8001

        # 1. 注册服务
        result = ConsulUtil.register_service(
            service_name=service_name,
            ip="192.168.1.100",
            port=port
        )
        assert result is True

        # 2. 发现服务
        mock_consul_client.health.service.return_value = (
            None,
            [
                {
                    "Service": {
                        "Address": "192.168.1.100",
                        "Port": port,
                        "ID": f"{service_name}-192.168.1.100-{port}",
                        "Service": service_name,
                        "Tags": []
                    },
                    "Checks": [{"Status": "passing"}]
                }
            ]
        )
        instance = ConsulUtil.discover_service(service_name)
        assert instance is not None

        # 3. 注销服务
        result = ConsulUtil.deregister_service(service_name)
        assert result is True

    def test_multiple_service_instances(self, mock_consul_client):
        """测试同一服务的多个实例"""
        service_name = "system-service"
        instances = [
            {"ip": "192.168.1.100", "port": 8001},
            {"ip": "192.168.1.101", "port": 8001},
            {"ip": "192.168.1.102", "port": 8001}
        ]

        # 注册多个实例
        for inst in instances:
            ConsulUtil.register_service(
                service_name=service_name,
                ip=inst["ip"],
                port=inst["port"]
            )

        # 获取所有实例
        mock_consul_client.health.service.return_value = (
            None,
            [
                {
                    "Service": {
                        "Address": inst["ip"],
                        "Port": inst["port"],
                        "ID": f"{service_name}-{inst['ip']}-{inst['port']}",
                        "Service": service_name,
                        "Tags": []
                    },
                    "Checks": [{"Status": "passing"}]
                }
                for inst in instances
            ]
        )

        all_instances = ConsulUtil.get_service_instances(service_name)
        assert len(all_instances) == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])