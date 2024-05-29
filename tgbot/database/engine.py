from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from tgbot.database.models import Base
from tgbot.database.orm_query import init_admin
from tgbot.constants import DB_URL, DB_LITE


engine = create_async_engine(DB_LITE, echo=True)


session_maker = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False)


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with session_maker() as session:
        await init_admin(session)


async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
