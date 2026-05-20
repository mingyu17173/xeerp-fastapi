from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from core.env import AppConfig

DATABASE_URL = f"mysql+aiomysql://{AppConfig.db_user}:{AppConfig.db_password}@{AppConfig.db_host}:{AppConfig.db_port}/{AppConfig.db_name}?charset=utf8mb4"

engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=50,
    pool_timeout=30,
    pool_recycle=1800,
)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()