# Nacos服务注册

## 1. 概述

Nacos是阿里巴巴开源的动态服务发现、配置管理和服务管理平台。本项目集成Nacos实现微服务的自动注册与发现，实现服务的动态路由和负载均衡。

## 2. 服务注册架构

### 2.1 整体架构

```
┌─────────────────────────────────────────────────────────┐
│                      Nacos Server                        │
│           (服务注册中心 / 配置管理中心)                     │
└─────────────────────────────────────────────────────────┘
                          ▲
                          │ 注册/发现/心跳
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
┌───────▼──────┐  ┌───────▼──────┐  ┌──────▼──────┐
│   Gateway    │  │   System     │  │   Product   │
│   :8000      │  │   :8001      │  │   :8002     │
│  (服务发现)   │  │  (自动注册)   │  │  (自动注册)   │
└──────────────┘  └──────────────┘  └──────────────┘
        │                 │                 │
        └─────────────────┼─────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
┌───────▼──────┐  ┌───────▼──────┐  ┌──────▼──────┐
│   Stock      │  │ Production   │  │   Report    │
│   :8003      │  │   :8004      │  │   :8005     │
│  (自动注册)   │  │  (自动注册)   │  │  (自动注册)   │
└──────────────┘  └──────────────┘  └──────────────┘
```

### 2.2 服务列表

| 服务名称 | 服务键 | 端口 | 描述 |
|---------|--------|------|------|
| gateway-service | gateway | 8000 | 网关服务 |
| system-service | system | 8001 | 系统服务 |
| product-service | product | 8002 | 商品服务 |
| stock-service | stock | 8003 | 库存服务 |
| production-service | production | 8004 | 生产服务 |
| report-service | report | 8005 | 报表服务 |
| approval-service | approval | 8006 | 审批流服务 |
| partner-service | partner | 8007 | 往来单位服务 |
| order-service | order | 8008 | 订单中心服务 |
| purchase-service | purchase | 8009 | 采购中心服务 |
| sales-service | sales | 8010 | 销售服务 |

## 3. 核心组件

### 3.1 Nacos工具类

**文件路径**: `utils/nacos_util.py`

提供Nacos客户端的封装，包含以下功能：

- `create_nacos_client()` - 创建Nacos客户端连接
- `register_service()` - 注册服务实例
- `deregister_service()` - 注销服务实例
- `get_service_instances()` - 获取服务实例列表
- `send_heartbeat()` - 发送心跳
- `get_local_ip()` - 获取本地IP地址

### 3.2 服务注册助手

**文件路径**: `utils/service_registry.py`

提供服务注册的便捷接口：

- `auto_register(service_key)` - 自动注册服务
- 支持信号处理（SIGTERM、SIGINT）
- 退出时自动注销服务

### 3.3 服务发现模块

**文件路径**: `gateway/core/nacos_discovery.py`

Gateway专用的服务发现模块：

- `get_service_url(service_name)` - 获取服务URL
- `get_service_url_with_fallback()` - 支持降级的服务获取
- 服务URL缓存机制

## 4. 使用方法

### 4.1 服务注册

在各微服务的启动文件中添加注册代码：

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from utils.service_registry import auto_register

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 注册服务到Nacos
    auto_register("system")
    
    # 其他初始化...
    logger.info("服务启动成功")
    yield
    # 清理资源...
```

### 4.2 服务发现

Gateway通过Nacos动态发现服务：

```python
from core.nacos_discovery import NacosServiceDiscovery

# 获取服务URL（支持降级）
url = NacosServiceDiscovery.get_service_url_with_fallback(
    "system-service",
    "http://127.0.0.1:8001"  # 降级URL
)
```

## 5. 配置说明

### 5.1 Nacos服务器配置

**环境变量**:

```env
NACOS_SERVER_ADDRESSES=127.0.0.1:8848
NACOS_NAMESPACE=public
NACOS_USERNAME=nacos
NACOS_PASSWORD=nacos
```

### 5.2 Gateway配置

**文件路径**: `gateway/core/env.py`

```python
class AppConfig(BaseSettings):
    # Nacos配置
    nacos_enabled: bool = True
    nacos_server_addresses: str = "127.0.0.1:8848"
    nacos_namespace: str = "public"
```

### 5.3 路由映射

**文件路径**: `gateway/router/gateway_router.py`

```python
# 路径 -> 服务名称映射
service_routes = {
    "/api/user": "system-service",
    "/api/product": "product-service",
    "/api/stock": "stock-service",
    # ...
}

