from sqlalchemy.ext.asyncio import AsyncSession
from core.database import AsyncSessionLocal


async def get_db() -> AsyncSession:
    """
    获取数据库会话
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_create_table():
    """
    初始化创建数据表
    """
    from core.database import async_engine
    from models.product import Base as ProductBase
    from models.unit import Base as UnitBase
    from models.category import Base as CategoryBase
    from models.brand import Base as BrandBase
    
    async with async_engine.begin() as conn:
        await conn.run_sync(ProductBase.metadata.create_all)
        await conn.run_sync(UnitBase.metadata.create_all)
        await conn.run_sync(CategoryBase.metadata.create_all)
        await conn.run_sync(BrandBase.metadata.create_all)