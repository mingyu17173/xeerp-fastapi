import redis
from core.env import AppConfig

redis_client = redis.Redis(
    host=AppConfig.redis_host,
    port=AppConfig.redis_port,
    db=AppConfig.redis_db,
    decode_responses=True
)

def get_redis():
    return redis_client