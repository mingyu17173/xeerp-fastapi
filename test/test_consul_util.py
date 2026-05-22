"""
Consul 工具类单元测试
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from utils.consul_util import ConsulUtil


class TestConsulUtil:
    """ConsulUtil 单元测试类"""

    @patch('consul.Consul')
    def test_init_client_success(self, mock_consul_class):
        """测试初始化 Consul 客户端成功"""
        # 设置 mock
        mock_client = Mock()
        mock_consul_class.return_value = mock_client
        mock_client.agent.self.return_value = {}

        # 执行测试
        result = ConsulUtil.init_client(host="127.0.0.1", port=8500)

        # 验证结果
        assert result is True
        mock_consul_class.assert_called_once_with(host="127.0.0.1", port=8500)
        mock_client.agent.self.assert_called_once()

    @patch('consul.Consul')
    def test_init_client_failure(self, mock_consul_class):
        """测试初始化 Consul 客户端失败"""
        # 设置 mock - 连接失败
        mock_consul_class.side_effect = Exception("Connection refused")

        # 执行测试
        result = ConsulUtil.init_client(host="127.0.0.1", port=8500)

        # 验证结果
        assert result is False

    def test_get_local_ip(self):
        """测试获取本地 IP"""
        ip = ConsulUtil.get_local_ip()
        
        # 验证返回值是有效的 IP 地址格式
        parts = ip.split('.')
        assert len(parts) == 4
        for part in parts:
            assert part.isdigit()
            assert 0 <= int(part) <= 255

    @patch('utils.consul_util.ConsulUtil.get_client')
    def test_register_service_success(self, mock_get_client):
        """测试注册服务成功"""
        # 设置 mock
        mock_client = Mock()
        mock_get_client.return_value = mock_client

        # 执行测试
        result = ConsulUtil.register_service(
            service_name="test-service",
            ip="192.168.1.100",
            port=8000
        )

        # 验证结果
        assert result is True
        mock_client.agent.service.register.assert_called_once()

    @patch('utils.consul_util.ConsulUtil.get_client')
    def test_register_service_failure(self, mock_get_client):
        """测试注册服务失败"""
        # 设置 mock - 注册失败
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        mock_client.agent.service.register.side_effect = Exception("Register failed")

        # 执行测试
        result = ConsulUtil.register_service(
            service_name="test-service",
            ip="192.168.1.100",
            port=8000
        )

        # 验证结果
        assert result is False

    @patch('utils.consul_util.ConsulUtil.get_client')
    def test_deregister_service_success(self, mock_get_client):
        """测试注销服务成功"""
        # 设置 mock
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        ConsulUtil._registered_services["test-service"] = {
            "service_id": "test-service-192.168.1.100-8000",
            "ip": "192.168.1.100",
            "port": 8000
        }

        # 执行测试
        result = ConsulUtil.deregister_service(service_name="test-service")

        # 验证结果
        assert result is True
        mock_client.agent.service.deregister.assert_called_once()

    @patch('utils.consul_util.ConsulUtil.get_client')
    def test_get_service_instances(self, mock_get_client):
        """测试获取服务实例"""
        # 设置 mock
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        
        mock_client.health.service.return_value = (
            None,
            [
                {
                    "Service": {
                        "Address": "192.168.1.100",
                        "Port": 8000,
                        "ID": "service-1",
                        "Service": "test-service",
                        "Tags": []
                    },
                    "Checks": [{"Status": "passing"}]
                }
            ]
        )

        # 执行测试
        instances = ConsulUtil.get_service_instances("test-service")

        # 验证结果
        assert len(instances) == 1
        assert instances[0]["ip"] == "192.168.1.100"
        assert instances[0]["port"] == 8000
        assert instances[0]["healthy"] is True

    @patch('utils.consul_util.ConsulUtil.get_client')
    def test_list_services(self, mock_get_client):
        """测试获取服务列表"""
        # 设置 mock
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        mock_client.catalog.services.return_value = (None, {"service1": [], "service2": []})

        # 执行测试
        services = ConsulUtil.list_services()

        # 验证结果
        assert isinstance(services, list)
        assert "service1" in services
        assert "service2" in services

    def test_parse_tags(self):
        """测试解析标签"""
        tags = ["cluster=DEFAULT", "weight=1.0", "description=test"]
        
        # 执行测试
        metadata = ConsulUtil._parse_tags(tags)

        # 验证结果
        assert metadata["cluster"] == "DEFAULT"
        assert metadata["weight"] == "1.0"
        assert metadata["description"] == "test"

    @patch('utils.consul_util.ConsulUtil.get_client')
    def test_discover_service_random(self, mock_get_client):
        """测试随机策略发现服务"""
        # 设置 mock
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        
        mock_client.health.service.return_value = (
            None,
            [
                {
                    "Service": {
                        "Address": "192.168.1.100",
                        "Port": 8000,
                        "ID": "service-1",
                        "Service": "test-service",
                        "Tags": ["weight=1.0"]
                    },
                    "Checks": [{"Status": "passing"}]
                },
                {
                    "Service": {
                        "Address": "192.168.1.101",
                        "Port": 8001,
                        "ID": "service-2",
                        "Service": "test-service",
                        "Tags": ["weight=2.0"]
                    },
                    "Checks": [{"Status": "passing"}]
                }
            ]
        )

        # 执行测试
        instance = ConsulUtil.discover_service("test-service", strategy="random")

        # 验证结果
        assert instance is not None
        assert instance["ip"] in ["192.168.1.100", "192.168.1.101"]

    @patch('utils.consul_util.ConsulUtil.get_client')
    def test_discover_service_no_instances(self, mock_get_client):
        """测试没有可用实例的情况"""
        # 设置 mock
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        mock_client.health.service.return_value = (None, [])

        # 执行测试
        instance = ConsulUtil.discover_service("test-service")

        # 验证结果
        assert instance is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
