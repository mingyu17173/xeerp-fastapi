from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "xeerp-order"
    app_version: str = "1.0.0"
    app_env: str = "dev"
    
    db_host: str = "localhost"
    db_port: int = 3306
    db_name: str = "xeerp_order"
    db_user: str = "root"
    db_password: str = "123456"
    
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 8
    
    jwt_secret_key: str = "xeerp_order_jwt_secret_key_2024"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 120
    
    partner_service_url: str = "http://127.0.0.1:8007"
    product_service_url: str = "http://127.0.0.1:8002"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()