"""
服务注册助手单元测试
"""

import pytest
from unittest.mock import Mock, patch
from utils.service_registry import ServiceRegistry, auto_register


class TestServiceRegistry:
    """ServiceRegistry 单元测试类"""

    @patch('utils.service_registry.ConsulUtil.register_service')
    def test_register_success(self, mock_register):
        """测试注册服务成功"""
        # 设置 mock
        mock_register.return_value = True

        # 执行测试
        result = ServiceRegistry.register("system")

        # 验证结果
        assert result is True
        mock_register.assert_called_once()

    @patch('utils.service_registry.ConsulUtil.register_service')
    def test_register_failure_not_required(self, mock_register):
        """测试注册失败（非必须）"""
        # 设置 mock
        mock_register.return_value = False

        # 执行测试
        result = ServiceRegistry.register("system", required=False)

        # 验证结果
        assert result is False

    @patch('utils.service_registry.ConsulUtil.register_service')
    def test_register_failure_required(self, mock_register):
        """测试注册失败（必须，抛出异常）"""
        # 设置 mock
        mock_register.return_value = False

        # 执行测试并验证异常
        with pytest.raises(RuntimeError):
            ServiceRegistry.register("system", required=True)

    def test_register_unknown_service(self):
        """测试注册未知服务"""
        # 执行测试
        result = ServiceRegistry.register("unknown-service")

        # 验证结果
        assert result is False

    @patch('utils.service_registry.ConsulUtil.deregister_service')
    def test_deregister_on_exit(self, mock_deregister):
        """测试退出时注销服务"""
        # 设置状态
        ServiceRegistry._registered = True
        ServiceRegistry._service_name = "test-service"
        ServiceRegistry._service_id = "test-service-127.0.0.1-8000"

        # 执行测试
        ServiceRegistry._deregister_on_exit()

        # 验证结果
        mock_deregister.assert_called_once()

    def test_get_service_info(self):
        """测试获取服务信息"""
        # 设置状态
        ServiceRegistry._service_name = "test-service"
        ServiceRegistry._ip = "192.168.1.100"
        ServiceRegistry._port = 8000
        ServiceRegistry._service_id = "test-service-192.168.1.100-8000"

        # 执行测试
        info = ServiceRegistry.get_service_info()

        # 验证结果
        assert info is not None
        assert info["service_name"] == "test-service"
        assert info["ip"] == "192.168.1.100"
        assert info["port"] == 8000

    def test_get_service_info_none(self):
        """测试未注册时获取服务信息"""
        # 重置状态
        ServiceRegistry._service_name = None
        ServiceRegistry._ip = None
        ServiceRegistry._port = None

        # 执行测试
        info = ServiceRegistry.get_service_info()

        # 验证结果
        assert info is None


class TestAutoRegister:
    """auto_register 函数单元测试"""

    @patch('utils.service_registry.ServiceRegistry.register')
    def test_auto_register_enabled(self, mock_register):
        """测试启用注册"""
        # 设置 mock
        mock_register.return_value = True

        # 执行测试
        result = auto_register("system", enabled=True)

        # 验证结果
        assert result is True
        mock_register.assert_called_once()

    @patch('utils.service_registry.ServiceRegistry.register')
    def test_auto_register_disabled(self, mock_register):
        """测试禁用注册"""
        # 执行测试
        result = auto_register("system", enabled=False)

        # 验证结果
        assert result is False
        mock_register.assert_not_called()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