# 降级URL配置
fallback_service_urls = {
    "system-service": "http://127.0.0.1:8001",
    "product-service": "http://127.0.0.1:8002",
    # ...
}
```

## 6. 工作流程

### 6.1 服务注册流程

1. 服务启动时调用 `auto_register(service_key)`
2. 获取本地IP地址和服务端口
3. 通过Nacos客户端注册服务实例
4. 注册退出信号处理器（SIGTERM、SIGINT）
5. 服务退出时自动注销

### 6.2 服务发现流程

1. Gateway接收到客户端请求
2. 根据请求路径匹配目标服务名称
3. 从Nacos获取服务实例列表
4. 选择健康的服务实例
5. 转发请求到目标服务
6. 返回响应给客户端

### 6.3 降级机制

当Nacos不可用时，Gateway会使用预配置的降级URL：

```python
def get_service_url_with_fallback(service_name, fallback_url):
    if nacos_enabled:
        url = get_service_url(service_name)
        if url:
            return url
    return fallback_url
```

## 7. 高可用特性

### 7.1 心跳机制

Nacos客户端会定期发送心跳保持服务实例活跃状态，默认时间间隔为5秒。

### 7.2 健康检查

Nacos会自动检测服务实例的健康状态，不健康的实例会被自动剔除。

### 7.3 负载均衡

Gateway支持多种负载均衡策略（可扩展）：

- 轮询（Round Robin）
- 随机（Random）
- 加权轮询（Weighted Round Robin）

### 7.4 故障转移

当某个服务实例不可用时，Gateway会自动选择其他健康实例。

## 8. 部署说明

### 8.1 Nacos Server部署

**使用Docker部署**:

```bash
docker run -d \
  -p 8848:8848 \
  -p 9848:9848 \
  -e MODE=standalone \
  -v /opt/nacos/data:/home/nacos/data \
  nacos/nacos-server:v2.3.2
```

### 8.2 访问Nacos控制台

```
http://localhost:8848/nacos
用户名: nacos
密码: nacos
```

### 8.3 服务启动顺序

1. 启动Nacos Server
2. 启动各微服务（自动注册）
3. 启动Gateway（服务发现）

## 9. 代码示例

### 9.1 完整的服务启动示例

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from core.logger import logger
from utils.service_registry import auto_register

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("服务开始启动...")
    
    # 注册服务到Nacos
    auto_register("product")
    
    # 初始化数据库等
    await init_db()
    
    logger.info("服务启动成功")
    yield
    logger.info("服务正在停止...")

app = FastAPI(lifespan=lifespan)

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "product-service"}
```

### 9.2 Gateway路由转发示例

```python
@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_request(request: Request, path: str):
    # 获取目标服务
    target_service = await get_target_service(f"/{path}")
    
    if not target_service:
        raise HTTPException(status_code=404, detail="服务未找到")
    
    # 转发请求
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=f"{target_service}/{path}",
            headers=request.headers
        )
    
    return response
```

## 10. 注意事项

### 10.1 网络配置

确保各服务能够访问Nacos Server，防火墙开放8848端口。

### 10.2 命名空间

使用不同的命名空间隔离不同环境（dev、test、prod）。

### 10.3 临时实例

默认使用临时实例（ephemeral=true），服务停止后会自动从Nacos移除。

### 10.4 日志记录

注册和发现操作都会记录日志，便于问题排查。

## 11. 故障排查

### 11.1 服务注册失败

检查：
- Nacos Server是否正常运行
- 网络是否可达
- 配置是否正确

### 11.2 服务发现失败

检查：
- 服务是否已注册到Nacos
- 服务实例是否健康
- Gateway配置是否正确

### 11.3 心跳失败

检查：
- Nacos Server连接状态
- 网络稳定性
- 服务实例状态

## 12. 扩展建议

### 12.1 配置管理

使用Nacos配置管理功能管理各服务的配置文件。

### 12.2 集群部署

部署Nacos集群提高可用性。

### 12.3 服务监控

集成Prometheus和Grafana监控服务状态。

### 12.4 链路追踪

集成Zipkin或Jaeger实现分布式链路追踪。

---

**版本**: 1.0.0  
**创建时间**: 2026年5月  
**适用场景**: XEERP微服务架构