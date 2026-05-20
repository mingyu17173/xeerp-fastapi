from sqlalchemy.ext.asyncio import AsyncSession
from core.database import AsyncSessionLocal, engine, Base
import logging

logger = logging.getLogger(__name__)

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

async def init_create_table():
    logger.info("Initializing database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables initialized successfully")