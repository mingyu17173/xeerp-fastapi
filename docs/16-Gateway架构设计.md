# Gateway 服务架构设计

## 一、架构概览

```
┌─────────────────────────────────────────────────────────────────┐
│                        Client (前端/移动端)                       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Gateway Service (8000)                      │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Middleware Layer                        │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐ │  │
│  │  │ Request  │ │  Logging │ │   Auth   │ │   Rate       │ │  │
│  │  │    ID    │ │          │ │          │ │   Limit      │ │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────────┘ │  │
│  └───────────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Core Layer                              │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐ │  │
│  │  │ Service  │ │  Load    │ │  Circuit │ │   Metrics    │ │  │
│  │  │Discovery │ │ Balancer │ │  Breaker │ │              │ │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────────┘ │  │
│  └───────────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Router Layer                            │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐ │  │
│  │  │  Path    │ │  Header  │ │  Query   │ │   Body       │ │  │
│  │  │  Router  │ │  Router  │ │  Router  │ │  Transform   │ │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────────┘ │  │
│  └───────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Consul (8500)                             │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐       │
│  │  Service │ │  Health  │ │   KV     │   Service     │       │
│  │ Registry │ │  Check   │ │  Store   │   Discovery   │       │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────┘       │
└─────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Microservices Layer                           │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐       │
│  │  System  │ │  Product │ │  Stock   │ │   Order ...  │       │
│  │  (8001)  │ │  (8002)  │ │  (8003)  │ │              │       │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────┘       │
└─────────────────────────────────────────────────────────────────┘
```

## 二、Gateway 服务核心功能模块

### 2.1 中间件层 (Middleware Layer)

#### 2.1.1 请求追踪中间件 (Request Trace Middleware)
- **功能**：为每个请求生成唯一 Trace ID
- **实现**：使用 UUID 生成 8 位短 ID
- **作用**：
  - 请求链路追踪
  - 日志关联查询
  - 问题定位排查

#### 2.1.2 日志中间件 (Logging Middleware)
- **功能**：记录请求和响应的详细信息
- **记录内容**：
  - 请求方法、路径、参数
  - 客户端 IP、端口
  - 响应状态码、处理时间
  - 错误信息
- **日志级别**：
  - INFO：正常请求
  - WARNING：认证失败
  - ERROR：服务异常

#### 2.1.3 认证中间件 (Authentication Middleware)
- **功能**：JWT Token 验证
- **认证方式**：
  - Bearer Token（JWT）
  - API Key（可选）
- **公开路径白名单**：
  - `/api/docs` - API 文档
  - `/api/captchaImage` - 验证码
  - `/api/auth/*` - 登录注册
  - `/health` - 健康检查
- **Token 验证**：
  - 签名验证
  - 过期时间检查
  - 签发者验证

#### 2.1.4 限流中间件 (Rate Limit Middleware)
- **功能**：防止 API 滥用
- **限流策略**：
  - IP 级别限流：100 请求/分钟
  - 用户级别限流：200 请求/分钟
  - API 级别限流：1000 请求/分钟
- **存储**：Redis
- **限流算法**：滑动窗口

#### 2.1.5 CORS 中间件
- **功能**：跨域资源共享
- **配置**：
  - 允许所有来源（开发环境）
  - 允许所有方法
  - 允许所有请求头
  - 暴露 `X-Trace-Id` 响应头

#### 2.1.6 Gzip 中间件
- **功能**：响应数据压缩
- **压缩级别**：默认 6
- **适用场景**：JSON 响应

#### 2.1.7 错误处理中间件 (Error Handling Middleware)
- **功能**：统一异常处理
- **处理异常类型**：
  - HTTPException：HTTP 异常
  - RateLimitExceeded：限流异常
  - 服务不可用异常
  - 未处理异常

### 2.2 核心层 (Core Layer)

#### 2.2.1 服务发现 (Service Discovery)
- **功能**：从 Consul 获取服务实例列表
- **实现方式**：
  - 实时查询：每次请求查询 Consul
  - 缓存机制：本地缓存服务列表（TTL 30s）
  - 健康检查：只返回健康实例
- **降级策略**：
  - Consul 不可用时使用配置文件中的 URL
  - 服务无健康实例时返回 503

#### 2.2.2 负载均衡 (Load Balancer)
- **功能**：在多个服务实例间分配请求
- **策略**：
  - 轮询 (Round Robin)：默认
  - 随机 (Random)：可选
  - 加权轮询 (Weighted Round Robin)：可选
  - 最少连接 (Least Connections)：可选

