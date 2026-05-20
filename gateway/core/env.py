from pydantic_settings import BaseSettings, SettingsConfigDict

class AppConfig(BaseSettings):
    app_name: str = "xeerp-gateway"
    app_version: str = "1.0.0"
    app_env: str = "dev"
    
    jwt_secret_key: str = "xeerp_gateway_jwt_secret_key_2024"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 120
    
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    
    system_service_url: str = "http://127.0.0.1:8001"
    product_service_url: str = "http://127.0.0.1:8002"
    stock_service_url: str = "http://127.0.0.1:8003"
    production_service_url: str = "http://127.0.0.1:8004"
    report_service_url: str = "http://127.0.0.1:8005"
    
    rate_limit_requests: int = 100
    rate_limit_window_seconds: int = 60

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

AppConfig = AppConfig()