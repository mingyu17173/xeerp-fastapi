# 微服务测试说明

## 测试文件结构

```
test/
├── test_consul_util.py          # Consul 工具类单元测试
├── test_service_registry.py     # 服务注册助手单元测试
└── test_microservices.py        # 微服务集成测试
```

## 测试覆盖范围

### 1. Consul 工具类测试 (test_consul_util.py)

| 测试用例 | 测试内容 |
|---------|---------|
| test_init_client_success | 测试 Consul 客户端初始化成功 |
| test_init_client_failure | 测试 Consul 客户端初始化失败 |
| test_get_local_ip | 测试获取本地 IP |
| test_register_service_success | 测试服务注册成功 |
| test_register_service_failure | 测试服务注册失败 |
| test_deregister_service_success | 测试服务注销成功 |
| test_get_service_instances | 测试获取服务实例 |
| test_list_services | 测试获取服务列表 |
| test_parse_tags | 测试标签解析 |
| test_discover_service_random | 测试随机策略发现服务 |
| test_discover_service_no_instances | 测试无可用实例情况 |

### 2. 服务注册助手测试 (test_service_registry.py)

| 测试用例 | 测试内容 |
|---------|---------|
| test_register_success | 测试注册服务成功 |
| test_register_failure_not_required | 测试注册失败（非必须） |
| test_register_failure_required | 测试注册失败（必须，抛出异常） |
| test_register_unknown_service | 测试注册未知服务 |
| test_deregister_on_exit | 测试退出时注销服务 |
| test_get_service_info | 测试获取服务信息 |
| test_get_service_info_none | 测试未注册时获取服务信息 |
| test_auto_register_enabled | 测试启用注册 |
| test_auto_register_disabled | 测试禁用注册 |

### 3. 微服务集成测试 (test_microservices.py)

| 测试用例 | 测试内容 |
|---------|---------|
| test_all_services_config | 测试所有服务的配置是否正确 |
| test_register_single_service | 测试单个服务注册（参数化测试） |
| test_register_all_services | 测试注册所有服务 |
| test_discover_all_services | 测试发现所有服务 |
| test_discover_service_by_name | 测试按服务名发现服务（参数化测试） |
| test_service_registry_register_all | 测试使用 ServiceRegistry 注册所有服务 |
| test_auto_register_all_services | 测试使用 auto_register 注册所有服务 |
| test_auto_register_disabled | 测试禁用自动注册 |
| test_deregister_all_services | 测试注销所有服务 |
| test_service_discovery_strategies | 测试不同的服务发现策略 |
| test_get_service_instances_healthy_only | 测试只获取健康的服务实例 |
| test_service_health_status | 测试服务健康状态查询 |
| test_kv_config_storage | 测试 KV 配置存储 |
| test_concurrent_service_registration | 测试并发服务注册 |
| test_service_lifecycle | 测试服务完整生命周期 |
| test_multiple_service_instances | 测试同一服务的多个实例 |

## 微服务配置

| 服务键 | 服务名称 | 端口 | 描述 |
|--------|----------|------|------|
| system | system-service | 8001 | 系统服务 |
| product | product-service | 8002 | 商品服务 |
| stock | stock-service | 8003 | 库存服务 |
| production | production-service | 8004 | 生产服务 |
| report | report-service | 8005 | 报表服务 |
| approval | approval-service | 8006 | 审批流服务 |
| partner | partner-service | 8007 | 往来单位服务 |
| order | order-service | 8008 | 订单中心服务 |
| purchase | purchase-service | 8009 | 采购中心服务 |
| gateway | gateway-service | 8000 | 网关服务 |

## 运行测试

### 安装依赖

```bash
pip install pytest pytest-mock pytest-cov
```

### 运行所有测试

```bash
pytest test/ -v
```

### 运行特定测试文件

```bash
# 运行 Consul 工具类测试
pytest test/test_consul_util.py -v

# 运行服务注册助手测试
pytest test/test_service_registry.py -v

# 运行微服务集成测试
pytest test/test_microservices.py -v
```

### 运行特定测试用例

```bash
# 运行单个测试
pytest test/test_microservices.py::TestMicroServiceRegistry::test_register_all_services -v

# 运行参数化测试
pytest test/test_microservices.py::TestMicroServiceRegistry::test_register_single_service -v
```

### 运行标记的测试

```bash
# 运行单元测试
pytest test/ -m unit -v

# 运行集成测试
pytest test/ -m integration -v
```

### 生成覆盖率报告

```bash
# 生成 HTML 覆盖率报告
pytest test/ --cov=utils --cov-report=html

# 查看报告
open htmlcov/index.html
```

## 测试策略

### 单元测试
- 使用 Mock 模拟 Consul 客户端
- 测试单个函数和方法
- 不依赖外部服务

### 集成测试
- 测试多个组件的交互
- 测试服务注册和发现的完整流程
- 测试并发场景

### 参数化测试
- 使用 `@pytest.mark.parametrize` 测试多个相似场景
- 减少重复代码
- 提高测试覆盖率

## 注意事项

1. **Mock 使用**：单元测试使用 Mock 模拟 Consul 客户端，不需要真实的 Consul 服务
2. **健康检查**：集成测试中的健康检查使用模拟服务器
3. **并发测试**：并发测试使用线程池模拟真实场景
4. **清理资源**：测试完成后自动清理注册的服务

## CI/CD 集成

在 CI/CD 流程中运行测试：

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: |
          pip install pytest pytest-mock pytest-cov
          pip install -r requirements.txt
      - name: Run tests
        run: pytest test/ -v --cov=utils
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

## 持续改进

- 添加更多边界条件测试
- 增加性能测试
- 添加端到端测试
- 完善测试文档