#### 2.2.3 熔断器 (Circuit Breaker)
- **功能**：防止级联故障
- **状态**：
  - Closed：正常状态
  - Open：熔断状态（拒绝请求）
  - Half-Open：半开状态（尝试恢复）
- **配置**：
  - 失败阈值：5 次失败
  - 超时时间：60 秒
  - 半开请求数：3 次

#### 2.2.4 指标收集 (Metrics)
- **功能**：收集网关运行指标
- **指标类型**：
  - 请求总数
  - 响应时间
  - 错误率
  - 服务可用性
- **存储**：Prometheus + Grafana

### 2.3 路由层 (Router Layer)

#### 2.3.1 路径路由 (Path Router)
- **功能**：根据 URL 路径匹配目标服务
- **匹配规则**：
  - 精确匹配：`/api/user` -> system-service
  - 前缀匹配：`/product/*` -> product-service
  - 正则匹配：高级路由规则

#### 2.3.2 请求转换 (Request Transform)
- **功能**：修改请求内容
- **转换类型**：
  - 路径重写：`/api/captchaImage` -> `/captchaImage`
  - 请求头添加：`X-Gateway`, `X-Trace-Id`
  - 请求头移除：`Host`
  - 请求体转换：JSON 格式化

#### 2.3.3 响应转换 (Response Transform)
- **功能**：修改响应内容
- **转换类型**：
  - 响应头添加：`X-Trace-Id`
  - 响应头移除：敏感信息
  - 响应体转换：统一格式

### 2.4 配置层 (Configuration Layer)

#### 2.4.1 环境配置
- **服务配置**：名称、版本、端口
- **JWT 配置**：密钥、算法、过期时间
- **Redis 配置**：主机、端口、密码
- **Consul 配置**：主机、端口、命名空间
- **限流配置**：请求数、时间窗口
- **超时配置**：请求超时时间

## 三、Consul 服务注册与发现

### 3.1 服务注册流程

```
┌─────────────┐
│  Service    │
│   Start     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Get Local  │
│     IP      │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Register   │
│   to Consul │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Setup      │
│  Health     │
│   Check     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Service    │
│   Running   │
└─────────────┘
```

### 3.2 服务注册配置

```python
{
    "service_name": "system-service",
    "service_id": "system-service-192.168.1.100:8001",
    "address": "192.168.1.100",
    "port": 8001,
    "check": {
        "http": "http://192.168.1.100:8001/health",
        "interval": "10s",
        "timeout": "5s",
        "deregister_critical_service_after": "30s"
    },
    "tags": ["system", "core"],
    "meta": {
        "version": "1.0.0",
        "environment": "production"
    }
}
```

### 3.3 服务发现流程

```
┌─────────────┐
│   Gateway   │
│   Request   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Parse      │
│   Path      │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Get Target │
│   Service   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Query      │
│   Consul    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Filter     │
│  Healthy    │
│  Instances  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Load       │
│  Balance    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Forward    │
│   Request   │
└─────────────┘
```

### 3.4 健康检查机制

- **检查类型**：HTTP 检查
- **检查端点**：`/health`
- **检查间隔**：10 秒
- **超时时间**：5 秒
- **失败阈值**：3 次失败标记为不健康
- **自动注销**：30 秒不健康后自动注销

## 四、Gateway 目录结构

```
gateway/
├── api/                          # API 层
│   └── v1/
│       ├── __init__.py
│       ├── gateway_controller.py # 网关控制器
│       └── metrics_controller.py # 指标控制器
├── core/                         # 核心层
│   ├── __init__.py
│   ├── env.py                    # 环境配置
│   ├── auth.py                   # 认证模块
│   ├── limiter.py                # 限流模块
│   ├── logger.py                 # 日志模块
│   ├── consul_discovery.py       # Consul 服务发现
│   ├── load_balancer.py          # 负载均衡
│   ├── circuit_breaker.py        # 熔断器
│   └── metrics.py                # 指标收集
├── middlewares/                  # 中间件层
│   ├── __init__.py
│   ├── trace_middleware.py       # 请求追踪
│   ├── logging_middleware.py     # 日志记录
│   ├── auth_middleware.py        # 认证鉴权
│   ├── rate_limit_middleware.py  # 限流控制
│   ├── cors_middleware.py        # 跨域处理
│   └── error_middleware.py       # 错误处理
├── router/                       # 路由层
│   ├── __init__.py
│   ├── gateway_router.py         # 网关路由
│   └── path_router.py            # 路径路由
├── utils/                        # 工具类
│   ├── __init__.py
│   ├── request_util.py           # 请求工具
│   ├── response_util.py          # 响应工具
│   └── trace_util.py             # 追踪工具
├── server.py                     # FastAPI 应用入口
├── run.py                        # 服务启动脚本
└── gunicorn_conf.py              # Gunicorn 配置
```

