"""
测试 Consul 服务注册与发现功能
包含健康检查服务
"""

import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from utils.consul_util import ConsulUtil

# 健康检查服务器
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status": "UP"}')
        else:
            self.send_response(404)
            self.end_headers()

def start_health_server(port):
    """启动健康检查服务器"""
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    print(f"🏥 健康检查服务器启动在端口 {port}")
    server.serve_forever()

def test_consul():
    """测试 Consul 功能"""
    print("=" * 60)
    print("测试 Consul 服务注册与发现")
    print("=" * 60)

    test_port = 9999

    # 1. 启动健康检查服务器
    print("\n0. 启动健康检查服务器...")
    server_thread = threading.Thread(target=start_health_server, args=(test_port,))
    server_thread.daemon = True
    server_thread.start()
    time.sleep(1)  # 等待服务器启动

    # 2. 初始化客户端
    print("\n1. 初始化 Consul 客户端...")
    success = ConsulUtil.init_client(host="127.0.0.1", port=8500)
    if not success:
        print("❌ Consul 客户端初始化失败，请检查 Consul 服务是否运行")
        return

    # 3. 获取本地 IP
    local_ip = ConsulUtil.get_local_ip()
    print(f"\n2. 本地 IP: {local_ip}")

    # 4. 注册测试服务
    print("\n3. 注册测试服务...")
    success = ConsulUtil.register_service(
        service_name="test-consul-service",
        ip=local_ip,
        port=test_port,
        metadata={"description": "测试服务", "env": "test"}
    )

    if success:
        # 等待健康检查
        print("\n4. 等待健康检查...")
        time.sleep(3)  # 等待健康检查执行

        # 5. 查询服务列表
        print("\n5. 查询已注册的服务列表...")
        services = ConsulUtil.list_services()
        print(f"已注册服务: {services}")

        # 6. 获取服务实例
        print("\n6. 获取测试服务实例...")
        instances = ConsulUtil.get_service_instances("test-consul-service")
        print(f"找到 {len(instances)} 个实例:")
        for inst in instances:
            print(f"  - {inst['ip']}:{inst['port']} (健康: {inst['healthy']})")

        # 7. 获取健康实例
        print("\n7. 获取健康的服务实例...")
        healthy_instances = ConsulUtil.get_service_instances("test-consul-service", healthy_only=True)
        print(f"找到 {len(healthy_instances)} 个健康实例:")
        for inst in healthy_instances:
            print(f"  - {inst['ip']}:{inst['port']}")

        # 8. 测试服务发现（随机策略）
        print("\n8. 测试服务发现（随机策略）...")
        instance = ConsulUtil.discover_service("test-consul-service", strategy="random")
        if instance:
            print(f"随机选择的实例: {instance['ip']}:{instance['port']}")

        # 9. 获取健康状态
        print("\n9. 获取健康状态...")
        status = ConsulUtil.get_health_status("test-consul-service")
        print(f"健康状态: {status}")

        # 10. 注销测试服务
        print("\n10. 注销测试服务...")
        success = ConsulUtil.deregister_service("test-consul-service")
        if success:
            print("✅ 服务注销成功")

            # 11. 验证注销结果
            print("\n11. 验证服务是否已注销...")
            instances = ConsulUtil.get_service_instances("test-consul-service")
            print(f"剩余实例数: {len(instances)}")

    else:
        print("❌ 服务注册失败")

if __name__ == "__main__":
    test_consul()
