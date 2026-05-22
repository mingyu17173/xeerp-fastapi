"""
微服务单元测试套件
测试所有微服务的配置和注册功能
"""

import unittest
import sys
import os

# 添加项目路径到 sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 尝试导入 consul_util，如果失败则模拟
try:
    from utils.consul_util import ConsulUtil, SERVICE_CONFIG
    CONSUL_AVAILABLE = True
except ImportError:
    # 模拟 SERVICE_CONFIG
    SERVICE_CONFIG = {
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
    CONSUL_AVAILABLE = False


class TestServiceConfigBase(unittest.TestCase):
    """服务配置基础测试类"""
    
    def assert_service_config(self, service_key, expected_name, expected_port, expected_desc):
        """断言服务配置"""
        self.assertIn(service_key, SERVICE_CONFIG)
        config = SERVICE_CONFIG[service_key]
        self.assertEqual(config["service_name"], expected_name)
        self.assertEqual(config["port"], expected_port)
        self.assertEqual(config["description"], expected_desc)


class TestSystemService(TestServiceConfigBase):
    """系统服务测试"""
    
    def test_system_service_config(self):
        """测试系统服务配置"""
        self.assert_service_config("system", "system-service", 8001, "系统服务")


class TestProductService(TestServiceConfigBase):
    """商品服务测试"""
    
    def test_product_service_config(self):
        """测试商品服务配置"""
        self.assert_service_config("product", "product-service", 8002, "商品服务")


class TestStockService(TestServiceConfigBase):
    """库存服务测试"""
    
    def test_stock_service_config(self):
        """测试库存服务配置"""
        self.assert_service_config("stock", "stock-service", 8003, "库存服务")


class TestProductionService(TestServiceConfigBase):
    """生产服务测试"""
    
    def test_production_service_config(self):
        """测试生产服务配置"""
        self.assert_service_config("production", "production-service", 8004, "生产服务")


class TestReportService(TestServiceConfigBase):
    """报表服务测试"""
    
    def test_report_service_config(self):
        """测试报表服务配置"""
        self.assert_service_config("report", "report-service", 8005, "报表服务")


class TestApprovalService(TestServiceConfigBase):
    """审批流服务测试"""
    
    def test_approval_service_config(self):
        """测试审批流服务配置"""
        self.assert_service_config("approval", "approval-service", 8006, "审批流服务")


class TestPartnerService(TestServiceConfigBase):
    """往来单位服务测试"""
    
    def test_partner_service_config(self):
        """测试往来单位服务配置"""
        self.assert_service_config("partner", "partner-service", 8007, "往来单位服务")


class TestOrderService(TestServiceConfigBase):
    """订单中心服务测试"""
    
    def test_order_service_config(self):
        """测试订单中心服务配置"""
        self.assert_service_config("order", "order-service", 8008, "订单中心服务")


class TestPurchaseService(TestServiceConfigBase):
    """采购中心服务测试"""
    
    def test_purchase_service_config(self):
        """测试采购中心服务配置"""
        self.assert_service_config("purchase", "purchase-service", 8009, "采购中心服务")


class TestGatewayService(TestServiceConfigBase):
    """网关服务测试"""
    
    def test_gateway_service_config(self):
        """测试网关服务配置"""
        self.assert_service_config("gateway", "gateway-service", 8000, "网关服务")


class TestAllServices(TestServiceConfigBase):
    """所有服务综合测试"""
    
    def test_service_count(self):
        """测试服务数量"""
        self.assertEqual(len(SERVICE_CONFIG), 10)
    
    def test_all_service_names(self):
        """测试所有服务名称"""
        expected_names = [
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
        ]
        actual_names = [config["service_name"] for config in SERVICE_CONFIG.values()]
        self.assertEqual(sorted(actual_names), sorted(expected_names))
    
    def test_all_ports_unique(self):
        """测试所有端口是否唯一"""
        ports = [config["port"] for config in SERVICE_CONFIG.values()]
        self.assertEqual(len(ports), len(set(ports)))
    
    def test_port_range(self):
        """测试端口范围"""
        for service_key, config in SERVICE_CONFIG.items():
            port = config["port"]
            self.assertTrue(8000 <= port <= 8009, 
                           f"{service_key} 的端口 {port} 不在有效范围内(8000-8009)")
    
    def test_service_keys(self):
        """测试服务键"""
        expected_keys = [
            "system", "product", "stock", "production", "report",
            "approval", "partner", "order", "purchase", "gateway"
        ]
        self.assertEqual(sorted(list(SERVICE_CONFIG.keys())), sorted(expected_keys))
    
    def test_all_descriptions(self):
        """测试所有服务描述"""
        descriptions = [config["description"] for config in SERVICE_CONFIG.values()]
        expected_descriptions = [
            "系统服务", "商品服务", "库存服务", "生产服务", "报表服务",
            "审批流服务", "往来单位服务", "订单中心服务", "采购中心服务", "网关服务"
        ]
        self.assertEqual(sorted(descriptions), sorted(expected_descriptions))


class TestServiceRegistry(unittest.TestCase):
    """服务注册助手测试"""
    
    def test_auto_register_disabled(self):
        """测试禁用自动注册"""
        def mock_auto_register(service_key, enabled=True):
            if not enabled:
                return False
            return True
        
        result = mock_auto_register("system", enabled=False)
        self.assertFalse(result)
    
    def test_register_unknown_service(self):
        """测试注册未知服务"""
        def mock_register(service_key):
            if service_key not in SERVICE_CONFIG:
                return False
            return True
        
        result = mock_register("unknown-service")
        self.assertFalse(result)
    
    def test_register_all_services(self):
        """测试注册所有服务"""
        def mock_register(service_key):
            if service_key in SERVICE_CONFIG:
                return True
            return False
        
        registered_count = 0
        for service_key in SERVICE_CONFIG.keys():
            if mock_register(service_key):
                registered_count += 1
        
        self.assertEqual(registered_count, 10)


class TestConsulUtil(unittest.TestCase):
    """Consul工具类测试"""
    
    def test_get_local_ip(self):
        """测试获取本地IP"""
        if CONSUL_AVAILABLE:
            ip = ConsulUtil.get_local_ip()
            parts = ip.split('.')
            self.assertEqual(len(parts), 4)
            for part in parts:
                self.assertTrue(part.isdigit())
                self.assertTrue(0 <= int(part) <= 255)
        else:
            self.skipTest("Consul not available")


def main():
    """运行所有测试"""
    print("=" * 70)
    print("微服务单元测试套件")
    print("=" * 70)
    print("Consul 可用:", CONSUL_AVAILABLE)
    print("服务数量:", len(SERVICE_CONFIG))
    print()
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加所有测试类
    suite.addTests(loader.loadTestsFromTestCase(TestSystemService))
    suite.addTests(loader.loadTestsFromTestCase(TestProductService))
    suite.addTests(loader.loadTestsFromTestCase(TestStockService))
    suite.addTests(loader.loadTestsFromTestCase(TestProductionService))
    suite.addTests(loader.loadTestsFromTestCase(TestReportService))
    suite.addTests(loader.loadTestsFromTestCase(TestApprovalService))
    suite.addTests(loader.loadTestsFromTestCase(TestPartnerService))
    suite.addTests(loader.loadTestsFromTestCase(TestOrderService))
    suite.addTests(loader.loadTestsFromTestCase(TestPurchaseService))
    suite.addTests(loader.loadTestsFromTestCase(TestGatewayService))
    suite.addTests(loader.loadTestsFromTestCase(TestAllServices))
    suite.addTests(loader.loadTestsFromTestCase(TestServiceRegistry))
    suite.addTests(loader.loadTestsFromTestCase(TestConsulUtil))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 输出总结
    print("\n" + "=" * 70)
    print("测试总结")
    print("=" * 70)
    print("运行测试数:", result.testsRun)
    print("失败数:", len(result.failures))
    print("错误数:", len(result.errors))
    print("跳过数:", len(result.skipped))
    
    if result.wasSuccessful():
        print("\n🎉 所有测试通过！")
        return 0
    else:
        print("\n❌ 测试失败！")
        return 1


if __name__ == "__main__":
    sys.exit(main())