## 五、关键实现要点

### 5.1 Consul 服务发现实现

```python
class ConsulServiceDiscovery:
    def __init__(self, host: str = "127.0.0.1", port: int = 8500):
        self.consul = consul.Consul(host=host, port=port)
        self.cache = {}
        self.cache_ttl = 30
    
    async def get_service_url(self, service_name: str) -> str:
        """获取服务 URL（带缓存）"""
        if service_name in self.cache:
            cached = self.cache[service_name]
            if time.time() - cached['timestamp'] < self.cache_ttl:
                return cached['url']
        
        # 从 Consul 获取服务实例
        _, instances = self.consul.health.service(
            service_name, 
            passing=True
        )
        
        if not instances:
            raise ServiceUnavailableException(
                f"Service {service_name} not available"
            )
        
        # 负载均衡选择实例
        instance = self.load_balancer.select(instances)
        url = f"http://{instance['Service']['Address']}:{instance['Service']['Port']}"
        
        # 更新缓存
        self.cache[service_name] = {
            'url': url,
            'timestamp': time.time()
        }
        
        return url
```

### 5.2 负载均衡实现

```python
class LoadBalancer:
    def __init__(self, strategy: str = "round_robin"):
        self.strategy = strategy
        self.round_robin_index = {}
    
    def select(self, instances: list) -> dict:
        """选择服务实例"""
        if self.strategy == "round_robin":
            return self._round_robin(instances)
        elif self.strategy == "random":
            return self._random(instances)
        elif self.strategy == "least_connections":
            return self._least_connections(instances)
        else:
            return instances[0]
    
    def _round_robin(self, instances: list) -> dict:
        """轮询策略"""
        service_name = instances[0]['Service']['Service']
        if service_name not in self.round_robin_index:
            self.round_robin_index[service_name] = 0
        
        index = self.round_robin_index[service_name] % len(instances)
        self.round_robin_index[service_name] += 1
        
        return instances[index]
```

### 5.3 熔断器实现

```python
class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = {}
        self.last_failure_time = {}
        self.state = {}  # closed, open, half_open
    
    async def call(self, service_name: str, func: callable):
        """调用服务（带熔断）"""
        state = self.state.get(service_name, "closed")
        
        if state == "open":
            # 检查是否可以尝试恢复
            if time.time() - self.last_failure_time[service_name] > self.timeout:
                self.state[service_name] = "half_open"
            else:
                raise CircuitBreakerOpenException(
                    f"Circuit breaker is open for {service_name}"
                )
        
        try:
            result = await func()
            
            # 成功则重置
            if state == "half_open":
                self.state[service_name] = "closed"
                self.failure_count[service_name] = 0
            
            return result
        except Exception as e:
            self.failure_count[service_name] = self.failure_count.get(service_name, 0) + 1
            self.last_failure_time[service_name] = time.time()
            
            # 达到失败阈值则打开熔断器
            if self.failure_count[service_name] >= self.failure_threshold:
                self.state[service_name] = "open"
            
            raise e
```

## 六、部署建议

### 6.1 单机部署
- Gateway 单实例
- Consul 单实例
- 适合开发测试环境

### 6.2 高可用部署
- Gateway 多实例（2-3 个）
- Consul 集群（3 或 5 个节点）
- Nginx 负载均衡
- 适合生产环境

### 6.3 监控告警
- Prometheus + Grafana 监控
- 告警规则：
  - Gateway 实例宕机
  - 服务不可用
  - 请求错误率 > 5%
  - 响应时间 > 1s

## 七、总结

Gateway 服务作为微服务架构的统一入口，需要具备以下核心能力：

1. **服务发现**：动态发现服务实例
2. **负载均衡**：合理分配请求
3. **认证鉴权**：保护 API 安全
4. **限流控制**：防止 API 滥用
5. **熔断降级**：保证系统稳定性
6. **请求追踪**：便于问题排查
7. **日志监控**：实时监控系统状态

通过 Consul 实现服务注册与发现，Gateway 实现统一的路由转发和流量控制，可以构建一个高可用、可扩展的微服务架构。