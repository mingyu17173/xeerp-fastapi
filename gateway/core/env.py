"""
Gateway Service Configuration
网关服务配置
"""

from pydantic_settings import BaseSettings, SettingsConfigDict

class AppConfig(BaseSettings):
    # 服务基本配置
    app_name: str = "xeerp-gateway"
    app_version: str = "1.0.0"
    app_env: str = "dev"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    
    # JWT配置
    jwt_secret_key: str = "xeerp_gateway_jwt_secret_key_2024"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 120
    
    # Redis配置
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: str = ""
    
    # 限流配置
    rate_limit_requests: int = 100
    rate_limit_window_seconds: int = 60
    
    # 服务路由配置
    system_service_url: str = "http://127.0.0.1:8001"
    product_service_url: str = "http://127.0.0.1:8002"
    stock_service_url: str = "http://127.0.0.1:8003"
    production_service_url: str = "http://127.0.0.1:8004"
    report_service_url: str = "http://127.0.0.1:8005"
    approval_service_url: str = "http://127.0.0.1:8006"
    partner_service_url: str = "http://127.0.0.1:8007"
    order_service_url: str = "http://127.0.0.1:8008"
    purchase_service_url: str = "http://127.0.0.1:8009"
    sales_service_url: str = "http://127.0.0.1:8010"
    
    # 请求超时配置（秒）
    request_timeout: int = 30
    
    # 公开路径配置（不需要认证的路径）
    public_paths: str = "/api/docs,/api/redoc,/api/openapi.json"
    public_path_prefixes: str = "/api/auth/,/api/captchaImage,/api/public/"
    
    # Nacos 配置
    nacos_enabled: bool = True
    nacos_server_addresses: str = "192.168.20.43:18848"
    nacos_namespace: str = "public"
    nacos_username: str = "nacos"
    nacos_password: str = "nacos"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

AppConfig = AppConfig()